"""Shared trajectory parsing: behaviour categories, tool-error taxonomy, per-attempt features.

Used by build_master.py (this batch) and build_old.py (earlier package), so both are measured
with the same code.
"""
import collections
import csv
import hashlib
import json
import os
import re

# --------------------------------------------------------------------------- helpers


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    x = str(x).strip()
    if not x:
        return None
    try:
        return float(x)
    except ValueError:
        return None


def load_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def text_of(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False)


# --------------------------------------------------------------------------- taxonomies

# Order matters: the first matching rule wins. "model" = the call itself was wrong (bad API
# use, bad arguments); "infra" = the environment failed independently of what was asked;
# everything else stays "unknown" and is listed in error_signatures.csv for manual labelling.
ERROR_RULES = [
    # --- environment: the account's Figma MCP quota tripped, or the response was lost in transit
    ("infra", "mcp_quota_circuit_open", r"tool call limit|circuit is open|resource recovery check"),
    ("infra", "tool_timeout", r"没有响应|已中止"),
    ("infra", "harness_internal", r"Tool result missing due to internal error|unhandled errors in a TaskGroup"),
    ("model", "wrong_tool_name", r"No such tool available"),
    ("infra", "response_lost", r"response lost|operation may already have applied"),
    # --- not a failure: the model throws an Error on purpose to print data back to itself
    ("intentional", "throw_as_output", r"^\s*Error: (LOG|[A-Z][A-Z0-9_]{5,}|Brief Content|X \d+ kids|\{|\[)"),
    # --- model: asked for a tool or argument that the harness does not offer
    ("model", "wrong_tool_name", r"不允许的工具|未开放|只能使用"),
    ("model", "bad_session_argument", r"Invalid sessionId"),
    ("model", "plugin_api_misuse", r"Error: in \w+:|Removing this node is not allowed|Component with key|Unexpected reserved word|Invalid \w+ hash"),
    ("model", "plugin_api_misuse", r"TypeError|ReferenceError|SyntaxError|RangeError|no such property|is not a function|is not defined|is not iterable|Cannot (read|set|access)|not extensible|object is not|undefined is not|null is not|unexpected token|Unexpected (identifier|end|token)|invalid or unexpected"),
    ("model", "schema_validation", r"failed validation|Unrecognized key|Invalid literal|Expected .*received|Required value missing|Invalid discriminator|Invalid enum|input validation|Invalid arguments|invalid_type|must be (a|an|one of)"),
    ("model", "font_not_loaded", r"unloaded font|loadFontAsync|font .*(not|n't).*(loaded|available|exist)"),
    ("model", "bad_node_reference", r"node .*(not found|does not exist|removed)|does not exist|Could not find|No node|cannot find node|was removed|in a different (page|document)|null.*getNodeById"),
    ("model", "unsupported_api", r"not supported|unsupported|is read-only|read only|Cannot (add|move|modify|write)|in dynamic-page|documentAccess"),
    ("model", "layout_constraint", r"layout|auto-layout|constraint|resize|sizing|FILL can only|HUG can only|overrid"),
    ("infra", "rate_limit", r"\b429\b|rate.?limit|too many requests|quota"),
    ("infra", "transport", r"transport|ECONN|ETIMEDOUT|EPIPE|socket hang|fetch failed|network|connection (closed|reset|refused|lost)|JSON-RPC|no matching .*response|MCP error|stream (closed|ended)|aborted"),
    ("infra", "server_error", r"\b50[0-4]\b|internal server error|service unavailable|bad gateway|overloaded|upstream"),
    ("infra", "auth_or_access", r"\b40[13]\b|unauthori[sz]ed|forbidden|not authenticated|permission|access denied|token (expired|invalid)|login"),
    ("infra", "tool_timeout", r"timed out|time-?out|deadline exceeded|took too long"),
    ("ambiguous", "payload_too_large", r"too large|exceeds|maximum .*(size|length|tokens)|truncat|maxLength"),
]
ERROR_RULES = [(c, k, re.compile(p, re.I)) for c, k, p in ERROR_RULES]


def classify_error(msg):
    head = msg[:1500]
    for cause, kind, pat in ERROR_RULES:
        if pat.search(head):
            return cause, kind
    return "unknown", "unclassified"


def error_signature(msg):
    s = msg.strip().split("\n")[0][:140]
    s = re.sub(r"Figma Debug UUID.*", "", s)
    s = re.sub(r"[0-9a-f]{8}-[0-9a-f-]{20,}", "<uuid>", s)
    s = re.sub(r"'[^']{1,60}'", "'<x>'", s)
    s = re.sub(r'"[^"]{1,60}"', '"<x>"', s)
    s = re.sub(r"\d+", "N", s)
    return s.strip()


CREATE_RE = re.compile(r"figma\.create[A-Z]\w*\s*\(|\.createInstance\s*\(|\.clone\s*\(|createNodeFromSvg|importComponent\w*\s*\(|figma\.(union|subtract|group|flatten|combineAsVariants)\s*\(")
PROTO_RE = re.compile(r"setReactionsAsync|\.reactions\s*=[^=]|flowStartingPoints")
DELETE_RE = re.compile(r"\.remove\s*\(\s*\)")
MUTATE_RE = re.compile(r"\.appendChild\s*\(|\.insertChild\s*\(|\.resize\w*\s*\(|\.rescale\s*\(|\.setProperties\s*\(|\.swapComponent\s*\(|set(?!CurrentPage)\w+Async\s*\(|\.setBoundVariable\s*\(|\b[\w\]\)]+\.(x|y|name|characters|fills|strokes|effects|opacity|visible|fontSize|fontName|layoutMode|layoutSizingHorizontal|layoutSizingVertical|itemSpacing|paddingLeft|paddingRight|paddingTop|paddingBottom|cornerRadius|primaryAxisAlignItems|counterAxisAlignItems|textAlignHorizontal|lineHeight|letterSpacing|clipsContent|rotation|strokeWeight|constraints|layoutAlign|layoutGrow|textAutoResize)\s*=[^=]")

READ_ONLY_TOOLS = {
    "get_metadata", "get_screenshot", "get_design_context", "get_variable_defs",
    "search_design_system", "get_libraries", "get_figjam", "get_motion_context",
    "get_code_connect_map", "get_context_for_code_connect", "get_code_connect_suggestions",
    "list_file_shaders", "download_assets",
}


def short_tool(name):
    return (name or "unknown").split("__")[-1]


ELIDED_MARK = "历史已执行脚本已省略"
DESC_KW = [  # used only when the code itself is not in the trajectory
    ("prototype", re.compile(r"\b(wire|wiring|link|prototyp|reaction|interaction|navigation|hotspot)", re.I)),
    ("construct", re.compile(r"\b(build|create|add|make|draw|construct|generate|clone|instantiate)", re.I)),
    ("modify", re.compile(r"\b(fix|adjust|update|remove|delete|recolou?r|align|cent(er|re)|resize|rename|move|tweak|polish|refine|correct|repair|replace|clean|hide|swap|patch)", re.I)),
    ("inspect", re.compile(r"\b(inspect|read|list|dump|check|verify|get|find|map|audit|scan|examine|count|extract|probe|test|confirm)", re.I)),
]


def classify_from_description(desc):
    for cat, pat in DESC_KW:
        if pat.search(desc or ""):
            return cat
    return "unknown"


def classify_call(name, args):
    """Behaviour category of one tool call, from the tool name and (for use_figma) its code.

    These are descriptive labels, not a judgement that a category is wasteful.
    """
    t = short_tool(name)
    if t == "whoami":
        return "setup", False
    if t == "get_screenshot":
        return "verify", False
    if t in READ_ONLY_TOOLS:
        return "inspect", False
    if t == "use_figma":
        code = ""
        if isinstance(args, dict):
            code = text_of(args.get("code"))
        elif isinstance(args, str):
            code = args
        if ELIDED_MARK in code or not code.strip():
            desc = args.get("description", "") if isinstance(args, dict) else ""
            return classify_from_description(desc), False
        deletes = bool(DELETE_RE.search(code))
        if CREATE_RE.search(code):
            return "construct", deletes
        if PROTO_RE.search(code):
            return "prototype", deletes
        if deletes or MUTATE_RE.search(code):
            return "modify", deletes
        return "inspect", False
    return "other_tool", False


CATS = ["setup", "inspect", "construct", "modify", "prototype", "verify", "other_tool", "unknown"]

# --------------------------------------------------------------------------- trajectories


REMINDER_RE = re.compile(r"\s*<system-reminder>.*?</system-reminder>\s*", re.S)


def normalize_messages(msgs):
    """Return messages in the flat (OpenAI-like) shape used by the direct runner.

    Some earlier trajectories keep Anthropic content blocks (tool_use / tool_result inside
    assistant / user messages). Harness reminders appended to tool results are split off into
    their own user message so they are counted as harness overhead, not as tool output."""
    if not any(isinstance(m.get("content"), list) for m in msgs):
        return msgs
    out = []
    for m in msgs:
        c = m.get("content")
        if not isinstance(c, list):
            out.append(m)
            continue
        role = m.get("role")
        if role == "assistant":
            text = "".join(b.get("text", "") for b in c if b.get("type") == "text")
            think = "".join(b.get("thinking", "") for b in c if b.get("type") == "thinking")
            calls = [{"id": b.get("id"), "type": "function",
                      "function": {"name": b.get("name"), "arguments": b.get("input")}}
                     for b in c if b.get("type") == "tool_use"]
            out.append({"role": "assistant", "content": text, "reasoning_content": think, "tool_calls": calls})
        elif role == "user":
            texts = []
            for b in c:
                if b.get("type") == "tool_result":
                    inner = b.get("content")
                    if isinstance(inner, list):
                        parts = [x.get("text", "") for x in inner if x.get("type") == "text"]
                        rem = [p for p in parts if p.lstrip().startswith("<system-reminder>")]
                        body = "\n".join(p for p in parts if not p.lstrip().startswith("<system-reminder>"))
                        texts.extend(rem)
                    else:
                        body = text_of(inner)
                    out.append({"role": "tool", "tool_call_id": b.get("tool_use_id"), "content": body,
                                "success": not b.get("is_error", False)})
                elif b.get("type") == "text":
                    texts.append(b.get("text", ""))
            if texts:
                out.append({"role": "user", "content": "\n".join(texts)})
        else:
            out.append({"role": role, "content": "".join(b.get("text", "") for b in c if isinstance(b, dict))})
    return out


def parse_attempt(path):
    """Summarise one trajectory file. Returns (attempt_row, error_rows, call_ids)."""
    recs = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except ValueError:
                pass
    base = os.path.basename(path)
    row = {"trajectory_file": base, "parse_ok": bool(recs), "n_records": len(recs)}
    m = re.match(r"trajectory-attempt-(\d+)-(.*)\.jsonl", base)
    row["attempt_label"] = m.group(2) if m else "primary"
    row["attempt_kind"] = (
        "primary" if not m else
        "continuation" if "continuation" in m.group(2) else
        "restart" if "restart" in m.group(2) else
        "resume" if "resume" in m.group(2) else "other")
    row["mtime"] = os.path.getmtime(path)
    if not recs:
        return row, [], set()
    r = recs[-1]
    md = r.get("metadata") or {}
    rc = md.get("reasoning_control") or {}
    usage = md.get("usage") or {}
    msgs = normalize_messages(r.get("messages") or [])
    row.update({
        "traj_status": r.get("status"),
        "total_steps": r.get("total_steps"),
        "enable_thinking": r.get("enable_thinking"),
        "api_model": md.get("model"),
        "harness_source": md.get("source"),
        "harness_client": md.get("client"),
        "api_format": rc.get("api_format"),
        "requested_effort": rc.get("requested_effort") or "not_set",
        "effort_policy_activated_at": rc.get("activated_at") or "",
        "session_id": md.get("session_id"),
        "usage_input_tokens": usage.get("input_tokens"),
        "usage_output_tokens": usage.get("output_tokens"),
        "n_messages": len(msgs),
    })
    sys_text = text_of(msgs[0].get("content")) if msgs and msgs[0].get("role") == "system" else ""
    fk = re.search(r"fileKey ([0-9A-Za-z]{15,})", sys_text)
    row["file_key"] = fk.group(1) if fk else ""
    acct = re.search(r"assigned account is ([^\s.]+@[\w.-]+\w)", sys_text)
    row["assigned_account"] = acct.group(1) if acct else ""
    fixed_chars = len(sys_text) + len(json.dumps(r.get("tools") or [], ensure_ascii=False))
    row["fixed_prompt_chars"] = fixed_chars

    # index of every assistant turn, to know how many later requests re-send each message
    turn_idx = [i for i, mm in enumerate(msgs) if mm.get("role") == "assistant"]
    n_turns = len(turn_idx)

    def later_turns(i):
        # number of model requests whose input contains message i
        return sum(1 for t in turn_idx if t > i)

    calls = {}          # tool_call_id -> dict
    order = []          # call ids in order
    call_ids = set()
    fresh = collections.Counter()   # chars produced, by category
    carry = collections.Counter()   # chars x number of later requests that re-read them
    reasoning_chars = 0
    assistant_text_chars = 0
    n_reminders = 0
    for i, mm in enumerate(msgs):
        role = mm.get("role")
        if role == "assistant":
            reasoning_chars += len(text_of(mm.get("reasoning_content")))
            ctext = text_of(mm.get("content"))
            assistant_text_chars += len(ctext)
            lt = later_turns(i)
            fresh["assistant_text"] += len(ctext)
            carry["assistant_text"] += len(ctext) * lt
            for tc in mm.get("tool_calls") or []:
                fn = tc.get("function") or {}
                args = fn.get("arguments")
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except ValueError:
                        pass
                cat, deletes = classify_call(fn.get("name"), args)
                arg_text = text_of(args)
                cid = tc.get("id") or f"noid-{i}-{len(order)}"
                calls[cid] = {
                    "id": cid, "tool": short_tool(fn.get("name")), "cat": cat, "deletes": deletes,
                    "arg_chars": len(arg_text),
                    "arg_hash": hashlib.md5((short_tool(fn.get("name")) + arg_text).encode()).hexdigest(),
                    "target": text_of(args.get("nodeId")) if isinstance(args, dict) else "",
                    "result_chars": None, "success": None, "msg_index": i, "turn": turn_idx.index(i),
                }
                order.append(cid)
                call_ids.add(cid)
                fresh["args:" + cat] += len(arg_text)
                carry["args:" + cat] += len(arg_text) * lt
        elif role == "user":
            ctext = text_of(mm.get("content"))
            if ctext.lstrip().startswith("<system-reminder>") and not REMINDER_RE.sub("", ctext).strip():
                n_reminders += 1
                fresh["harness_reminders"] += len(ctext)
                carry["harness_reminders"] += len(ctext) * later_turns(i)
        elif role == "tool":
            cid = mm.get("tool_call_id")
            ctext = text_of(mm.get("content"))
            c = calls.get(cid)
            if c is None:
                c = {"id": cid or f"orphan-{i}", "tool": short_tool(mm.get("name")), "cat": "other_tool",
                     "deletes": False, "arg_chars": 0, "arg_hash": "", "target": "",
                     "msg_index": i, "turn": None}
                calls[c["id"]] = c
                order.append(c["id"])
            ok = mm.get("success")
            if ok is None:
                ok = not re.match(r"\s*(Error|TypeError|\{\s*\"error\")", ctext)
            c["success"] = bool(ok)
            c["result_chars"] = len(ctext)
            c["result_head"] = ctext[:1500]
            lt = later_turns(i)
            fresh["result:" + c["cat"]] += len(ctext)
            carry["result:" + c["cat"]] += len(ctext) * lt

    seq = [calls[c] for c in order]
    answered = [c for c in seq if c["success"] is not None]
    failed = [c for c in answered if not c["success"]]
    err_rows = []
    cause_counts = collections.Counter()
    for c in failed:
        cause, kind = classify_error(c.get("result_head", ""))
        c["err_cause"], c["err_kind"] = cause, kind
        cause_counts[cause] += 1
        err_rows.append({
            "trajectory_file": base, "call_index": order.index(c["id"]), "tool": c["tool"],
            "call_category": c["cat"], "auto_cause": cause, "auto_kind": kind,
            "signature": error_signature(c.get("result_head", "")),
            "message_head": c.get("result_head", "")[:300].replace("\n", " "),
        })

    # sequences: failure streaks, retries after an error, repeated identical calls
    max_streak = streak = 0
    retries_after_error = 0
    same_error_repeat = 0
    prev = None
    for c in answered:
        if not c["success"]:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
        if prev is not None and not prev["success"]:
            retries_after_error += 1
            if (not c["success"]
                    and error_signature(c.get("result_head", "")) == error_signature(prev.get("result_head", ""))):
                same_error_repeat += 1
        prev = c
    hash_counts = collections.Counter(c["arg_hash"] for c in seq if c["arg_hash"])
    dup_calls = sum(v - 1 for v in hash_counts.values() if v > 1)
    read_targets = collections.Counter((c["tool"], c["target"]) for c in seq if c["tool"] == "get_metadata")
    repeat_reads = sum(v - 1 for v in read_targets.values() if v > 1)

    first_build = next((k for k, c in enumerate(seq) if c["cat"] == "construct" and c["success"]), None)
    last_build = max((k for k, c in enumerate(seq) if c["cat"] in ("construct", "modify", "prototype") and c["success"]), default=None)
    post_build_inspect = sum(1 for k, c in enumerate(seq) if first_build is not None and k > first_build and c["cat"] == "inspect")

    row.update({
        "assistant_turns": n_turns,
        "tool_calls": len(seq),
        "tool_calls_answered": len(answered),
        "tool_errors": len(failed),
        "tool_errors_model": cause_counts["model"],
        "tool_errors_infra": cause_counts["infra"],
        "tool_errors_ambiguous": cause_counts["ambiguous"],
        "tool_errors_unknown": cause_counts["unknown"],
        "tool_errors_intentional": cause_counts["intentional"],
        "max_error_streak": max_streak,
        "retries_after_error": retries_after_error,
        "same_error_repeats": same_error_repeat,
        "duplicate_calls": dup_calls,
        "repeat_metadata_reads": repeat_reads,
        "calls_with_delete": sum(1 for c in seq if c["deletes"]),
        "calls_before_first_build": first_build if first_build is not None else "",
        "calls_after_last_write": (len(seq) - 1 - last_build) if last_build is not None else "",
        "post_build_inspect_calls": post_build_inspect,
        "reasoning_chars": reasoning_chars,
        "assistant_text_chars": assistant_text_chars,
        "ended_with_text_answer": bool(msgs and msgs[-1].get("role") == "assistant" and not (msgs[-1].get("tool_calls") or [])),
        "last_role": msgs[-1].get("role") if msgs else "",
    })
    for cat in CATS:
        row[f"calls_{cat}"] = sum(1 for c in seq if c["cat"] == cat)
        row[f"errors_{cat}"] = sum(1 for c in failed if c["cat"] == cat)
        row[f"result_chars_{cat}"] = fresh["result:" + cat]
        row[f"arg_chars_{cat}"] = fresh["args:" + cat]
        row[f"carry_chars_{cat}"] = carry["result:" + cat] + carry["args:" + cat]
    row["carry_chars_assistant_text"] = carry["assistant_text"]
    row["carry_chars_fixed_prompt"] = fixed_chars * n_turns
    row["carry_chars_harness_reminders"] = carry["harness_reminders"]
    row["harness_reminder_messages"] = n_reminders
    row["carry_chars_total"] = sum(v for k, v in row.items() if k.startswith("carry_chars_") and k != "carry_chars_total")
    largest = max((c["result_chars"] or 0 for c in seq), default=0)
    row["largest_result_chars"] = largest
    return row, err_rows, call_ids



SUM_FIELDS = [
    "assistant_turns", "tool_calls", "tool_calls_answered", "tool_errors", "tool_errors_model",
    "tool_errors_infra", "tool_errors_ambiguous", "tool_errors_unknown", "tool_errors_intentional",
    "retries_after_error",
    "same_error_repeats", "duplicate_calls", "repeat_metadata_reads", "calls_with_delete",
    "post_build_inspect_calls", "reasoning_chars", "assistant_text_chars", "carry_chars_total",
    "carry_chars_assistant_text", "carry_chars_fixed_prompt", "carry_chars_harness_reminders",
    "harness_reminder_messages",
] + [f"{p}_{c}" for c in CATS for p in ("calls", "errors", "result_chars", "arg_chars", "carry_chars")]
