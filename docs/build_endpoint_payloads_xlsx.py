#!/usr/bin/env python3
"""Build one Excel workbook: eight endpoint tabs, JSON keys as columns."""
from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, GradientFill, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.page import PageMargins

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "SAT-Datashare-Kenya-Endpoint-Payloads.xlsx"

PAYLOAD_JSON = {
    "Invoice": ROOT / "payloads" / "invoice.json",
    "Order": ROOT / "payloads" / "order.json",
    "Product": ROOT / "payloads" / "product.json",
    "Route": ROOT / "payloads" / "route.json",
    "SalesRep": ROOT / "payloads" / "salesrep.json",
    "Customer": ROOT / "payloads" / "customer.json",
    "Stock": ROOT / "payloads" / "stock.json",
    "Warehouse": ROOT / "payloads" / "warehouse.json",
}

SHEET_ORDER = [
    "Invoice",
    "Order",
    "Product",
    "Route",
    "SalesRep",
    "Customer",
    "Stock",
    "Warehouse",
]

# Blue column headers and sheet tabs; grey body rows.
TAB_COLORS = {
    "Invoice": "1B365D",
    "Order": "1E3D63",
    "Product": "214269",
    "Route": "24476F",
    "SalesRep": "274C75",
    "Customer": "2A517B",
    "Stock": "2D5681",
    "Warehouse": "305B87",
}

DARK_BLUE = "1B365D"
MID_BLUE = "2563EB"
WHITE = "FFFFFF"
ZEBRA = "E5E7EB"
ALT_ROW = "F3F4F6"
BORDER_GREY = "D1D5DB"
INK = "374151"

THIN = Border(
    left=Side(style="thin", color=BORDER_GREY),
    right=Side(style="thin", color=BORDER_GREY),
    top=Side(style="thin", color=BORDER_GREY),
    bottom=Side(style="thin", color=BORDER_GREY),
)
HEADER_FONT = Font(name="Calibri", bold=True, color=WHITE, size=11)
CELL_FONT = Font(name="Calibri", size=10, color=INK)
HEADER_FILL = PatternFill("solid", fgColor=DARK_BLUE)
HEADER_GRADIENT = GradientFill(stop=(DARK_BLUE, MID_BLUE), degree=0)
ZEBRA_FILL = PatternFill("solid", fgColor=ZEBRA)
ALT_FILL = PatternFill("solid", fgColor=ALT_ROW)
WRAP = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center")
RIGHT = Alignment(horizontal="right", vertical="center")

TEXT_KEYS = {
    "ProductID",
    "ProductSKU",
    "DistributorID",
    "VATAmount",
    "AmountInvoiced",
    "AmountOrdered",
    "InvoiceDate",
    "InvoiceTime",
    "InvoiceStatus",
    "OrderDate",
    "OrderStartTime",
    "OrderEndTime",
    "OrderStatus",
    "UnitOfMeasure",
    "Currency",
    "TransType",
    "RouteName",
    "RouteType",
    "SalesRepName",
    "SalesRepType",
    "StoreName",
    "StoreCategory",
    "Channel",
    "StoreClassification",
    "City",
    "Region",
    "County",
    "StoreCreationDate",
    "StoreSize",
    "DistributorWarehouseCode",
    "Date",
    "WarehouseName",
}


def load_rows(name: str) -> list[dict]:
    path = PAYLOAD_JSON[name]
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("data") or []
    if not rows:
        raise SystemExit(f"{path} has no data array")
    return rows


def columns_for(rows: list[dict]) -> list[str]:
    keys: list[str] = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                keys.append(key)
    return keys


def cell_value(key: str, value):
    if value is None:
        return None
    if key in TEXT_KEYS or key in {"RouteID", "OrderNumber"}:
        if value == "":
            return ""
        return str(value)
    return value


def autosize(ws, headers: list[str], rows: list[dict]) -> None:
    for i, header in enumerate(headers, 1):
        longest = len(str(header))
        for row in rows[:200]:
            val = row.get(header)
            if val is None:
                continue
            longest = max(longest, min(len(str(val)), 48))
        ws.column_dimensions[get_column_letter(i)].width = min(max(longest + 3, 12), 42)


def write_sheet(wb: Workbook, name: str, rows: list[dict]) -> None:
    ws = wb.create_sheet(name)
    headers = columns_for(rows)
    ws.sheet_properties.tabColor = TAB_COLORS[name]
    ws.freeze_panes = "A2"
    last_col = get_column_letter(len(headers))
    last_row = len(rows) + 1
    ws.auto_filter.ref = f"A1:{last_col}{last_row}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.6, bottom=0.6)
    ws.oddHeader.left.text = f"SAT Datashare · {name}"
    ws.oddFooter.left.text = "Confidential · v1.0"
    ws.oddFooter.right.text = "Page &P"

    for col, header in enumerate(headers, 1):
        cell = ws.cell(1, col, header)
        cell.font = HEADER_FONT
        cell.fill = HEADER_GRADIENT
        cell.alignment = WRAP
        cell.border = THIN
    ws.row_dimensions[1].height = 22

    for r_i, row in enumerate(rows, 2):
        fill = ZEBRA_FILL if r_i % 2 == 0 else ALT_FILL
        for c_i, header in enumerate(headers, 1):
            value = cell_value(header, row.get(header))
            cell = ws.cell(r_i, c_i, value)
            cell.font = CELL_FONT
            cell.border = THIN
            cell.fill = fill
            if header in TEXT_KEYS or header in {"RouteID", "OrderNumber", "ProductID"}:
                cell.number_format = "@"
                cell.alignment = LEFT
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                cell.alignment = RIGHT
            else:
                cell.alignment = LEFT

    autosize(ws, headers, rows)

    table = Table(
        displayName=f"{name}Data",
        ref=f"A1:{last_col}{last_row}",
    )
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(table)

    # Re-apply blue header after the table so the custom fill survives Excel table styles.
    for col in range(1, len(headers) + 1):
        cell = ws.cell(1, col)
        cell.fill = HEADER_GRADIENT
        cell.font = HEADER_FONT
        cell.alignment = WRAP
        cell.border = THIN


def main() -> None:
    wb = Workbook()
    default = wb.active
    wb.remove(default)

    wb.properties.creator = "SAT Datashare"
    wb.properties.lastModifiedBy = "SAT Datashare"
    wb.properties.title = "SAT Datashare Kenya endpoint payloads"
    wb.properties.subject = "Experience API sample rows by endpoint"
    wb.properties.description = ""
    wb.properties.keywords = "SAT Datashare, Kenya, Invoice, Order, Product"

    counts = {}
    for name in SHEET_ORDER:
        rows = load_rows(name)
        write_sheet(wb, name, rows)
        counts[name] = len(rows)

    wb.save(OUT)
    print(f"Wrote {OUT}")
    for name, n in counts.items():
        print(f"  {name}: {n} row(s)")


if __name__ == "__main__":
    main()
