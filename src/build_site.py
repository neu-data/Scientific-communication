"""Builds the course website into docs/ for GitHub Pages.

Following the neu-data course sites, the facilitator guide is not published here:
participants should not see the model answers before the session.
"""
import html
import json
import shutil
from pathlib import Path

import course as c
import sources as src

ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs"
MAT = ROOT / "materials"
DL = DOCS / "downloads"
DL.mkdir(parents=True, exist_ok=True)
(DOCS / ".nojekyll").write_text("")
shutil.copy(ROOT / "src/assets/neudata-logo-transparent.png", DOCS / "neudata-logo.png")

W = json.load(open(ROOT / "src/_workshop_slides.json"))
T = json.load(open(ROOT / "src/_talk_slides.json"))

CSS = """
:root{--teal:#055F56;--navy:#04242F;--blue:#0B376C;--mist:#EAF2F5;--ink:#1F2D33;--grey:#5B6B74;--line:#C9D5DA}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:17px/1.6 "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--blue)}
header{background:var(--navy);border-bottom:4px solid var(--teal)}
.bar{max-width:1040px;margin:0 auto;padding:10px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px}
.bar img{height:40px;background:#fff;border-radius:6px;padding:2px 6px}
.bar strong{color:#fff;font-weight:600;margin-right:auto}
nav a{color:#fff;text-decoration:none;margin-right:16px;white-space:nowrap}
nav a:hover,nav a[aria-current]{text-decoration:underline}
main{max-width:1040px;margin:0 auto;padding:28px 16px 48px}
h1,h2,h3{font-family:"Century Gothic","URW Gothic","Avenir Next","Segoe UI",Arial,sans-serif;color:var(--navy);line-height:1.25}
h1{font-size:2.1rem;margin:.2em 0 .4em}
h2{font-size:1.35rem;margin-top:1.8em;border-bottom:2px solid var(--teal);padding-bottom:4px}
.lead{font-size:1.15rem;max-width:44em}
.note{background:var(--mist);border-left:4px solid var(--teal);padding:12px 16px;margin:16px 0}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.card{background:var(--mist);padding:16px 18px}
.card h3{margin:0 0 6px;font-size:1.1rem}
.wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.94rem;margin:12px 0}
th{background:var(--navy);color:#fff;text-align:left;padding:7px 10px}
td{border-bottom:1px solid var(--line);padding:7px 10px;vertical-align:top}
tfoot td{font-weight:600}
footer{background:var(--navy);color:#fff;font-size:.9rem}
footer div{max-width:1040px;margin:0 auto;padding:16px}
footer a{color:#fff}
ul{padding-left:1.2em}
""".strip()
(DOCS / "style.css").write_text(CSS, encoding="utf8")

PAGES = [("index.html", "Home"), ("workshop.html", "Three-hour workshop"), ("talk.html", "One-hour talk"), ("materials.html", "Materials"), ("evidence.html", "Evidence")]


def page(fn, title, body):
    nav = "".join(f'<a href="{f}"{" aria-current=page" if f == fn else ""}>{t}</a>' for f, t in PAGES)
    doc = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Scientific Communication | neu-data</title>
<meta name="description" content="Teaching materials on scientific writing, slide design and presentation skills from Neudata Consulting Ltd.">
<link rel="icon" href="neudata-logo.png"><link rel="stylesheet" href="style.css"></head><body>
<header><div class="bar"><img src="neudata-logo.png" alt="Neudata logo"><strong>Scientific Communication</strong><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer><div><strong>Neudata Consulting Ltd</strong>, Insight. Impact. Innovation. #ClearDataClearImpact<br>
<a href="https://www.neu-data.com">www.neu-data.com</a>. Copyright Neudata, 2026. All rights reserved.</div></footer>
</body></html>"""
    (DOCS / fn).write_text(doc, encoding="utf8")


def schedule(items):
    rows = "".join(f"<tr><td>{c.fmt(s)} to {c.fmt(e)}</td><td>{m}</td><td>{html.escape(t)}</td><td>{html.escape(w)}</td><td>{html.escape(o) or ''}</td></tr>" for s, e, t, m, k, w, o, l in c.clock(items))
    total = sum(b[1] for b in items)
    return f'<div class="wrap"><table><thead><tr><th>Time</th><th>Min</th><th>Block</th><th>What happens</th><th>Product</th></tr></thead><tbody>{rows}</tbody><tfoot><tr><td></td><td>{total}</td><td>Total</td><td></td><td></td></tr></tfoot></table></div>'


outcomes = "".join(f"<li>{html.escape(v)}</li>" for v in c.OUTCOMES.values())
page("index.html", "Home", f"""
<h1>Scientific Communication</h1>
<p class="lead">Writing, slide design and presentation skills for people who know their subject and want to communicate it clearly, without overstating their evidence.</p>
<div class="two">
<div class="card"><h3><a href="workshop.html">Three-hour practical workshop</a></h3>For 12 to 24 people. Exercises, feedback, timed rehearsal and a 12-minute break. Exactly 180 minutes.</div>
<div class="card"><h3><a href="talk.html">One-hour talk</a></h3>A realistic subset for any size of audience, with a brief activity and questions. Exactly 60 minutes.</div>
</div>
<h2>Who it is for</h2>
<ul><li>Researchers preparing conference presentations.</li><li>Students preparing thesis defences.</li><li>Professionals in hospitals and other organisations presenting evidence, findings or recommendations.</li></ul>
<p>The course is built for all disciplines, with health and research examples, and it welcomes people presenting in English as an additional language. Feedback looks at clarity and understanding, and never at accent or personality.</p>
<h2>Learning outcomes</h2>
<p>By the end of the workshop, participants should be able to:</p><ul>{outcomes}</ul>
<p>This is an introduction with guided practice. It does not promise mastery of scientific writing or public speaking.</p>
<div class="note">All case data in this course are fictional and labelled as such. CareCall and CoolRoom are teaching inventions, not real study results.</div>
""")
page("workshop.html", "Three-hour workshop", f"""
<h1>Three-hour practical workshop</h1>
<p class="lead">Participants leave with a revised paragraph, a short presentation storyboard, one redesigned slide and a rehearsed explanation.</p>
<p>The deck has {W['total']} slides, including three backups, with speaker notes on every slide.</p>
<h2>Schedule</h2>{schedule(c.WORKSHOP)}
<h2>Download</h2>
<ul><li><a href="downloads/Scientific_Communication_Workshop_3h.pdf">Workshop slides (PDF)</a></li><li><a href="downloads/Scientific_Communication_Workshop_3h.pptx">Workshop slides (editable PowerPoint)</a></li><li><a href="downloads/Participant_Workbook.pdf">Participant workbook (PDF)</a></li></ul>
""")
page("talk.html", "One-hour talk", f"""
<h1>One-hour talk</h1>
<p class="lead">Clear Claims, Clear Slides, Clear Delivery. A standalone talk that selects the ideas with the highest value for one hour.</p>
<p>The deck has {T['total']} slides with speaker notes. It leaves out paragraph editing, storyboarding, slide redesign and rehearsal, which need the workshop.</p>
<h2>Schedule</h2>{schedule(c.TALK)}
<h2>Download</h2>
<ul><li><a href="downloads/Scientific_Communication_Talk_1h.pdf">Talk slides (PDF)</a></li><li><a href="downloads/Scientific_Communication_Talk_1h.pptx">Talk slides (editable PowerPoint)</a></li></ul>
""")

files = [("workbook/Participant_Workbook", "Participant workbook", True), ("examples/Before_After_Writing_Examples", "Before-and-after writing examples", True), ("examples/Before_After_Slides", "Before-and-after slides", True),
         ("exercises/Slide_Redesign_Exercise", "Slide redesign exercise", True), ("references/References_and_Source_Map", "References and source map", True)]
worksheets = sorted((MAT / "worksheets").glob("*.docx"))
files += [(f"worksheets/{p.stem}", p.stem.replace("_", " "), True) for p in worksheets]
files += [("workshop_3h/Scientific_Communication_Workshop_3h", "Workshop slides", True), ("talk_1h/Scientific_Communication_Talk_1h", "Talk slides", True)]
rows = ""
for rel, label, _ in files:
    links = []
    for ext, nm in ((".pdf", "PDF"), (".docx", "Word"), (".pptx", "PowerPoint")):
        p = MAT / (rel + ext)
        if p.exists():
            shutil.copy(p, DL / p.name)
            links.append(f'<a href="downloads/{p.name}">{nm}</a>')
    rows += f"<tr><td>{html.escape(label)}</td><td>{' &nbsp; '.join(links)}</td></tr>"
page("materials.html", "Materials", f"""
<h1>Materials</h1>
<p class="lead">Every file is available in an editable format and as a PDF made from that file.</p>
<div class="wrap"><table><thead><tr><th>Material</th><th>Download</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="note">The facilitator guide holds the model answers, so it is kept with the course source for trainers and is not published on this site.</div>
""")

kinds = [src.RF, src.RC, src.PG, src.SP, src.TR]
rows = ""
for s in src.SOURCES:
    link = f"https://doi.org/{s[3]}" if s[3] else s[2]
    rows += f"<tr><td>{html.escape(s[1])} <a href=\"{html.escape(link)}\">Link</a></td><td>{s[4]}</td><td>{s[6].replace('F', 'Facilitation')}</td><td>{html.escape(s[7])}</td></tr>"
page("evidence.html", "Evidence", f"""
<h1>Evidence behind the course</h1>
<p class="lead">We separate research findings from professional advice and from our own teaching recommendations. Each source below was opened and read on 4 November 2026.</p>
<h2>Rules of thumb are not findings</h2>
<p>We searched for experiments that set a slides-per-minute rate, a six-by-six word limit, or a minimum font size for projected slides, and found none. Published font advice ranges from 18 to 32 points, and legibility depends on screen size and viewing distance, so the best test is the back row of the actual room. The search was targeted, so this means we found no evidence and does not mean none exists.</p>
<h2>Sources</h2>
<p>M1 to M6 are the course modules: {'; '.join(f'{k} {v.lower()}' for k, v in src.MODULE_NAMES.items() if k != 'F')}.</p>
<div class="wrap"><table><thead><tr><th>Source</th><th>Type</th><th>Modules</th><th>What it supports</th></tr></thead><tbody>{rows}</tbody></table></div>
""")
print("site built:", len(list(DOCS.glob('*.html'))), "pages,", len(list(DL.iterdir())), "downloads")
