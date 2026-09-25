#!/usr/bin/env python3
"""Client-facing SAT Datashare Experience API test guide. No PRC / SYS detail."""
from __future__ import annotations

import json
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.shared import Cm, Inches, Pt, RGBColor

OUT = Path(__file__).resolve().parent / "SAT-Datashare-Client-Test-Guide-Kenya.docx"

NAVY = RGBColor(0x1F, 0x4E, 0x79)
TEAL = RGBColor(0x2E, 0x75, 0xB6)
TEXT = RGBColor(0x2D, 0x2D, 0x2D)
MUTED = RGBColor(0x5B, 0x65, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
NAVY_HEX = "1F4E79"
TEAL_HEX = "2E75B6"
ROW_HEX = "E9F0F7"
LIGHT_HEX = "F4F7FA"
CODE_HEX = "F3F4F6"
AMBER_HEX = "FFF4D6"

BASE = "https://exp-sat-datashare-prod-api-vx7q2k.2ky31l-1.deu-c1.eu1.cloudhub.io"
TOKEN_URL = (
    "https://login.microsoftonline.com/"
    "f4faf003-d90b-4832-9df8-c8a22d29bdd4/oauth2/v2.0/token"
)
SCOPE = "https://graph.microsoft.com/.default"

SAMPLES = {
    "Invoice": {
        "STOREID": 2655,
        "Discount": 0,
        "SalesRepID": 111,
        "VATAmount": "80.46",
        "RouteID": "",
        "DistributorID": "1000097205",
        "ProductID": "3286535",
        "WarehouseID": 1925,
        "OrderNumber": 265,
        "InvoiceNumber": 2857,
        "InvoiceDate": "24/09/2026",
        "InvoiceTime": "15:46:26",
        "InvoiceStatus": "Delivered",
        "UnitOfMeasure": "PIECE",
        "Currency": "KES",
        "QuantityInvoiced": 10,
        "AmountInvoiced": "583.30",
        "TransType": "Sale",
    },
    "Order": {
        "StoreID": 2348,
        "SalesRepID": 108,
        "RouteID": "",
        "ProductID": "3049801",
        "DistributorID": "1000097205",
        "WarehouseID": 2503,
        "OrderNumber": 320,
        "OrderDate": "24/09/2026",
        "OrderStartTime": "",
        "OrderEndTime": "",
        "OrderStatus": "Open",
        "UnitOfMeasure": "PIECE",
        "Currency": "KES",
        "QuantityOrdered": 5,
        "AmountOrdered": "590.90",
        "Discount": 0,
        "VATAmount": "81.50",
    },
    "Product": {
        "ProductID": "3268896",
        "ProductSKU": "AWICK FRESHMATIC ROSE  + GADGET SEEDING PRICE 250ML (4)",
        "UnitofMeasure": "PIECE",
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
        "ProductSKU": "3300090",
        "UnitofMeasure": "PIECE",
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

DATE_PARAMS = [
    ("fromDate", "Yes", "YYYY-MM-DD", "2026-09-24", "Inclusive start date. Date only. Do not send a time."),
    ("toDate", "Yes", "YYYY-MM-DD", "2026-09-24", "Inclusive end date. Date only. Do not send a time."),
    ("pageNumber", "No", "Integer, 0-based", "0", "Omit on the first call. Use 1, 2, … if a next page is returned."),
]
PAGE_PARAMS = [
    ("pageNumber", "No", "Integer, 0-based", "0", "Omit on the first call. Use 1, 2, … if a next page is returned."),
]

ENDPOINTS = [
    {
        "name": "Invoice",
        "path": "/api/v1/Invoice",
        "params": DATE_PARAMS,
        "query": "fromDate=2026-09-24&toDate=2026-09-24&pageNumber=0",
        "notes": "Returns invoiced sale lines for the date range.",
    },
    {
        "name": "Order",
        "path": "/api/v1/Order",
        "params": DATE_PARAMS,
        "query": "fromDate=2026-09-24&toDate=2026-09-24&pageNumber=0",
        "notes": "Returns order lines for the date range.",
    },
    {
        "name": "Product",
        "path": "/api/v1/Product",
        "params": [],
        "query": "",
        "notes": "Returns the product catalogue.",
    },
    {
        "name": "Route",
        "path": "/api/v1/Route",
        "params": [],
        "query": "",
        "notes": "Returns sales routes.",
    },
    {
        "name": "SalesRep",
        "path": "/api/v1/SalesRep",
        "params": [],
        "query": "",
        "notes": "Returns sales representatives.",
    },
    {
        "name": "Customer",
        "path": "/api/v1/Customer",
        "params": DATE_PARAMS,
        "query": "fromDate=2026-09-24&toDate=2026-09-24&pageNumber=0",
        "notes": "Returns stores created in the date range.",
    },
    {
        "name": "Stock",
        "path": "/api/v1/Stock",
        "params": PAGE_PARAMS,
        "query": "pageNumber=0",
        "notes": "Returns inventory by warehouse.",
    },
    {
        "name": "Warehouse",
        "path": "/api/v1/Warehouse",
        "params": [],
        "query": "",
        "notes": "Returns warehouses.",
    },
]


def shade(cell, hex_color: str) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_border(cell, color="BFBFBF") -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        tcBorders.append(el)
    tcPr.append(tcBorders)


def set_run(run, *, name="Calibri", size=11, bold=False, color=TEXT, italic=False) -> None:
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = name
    run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)


def write_cell(cell, text, *, bold=False, size=10, color=TEXT, font="Calibri", fill=None, align=None) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if align:
        p.alignment = align
    run = p.add_run(text)
    set_run(run, name=font, size=size, bold=bold, color=color)
    if fill:
        shade(cell, fill)
    set_cell_border(cell)


def add_para(doc, text, *, size=11, bold=False, color=TEXT, space_after=8, space_before=0, align=None) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if align:
        p.alignment = align
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color)
    return p


def add_heading_styled(doc, text, size=16) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_run(run, size=size, bold=True, color=NAVY)


def add_code_block(doc, text) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.1
    run = p.add_run(text)
    set_run(run, name="Consolas", size=8.5, color=TEXT)
    shade(cell, CODE_HEX)
    set_cell_border(cell, "D0D5DD")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def set_col_widths(table, widths) -> None:
    table.autofit = False
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width


def style_table(table, header=True) -> None:
    for r_i, row in enumerate(table.rows):
        for cell in row.cells:
            set_cell_border(cell)
            if header and r_i == 0:
                shade(cell, NAVY_HEX)
                for p in cell.paragraphs:
                    for run in p.runs:
                        set_run(run, size=9.5, bold=True, color=WHITE)
            elif r_i % 2 == 0:
                shade(cell, ROW_HEX)


def add_kv_table(doc, rows) -> None:
    table = doc.add_table(rows=len(rows), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(rows):
        write_cell(table.cell(i, 0), k, bold=True, size=10, fill=ROW_HEX)
        write_cell(table.cell(i, 1), v, size=10)
    set_col_widths(table, (Cm(5.2), Cm(12.3)))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_header_footer(doc) -> None:
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""
    run = hp.add_run("SAT Datashare  ·  exp-sat-datashare-prod-api  ·  Kenya client test guide")
    set_run(run, size=9, color=NAVY, bold=True)
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""
    run = fp.add_run("Confidential  ·  For the client test team  ·  Client secret sent separately  ·  Page ")
    set_run(run, size=8.5, color=MUTED)
    # PAGE field
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    run2 = fp.add_run()
    run2._r.append(fld)
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    run3 = fp.add_run()
    run3._r.append(instr)
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run4 = fp.add_run()
    run4._r.append(fld_end)
    for r in (run2, run3, run4):
        set_run(r, size=8.5, color=MUTED)


def token_curl() -> str:
    return (
        f"curl --location '{TOKEN_URL}' \\\n"
        "  --header 'Content-Type: application/x-www-form-urlencoded' \\\n"
        "  --data-urlencode 'grant_type=client_credentials' \\\n"
        "  --data-urlencode 'client_id=<YOUR_KENYA_CLIENT_ID>' \\\n"
        f"  --data-urlencode 'scope={SCOPE}'"
    )


def api_curl(path: str, query: str) -> str:
    url = BASE + path
    if query:
        url = f"{url}?{query}"
    return (
        f"curl --location '{url}' \\\n"
        "  --header 'Authorization: Bearer <ACCESS_TOKEN>' \\\n"
        "  --header 'Accept: application/json'"
    )


def sample_payload(name: str) -> str:
    return json.dumps({"data": [SAMPLES[name]]}, indent=2, ensure_ascii=False)


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    add_header_footer(doc)

    add_para(doc, "CLIENT TEST GUIDE", size=11, bold=True, color=TEAL, space_after=2)
    add_para(doc, "SAT Datashare Experience API", size=22, bold=True, color=NAVY, space_after=4)
    add_para(
        doc,
        "How to request a Kenya token and call the eight production GET endpoints.",
        size=12,
        color=MUTED,
        space_after=10,
    )

    add_kv_table(
        doc,
        [
            ("API name", "exp-sat-datashare-prod-api"),
            ("Base URL", BASE),
            ("Country", "Kenya"),
            ("Database", "sat_nobleoutlook"),
            ("Supplier", "RECKITT BENCKISER"),
            ("Auth", "Azure AD client credentials  →  Bearer access token"),
            ("Date format", "fromDate / toDate = YYYY-MM-DD   (example: 2026-09-24)"),
        ],
    )

    add_heading_styled(doc, "1. What to replace before you test", size=14)
    add_para(
        doc,
        "This document is a template. Replace the placeholders below with the values issued to you. "
        "The client secret is not included here. It will be sent separately.",
        size=11,
        space_after=8,
    )
    table = doc.add_table(rows=3, cols=3)
    headers = ("Placeholder", "Where it is used", "Replace with")
    rows = [
        ("<YOUR_KENYA_CLIENT_ID>", "Token request — client_id", "Kenya OAuth application (client) ID"),
        ("<ACCESS_TOKEN>", "Every GET — Authorization header", "access_token from the token response"),
    ]
    for i, h in enumerate(headers):
        write_cell(table.cell(0, i), h, bold=True, size=9.5, color=WHITE, fill=NAVY_HEX)
    for r, row in enumerate(rows, start=1):
        fill = ROW_HEX if r % 2 == 0 else "FFFFFF"
        write_cell(table.cell(r, 0), row[0], size=9, font="Consolas", fill=fill)
        write_cell(table.cell(r, 1), row[1], size=9.5, fill=fill)
        write_cell(table.cell(r, 2), row[2], size=9.5, fill=fill)
    set_col_widths(table, (Cm(6.2), Cm(5.8), Cm(5.5)))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_styled(doc, "2. Kenya environment", size=14)
    add_para(
        doc,
        "Kenya Reckitt data is selected from your Kenya OAuth client "
        "(sat_nobleoutlook / RECKITT BENCKISER).",
        size=11,
        space_after=8,
    )

    add_heading_styled(doc, "3. Step 1 — get a Kenya access token", size=14)
    add_para(
        doc,
        "Call Azure AD with grant_type=client_credentials. Copy access_token from the JSON response. "
        "Tokens expire (typically about 60 minutes). Request a new token when calls return HTTP 401. "
        "The client secret will be sent separately. Add it to this token request when you receive it.",
        size=11,
        space_after=6,
    )
    add_para(doc, "Token cURL", size=11, bold=True, color=NAVY, space_after=4)
    add_code_block(doc, token_curl())
    add_para(
        doc,
        "Note: the client secret is not shown in this guide. It will be sent separately. "
        "When you have it, include it on the token request as the client_secret form field.",
        size=10.5,
        color=NAVY,
        space_after=8,
    )
    add_para(doc, "Token form fields", size=11, bold=True, color=NAVY, space_after=4)
    t = doc.add_table(rows=4, cols=3)
    for i, h in enumerate(("Field", "Required", "Value")):
        write_cell(t.cell(0, i), h, bold=True, size=9.5, color=WHITE, fill=NAVY_HEX)
    fields = [
        ("grant_type", "Yes", "client_credentials"),
        ("client_id", "Yes", "<YOUR_KENYA_CLIENT_ID>"),
        ("scope", "Yes", SCOPE),
    ]
    for r, row in enumerate(fields, start=1):
        fill = ROW_HEX if r % 2 == 0 else "FFFFFF"
        write_cell(t.cell(r, 0), row[0], size=9.5, font="Consolas", fill=fill)
        write_cell(t.cell(r, 1), row[1], size=9.5, fill=fill)
        write_cell(t.cell(r, 2), row[2], size=9, font="Consolas", fill=fill)
    set_col_widths(t, (Cm(4.5), Cm(3.0), Cm(10.0)))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_para(doc, "Successful token response (shape)", size=11, bold=True, color=NAVY, space_after=4)
    add_code_block(
        doc,
        json.dumps(
            {
                "token_type": "Bearer",
                "expires_in": 3599,
                "ext_expires_in": 3599,
                "access_token": "<ACCESS_TOKEN>",
            },
            indent=2,
        ),
    )

    add_heading_styled(doc, "4. How to call every endpoint", size=14)
    for line in (
        "Use GET. Send only the Authorization header and the query parameters listed for that endpoint.",
        "Authorization: Bearer <ACCESS_TOKEN>",
        "fromDate and toDate are YYYY-MM-DD only. Example: 2026-09-24. Do not send a time (no 00:00:00).",
        "pageNumber is 0-based. First call can omit it or send 0. If the body contains next, call again with the next pageNumber.",
        "A successful call returns HTTP 200 and a JSON object with a data array. Dates inside the payload use dd/MM/yyyy.",
    ):
        p = doc.add_paragraph(style=None)
        p.paragraph_format.left_indent = Cm(0.4)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run("•  " + line)
        set_run(run, size=11, color=TEXT)

    add_heading_styled(doc, "5. Endpoint catalogue", size=14)
    cat = doc.add_table(rows=9, cols=4)
    for i, h in enumerate(("#", "Endpoint", "Path", "Query parameters you send")):
        write_cell(cat.cell(0, i), h, bold=True, size=9, color=WHITE, fill=NAVY_HEX)
    for i, ep in enumerate(ENDPOINTS, start=1):
        fill = ROW_HEX if i % 2 == 0 else "FFFFFF"
        write_cell(cat.cell(i, 0), str(i), size=9.5, fill=fill, align=WD_ALIGN_PARAGRAPH.CENTER)
        write_cell(cat.cell(i, 1), ep["name"], size=9.5, bold=True, fill=fill)
        write_cell(cat.cell(i, 2), ep["path"], size=9, font="Consolas", fill=fill)
        qp = "fromDate, toDate, pageNumber" if ep["params"] is DATE_PARAMS else (
            "pageNumber" if ep["params"] is PAGE_PARAMS else "None"
        )
        write_cell(cat.cell(i, 3), qp, size=9.5, fill=fill)
    set_col_widths(cat, (Cm(1.2), Cm(3.4), Cm(5.2), Cm(7.7)))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    add_heading_styled(doc, "6. Date format", size=14)
    add_para(
        doc,
        "Query parameters fromDate and toDate must be ISO date-only: YYYY-MM-DD. Both dates are inclusive. "
        "The same calendar day is valid (fromDate=2026-09-24 and toDate=2026-09-24). "
        "Payload dates such as InvoiceDate and OrderDate are returned as dd/MM/yyyy.",
        size=11,
        space_after=6,
    )
    df = doc.add_table(rows=4, cols=3)
    for i, h in enumerate(("Use", "Format", "Example")):
        write_cell(df.cell(0, i), h, bold=True, size=9.5, color=WHITE, fill=NAVY_HEX)
    for r, row in enumerate(
        (
            ("fromDate / toDate on the URL", "YYYY-MM-DD", "2026-09-24"),
            ("Do not send", "date + time", "2026-09-24T00:00:00  or  24/09/2026"),
            ("Dates inside the JSON body", "dd/MM/yyyy", "24/09/2026"),
        ),
        start=1,
    ):
        fill = ROW_HEX if r % 2 == 0 else "FFFFFF"
        write_cell(df.cell(r, 0), row[0], size=9.5, fill=fill)
        write_cell(df.cell(r, 1), row[1], size=9.5, font="Consolas", fill=fill)
        write_cell(df.cell(r, 2), row[2], size=9.5, font="Consolas", fill=fill)
    set_col_widths(df, (Cm(6.5), Cm(5.0), Cm(6.0)))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    add_heading_styled(doc, "7. Endpoints — cURL and sample output", size=14)
    add_para(
        doc,
        "For each endpoint: copy the cURL, replace <ACCESS_TOKEN>, and confirm HTTP 200. "
        "Sample output is one production row inside the data array.",
        size=11,
        space_after=8,
    )

    for idx, ep in enumerate(ENDPOINTS, start=1):
        add_heading_styled(doc, f"{idx}) {ep['name']}", size=13)
        add_kv_table(
            doc,
            [
                ("Endpoint name", ep["name"]),
                ("Method", "GET"),
                ("URL", BASE + ep["path"]),
                ("Query parameters", "See table below" if ep["params"] else "None"),
            ],
        )
        add_para(doc, ep["notes"], size=10.5, color=MUTED, space_after=6)

        if ep["params"]:
            add_para(doc, "Query parameters", size=11, bold=True, color=NAVY, space_after=4)
            pt = doc.add_table(rows=1 + len(ep["params"]), cols=5)
            for i, h in enumerate(("Parameter", "Required", "Format", "Example", "What to provide")):
                write_cell(pt.cell(0, i), h, bold=True, size=8.5, color=WHITE, fill=NAVY_HEX)
            for r, row in enumerate(ep["params"], start=1):
                fill = ROW_HEX if r % 2 == 0 else "FFFFFF"
                write_cell(pt.cell(r, 0), row[0], size=8.5, font="Consolas", fill=fill)
                write_cell(pt.cell(r, 1), row[1], size=8.5, fill=fill)
                write_cell(pt.cell(r, 2), row[2], size=8.5, fill=fill)
                write_cell(pt.cell(r, 3), row[3], size=8.5, font="Consolas", fill=fill)
                write_cell(pt.cell(r, 4), row[4], size=8, fill=fill)
            set_col_widths(pt, (Cm(2.8), Cm(2.0), Cm(3.2), Cm(2.6), Cm(6.9)))
            doc.add_paragraph().paragraph_format.space_after = Pt(4)

        add_para(doc, "cURL", size=11, bold=True, color=NAVY, space_after=4)
        add_code_block(doc, api_curl(ep["path"], ep["query"]))
        add_para(doc, "Sample output", size=11, bold=True, color=NAVY, space_after=4)
        add_code_block(doc, sample_payload(ep["name"]))

    add_heading_styled(doc, "8. Expected results", size=14)
    exp = doc.add_table(rows=5, cols=2)
    write_cell(exp.cell(0, 0), "Check", bold=True, size=9.5, color=WHITE, fill=NAVY_HEX)
    write_cell(exp.cell(0, 1), "Pass when", bold=True, size=9.5, color=WHITE, fill=NAVY_HEX)
    checks = [
        ("Token call", "HTTP 200 and an access_token string"),
        ("Each GET", "HTTP 200 and a JSON body with a data array"),
        ("Date endpoints", "Rows fall inside the fromDate / toDate window you sent"),
        ("401 Unauthorized", "Token missing, expired, or wrong client — request a new token"),
    ]
    for i, (k, v) in enumerate(checks, start=1):
        fill = ROW_HEX if i % 2 == 0 else "FFFFFF"
        write_cell(exp.cell(i, 0), k, size=9.5, bold=True, fill=fill)
        write_cell(exp.cell(i, 1), v, size=9.5, fill=fill)
    set_col_widths(exp, (Cm(4.5), Cm(13.0)))

    add_para(
        doc,
        "If you need a different date window, change only fromDate and toDate. Keep the YYYY-MM-DD format.",
        size=11,
        space_before=12,
        space_after=4,
    )

    doc.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(path)
