"""Checks schedules, alignment, editability, PDF match and writing standards.

    python scripts/check_materials.py
"""
import re
import sys
from pathlib import Path

import fitz
from docx import Document
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))
import course as c  # noqa: E402

problems = []


def fail(msg):
    problems.append(msg)
    print("BAD", msg)


# --------------------------------------------------- Schedules
wt, tt = sum(b[1] for b in c.WORKSHOP), sum(b[1] for b in c.TALK)
print("workshop schedule total", wt, "| talk schedule total", tt)
assert wt == 180 and tt == 60


def notes_minutes(path):
    p = Presentation(path)
    total = 0.0
    for s in p.slides:
        n = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        m = re.match(r"Timing: ([\d.]+) min", n)
        if m:
            total += float(m.group(1))
    return total


w_pptx = ROOT / "materials/workshop_3h/Scientific_Communication_Workshop_3h.pptx"
t_pptx = ROOT / "materials/talk_1h/Scientific_Communication_Talk_1h.pptx"
print("minutes in workshop speaker notes", notes_minutes(w_pptx), "| talk", notes_minutes(t_pptx))
assert notes_minutes(w_pptx) == 180 and notes_minutes(t_pptx) == 60
break_min = [b[1] for b in c.WORKSHOP if b[2] == "break"]
assert break_min == [12]

# --------------------------------------------------- Outcomes, activities, assessment
required = {"Audience-and-message worksheet": "LO1", "Revised paragraph": "LO3", "Short presentation storyboard": "LO2", "One redesigned slide": "LO4", "Rehearsed explanation, peer feedback": "LO5"}
outs = {b[4]: b[5] for b in c.WORKSHOP}
for prod, lo in required.items():
    assert prod in outs and lo in outs[prod], prod
for lo in c.OUTCOMES:
    assert any(lo in b[5] for b in c.WORKSHOP), lo
    assert any(a[0] == lo for a in c.ALIGNMENT), lo
criteria = {r[0] for r in c.RUBRIC}
assert criteria == {"Message", "Structure", "Writing", "Evidence", "Visual clarity", "Timing", "Responses to questions"}
for a in c.ALIGNMENT:
    for crit in a[3].split(", "):
        assert crit == "All criteria" or crit in criteria, crit
print("outcomes aligned with activities, products and rubric criteria")

# --------------------------------------------------- Decks
for path in sorted((ROOT / "materials").rglob("*.pptx")):
    p = Presentation(path)
    pdf = path.with_suffix(".pdf")
    n = len(p.slides._sldIdLst)
    pages = len(fitz.open(pdf))
    if n != pages:
        fail(f"{path.name}: {n} slides, {pages} PDF pages")
    if pdf.stat().st_mtime < path.stat().st_mtime - 5:
        fail(f"{path.name}: PDF older than PPTX")
    charts = tables = pics = titles = no_notes = 0
    seen = {}
    for i, s in enumerate(p.slides, 1):
        for sh in s.shapes:
            charts += sh.has_chart if hasattr(sh, "has_chart") else 0
            tables += sh.has_table if hasattr(sh, "has_table") else 0
            pics += sh.shape_type == MSO_SHAPE_TYPE.PICTURE
        t = s.shapes.title.text if s.shapes.title is not None else ""
        titles += bool(t)
        if t:
            seen.setdefault(t, []).append(i)
        if not (s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip()):
            no_notes += 1
    if no_notes:
        fail(f"{path.name}: {no_notes} slides without notes")
    if pics:
        fail(f"{path.name}: {pics} pictures on slides, expected native objects only")
    print(f"{path.name}: {n} slides = {pages} PDF pages, {charts} native charts, {tables} native tables, 0 slide pictures, all notes present")
    if "Workshop" in path.name or "Talk" in path.name:
        words = [len(s.notes_slide.notes_text_frame.text.split()) for s in p.slides]
        print(f"  speaker notes: {sum(words)} words")

# --------------------------------------------------- Writing standards across all text
texts = {}
for path in (ROOT / "materials").rglob("*.pptx"):
    p = Presentation(path)
    buf = []
    for s in p.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                buf.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    buf += [cell.text for cell in row.cells]
        if s.has_notes_slide:
            buf.append(s.notes_slide.notes_text_frame.text)
    texts[path.name] = "\n".join(buf)
for path in (ROOT / "materials").rglob("*.docx"):
    d = Document(path)
    buf = [x.text for x in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            buf += [cell.text for cell in row.cells]
    texts[path.name] = "\n".join(buf)
for path in list((ROOT / "materials").rglob("*.md")) + [ROOT / "README.md"] + list((ROOT / "docs").glob("*.html")):
    if path.exists():
        texts[path.name] = path.read_text(encoding="utf8")

placeholders = [r"\bTODO\b", r"\bTBC\b", r"\bTBD\b", r"\bXXX?\b", r"lorem ipsum", r"\[Author\]", r"DD-MM-YYYY", r"\[insert", r"placeholder"]
stock = [r"\bdelve", r"\bleverage", r"\bseamless", r"\bpivotal\b", r"it is important to note", r"a testament to", r"\bunlock", r"navigate the landscape", r"fast-paced world"]
invented = [r"Dr\.? [A-Z]", r"Prof\.? [A-Z]", r"certified", r"accredited"]
for name, tx in texts.items():
    if "—" in tx:
        fail(f"{name}: em dash")
    for pat in placeholders + stock + invented:
        if re.search(pat, tx, re.I if pat in stock else 0):
            fail(f"{name}: matched {pat}")
    if re.search(r"\bClaude\b", tx):
        fail(f"{name}: mentions Claude")
print(f"writing standards checked across {len(texts)} files")

if problems:
    print(f"\n{len(problems)} problem(s)")
    sys.exit(1)
print("\nAll material checks passed.")
