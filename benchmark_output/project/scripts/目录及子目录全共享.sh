#!/usr/bin/env bash
# 在目标目录下执行后，将该目录及全部子目录、文件的权限开放给所有人。
# 用法：
#   cd /path/to/shared-dir
#   bash /path/to/目录及子目录全共享.sh          # 处理当前目录，执行前确认
#   bash /path/to/目录及子目录全共享.sh -y       # 跳过确认
#   bash /path/to/目录及子目录全共享.sh /other   # 处理指定目录
#   bash /path/to/目录及子目录全共享.sh -y /other
set -euo pipefail

YES=0
TARGET="."

usage() {
  cat <<'EOF'
用法: 目录及子目录全共享.sh [-y] [目录]

把目录及全部子目录、文件开放为所有人可读写执行（在现有权限上增加 a+rwx）。
目录还会写入默认 ACL（若系统有 setfacl），使之后新建的文件和子目录同样对所有人开放。
默认处理当前工作目录。-y 跳过确认。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes) YES=1 ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) echo "未知参数: $1" >&2; usage >&2; exit 2 ;;
    *)
      if [[ "$TARGET" != "." ]]; then
        echo "只能指定一个目录" >&2
        exit 2
      fi
      TARGET="$1"
      ;;
  esac
  shift
done

if [[ $# -gt 0 ]]; then
  if [[ "$TARGET" != "." ]]; then
    echo "只能指定一个目录" >&2
    exit 2
  fi
  TARGET="$1"
fi

if [[ ! -d "$TARGET" ]]; then
  echo "不是目录: $TARGET" >&2
  exit 1
fi

TARGET="$(cd "$TARGET" && pwd -P)"

is_forbidden() {
  local path="$1"
  case "$path" in
    /|/bin|/boot|/dev|/etc|/home|/lib|/lib64|/mnt|/opt|/proc|/root|/run|/sbin|/sys|/tmp|/usr|/var)
      return 0
      ;;
    /bin/*|/boot/*|/dev/*|/etc/*|/lib/*|/lib64/*|/proc/*|/root/*|/run/*|/sbin/*|/sys/*|/usr/*|/var/*)
      return 0
      ;;
  esac
  return 1
}

if is_forbidden "$TARGET"; then
  echo "拒绝修改系统目录: $TARGET" >&2
  exit 1
fi

echo "目标目录: $TARGET"
echo "将递归增加权限 a+rwx（所有人可读、可写、可执行），并给目录设置默认 ACL。"
echo "符号链接本身不会被深入，避免改到目录树外面。"

if [[ "$YES" -ne 1 ]]; then
  if [[ ! -t 0 ]]; then
    echo "非交互环境请加上 -y 确认执行" >&2
    exit 1
  fi
  read -r -p "确认继续？[y/N] " answer
  case "$answer" in
    y|Y|yes|YES) ;;
    *) echo "已取消"; exit 0 ;;
  esac
fi

chmod -R a+rwx "$TARGET"

if command -v setfacl >/dev/null 2>&1; then
  # 默认 ACL 让之后在这些目录里新建的文件/子目录也对所有人开放。
  # 已有符号链接不会被 find -type d 选中，因此不会跟着链到外部目录。
  find "$TARGET" -type d -exec setfacl \
    -m u::rwx,g::rwx,o::rwx \
    -d -m u::rwx,g::rwx,o::rwx \
    {} +
  echo "完成: 现有内容已开放，且新文件会继承对所有人开放的默认 ACL。"
else
  echo "完成: 现有内容已开放。系统没有 setfacl，之后新建的文件仍受创建者 umask 影响。" >&2
fi
