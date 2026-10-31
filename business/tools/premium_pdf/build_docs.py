#!/usr/bin/env python3.13
"""Hagiazo Hair — premium editorial PDF builder.

markdown (business/*.md)  ->  designed HTML (cover + body)  ->  Chromium PDF  ->  merged.
Run:  python3.13 build_docs.py            (writes to ./out — needs pandoc, pdfunite, node + playwright)
Outputs are build artefacts: out/ and work/ are git-ignored.
"""
import base64, html, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BIZ = REPO / "business"
OUT = HERE / "out"
WORK = HERE / "work"
FONTS = HERE / "fonts"
for d in (OUT, WORK):
    d.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- catalogue
# (series, number, source, friendly file name)
DOCS = [
    ("Business Document", "00", BIZ / "08_Hagiazo_Vision.md",          "00 The Hagiazo Vision"),
    ("Business Document", "01", BIZ / "07_Business_Summary.md",        "01 Business Summary"),
    ("Business Document", "02", BIZ / "00_Compliance.md",              "02 Compliance One-Pager"),
    ("Business Document", "03", BIZ / "01_Privacy_and_Consent.md",     "03 Privacy & Consent Policy"),
    ("Business Document", "04", BIZ / "02_Brand_Truth.md",             "04 Brand & Theme Guideline"),
    ("Business Document", "05", BIZ / "03_Pricing_and_Costing.md",     "05 Pricing & Costing"),
    ("Business Document", "06", BIZ / "04_Booking_and_Cancellation.md","06 Booking & Cancellation"),
    ("Business Document", "07", BIZ / "05_Consultation_and_Aftercare.md","07 Consultation & Aftercare"),
    ("Business Document", "08", BIZ / "06_Money_and_Direction.md",     "08 Money & Direction"),
    ("Business Document", "09", BIZ / "README.md",                     "09 How To Use This Pack"),
    ("Business Document", "10", BIZ / "09_Trademark_Guide.md",         "10 Trademark Guide"),
]
PRINTABLES = [
    ("form",  BIZ / "client/Consultation_Intake_Form.md", "Consultation & Intake Form"),
    ("cards", BIZ / "client/Aftercare_Cards.md",          "Aftercare Cards"),
]
START_HERE = HERE / "start_here.md"

# --------------------------------------------------------------------------- assets
def b64(path, mime="image/png"):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()

HH_LIGHT = b64(REPO / "assets/hh-light.png")   # ivory monogram → for dark backgrounds
HH_DARK  = b64(REPO / "assets/hh-dark.png")    # ink monogram   → for light backgrounds
FONT_CSS = (FONTS / "fraunces-local.css").read_text().replace("url('fonts/", f"url('file://{FONTS}/")

# --------------------------------------------------------------------------- styles
TOKENS = """
:root{--ink:#131110;--dark:#0D0A07;--accent:#2A2420;--graphite:#45413C;--stone:#ECEBE7;
--cream:#FAFAF8;--text:#1A1714;--muted:#6E6A64;--label:#8A847C;--border:#E3E1DC;--paper:#FFFFFF}
"""
BASE_CSS = TOKENS + FONT_CSS + """
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;font-weight:400;font-size:10.4pt;line-height:1.62;
 color:var(--text);background:var(--cream);-webkit-print-color-adjust:exact;print-color-adjust:exact;
 font-feature-settings:"cv11","ss01","tnum"}
.serif{font-family:Fraunces,Georgia,serif}
.label{font-family:Inter;font-size:7.2pt;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--label)}
.rule{display:block;width:44px;height:2px;background:var(--accent);margin:0 0 14px}
"""

BODY_CSS = BASE_CSS + """
@page{size:A4}
body{padding:0}
.page{padding:0 2mm}
h1{display:none}
h2{font-family:Fraunces,Georgia,serif;font-weight:500;font-size:20.5pt;line-height:1.18;letter-spacing:-.005em;
 color:var(--ink);margin:30pt 0 10pt;padding-top:14pt;border-top:1px solid var(--border);break-after:avoid;position:relative}
h2::before{content:"";display:block;width:44px;height:2px;background:var(--accent);position:absolute;top:-1px;left:0}
h2:first-of-type{margin-top:6pt}
h2 em{font-style:italic;font-weight:400}
h3{font-family:Fraunces,Georgia,serif;font-weight:500;font-size:14pt;line-height:1.25;color:var(--ink);margin:20pt 0 6pt;break-after:avoid}
h4{font-family:Inter;font-size:7.6pt;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--graphite);margin:16pt 0 5pt;break-after:avoid}
p{margin:0 0 8.5pt;orphans:3;widows:3}
p.lede{font-family:Fraunces,Georgia,serif;font-size:13pt;line-height:1.5;color:var(--graphite);font-weight:400;margin:0 0 16pt}
strong{font-weight:600;color:var(--ink)}
em{font-style:italic}
a{color:var(--ink);text-decoration:underline;text-decoration-color:#B9B3AA;text-underline-offset:2px;text-decoration-thickness:1px}
code{font-family:"DejaVu Sans Mono",monospace;font-size:8.6pt;background:var(--stone);padding:1px 4px;color:var(--graphite)}
hr{border:0;border-top:1px solid var(--border);margin:16pt 0}
ul,ol{margin:0 0 9pt;padding-left:16pt}
li{margin:0 0 3.5pt;padding-left:2pt}
ul li::marker{color:var(--label);font-size:9pt}
ol li::marker{font-family:Fraunces;font-weight:500;color:var(--graphite)}
li.task-list-item{list-style:none;margin-left:-16pt;padding-left:22pt;position:relative}
li.task-list-item input{appearance:none;-webkit-appearance:none;position:absolute;left:0;top:3.5pt;width:10pt;height:10pt;
 border:1.2px solid var(--accent);background:#fff;margin:0}
li.task-list-item input:checked::after{content:"";position:absolute;left:2px;top:2px;right:2px;bottom:2px;background:var(--accent)}
del{color:var(--label);text-decoration-color:var(--label)}
blockquote{margin:12pt 0 14pt;padding:2pt 0 2pt 16pt;border-left:2px solid var(--accent);break-inside:avoid}
blockquote p{font-family:Fraunces,Georgia,serif;font-style:italic;font-size:11.4pt;line-height:1.55;color:var(--graphite);margin:0 0 6pt}
blockquote p:last-child{margin:0}
blockquote.notice{border:0;background:var(--stone);padding:11pt 14pt 11pt 14pt}
blockquote.notice p{font-family:Inter;font-style:normal;font-size:9.4pt;color:var(--text)}
blockquote strong{color:var(--ink)}
table{width:100%;border-collapse:collapse;margin:8pt 0 14pt;font-size:9.3pt;line-height:1.45;break-inside:auto}
thead th{font-family:Inter;font-size:7pt;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--label);
 text-align:left;padding:0 9pt 7pt 0;border-bottom:1px solid var(--ink);vertical-align:bottom}
thead th:first-child,tbody td:first-child{padding-left:0}
tbody td{padding:6.5pt 9pt 6.5pt 0;border-bottom:1px solid var(--border);vertical-align:top}
tbody tr{break-inside:avoid}
tbody tr:last-child td{border-bottom:1px solid var(--ink)}
td strong{font-weight:600}
table.kv td:first-child{width:30%;color:var(--graphite);font-weight:500}
table.changelog{font-size:8.3pt;color:var(--muted)}
table.changelog td,table.changelog th{padding-top:4pt;padding-bottom:4pt}
h2.changelog{font-size:9pt;font-family:Inter;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--label);margin-top:34pt;padding-top:12pt}
h2.changelog::before{display:none}

pre{background:var(--stone);padding:10pt 12pt;font-size:8.2pt;line-height:1.5;white-space:pre-wrap;margin:8pt 0 12pt;color:var(--graphite)}
pre code{background:none;padding:0;font-size:inherit}
/* brand tree */
.tree{margin:10pt 0 18pt;break-inside:avoid}
.tree .parent{display:inline-block;border:1.2px solid var(--ink);padding:8pt 18pt;font-family:Inter;font-size:9pt;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:var(--ink);background:#fff}
.tree .pnote{display:block;font-family:Fraunces;font-style:italic;font-size:9pt;color:var(--muted);margin:5pt 0 0}
.tree .stem{width:1px;height:14pt;background:var(--graphite);margin:6pt 0 0 60pt}
.tree .bar{height:1px;background:var(--graphite);margin:0 0 0 60pt;width:calc(100% - 60pt - 11.5%)}
.tree .kids{display:grid;grid-template-columns:repeat(4,1fr);gap:0}
.tree .kid{position:relative;padding:14pt 8pt 0 0}
.tree .kid::before{content:"";position:absolute;left:60pt;top:0;width:1px;height:12pt;background:var(--graphite)}
.tree .kid:first-child::before{left:60pt}
.tree .kid .name{font-family:Fraunces;font-size:11.5pt;color:var(--ink);line-height:1.2}
.tree .kid .name b{font-weight:500}
.tree .kid .st{font-family:Inter;font-size:6.6pt;letter-spacing:.2em;text-transform:uppercase;color:var(--label);font-weight:600;margin-top:3pt}
.tree .kid.live .st{color:#2D6A4F}
/* control strip */
.control{display:grid;grid-template-columns:repeat(4,1fr);gap:10pt 18pt;border-top:1px solid var(--ink);border-bottom:1px solid var(--border);
 padding:11pt 0;margin:0 0 20pt}
.control div{min-width:0}
.control .k{font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--label);font-weight:600;margin-bottom:2pt}
.control .v{font-size:8.9pt;line-height:1.4;color:var(--text)}

/* chips, dots, fields */
.tag{display:inline-block;font-family:Inter;font-size:6.6pt;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--graphite);
 border:1px solid var(--graphite);padding:1.5pt 5.5pt 1pt;vertical-align:2px;line-height:1.2;margin:0 2pt;white-space:nowrap}
.tag.assume{border-style:dashed}
h2 .tag{font-size:7pt;vertical-align:6px;margin-left:8pt}
.dot{display:inline-block;width:7pt;height:7pt;border-radius:50%;vertical-align:-0.5pt;margin-right:5pt;border:1px solid transparent}
.dot-g{background:#2D6A4F}.dot-a{background:#C9A227}.dot-r{background:#9B2C2C}.dot-n{background:transparent;border-color:var(--label)}
.warn{display:inline-block;width:11pt;height:11pt;border:1.2px solid var(--ink);color:var(--ink);font-size:7.5pt;font-weight:700;text-align:center;line-height:10pt;margin-right:5pt;vertical-align:0}
.tick{color:#2D6A4F;font-weight:700}.cross{color:#9B2C2C;font-weight:700}
.box{display:inline-block;width:9pt;height:9pt;border:1.1px solid var(--accent);vertical-align:-1pt;margin:0 3pt 0 0;background:#fff}
.fill{display:inline-block;font-family:Fraunces,Georgia,serif;font-style:italic;color:var(--graphite);border-bottom:1px dotted var(--graphite);
 padding:0 3pt;line-height:1.1;margin:0 1pt;position:relative;white-space:nowrap}
.fill i{font-family:Inter;font-style:normal;font-size:5.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--label);margin-left:4pt;vertical-align:2pt}
.rulefield{display:inline-block;min-width:120pt;width:100%;border-bottom:1px solid var(--graphite);height:11pt;vertical-align:baseline}
"""

COVER_CSS = BASE_CSS + """
@page{size:A4;margin:0}
body{background:var(--dark);color:#FAFAF8;width:210mm;height:297mm;overflow:hidden;position:relative}
.frame{position:absolute;inset:12mm;border:1px solid rgba(250,250,248,.16)}
.mono{position:absolute;top:22mm;left:22mm;width:14mm}
.house{position:absolute;top:24mm;right:22mm;text-align:right}
.house .label{color:rgba(250,250,248,.62)}
.house .sub{font-family:Fraunces;font-style:italic;font-size:9.5pt;color:rgba(250,250,248,.5);margin-top:2mm}
.titleblock{position:absolute;left:22mm;right:22mm;top:112mm}
.titleblock .label{color:rgba(250,250,248,.62);margin-bottom:5mm;display:block}
.titleblock .rule{background:rgba(250,250,248,.82);margin-bottom:9mm}
.titleblock h1{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:46pt;line-height:1.04;letter-spacing:-.012em;margin:0 0 7mm;color:#FAFAF8;max-width:150mm}
.titleblock h1 em{font-style:italic;font-weight:300}
.titleblock .subtitle{font-family:Fraunces,Georgia,serif;font-style:italic;font-weight:300;font-size:15pt;line-height:1.4;color:rgba(250,250,248,.66);max-width:140mm;margin:0}
.meta{position:absolute;left:22mm;right:22mm;bottom:40mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm 6mm;border-top:1px solid rgba(250,250,248,.18);padding-top:5mm}
.meta .k{font-size:6.6pt;letter-spacing:.22em;text-transform:uppercase;color:rgba(250,250,248,.5);font-weight:600;margin-bottom:1.2mm}
.meta .v{font-size:8.6pt;line-height:1.45;color:rgba(250,250,248,.9)}
.foot{position:absolute;left:22mm;right:22mm;bottom:22mm;display:flex;justify-content:space-between;align-items:flex-end}
.foot .label{color:rgba(250,250,248,.55)}
.foot .strap{font-family:Fraunces;font-style:italic;font-size:11pt;color:rgba(250,250,248,.82)}
.num{position:absolute;right:22mm;top:112mm;font-family:Fraunces;font-weight:300;font-size:46pt;line-height:1;color:rgba(250,250,248,.22);letter-spacing:-.02em}
"""

PRINT_CSS = BASE_CSS + """
@page{size:A4;margin:0}
.lockup{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:1px solid var(--ink);padding-bottom:9pt;margin-bottom:14pt}
.lockup .left{display:flex;align-items:center;gap:10pt}
.lockup img{width:11mm}
.lockup .name{font-family:Inter;font-size:8pt;font-weight:600;letter-spacing:.26em;text-transform:uppercase;color:var(--ink)}
.lockup .strap{font-family:Fraunces;font-style:italic;font-size:9.5pt;color:var(--muted);margin-top:1pt}
.lockup .right{text-align:right}
.lockup .right .label{display:block}
.lockup .right .house{font-family:Fraunces;font-style:italic;font-size:8.5pt;color:var(--label)}
h1{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:26pt;line-height:1.1;letter-spacing:-.01em;margin:0 0 6pt;color:var(--ink)}
p.lede{font-family:Fraunces,Georgia,serif;font-size:11.2pt;line-height:1.5;color:var(--graphite);margin:0 0 14pt}
h2{font-family:Inter;font-size:7.6pt;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--label);margin:16pt 0 6pt;break-after:avoid}
h2::before{content:"";display:block;width:44px;height:2px;background:var(--accent);margin-bottom:7pt}
table{width:100%;border-collapse:collapse;margin:0 0 10pt;font-size:9.4pt}
td{padding:7pt 8pt 7pt 0;border-bottom:1px solid var(--border);vertical-align:bottom;line-height:1.5}
tr{break-inside:avoid}
table.kv td:first-child{width:36%;font-weight:500;color:var(--graphite);font-size:8.8pt}
hr{border:0;border-top:1px solid var(--border);margin:12pt 0}
.rulefield{display:inline-block;min-width:60pt;width:98%;border-bottom:1px solid var(--graphite);height:10pt;vertical-align:baseline}
.box{display:inline-block;width:9.5pt;height:9.5pt;border:1.1px solid var(--accent);vertical-align:-1.5pt;margin:0 4pt 0 0;background:#fff}
strong{font-weight:600;color:var(--ink)} em{font-style:italic}
ul{margin:0 0 8pt;padding-left:14pt} li{margin:0 0 3pt}
p{margin:0 0 7pt}
.sign{display:grid;grid-template-columns:1fr 1fr;gap:16pt;margin-top:10pt}
.sign div{border-top:1px solid var(--graphite);padding-top:4pt;font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:var(--label);font-weight:600;margin-top:28pt}
.pfoot{margin-top:18pt;border-top:1px solid var(--border);padding-top:7pt;display:flex;justify-content:space-between;font-size:7pt;letter-spacing:.18em;text-transform:uppercase;color:var(--label);font-weight:600}
/* cards */
.cards{display:grid;grid-template-columns:1fr;gap:9mm}
.card{border:1px solid var(--ink);padding:9mm 11mm 8mm;break-inside:avoid;position:relative;background:#fff;min-height:96mm;display:flex;flex-direction:column}
.card .chead{display:flex;justify-content:space-between;align-items:center;margin-bottom:6mm}
.card .chead img{width:9mm}
.card .chead .name{font-family:Inter;font-size:7pt;font-weight:600;letter-spacing:.26em;text-transform:uppercase;color:var(--ink)}
.card .chead .strap{font-family:Fraunces;font-style:italic;font-size:8.5pt;color:var(--muted)}
.card h2{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:19pt;letter-spacing:-.01em;text-transform:none;color:var(--ink);margin:0 0 3mm}
.card h2::before{display:none}
.card p.hook{font-family:Fraunces;font-style:italic;font-size:11.5pt;color:var(--graphite);margin:0 0 5mm}
.card ul{list-style:none;padding:0;margin:0 0 auto}
.card li{padding:4pt 0;border-top:1px solid var(--border);font-size:9.4pt;line-height:1.5;margin:0}
.card li:last-child{border-bottom:1px solid var(--border)}
.card p.cfoot{font-family:Fraunces;font-style:italic;font-size:8.6pt;color:var(--label);margin:6mm 0 0}
.card .bigmono{position:absolute;right:9mm;bottom:8mm;width:16mm;opacity:.08}
.cutnote{font-size:7.2pt;letter-spacing:.18em;text-transform:uppercase;color:var(--label);font-weight:600;margin:0 0 7mm}
"""

# --------------------------------------------------------------------------- markdown preprocessing
EMOJI = {
    "🟢": '<span class="dot dot-g"></span>', "🟡": '<span class="dot dot-a"></span>',
    "🔴": '<span class="dot dot-r"></span>', "⚪": '<span class="dot dot-n"></span>',
    "⏳": '<span class="dot dot-a"></span>', "⚠️": '<span class="warn">!</span>', "⚠": '<span class="warn">!</span>',
    "✅": '<span class="tick">✓</span>', "❌": '<span class="cross">✕</span>', "☐": '<span class="box"></span>',
    "✦": "✦", "→": "→",
}
TAG_RE = re.compile(r"(\*\*)?\[(REGULATORY|BEST PRACTICE|ASSUMPTION)([^\]]*)\](\*\*)?")
FILL_RE = re.compile(r"(\*\*)?\[([^\[\]<>`]{1,48})\](?!\()(\*\*)?")

def tag_sub(m):
    kind, rest = m.group(2), m.group(3).strip(" —–-:")
    cls = " assume" if kind == "ASSUMPTION" else ""
    text = kind if not rest else f"{kind} · {rest}"
    return f'<span class="tag{cls}">{html.escape(text)}</span>'

def fill_sub(m):
    body = m.group(2).strip()
    if body in ("", " ", "x", "X"):          # task-list boxes
        return m.group(0)
    body = re.sub(r"\*\*", "", body)
    return f'<span class="fill">{body}<i>to confirm</i></span>'

def transform_inline(seg):
    for k, v in EMOJI.items():
        seg = seg.replace(k, v)
    seg = TAG_RE.sub(tag_sub, seg)
    seg = FILL_RE.sub(fill_sub, seg)
    seg = re.sub(r"_{5,}", '<span class="rulefield"></span>', seg)
    return seg

def transform_line(line):
    if line.lstrip().startswith(("- [ ]", "* [ ]", "- [x]", "* [x]")):
        head, rest = line.split("]", 1)
        return head + "]" + transform_inline(rest)
    parts = line.split("`")
    return "`".join(transform_inline(p) if i % 2 == 0 else p for i, p in enumerate(parts))

def parse_doc(md_text):
    """Return (title, subtitle, control:dict, body_md)."""
    lines = md_text.splitlines()
    title, subtitle, control, body = "", "", {}, []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not title and ln.startswith("# "):
            t = ln[2:].strip()
            m = re.match(r"^(?:BIZ-\d+\s+—\s+)?(.*?)\s*(?:\*\((.*?)\)\*)?\s*$", t)
            title, subtitle = m.group(1), (m.group(2) or "")
            i += 1; continue
        if ln.startswith("> **Document control**"):
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                row = lines[i].lstrip("> ").strip()
                m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|$", row)
                if m:
                    control[m.group(1)] = m.group(2)
                i += 1
            continue
        body.append(ln); i += 1
    # drop a leading hr / blank lines left after control
    while body and body[0].strip() in ("", "---"):
        body.pop(0)
    return title, subtitle, control, "\n".join(body)

TREE_HTML = """<div class="tree">
<span class="parent">Hagiazo</span><span class="pnote">the parent — the house. Distinct mark: to come.</span>
<div class="stem"></div><div class="bar"></div>
<div class="kids">
<div class="kid live"><div class="name">Hagiazo <b>Hair</b></div><div class="st">Venture I · live</div></div>
<div class="kid"><div class="name">Hagiazo <b>Homes</b></div><div class="st">Venture II · next</div></div>
<div class="kid"><div class="name">Hagiazo <b>Beauty</b></div><div class="st">Envisioned</div></div>
<div class="kid"><div class="name">Hagiazo <b>…</b></div><div class="st">Next ventures</div></div>
</div></div>"""

def md_to_html(md):
    md = re.sub(r"```\n\s+HAGIAZO.*?```", TREE_HTML, md, flags=re.S)
    md = "\n".join(transform_line(l) for l in md.splitlines())
    r = subprocess.run(["pandoc", "-f", "markdown+task_lists+pipe_tables+strikeout+raw_html-smart", "-t", "html5", "--wrap=none"],
                       input=md, text=True, capture_output=True, check=True)
    h = r.stdout
    # lead paragraph
    h = re.sub(r"^\s*<p>", '<p class="lede">', h, count=1)
    # blockquote classes
    h = re.sub(r'<blockquote>\s*<p>\s*(<span class="warn">)', r'<blockquote class="notice"><p>\1', h)
    # key/value tables (two columns, blank header) → .kv ; change-log table → .changelog
    h = re.sub(r"<table>\s*<colgroup>.*?</colgroup>", "<table>", h, flags=re.S)
    h = re.sub(r"<table>\s*<thead>\s*<tr[^>]*>\s*<th[^>]*></th>\s*<th[^>]*></th>\s*</tr>\s*</thead>", '<table class="kv">', h, flags=re.S)
    h = re.sub(r"<table>\s*<thead>\s*<tr[^>]*>\s*<th[^>]*>Field</th>", '<table class="kv"><thead><tr><th>Field</th>', h)
    h = re.sub(r'<h2 id="change-log">(.*?)</h2>\s*<table>', r'<h2 class="changelog" id="change-log">\1</h2><table class="changelog">', h, flags=re.S)
    h = re.sub(r'<h2 id="change-log">', '<h2 class="changelog" id="change-log">', h)
    h = h.replace('<th style="text-align: left;">', "<th>").replace('<td style="text-align: left;">', "<td>")
    h = re.sub(r'<input type="checkbox" disabled="" ?/?>', '<input type="checkbox" disabled>', h)
    return h

def control_value(v):
    v = transform_inline(v)
    v = re.sub(r"\*\*(.+?)\*\*", r"\1", v)
    v = re.sub(r"\*(.+?)\*", r"<em>\1</em>", v)
    v = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", v)
    v = re.sub(r"`(.+?)`", r"\1", v)
    return v

def italic_accent(title):
    """Italicise the word after an em dash or the final word, editorially."""
    if " — " in title:
        a, b = title.split(" — ", 1)
        return f"{html.escape(a)} — <em>{html.escape(b)}</em>"
    words = title.split()
    if len(words) >= 3:
        return html.escape(" ".join(words[:-1])) + f" <em>{html.escape(words[-1])}</em>"
    return html.escape(title)

# --------------------------------------------------------------------------- html assembly
def cover_html(series, num, title, subtitle, control):
    keys = [k for k in ("Status", "Owner", "Owners", "Date", "Review cycle") if k in control][:4]
    meta = "".join(f'<div><div class="k">{html.escape(k)}</div><div class="v">{control_value(control[k])}</div></div>' for k in keys)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{COVER_CSS}</style></head><body>
<div class="frame"></div>
<img class="mono" src="{HH_LIGHT}" alt="">
<div class="house"><span class="label">Hagiazo Hair · Operating Pack</span><div class="sub">A venture of Hagiazo</div></div>
<div class="num">{num}</div>
<div class="titleblock">
  <span class="label">{html.escape(series)} {num}</span>
  <span class="rule"></span>
  <h1>{italic_accent(title)}</h1>
  <p class="subtitle">{html.escape(subtitle) if subtitle else ""}</p>
</div>
<div class="meta">{meta}</div>
<div class="foot"><span class="label">Harlow, Essex · Confidential — internal working document</span><span class="strap">Be set apart</span></div>
</body></html>"""

def body_html(title, control, content):
    order = ["Reference", "Status", "Owner", "Owners", "Prepared by", "Approved by", "Date", "Review cycle", "Reference build"]
    keys = [k for k in order if k in control][:8]
    strip = ""
    if keys:
        strip = '<div class="control">' + "".join(
            f'<div><div class="k">{html.escape(k)}</div><div class="v">{control_value(control[k])}</div></div>' for k in keys) + "</div>"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BODY_CSS}</style></head><body><div class="page">
{strip}{content}
</div></body></html>"""

def header_tpl(title):
    return f"""<div style="font-family:Inter,sans-serif;font-size:6.4pt;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#8A847C;
 width:100%;padding:0 22mm;margin-top:11mm;display:flex;justify-content:space-between;-webkit-print-color-adjust:exact">
 <span>{html.escape(title)}</span><span>Hagiazo Hair</span></div>"""

FOOTER_TPL = """<div style="font-family:Inter,sans-serif;font-size:6.4pt;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#8A847C;
 width:100%;padding:0 22mm;margin-bottom:11mm;display:flex;justify-content:space-between;-webkit-print-color-adjust:exact">
 <span>A venture of Hagiazo &nbsp;·&nbsp; <span style="font-family:Fraunces,Georgia,serif;font-style:italic;text-transform:none;letter-spacing:0;font-size:8pt;font-weight:400">Be set apart</span></span>
 <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""

# --------------------------------------------------------------------------- printables
def printable_html(kind, md_text, name):
    title, subtitle, control, body = parse_doc(md_text)
    # first italic strap line "*Be set apart* ..." → lede
    lines = body.splitlines()
    lede = ""
    if lines and lines[0].startswith("*Be set apart*"):
        lede = lines.pop(0).replace("*Be set apart*", "").lstrip(" ·").strip()
        while lines and lines[0].strip():
            lede += " " + lines.pop(0).strip()
    body = "\n".join(lines)
    content = md_to_html(body)
    content = content.replace('<p class="lede">', "<p>", 1)
    lockup = f"""<div class="lockup"><div class="left"><img src="{HH_DARK}" alt=""><div><div class="name">Hagiazo Hair</div><div class="strap">Be set apart</div></div></div>
    <div class="right"><span class="label">Client printable</span><span class="house">A venture of Hagiazo</span></div></div>"""
    if kind == "form":
        content = content.replace("<hr />", "").replace("<hr>", "")
        inner = f"""{lockup}<h1>{html.escape(title.replace('Hagiazo Hair — ', ''))}</h1><p class="lede">{html.escape(lede) if lede else ''}</p>{content}
        {'' if 'signature' in content.lower() else '<div class="sign"><div>Client signature</div><div>Date</div></div>'}
        <div class="pfoot"><span>Hagiazo Hair · Harlow, Essex</span><span>Your details stay private — see our Privacy Policy</span></div>"""
    else:
        # split into cards on <h2
        parts = re.split(r"(?=<h2 )", content)
        intro = parts[0].replace("<hr />", "").replace("<hr>", "")
        cards = ""
        for sec in parts[1:]:
            sec = sec.replace("<hr />", "").replace("<hr>", "")
            sec = re.sub(r'<h2 id="[^"]*">✦\s*', "<h2>", sec)
            sec = re.sub(r"<p><strong>(.*?)</strong></p>", r'<p class="hook">\1</p>', sec, count=1)
            sec = re.sub(r"<p><em>(.*?)</em></p>\s*$", r'<p class="cfoot">\1</p>', sec.strip())
            chead = f'<div class="chead"><div><div class="name">Hagiazo Hair</div><div class="strap">Be set apart</div></div><img src="{HH_DARK}" alt=""></div>'
            cards += f'<div class="card">{chead}{sec}<img class="bigmono" src="{HH_DARK}" alt=""></div>'
        inner = f"""{lockup}<h1>{html.escape(title.replace('Hagiazo Hair — ', ''))}</h1><p class="lede">{html.escape(lede)}</p>{intro}
        <p class="cutnote">Print on card · trim to the frame · one per client</p><div class="cards">{cards}</div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{PRINT_CSS}</style></head><body><div class="page">{inner}</div></body></html>"""

# --------------------------------------------------------------------------- jobs
jobs = []
def add_doc(series, num, src, friendly, out_dir):
    title, subtitle, control, body = parse_doc(src.read_text())
    if src.name == "README.md":
        title, subtitle = "How To Use This Pack", "how the documents work together, and the tags they use"
        control = {"Status": "🟢 Current", "Owners": "Ruvimbo & Elkelvin", "Date": "2026-10-31", "Review cycle": "When a document is added"}
    stem = re.sub(r"[^\w]+", "_", friendly)
    (WORK / f"{stem}.cover.html").write_text(cover_html(series, num, title, subtitle, control))
    (WORK / f"{stem}.body.html").write_text(body_html(title, control, md_to_html(body)))
    jobs.append({"kind": "doc", "cover": str(WORK / f"{stem}.cover.html"), "body": str(WORK / f"{stem}.body.html"),
                 "header": header_tpl(f"{num} · {title}"), "footer": FOOTER_TPL,
                 "out": str(out_dir / f"{friendly}.pdf")})

def add_printable(kind, src, friendly, out_dir):
    stem = re.sub(r"[^\w]+", "_", friendly)
    (WORK / f"{stem}.html").write_text(printable_html(kind, src.read_text(), friendly))
    jobs.append({"kind": "print", "body": str(WORK / f"{stem}.html"), "out": str(out_dir / f"{friendly}.pdf")})

def main():
    docs_dir = OUT / "Business Documents (PDF)"; docs_dir.mkdir(exist_ok=True)
    cl_dir = OUT / "Client Printables (PDF)"; cl_dir.mkdir(exist_ok=True)
    only = sys.argv[1:]
    for series, num, src, friendly in DOCS:
        if only and not any(o in friendly for o in only): continue
        add_doc(series, num, src, friendly, docs_dir)
    for kind, src, friendly in PRINTABLES:
        if only and not any(o in friendly for o in only): continue
        add_printable(kind, src, friendly, cl_dir)
    if START_HERE.exists() and (not only or any("START" in o for o in only)):
        add_doc("Operating Pack", "", START_HERE, "START HERE", OUT)
    (WORK / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(HERE / "render.js"), str(WORK / "jobs.json")], check=True)
    print(f"built {len(jobs)} pdf(s) → {OUT}")

if __name__ == "__main__":
    main()
