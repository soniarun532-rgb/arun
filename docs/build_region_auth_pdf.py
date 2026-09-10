#!/usr/bin/env python3
"""Build the client presentation PDF: Client ID Enforcement vs JWT."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
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
RED = colors.HexColor("#C00000")
GREEN = colors.HexColor("#548235")
AMBER = colors.HexColor("#BF8F00")
TEXT = colors.HexColor("#2D2D2D")
MUTED = colors.HexColor("#5B6570")

OUT = Path(__file__).resolve().parent / "SAT-Datashare-Uganda-Malta-Authentication.pdf"


def styles():
    base = getSampleStyleSheet()
    s = {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", parent=base["Normal"], fontName="Helvetica",
            fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=8,
            letterSpacing=1.2,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, textColor=NAVY, alignment=TA_CENTER, leading=28, spaceAfter=10,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"], fontName="Helvetica",
            fontSize=12, textColor=MUTED, alignment=TA_CENTER, leading=16, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=16, textColor=NAVY, spaceBefore=4, spaceAfter=10, leading=20,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12.5, textColor=TEAL, spaceBefore=12, spaceAfter=6, leading=16,
        ),
        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=11, textColor=NAVY, spaceBefore=8, spaceAfter=4, leading=14,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10, textColor=TEXT, alignment=TA_JUSTIFY, leading=14,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=10, textColor=TEXT, leading=13.5, leftIndent=4,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"], fontName="Helvetica",
            fontSize=10, textColor=NAVY, leading=14, alignment=TA_LEFT,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Code"], fontName="Courier",
            fontSize=8.2, textColor=TEXT, leading=11.5, backColor=LIGHT,
            leftIndent=4, rightIndent=4,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, textColor=colors.white, leading=11, alignment=TA_LEFT,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.3, textColor=TEXT, leading=11, alignment=TA_LEFT,
        ),
        "footer": ParagraphStyle(
            "footer", parent=base["Normal"], fontName="Helvetica",
            fontSize=8, textColor=MUTED, alignment=TA_CENTER,
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=8.5, textColor=MUTED, spaceAfter=10, spaceBefore=2,
        ),
    }
    return s


def bullets(items, st):
    return ListFlowable(
        [ListItem(Paragraph(i, st["bullet"]), leftIndent=12, bulletColor=NAVY) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=16,
        bulletFontName="Helvetica",
        bulletFontSize=10,
        spaceAfter=8,
    )


def callout_box(text, st, border=NAVY):
    inner = Paragraph(text, st["callout"])
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def table(headers, rows, st, col_widths):
    head = [Paragraph(h, st["th"]) for h in headers]
    data = [head] + [[Paragraph(c, st["td"]) for c in row] for row in rows]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C5D4E4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW))
    t.setStyle(TableStyle(style))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, A4[1] - 8 * mm, "SAT Datashare  |  Regional access control")
    canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 8 * mm, "Confidential — client discussion")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 4 * mm, "Experience API  ·  Uganda / Malta")
    canvas.drawRightString(A4[0] - 18 * mm, 4 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 38 * mm, A4[0], 38 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, A4[1] - 42 * mm, A4[0], 4 * mm, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 8 * mm, "Not for public distribution")
    canvas.restoreState()


def build():
    st = styles()
    story = []

    story.append(Spacer(1, 48 * mm))
    story.append(Paragraph("SAT SOLUTECH DATASHARE", st["cover_kicker"]))
    story.append(Paragraph("Uganda and Malta data isolation", st["cover_title"]))
    story.append(Paragraph(
        "Same eight Experience API endpoints.<br/>Two regions. Two databases.<br/>"
        "Two authentication options for client review.",
        st["cover_sub"],
    ))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("Approach A — API Manager Client ID Enforcement", st["cover_sub"]))
    story.append(Paragraph("Approach B — JWT (JSON Web Token) validation", st["cover_sub"]))
    story.append(Spacer(1, 16 * mm))
    story.append(Paragraph("Prepared for client discussion", st["cover_sub"]))
    story.append(Paragraph("Experience layer (Exp) decides the database. Callers never send it.", st["cover_sub"]))
    story.append(PageBreak())

    # 1. Context
    story.append(Paragraph("1. What we are solving", st["h1"]))
    story.append(Paragraph(
        "SAT Datashare already exposes eight GET resources through one Experience API: "
        "Invoice, Order, Product, Route, SalesRep, Customer, Stock and Warehouse. "
        "Uganda and Malta will use <b>those same paths</b>. The only difference is which "
        "MySQL schema the System API queries (for example <font face='Courier'>sat_uganda</font> vs "
        "<font face='Courier'>sat_malta</font>).",
        st["body"],
    ))
    story.append(Paragraph(
        "Today the Experience API injects a single schema and supplier on every call. "
        "Clients do not send <font face='Courier'>database</font>. That is correct and must stay that way. "
        "If the caller were allowed to choose the schema, a Uganda integration could request Malta data.",
        st["body"],
    ))
    story.append(Paragraph("The requirement", st["h2"]))
    story.append(bullets([
        "Uganda must not read Malta rows.",
        "Malta must not read Uganda rows.",
        "Identify <b>who is calling</b> from the request itself.",
        "Set database (and supplier if needed) <b>inside the Experience API</b>.",
        "Do not duplicate the eight endpoints or the RAML resources.",
    ], st))
    story.append(callout_box(
        "<b>Non-negotiable rule.</b> The public client never supplies <font face='Courier'>database</font> "
        "or <font face='Courier'>supplier</font>. Those values are derived from authenticated identity in Exp, "
        "then passed privately to Process API and System API.",
        st, border=RED,
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("What we will not ask the client to send", st["h2"]))
    story.append(table(
        ["Parameter", "Who sends it", "Why"],
        [
            ["fromDate, toDate, pageNumber", "Uganda or Malta client", "Business filters. Same for both regions."],
            ["database / supplier", "Experience API only", "Choosing schema is an authorisation decision, not an input."],
            ["region=uganda in query or header", "Must not be trusted", "Anyone can type the other region’s name."],
        ],
        st, [48 * mm, 52 * mm, 70 * mm],
    ))
    story.append(Paragraph(
        "A query parameter or custom header such as <font face='Courier'>X-Region: malta</font> is not authentication. "
        "It is a label the caller controls.",
        st["caption"],
    ))

    # 2. Architecture
    story.append(Paragraph("2. Where identity is enforced", st["h1"]))
    story.append(Paragraph(
        "Traffic stays Exp → Process API (PAPI) → System API (SAPI) → MySQL. "
        "Only Exp is public. PAPI and SAPI must remain private (VPC, DLB or IP allowlist). "
        "If someone can call SAPI with <font face='Courier'>database=sat_malta</font>, Exp never gets a chance to stop them.",
        st["body"],
    ))
    story.append(table(
        ["Layer", "Role in this design"],
        [
            ["Experience API (Exp)", "Authenticate the caller. Map identity → schema. Inject database and supplier. Same eight URLs."],
            ["Process API (PAPI)", "Field mapping and paging only. Uses the schema Exp already chose. Not a public login point."],
            ["System API (SAPI)", "Runs SQL as <font face='Courier'>schema.table</font>. Already supports a database query parameter from trusted callers."],
            ["MySQL", "Two schemas on the same instance (simplest), or two hosts if operations require a hard split later."],
        ],
        st, [42 * mm, 128 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Both options below keep this layering. They differ only in <b>how Exp recognises Uganda vs Malta</b>.",
        st["body"],
    ))

    # 3. Approach A
    story.append(Paragraph("3. Approach A — Client ID Enforcement", st["h1"]))
    story.append(Paragraph(
        "Each region is registered as its own API Manager application. Uganda receives a "
        "<font face='Courier'>client_id</font> and <font face='Courier'>client_secret</font>. Malta receives a different pair. "
        "Anypoint API Manager applies the <b>Client ID Enforcement</b> policy on the Experience API. "
        "A request without a valid pair is rejected before the Mule flow runs.",
        st["body"],
    ))
    story.append(Paragraph("How a call works", st["h2"]))
    story.append(bullets([
        "SAT Uganda stores only the Uganda client_id and secret in its integration.",
        "Every GET to <font face='Courier'>/api/v1/Invoice</font> (and the other seven paths) includes those credentials "
        "(typically headers <font face='Courier'>client_id</font> and <font face='Courier'>client_secret</font>).",
        "API Manager checks the pair against the contracts on this API. Invalid → HTTP 401.",
        "Exp reads the authenticated <font face='Courier'>client_id</font>, looks it up in configuration, and sets "
        "<font face='Courier'>database = sat_uganda</font> (and the Uganda supplier if it differs).",
        "Exp calls PAPI with that schema. PAPI calls SAPI. SQL runs only on Uganda tables.",
        "The same path with Malta credentials resolves to <font face='Courier'>sat_malta</font> only.",
    ], st))
    story.append(Paragraph("Configuration sketch (Experience API properties)", st["h2"]))
    story.append(Preformatted(
        "region.uganda.clientId  =  <<API Manager client_id for Uganda>>\n"
        "region.uganda.database  =  sat_uganda\n"
        "region.uganda.supplier  =  <<Uganda supplier name>>\n"
        "\n"
        "region.malta.clientId   =  <<API Manager client_id for Malta>>\n"
        "region.malta.database   =  sat_malta\n"
        "region.malta.supplier   =  <<Malta supplier name>>",
        st["code"],
    ))
    story.append(Paragraph(
        "Unknown client_id after a successful policy check is treated as forbidden (HTTP 403). "
        "There is no default schema. There is no “if missing, use nobleoutlook”.",
        st["body"],
    ))
    story.append(Paragraph("What the client application does", st["h2"]))
    story.append(table(
        ["Item", "Uganda", "Malta"],
        [
            ["Base URL", "Same Exp host", "Same Exp host"],
            ["Paths", "Same eight GETs", "Same eight GETs"],
            ["Dates / paging", "fromDate, toDate, pageNumber", "fromDate, toDate, pageNumber"],
            ["Credentials", "Uganda client_id + secret", "Malta client_id + secret"],
            ["database query param", "Not sent", "Not sent"],
        ],
        st, [42 * mm, 64 * mm, 64 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Strengths", st["h2"]))
    story.append(bullets([
        "Fastest to deliver on CloudHub: one policy, a small lookup in Exp, no token server.",
        "Fits the current design: Exp already injects database; we only make that lookup identity-based.",
        "Operators can revoke one region in API Manager without redeploying SQL.",
        "No new login screens. Machine-to-machine integrations already understand client_id / secret.",
    ], st))
    story.append(Paragraph("Limits (must be stated to the client)", st["h2"]))
    story.append(callout_box(
        "<b>The client_id and secret <i>are</i> the identity.</b> If Uganda obtains Malta’s pair, the platform "
        "correctly treats them as Malta and returns Malta data. This is the same property as a stolen password. "
        "Client ID Enforcement stops “guess the other schema on the URL”. It does not stop a leaked secret.",
        st, border=AMBER,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Hardening if leakage is a realistic threat: store secrets only in each region’s SAT runtime; rotate on suspected leak; "
        "add an IP allowlist on the policy so Uganda’s credentials only work from Uganda egress IPs; "
        "or deploy two Experience applications so each runtime has only one schema in memory.",
        st["body"],
    ))
    story.append(Paragraph("Operational extras", st["h2"]))
    story.append(bullets([
        "SLA tiers in API Manager can throttle Uganda and Malta independently.",
        "Analytics show which contract called which resource.",
        "Secret rotation is an API Manager action plus an update in that region’s SAT config — not a RAML change.",
    ], st))

    # 4. Approach B
    story.append(Paragraph("4. Approach B — JWT validation", st["h1"]))
    story.append(Paragraph(
        "A JWT is a short-lived, <b>signed</b> statement of identity. An Identity Provider (Anypoint, Okta, Azure AD, or similar) "
        "issues the token. Exp does not trust a region name typed by the caller. It trusts a <font face='Courier'>region</font> "
        "(or <font face='Courier'>tenant</font>) claim that only the issuer can sign.",
        st["body"],
    ))
    story.append(Paragraph("How a call works", st["h2"]))
    story.append(bullets([
        "Uganda’s SAT application authenticates to the token endpoint (client credentials, or a user login if SAT later wants person-level tokens).",
        "The issuer returns a JWT. Typical claims:",
    ], st))
    story.append(Preformatted(
        "{\n"
        '  "sub": "sat-uganda",\n'
        '  "region": "uganda",\n'
        '  "aud": "exp-sat-datashare-api",\n'
        '  "exp": 1778000000\n'
        "}",
        st["code"],
    ))
    story.append(bullets([
        "Uganda calls the same eight paths with <font face='Courier'>Authorization: Bearer &lt;jwt&gt;</font>.",
        "API Manager <b>JWT Validation</b> policy on Exp checks signature, expiry, issuer and audience. Invalid → HTTP 401.",
        "Exp reads <font face='Courier'>region</font> from the validated token and maps <font face='Courier'>uganda → sat_uganda</font>, "
        "<font face='Courier'>malta → sat_malta</font>.",
        "Exp injects database and supplier on the private call to PAPI. Downstream SQL never sees the other schema.",
    ], st))
    story.append(Paragraph("Why a caller cannot forge the other region", st["h2"]))
    story.append(Paragraph(
        "A JWT is three Base64 parts: header, payload, signature. Changing <font face='Courier'>\"region\": \"malta\"</font> "
        "to <font face='Courier'>\"uganda\"</font> breaks the signature. Exp rejects it. That is the difference from a query parameter.",
        st["body"],
    ))
    story.append(Paragraph("What the client application does", st["h2"]))
    story.append(table(
        ["Step", "Uganda", "Malta"],
        [
            ["Get token", "Token URL + Uganda credentials (or user login)", "Token URL + Malta credentials (or user login)"],
            ["Call Exp", "Bearer token on the same eight GETs", "Bearer token on the same eight GETs"],
            ["Token lifetime", "Minutes (recommended 5–15)", "Minutes (recommended 5–15)"],
            ["database query param", "Not sent", "Not sent"],
            ["Refresh", "Request a new JWT when exp is near", "Same"],
        ],
        st, [42 * mm, 64 * mm, 64 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Two flavours of JWT (important for the client)", st["h3"]))
    story.append(table(
        ["Flavour", "Who the token represents", "If credentials leak"],
        [
            ["Client-credentials JWT (machine)", "The Uganda or Malta integration app", "Attacker can mint new tokens for that region until the client secret is revoked. Still cannot mint the other region’s tokens."],
            ["User JWT (authorisation code / SSO)", "A named person in that organisation", "Leak is one user session. Revoke that user. No shared country-wide password."],
        ],
        st, [48 * mm, 52 * mm, 70 * mm],
    ))
    story.append(Paragraph(
        "If the commercial concern is “the two countries might share secrets”, user JWTs are the stronger JWT variant. "
        "Client-credentials JWT is still strictly better than a static client_id on every request, because tokens expire.",
        st["caption"],
    ))
    story.append(Paragraph("Strengths", st["h2"]))
    story.append(bullets([
        "Short-lived: a copied Bearer token dies when <font face='Courier'>exp</font> is reached.",
        "Region is inside a signed claim. Exp does not maintain a large client_id table if the IdP already emits <font face='Courier'>region</font>.",
        "Same pattern scales to more countries later (Kenya, etc.) without new URL paths.",
        "Industry-standard header; many SAT / partner stacks already send Bearer tokens.",
        "Can add scopes later (for example read:invoice) without changing the eight resource names.",
    ], st))
    story.append(Paragraph("Limits", st["h2"]))
    story.append(bullets([
        "Needs a token issuer (Anypoint OpenID, Okta, Azure AD, or similar) and a JWT Validation policy. More moving parts than Client ID Enforcement.",
        "Clients must implement “get token, then call API, then refresh”. Slightly more work than sending two headers.",
        "A stolen <b>valid</b> JWT works until it expires. Keep TTL short; consider token revocation if the IdP supports it.",
        "A stolen <b>client secret</b> used at the token URL can still issue new JWTs for that region. JWT does not magically ignore leaked machine secrets — it contains the blast radius to that region and to a short window.",
    ], st))
    story.append(Paragraph("Experience API mapping after a valid JWT", st["h2"]))
    story.append(Preformatted(
        "region claim \"uganda\"  →  database sat_uganda,  supplier <Uganda>\n"
        "region claim \"malta\"   →  database sat_malta,   supplier <Malta>\n"
        "missing / unknown region →  HTTP 403, no query executed",
        st["code"],
    ))

    # 5. Comparison
    story.append(Paragraph("5. Side-by-side comparison", st["h1"]))
    story.append(table(
        ["Topic", "A — Client ID Enforcement", "B — JWT"],
        [
            ["Identity on each request", "client_id + client_secret (long-lived until rotated)", "Bearer token (minutes)"],
            ["Who decides region", "Exp maps client_id → schema", "IdP signs region/tenant claim; Exp maps claim → schema"],
            ["Same eight endpoints", "Yes", "Yes"],
            ["Caller sends database", "No", "No"],
            ["Forge the other region without its secret", "No", "No (signature would fail)"],
            ["Stolen other region’s secret", "Full access to that region until rotation", "Can mint tokens for that region until secret is revoked; captured JWT dies at exp"],
            ["Time to implement on this stack", "Shortest", "Short, but needs token URL + policy + client token handling"],
            ["Extra platform pieces", "API Manager applications + Client ID policy", "Token issuer + JWT Validation policy + clock skew / JWKS"],
            ["Revoke one country", "Remove or reset that contract in API Manager", "Revoke client or users at the IdP; tokens age out"],
            ["Fits current Exp inject-database pattern", "Yes — replace one property with a lookup", "Yes — lookup keyed by claim instead of client_id"],
            ["Partner familiarity", "Very common on Mule APIs", "Very common for Azure / Okta / OpenID shops"],
            ["Future user-level audit", "Application-level only", "Natural if you issue user JWTs (sub = person)"],
            ["Rate limit per country", "SLA tier per client application", "SLA per client, or per claim if policy supports it"],
        ],
        st, [38 * mm, 66 * mm, 66 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("6. Recommendation", st["h1"]))
    story.append(Paragraph(
        "Both approaches satisfy the functional requirement: same URLs, Exp chooses the schema, Uganda cannot select Malta’s database as a parameter.",
        st["body"],
    ))
    story.append(table(
        ["If the client’s priority is…", "Choose"],
        [
            ["Go live quickly, two machine integrations, secrets stay in each country’s SAT app", "<b>Approach A — Client ID Enforcement</b>"],
            ["Tokens that expire, signed region claim, possible SSO / named users later, or SAT already uses OAuth", "<b>Approach B — JWT</b>"],
            ["Even a stolen secret must not work from the other country", "Either approach <b>plus</b> IP allowlist, mTLS, or two separate Exp applications"],
        ],
        st, [100 * mm, 70 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(callout_box(
        "<b>Practical path.</b> Start with <b>JWT client-credentials</b> if the client already has (or wants) a token URL. "
        "Start with <b>Client ID Enforcement</b> if they want the smallest change to SAT. "
        "Do not start by letting the caller pass region or database. "
        "Keep PAPI and SAPI off the public internet in both cases.",
        st, border=GREEN,
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Suggested decision", st["h2"]))
    story.append(Paragraph(
        "For a two-country machine integration with Anypoint already in place, <b>Client ID Enforcement is the easiest</b> "
        "and is enough if secrets are not shared. <b>JWT is the better long-term standard</b> if the client expects more countries, "
        "short-lived credentials, or future user login. The Experience API mapping is almost identical; swapping A for B later "
        "does not require new Invoice/Order/… resources.",
        st["body"],
    ))

    # 7. What does not change
    story.append(Paragraph("7. What does not change in the APIs", st["h1"]))
    story.append(bullets([
        "The eight GET resources and their payloads / mappings.",
        "Paging (<font face='Courier'>pageNumber</font>, <font face='Courier'>next</font>).",
        "Date filters on Exp (<font face='Courier'>fromDate</font>, <font face='Courier'>toDate</font>).",
        "SAPI SQL shape: still <font face='Courier'>schema.table</font> with the schema name supplied by Exp.",
        "PAPI field mapping (STOREID, ProductID, and the rest).",
        "Exchange RAML resource names. Auth is a policy plus Exp configuration, not eight new paths.",
    ], st))
    story.append(Paragraph(
        "Work on Exp is: attach the chosen API Manager policy, add the region → database map, refuse unknown identities, "
        "and keep ignoring any client-supplied database parameter.",
        st["body"],
    ))

    # 8. Security checklist
    story.append(Paragraph("8. Security checklist (both approaches)", st["h1"]))
    story.append(table(
        ["Control", "Why it matters"],
        [
            ["No public PAPI / SAPI", "Stops bypassing Exp with database=theOtherCountry."],
            ["No database / supplier / region on the public query string", "Caller must not choose the schema."],
            ["TLS on Exp", "Secrets and tokens are not sent in clear text."],
            ["Secrets or private keys only in SAT + API Manager / IdP", "Not in Postman collections shared across countries."],
            ["Rotate on suspected leak", "Client ID reset or IdP client secret rotation."],
            ["Short JWT TTL if Approach B", "Limits the window for a copied Authorization header."],
            ["Logs: client_id or token sub, never the secret or full token", "Audit who hit which resource without leaking credentials."],
            ["Optional IP allowlist / mTLS", "Stolen credential used from the wrong network fails."],
        ],
        st, [70 * mm, 100 * mm],
    ))

    # 9. Implementation outline
    story.append(Paragraph("9. Implementation outline (after the client chooses)", st["h1"]))
    story.append(Paragraph("Approach A", st["h2"]))
    story.append(bullets([
        "Create two API Manager applications (Uganda, Malta) and contract them to the Experience API.",
        "Apply Client ID Enforcement on Exp (headers client_id / client_secret, or the equivalent for the policy version).",
        "Add region properties in Exp. Lookup by client_id. 403 if no match.",
        "Keep process-query-params as the single place that sets database and supplier — sourced from the lookup, not from a static property.",
        "Smoke-test: Uganda credentials return Uganda schema only; Malta the reverse; swapped credentials do not switch schema; missing credentials 401.",
    ], st))
    story.append(Paragraph("Approach B", st["h2"]))
    story.append(bullets([
        "Stand up or reuse a token issuer. Register Uganda and Malta clients. Put <font face='Courier'>region</font> (or tenant) in the access token.",
        "Apply JWT Validation on Exp (JWKS or signed cert, issuer, audience, clock skew).",
        "Exp maps validated <font face='Courier'>region</font> → database / supplier. 403 if claim missing.",
        "Document token URL, required claims, and example Authorization header for each country.",
        "Same smoke tests as A, plus expired token → 401 and tampered region claim → 401.",
    ], st))

    # 10. Open points
    story.append(Paragraph("10. Points to confirm with the client", st["h1"]))
    story.append(bullets([
        "Are Uganda and Malta two <b>schemas on one MySQL</b> (simplest; SAPI already prefixes <font face='Courier'>database.table</font>) or two database servers (needs a second JDBC config in SAPI)?",
        "Is supplier the same string in both countries or different?",
        "Who holds the credentials today — one SAT team or two local teams?",
        "Is there already an IdP (Okta / Azure AD / Anypoint) we should use for JWT?",
        "Is IP allowlist acceptable (known SAT egress IPs per country)?",
        "Do they need named-user audit, or is application-level identity enough?",
    ], st))
    story.append(Spacer(1, 4 * mm))
    story.append(callout_box(
        "<b>Bottom line for the meeting.</b> The eight endpoints stay. The database is not a client input. "
        "Client ID Enforcement is the fastest Mule-native lock. JWT is the same lock with a signed, expiring card "
        "and a cleaner path to more countries and user-level tokens. "
        "Neither replaces the need to keep PAPI/SAPI private and to treat secrets as region-specific.",
        st, border=NAVY,
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Document version 1.0  ·  SAT Datashare Experience API  ·  Uganda / Malta authentication options  ·  For client presentation",
        st["caption"],
    ))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="SAT Datashare — Uganda and Malta authentication options",
        author="SAT Solutech integration",
        subject="Client ID Enforcement vs JWT for regional database isolation",
    )
    doc.build(story, onFirstPage=cover_header_footer, onLaterPages=header_footer)
    print("wrote", OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    build()
