#!/usr/bin/env python3
"""Read the seven fresh workbooks and export their query cells verbatim."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

FILES = [f"figma_tasks_{i:02}_fresh.xlsx" for i in range(1, 8)]
PREVIOUS_FILES = ["figma_tasks_01_original.xlsx"] + [f"figma_tasks_{i:02}_copy{i-1:02}.xlsx" for i in range(2, 8)]
DATA_ROOT = Path("/mnt/afs/gaoyongyong/code/new_bench/data_syn")
PREVIOUS_SOURCE = DATA_ROOT / "figma_tasks_7_excels"
MODELS = [
    ("model_local_a282d9c9a73446c8", "Qwen3.8-27B Figma Edit · ckpt-270"),
    ("model_claude_opus55_direct", "Opus 5.5（三方A）"),
    ("model_claude_fable51_login", "Fable 5.1"),
    ("model_glm_53_flash_cc", "GLM-5.3 Flash"),
    ("model_gemini_31_pro_cc", "Gemini 3.5 Flash"),
    ("model_kimi_k3_cc", "Kimi K3"),
    ("model_de5fc4c9cdb841e8", "gpt-6-astra"),
]
NAMESPACE = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
URL = re.compile(r"https://(?:www\.)?figma\.com/(?:design|file)/[^\s]+")
FILE_KEY = re.compile(r"/(?:design|file)/([A-Za-z0-9]+)(?:[/?#]|$)")
# The original templates and previous runs cannot be used as fresh assignments.
TEMPLATE_KEYS = {"XVAY0zoM6wv3FT5ZgVUHlv", "gQXS37cyO0wGynFDdUUJeM", "o4N4pfpZFu9l66viOeZ2IR"}


def query_target(query):
    urls = URL.findall(query)
    match = FILE_KEY.search(urls[0]) if len(urls) == 1 else None
    if not match:
        raise ValueError("Expected exactly one Figma file URL in each query")
    return urls[0], match.group(1)


def workbook_queries(file):
    with zipfile.ZipFile(file) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared = ["".join(t.text or "" for t in item.findall(".//s:t", NAMESPACE))
                      for item in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("s:si", NAMESPACE)]
        cells = {}
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        for cell in sheet.findall(".//s:sheetData/s:row/s:c", NAMESPACE):
            value = cell.find("s:v", NAMESPACE)
            if cell.get("t") == "s" and value is not None:
                text = shared[int(value.text)]
            elif cell.get("t") == "inlineStr":
                text = "".join(t.text or "" for t in cell.findall(".//s:t", NAMESPACE))
            else:
                text = value.text or "" if value is not None else ""
            cells[cell.get("r")] = text
    if cells.get("F1") != "query":
        raise ValueError(f"{file}: expected query in F1")
    queries = [cells.get(f"F{i}", "") for i in range(2, 5)]
    if not all(queries) or any(value.strip() for key, value in cells.items()
                               if re.fullmatch(r"F\d+", key) and int(key[1:]) > 4):
        raise ValueError(f"{file}: expected exactly three query rows")
    return queries


def prepare(source, output, previous_source=PREVIOUS_SOURCE):
    source = source.resolve()
    output = output.resolve()
    if output.is_relative_to(source):
        raise ValueError("Write benchmark outputs outside the source workbook directory")
    excluded_keys = TEMPLATE_KEYS | {query_target(query)[1] for name in PREVIOUS_FILES
                                    for query in workbook_queries(previous_source / name)}
    groups = []
    variants = [set(), set(), set()]
    file_keys = set()
    for index, name in enumerate(FILES):
        file = source / name
        original_hash = hashlib.sha256(file.read_bytes()).hexdigest()
        tests = []
        for row, original in enumerate(workbook_queries(file), 2):
            url, file_key = query_target(original)
            if file_key in file_keys:
                raise ValueError(f"Figma file reused across model/task assignments: {file_key}")
            if file_key in excluded_keys:
                raise ValueError(f"Fresh input reuses a previous file or source template: {file_key}")
            file_keys.add(file_key)
            query = original
            variants[row - 2].add(URL.sub("<ASSIGNED_FIGMA_URL>", query))
            tests.append({"question": row - 1, "source_file": str(file), "source_cell": f"F{row}",
                          "original_query": original, "query": query, "query_modified": False,
                          "figma_url": url, "file_key": file_key,
                          "original_sha256": hashlib.sha256(original.encode()).hexdigest(),
                          "query_sha256": hashlib.sha256(query.encode()).hexdigest()})
        if hashlib.sha256(file.read_bytes()).hexdigest() != original_hash:
            raise RuntimeError(f"Original workbook changed while reading: {file}")
        groups.append({"task": f"task{index+1}", "model_id": MODELS[index][0], "model_name": MODELS[index][1],
                       "source_workbook_sha256": original_hash, "tests": tests})
    if any(len(items) != 1 for items in variants):
        raise ValueError("Corresponding queries differ beyond their assigned Figma URLs")
    result = {"mode": "benchmark-design", "questions": 3, "models": 7, "runs": 21,
              "source_directory": str(source), "original_workbooks_modified": False,
              "fresh_targets": True, "query_modified": False, "changes": [],
              "excluded_file_keys": sorted(excluded_keys),
              "groups": groups}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    temporary.chmod(0o600)
    temporary.replace(output)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DATA_ROOT / "figma_tasks_7_excels_fresh_20261026")
    parser.add_argument("--previous-source", type=Path, default=PREVIOUS_SOURCE)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "storage/benchmark-design/inputs.json")
    args = parser.parse_args()
    result = prepare(args.source, args.output, args.previous_source)
    print(json.dumps({"output": str(args.output), "questions": 3, "models": 7, "runs": 21,
                      "original_workbooks_modified": False, "query_modified": False,
                      "fresh_targets": True, "changes": result["changes"]}, ensure_ascii=False))
