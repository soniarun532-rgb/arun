#!/usr/bin/env python3
"""Simple client presentation: Client ID (simple) vs JWT (more steps)."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#1F4E79")
TEAL = colors.HexColor("#2E75B6")
LIGHT = colors.HexColor("#F2F6FA")
ROW = colors.HexColor("#E9F0F7")
GREEN = colors.HexColor("#548235")
AMBER = colors.HexColor("#BF8F00")
TEXT = colors.HexColor("#2D2D2D")
MUTED = colors.HexColor("#5B6570")

OUT = Path(__file__).resolve().parent / "SAT-Datashare-Uganda-Malta-Authentication.pdf"


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", parent=base["Normal"], fontName="Helvetica",
            fontSize=11, textColor=colors.white, alignment=TA_CENTER,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=20, textColor=NAVY, alignment=TA_CENTER, leading=26, spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"], fontName="Helvetica",
            fontSize=12, textColor=MUTED, alignment=TA_CENTER, leading=16, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=15, textColor=NAVY, spaceBefore=2, spaceAfter=8, leading=19,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12, textColor=TEAL, spaceBefore=10, spaceAfter=5, leading=15,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, textColor=TEXT, alignment=TA_LEFT, leading=15, spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, textColor=TEXT, leading=15,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, textColor=NAVY, leading=15,
        ),
        "ex": ParagraphStyle(
            "ex", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, textColor=NAVY, spaceBefore=4, spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Code"], fontName="Courier",
            fontSize=8.5, textColor=TEXT, leading=12, backColor=LIGHT,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9, textColor=colors.white, leading=12,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, textColor=TEXT, leading=12,
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, textColor=MUTED, spaceAfter=8,
        ),
    }


def bullets(items, st):
    return ListFlowable(
        [ListItem(Paragraph(i, st["bullet"]), leftIndent=10, bulletColor=NAVY) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=14,
        spaceAfter=8,
    )


def box(text, st, border=NAVY):
    t = Table([[Paragraph(text, st["callout"])]], colWidths=[172 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 1.2, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def table(headers, rows, st, widths):
    data = [[Paragraph(h, st["th"]) for h in headers]]
    data += [[Paragraph(c, st["td"]) for c in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C5D4E4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW))
    t.setStyle(TableStyle(cmds))
    return t


def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 11 * mm, A4[0], 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(16 * mm, A4[1] - 7 * mm, "SAT Datashare  ·  Uganda / Malta  ·  simple explanation")
    canvas.drawRightString(A4[0] - 16 * mm, A4[1] - 7 * mm, f"Page {doc.page}")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.drawString(16 * mm, 3.5 * mm, "For client discussion")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 36 * mm, A4[0], 36 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, A4[1] - 40 * mm, A4[0], 4 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 22 * mm, "SAT DATASHARE")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 7 * mm, "Simple version for the client meeting")
    canvas.restoreState()


def build():
    st = styles()
    story = []

    story.append(Spacer(1, 46 * mm))
    story.append(Paragraph("Uganda and Malta — who can see which data", st["cover_title"]))
    story.append(Paragraph("Same 8 APIs. Two countries. Two databases.", st["cover_sub"]))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("<b>Simple way:</b> Client ID and secret (like a username and password)", st["cover_sub"]))
    story.append(Paragraph("<b>More complete way:</b> JWT token (get a pass, then call the API)", st["cover_sub"]))
    story.append(PageBreak())

    story.append(Paragraph("The idea in one minute", st["h1"]))
    story.append(Paragraph(
        "We have 8 APIs (Invoice, Order, Product, Route, SalesRep, Customer, Stock, Warehouse).",
        st["body"],
    ))
    story.append(Paragraph(
        "Uganda and Malta will call <b>the same URLs</b>. Only the database behind the API is different.",
        st["body"],
    ))
    story.append(Paragraph(
        "The customer must <b>not</b> send the database name. If they could type <font face='Courier'>database=Malta</font>, "
        "Uganda could look at Malta data.",
        st["body"],
    ))
    story.append(box(
        "<b>Simple rule:</b> We look at <i>who is calling</i>. Then <b>our Experience API</b> picks the database. "
        "Uganda login → Uganda data. Malta login → Malta data.",
        st, border=GREEN,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Think of a hotel. Same front door. Uganda guest key opens Uganda rooms only. Malta key opens Malta rooms only. "
        "Nobody is asked “which floor do you want?” — the key already decides.",
        st["body"],
    ))

    story.append(Paragraph("What the customer sends (both ways)", st["h2"]))
    story.append(table(
        ["They send", "They do not send"],
        [
            ["fromDate, toDate, pageNumber", "database name"],
            ["Their login (Client ID <b>or</b> JWT token)", "supplier name"],
            ["Same URL, for example /api/v1/Invoice", "region=uganda or region=malta"],
        ],
        st, [86 * mm, 86 * mm],
    ))

    story.append(PageBreak())
    story.append(Paragraph("Option 1 — Simple: Client ID", st["h1"]))
    story.append(Paragraph(
        "Give each country a <b>ID</b> and a <b>password</b> (called client_id and client_secret).",
        st["body"],
    ))
    story.append(Paragraph("Example", st["h2"]))
    story.append(table(
        ["Country", "ID (example)", "Password (example)", "Database we set"],
        [
            ["Uganda", "ug-client-001", "UgSecret-AAA", "sat_uganda"],
            ["Malta", "mt-client-002", "MtSecret-BBB", "sat_malta"],
        ],
        st, [32 * mm, 40 * mm, 42 * mm, 58 * mm],
    ))
    story.append(Paragraph("Uganda calls Invoice", st["ex"]))
    story.append(Preformatted(
        "GET /api/v1/Invoice?fromDate=2026-08-01&toDate=2026-08-31&pageNumber=0\n"
        "client_id:     ug-client-001\n"
        "client_secret: UgSecret-AAA\n"
        "\n"
        "We see ID ug-client-001  →  we set database = sat_uganda\n"
        "Uganda gets Uganda invoices only.",
        st["code"],
    ))
    story.append(Paragraph("Malta calls the same Invoice URL", st["ex"]))
    story.append(Preformatted(
        "GET /api/v1/Invoice?fromDate=2026-08-01&toDate=2026-08-31&pageNumber=0\n"
        "client_id:     mt-client-002\n"
        "client_secret: MtSecret-BBB\n"
        "\n"
        "We see ID mt-client-002  →  we set database = sat_malta\n"
        "Malta gets Malta invoices only.",
        st["code"],
    ))
    story.append(Paragraph("If Uganda tries to cheat", st["ex"]))
    story.append(Preformatted(
        "GET /api/v1/Invoice?database=sat_malta     ← we ignore this\n"
        "client_id: ug-client-001\n"
        "\n"
        "Still Uganda data. The ID decides, not the URL.",
        st["code"],
    ))
    story.append(Paragraph("Wrong or missing password", st["ex"]))
    story.append(Paragraph("No ID / wrong password → <b>401 not allowed</b>. No data.", st["body"]))
    story.append(box(
        "<b>Easy to explain:</b> two logins, two databases. Same 8 APIs.<br/>"
        "<b>Watch out:</b> if Uganda learns Malta’s ID and password, they can open Malta data — "
        "same as using someone else’s hotel key. Keep passwords private. Change them if leaked.",
        st, border=AMBER,
    ))
    story.append(Paragraph(
        "This is the <b>simple process</b> for the client. Fast to build. SAT already works this way on many Mule APIs.",
        st["body"],
    ))

    story.append(PageBreak())
    story.append(Paragraph("Option 2 — More steps: JWT token", st["h1"]))
    story.append(Paragraph(
        "JWT is a <b>short pass</b> (like a visitor badge that expires in 10 minutes). "
        "You do not send the password on every Invoice call. You first get a badge, then you show the badge.",
        st["body"],
    ))
    story.append(Paragraph("Two steps — example for Uganda", st["h2"]))
    story.append(Paragraph("<b>Step 1 — Get a token</b> (once, then reuse until it expires)", st["body"]))
    story.append(Preformatted(
        "POST /token\n"
        "username / client:  ug-client-001\n"
        "password / secret:  UgSecret-AAA\n"
        "\n"
        "Reply (short example):\n"
        "{\n"
        '  "region": "uganda",\n'
        '  "exp":    "10 minutes from now"\n'
        "}\n"
        "This reply is signed. Nobody can change region to malta without breaking the badge.",
        st["code"],
    ))
    story.append(Paragraph("<b>Step 2 — Call Invoice with the token</b>", st["body"]))
    story.append(Preformatted(
        "GET /api/v1/Invoice?fromDate=2026-08-01&toDate=2026-08-31&pageNumber=0\n"
        "Authorization: Bearer  (the token from step 1)\n"
        "\n"
        "We read region = uganda  →  we set database = sat_uganda",
        st["code"],
    ))
    story.append(Paragraph("Malta is the same two steps", st["h2"]))
    story.append(Preformatted(
        "Step 1: Malta login  →  token with region = malta\n"
        "Step 2: same /api/v1/Invoice + Malta token  →  database = sat_malta",
        st["code"],
    ))
    story.append(Paragraph("If someone copies the token", st["ex"]))
    story.append(Paragraph(
        "It only works until it <b>expires</b> (for example 10 minutes). Then they must login again. "
        "That is the extra safety vs a password that stays the same for months.",
        st["body"],
    ))
    story.append(Paragraph("If someone changes the token text to say “uganda”", st["ex"]))
    story.append(Paragraph(
        "The signature will not match. We reject it. <b>401</b>. They cannot fake the other country.",
        st["body"],
    ))
    story.append(box(
        "<b>Why it is more complex:</b> SAT must call a token URL first, store the token, refresh it when it expires. "
        "We also need a token server (Anypoint / Okta / Azure).<br/>"
        "<b>Why some clients want it:</b> password is not sent on every request; pass expires; easy to add more countries later.",
        st, border=TEAL,
    ))

    story.append(PageBreak())
    story.append(Paragraph("Side by side", st["h1"]))
    story.append(table(
        ["", "Simple — Client ID", "More steps — JWT"],
        [
            ["What Uganda shows", "ID + password on every call", "A token (badge) on every call"],
            ["How many steps", "1 — call the API", "2 — get token, then call the API"],
            ["Same 8 URLs", "Yes", "Yes"],
            ["Who picks database", "We do, from the ID", "We do, from region inside the token"],
            ["Can they type the other database", "No", "No"],
            ["If password is leaked", "Other country can call until we change the password", "They can get new tokens for that country until we revoke; a copied token dies after a few minutes"],
            ["Build effort for us", "Small", "More (token server + policy)"],
            ["Build effort for SAT", "Small", "A bit more (get token, refresh)"],
            ["Best when", "Two systems, go live soon", "They already use OAuth, or want expiry / more countries later"],
        ],
        st, [42 * mm, 65 * mm, 65 * mm],
    ))

    story.append(Paragraph("What we recommend saying in the meeting", st["h2"]))
    story.append(bullets([
        "<b>Start with Client ID</b> if they want the simple process.",
        "<b>Use JWT</b> if they already have login/tokens, or they want the pass to expire.",
        "Either way: same 8 APIs. We set the database. They never send it.",
        "PAPI and SAPI stay internal. Only the Experience API is public.",
        "Passwords / tokens stay in each country’s system. Do not share Uganda login with Malta.",
    ], st))
    story.append(box(
        "<b>One line for the client:</b><br/>"
        "Simple = two passwords, we pick the database.<br/>"
        "JWT = first get a short pass, then call the same APIs. Safer over time, more moving parts.",
        st, border=GREEN,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("What does not change", st["h2"]))
    story.append(bullets([
        "The 8 endpoint names and the Excel mappings.",
        "Dates and paging.",
        "The SQL — only the schema name in front of the table changes (sat_uganda vs sat_malta).",
    ], st))
    story.append(Paragraph(
        "Simple version  ·  SAT Datashare  ·  Uganda / Malta",
        st["caption"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        title="SAT Datashare — Uganda and Malta (simple Client ID vs JWT)",
        author="SAT Solutech integration",
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=later_pages)
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    build()
