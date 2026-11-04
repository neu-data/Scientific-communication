"""Word document kit on top of the Neudata document template.

The template supplies the styles, header, footer and page setup. Text uses **bold**
and __italic__ inline markers.
"""
import copy
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

TEMPLATE = Path(__file__).parent / "assets" / "Neudata-Document.docx"
NAVY, TEAL, BLUE, MIST, GREY, LINE = "04242F", "055F56", "0B376C", "EAF2F5", "5B6B74", "C9D5DA"
TEXT_W = 16.6  # cm, A4 less the template margins


def _shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def _borders(cell, color=LINE, size=4, sides=("top", "bottom", "left", "right")):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        if side in sides:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(size))
            el.set(qn("w:color"), color)
        else:
            el.set(qn("w:val"), "nil")
        b.append(el)
    tcPr.append(b)


def runs(par, s, size=None, color=None):
    for part in re.split(r"(\*\*.+?\*\*|__.+?__)", s):
        if not part:
            continue
        if part.startswith("**"):
            r = par.add_run(part[2:-2])
            r.bold = True
        elif part.startswith("__"):
            r = par.add_run(part[2:-2])
            r.italic = True
        else:
            r = par.add_run(part)
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
    return par


class Doc:
    def __init__(self, title, subtitle, version_line, toc=False):
        self.d = Document(str(TEMPLATE))
        body = self.d.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)
        sec = self.d.sections[0]
        hp = sec.header.paragraphs[0]
        for r in hp.runs:
            if r.text.strip() and "Document title" in r.text:
                r.text = r.text.replace("Document title", title)
        self.d.core_properties.title = title
        self.d.core_properties.author = "Neudata Consulting Ltd"
        self.d.core_properties.subject = "Scientific Communication: Writing, Slide Design and Presentation Skills"
        self.d.core_properties.comments = ""
        self.d.add_paragraph(title, style="Title")
        self.d.add_paragraph(subtitle, style="Subtitle")
        self.d.add_paragraph(version_line, style="Neudata Small")
        if toc:
            self.toc()

    def toc(self):
        self.h2_plain("Contents")
        p = self.d.add_paragraph()
        for kind, txt in (("begin", None), (None, r'TOC \o "1-2" \h \z \u'), ("separate", None), ("t", "Update field to build contents."), ("end", None)):
            r = p.add_run()
            if kind in ("begin", "separate", "end"):
                f = OxmlElement("w:fldChar")
                f.set(qn("w:fldCharType"), kind)
                r._r.append(f)
            elif kind == "t":
                r.text = txt
            else:
                it = OxmlElement("w:instrText")
                it.set(qn("xml:space"), "preserve")
                it.text = txt
                r._r.append(it)
        self.page()

    def h2_plain(self, t):
        p = self.d.add_paragraph()
        r = p.add_run(t)
        r.bold = True
        r.font.size = Pt(15)
        r.font.name = "Century Gothic"
        r.font.color.rgb = RGBColor.from_string(NAVY)

    def h1(self, t):
        return self.d.add_paragraph(t, style="Heading 1")

    def h2(self, t):
        return self.d.add_paragraph(t, style="Heading 2")

    def h3(self, t):
        return self.d.add_paragraph(t, style="Heading 3")

    def p(self, t, size=None, keep=False):
        par = runs(self.d.add_paragraph(), t, size)
        if keep:
            par.paragraph_format.keep_with_next = True
        return par

    def key(self, t):
        return runs(self.d.add_paragraph(style="Key Findings"), t)

    def small(self, t):
        return runs(self.d.add_paragraph(style="Neudata Small"), t)

    def ref(self, text, url, tail):
        """A reference entry with a live link."""
        par = self.d.add_paragraph()
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.left_indent = Cm(0.7)
        par.paragraph_format.first_line_indent = Cm(-0.7)
        r = par.add_run(text + " ")
        r.font.size = Pt(9)
        rid = par.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
        h = OxmlElement("w:hyperlink")
        h.set(qn("r:id"), rid)
        nr = OxmlElement("w:r")
        rp = OxmlElement("w:rPr")
        col = OxmlElement("w:color")
        col.set(qn("w:val"), BLUE)
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "18")
        rp.extend([col, sz, u])
        nr.append(rp)
        t = OxmlElement("w:t")
        t.text = url
        nr.append(t)
        h.append(nr)
        par._p.append(h)
        r2 = par.add_run(" " + tail)
        r2.font.size = Pt(9)

    def bullets(self, items):
        for i in items:
            runs(self.d.add_paragraph(style="List Bullet"), i)

    def numbered(self, items):
        """Literal numbers, so each list restarts at 1 and survives editing and copying."""
        for n, i in enumerate(items, 1):
            par = runs(self.d.add_paragraph(), f"{n}.\t{i}")
            par.paragraph_format.left_indent = Cm(0.75)
            par.paragraph_format.first_line_indent = Cm(-0.75)
            par.paragraph_format.tab_stops.add_tab_stop(Cm(0.75))
            par.paragraph_format.space_after = Pt(3)

    def page(self):
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def table(self, rows, widths, header=True, size=9.5, caption=None, zebra=False, min_row=None, repeat=True, fills=None, keep=True):
        if caption:
            c = runs(self.d.add_paragraph(style="Caption"), caption)
            c.paragraph_format.keep_with_next = True
        t = self.d.add_table(rows=len(rows), cols=len(rows[0]))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        total = sum(widths)
        for ci, w in enumerate(widths):
            t.columns[ci].width = Cm(TEXT_W * w / total)
        for ri, row in enumerate(rows):
            tr = t.rows[ri]
            trPr = tr._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit")
            trPr.append(cs)
            if header and ri == 0 and repeat:
                th = OxmlElement("w:tblHeader")
                trPr.append(th)
            if min_row and ri > 0:
                tr.height = Cm(min_row)
            for ci, val in enumerate(row):
                cell = tr.cells[ci]
                cell.width = Cm(TEXT_W * widths[ci] / total)
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(2)
                par.paragraph_format.space_before = Pt(2)
                head = header and ri == 0
                lines = val.split("\n")
                for li, line in enumerate(lines):
                    if li:
                        par = cell.add_paragraph()
                        par.paragraph_format.space_after = Pt(2)
                    runs(par, f"**{line}**" if head and line else line, size, "FFFFFF" if head else None)
                _borders(cell)
                if head:
                    _shade(cell, NAVY)
                elif fills and fills.get((ri, ci)):
                    _shade(cell, fills[(ri, ci)])
                elif zebra and ri % 2 == 0:
                    _shade(cell, MIST)
        sp = self.d.add_paragraph()
        sp.paragraph_format.space_after = Pt(4)
        return t

    def write_lines(self, n, height=0.8):
        """Ruled space for handwriting. A table with bottom rules, so it also types well."""
        t = self.d.add_table(rows=n, cols=1)
        t.autofit = False
        t.columns[0].width = Cm(TEXT_W)
        for r in t.rows:
            r.height = Cm(height)
            c = r.cells[0]
            c.width = Cm(TEXT_W)
            _borders(c, color="9AA9B1", size=4, sides=("bottom",))
        sp = self.d.add_paragraph()
        sp.paragraph_format.space_after = Pt(2)

    def form(self, fields, label_w=5.0, height=1.4, size=9.5):
        """Two-column labelled form with room to write."""
        rows = [[f, ""] for f in fields]
        t = self.table(rows, [label_w, TEXT_W - label_w], header=False, size=size, min_row=None, repeat=False)
        for r in t.rows:
            r.height = Cm(height)
        for r in t.rows:
            _shade(r.cells[0], MIST)
        return t

    def picture(self, path, width_cm):
        self.d.add_picture(str(path), width=Cm(width_cm))

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        order = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"]
        rank = {qn(f"w:{n}"): i for i, n in enumerate(order)}
        for tcPr in self.d.element.body.iter(qn("w:tcPr")):
            kids = sorted(list(tcPr), key=lambda e: rank.get(e.tag, 99))
            seen = {}
            for k in kids:
                tcPr.remove(k)
            for k in kids:
                seen[k.tag] = k  # the last shading or border written wins
            for k in sorted(seen.values(), key=lambda e: rank.get(e.tag, 99)):
                tcPr.append(k)
        self.d.save(str(path))
