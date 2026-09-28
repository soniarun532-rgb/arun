#!/usr/bin/env python3
"""Build one Excel workbook: eight endpoint tabs, JSON keys as columns."""
from __future__ import annotations

import json
from copy import copy
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.page import PageMargins

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "SAT-Datashare-Kenya-Endpoint-Payloads.xlsx"
INVOICE_JSON = ROOT / "payloads" / "invoice.json"

SAMPLES = {
    "Order": {
        "StoreID": 2814,
        "SalesRepID": 103,
        "RouteID": 115,
        "ProductID": "3109556",
        "DistributorID": "1000097205",
        "WarehouseID": 2166,
        "OrderNumber": 366,
        "OrderDate": "25/09/2026",
        "OrderStartTime": "17:42:38",
        "OrderEndTime": "18:12:59",
        "OrderStatus": "Open",
        "UnitOfMeasure": "PIECE",
        "Currency": "KES",
        "QuantityOrdered": 6,
        "AmountOrdered": "1104.00",
        "Discount": 0,
        "VATAmount": "152.28",
    },
    "Product": {
        "ProductID": "3268896",
        "ProductSKU": "AWICK FRESHMATIC ROSE  + GADGET SEEDING PRICE 250ML (4)",
        "UnitOfMeasure": "PIECE",
    },
    "Route": {
        "RouteID": 110,
        "RouteName": "MOSES RB TUESDAY",
        "SalesRepID": 110,
        "RouteType": "Weekly",
        "SalesRepType": "Van Sales",
        "Date": "07/09/2026",
    },
    "SalesRep": {
        "SalesRepID": 100,
        "SalesRepName": "ISAAC MUGE",
        "DistributorID": "1000097205",
        "WarehouseID": 183,
        "SalesRepType": "Admin",
    },
    "Customer": {
        "StoreID": 1980,
        "StoreName": "ONE ZERO ONE SELFRIGES",
        "StoreCategory": "SHOP AND BROWSER",
        "Channel": "GENERAL TRADE",
        "StoreClassification": "GENERAL TRADE",
        "WarehouseID": None,
        "Longitude": 37.5852265,
        "Latitude": 0.3526255,
        "City": "MERU",
        "Region": "MOUNTAIN",
        "County": "",
        "StoreStatus": 1,
        "StoreCreationDate": "10/09/2026",
        "StoreSize": "",
    },
    "Stock": {
        "ProductID": "3300090",
        "UnitOfMeasure": "PIECE",
        "DistributorWarehouseCode": "EMBU STOCKPOINT",
        "Date": "22/09/2026",
        "InventoryQuantity": 21,
        "InventoryPrice": None,
    },
    "Warehouse": {
        "WarehouseID": 183,
        "WarehouseName": "GIKAMBURA STOCKPOINT",
        "DistributorID": "1000097205",
    },
}
OUT = ROOT / "SAT-Datashare-Kenya-Endpoint-Payloads.xlsx"
INVOICE_JSON = ROOT / "payloads" / "invoice.json"

NAVY = "1F4E79"
WHITE = "FFFFFF"
ZEBRA = "F3F6FA"
THIN = Border(
    left=Side(style="thin", color="D0D7DE"),
    right=Side(style="thin", color="D0D7DE"),
    top=Side(style="thin", color="D0D7DE"),
    bottom=Side(style="thin", color="D0D7DE"),
)
HEADER_FONT = Font(name="Calibri", bold=True, color=WHITE, size=11)
CELL_FONT = Font(name="Calibri", size=10, color="2D2D2D")
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
ZEBRA_FILL = PatternFill("solid", fgColor=ZEBRA)
WRAP = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center")
RIGHT = Alignment(horizontal="right", vertical="center")

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
    if name == "Invoice":
        payload = json.loads(INVOICE_JSON.read_text(encoding="utf-8"))
        rows = payload.get("data") or []
        if not rows:
            raise SystemExit(f"{INVOICE_JSON} has no data array")
        return rows
    sample = SAMPLES[name]
    return [copy(sample)]


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
    ws.sheet_properties.tabColor = NAVY
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(rows) + 1}"
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
        cell.fill = HEADER_FILL
        cell.alignment = WRAP
        cell.border = THIN
    ws.row_dimensions[1].height = 22

    for r_i, row in enumerate(rows, 2):
        fill = ZEBRA_FILL if r_i % 2 == 0 else None
        for c_i, header in enumerate(headers, 1):
            value = cell_value(header, row.get(header))
            cell = ws.cell(r_i, c_i, value)
            cell.font = CELL_FONT
            cell.border = THIN
            if fill:
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
        ref=f"A1:{get_column_letter(len(headers))}{len(rows) + 1}",
    )
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(table)


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
