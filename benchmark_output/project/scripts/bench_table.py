#!/usr/bin/env python3
"""Lossless local CSV/XLSX/JSON table I/O; never evaluate formulas or rewrite query cells."""
import argparse
import csv
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ALIASES = {"id": "case_id", "题目id": "case_id", "题号": "case_id", "figmaurl": "figma_url",
           "figma url": "figma_url", "url": "figma_url", "原始url": "source_figma_url", "原始query": "source_query"}


def read_rows(file):
    if file.suffix.lower() == ".xlsx":
        with zipfile.ZipFile(file) as archive:
            strings = []
            if "xl/sharedStrings.xml" in archive.namelist():
                strings = ["".join(n.text or "" for n in x.findall(".//s:t", NS))
                           for x in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("s:si", NS)]
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            first = workbook.find("s:sheets/s:sheet", NS)
            rel_id = first.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            target = next(x.get("Target") for x in rels if x.get("Id") == rel_id)
            member = target.lstrip("/") if target.startswith("/") else "xl/" + target
            matrix = []
            for row in ET.fromstring(archive.read(member)).findall(".//s:sheetData/s:row", NS):
                cells = {}
                for cell in row.findall("s:c", NS):
                    if cell.find("s:f", NS) is not None:
                        raise ValueError("Use literal strings for benchmark URLs and queries; formula cells cannot be imported")
                    column = "".join(c for c in cell.get("r", "") if c.isalpha())
                    value = cell.find("s:v", NS)
                    raw = value.text or "" if value is not None else ""
                    text = strings[int(raw)] if cell.get("t") == "s" else (
                        "".join(n.text or "" for n in cell.findall(".//s:t", NS)) if cell.get("t") == "inlineStr" else raw)
                    cells[column] = text
                matrix.append(cells)
            if not matrix:
                return []
            headers = matrix[0]
            rows = [{key: cells.get(column, "") for column, key in headers.items()}
                    for cells in matrix[1:] if any(value != "" for value in cells.values())]
    elif file.suffix.lower() == ".csv":
        with file.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
    else:
        raise ValueError("Expected CSV or XLSX")
    return [{ALIASES.get(str(k).strip().lower(), str(k).strip().lower()): v for k, v in row.items()} for row in rows]


def column_name(number):
    out = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        out = chr(65 + remainder) + out
    return out


def write_rows(rows, file):
    columns = list(dict.fromkeys(k for row in rows for k in row))
    if file.suffix.lower() == ".csv":
        with file.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        return
    if file.suffix.lower() != ".xlsx":
        raise ValueError("Expected CSV or XLSX export")
    namespace = NS["s"]
    sheet = ET.Element("worksheet", xmlns=namespace)
    data = ET.SubElement(sheet, "sheetData")
    for row_number, values in enumerate([columns] + [[row.get(k) for k in columns] for row in rows], 1):
        row = ET.SubElement(data, "row", r=str(row_number))
        for col, value in enumerate(values, 1):
            if value is None:
                continue
            cell = ET.SubElement(row, "c", r=f"{column_name(col)}{row_number}")
            if isinstance(value, bool):
                cell.set("t", "b")
                ET.SubElement(cell, "v").text = "1" if value else "0"
            elif isinstance(value, (int, float)):
                ET.SubElement(cell, "v").text = str(value)
            else:
                text = str(value)
                if len(text) > 32767:
                    raise ValueError("Excel cell exceeds 32767 characters; use the lossless JSON export for this data")
                cell.set("t", "inlineStr")
                inline = ET.SubElement(cell, "is")
                ET.SubElement(inline, "t", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"}).text = text
    with zipfile.ZipFile(file, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        archive.writestr("_rels/.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        archive.writestr("xl/workbook.xml", f'<workbook xmlns="{namespace}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Benchmark" sheetId="1" r:id="rId1"/></sheets></workbook>')
        archive.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        archive.writestr("xl/worksheets/sheet1.xml", ET.tostring(sheet, encoding="utf-8", xml_declaration=True).replace(b"\r", b"&#13;"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["read", "write"])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.operation == "read":
        json.dump(read_rows(args.input), sys.stdout, ensure_ascii=False)
    else:
        if not args.output:
            parser.error("write requires --output")
        write_rows(json.loads(args.input.read_text()), args.output)
