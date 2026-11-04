"""Small slide-building kit on top of the Neudata PowerPoint template.

Everything is drawn as native PowerPoint objects (placeholders, shapes, tables and
charts) so the decks stay editable. Coordinates are points on the 960 x 540 slide.
"""
import copy
import re
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

TEMPLATE = Path(__file__).parent / "assets" / "Neudata-Template-example.pptx"

TEAL = "0D7377"      # PowerPoint template teal, used for titles
DEEP = "055F56"      # logo teal
NAVY = "04242F"
BLUE = "0B376C"
MIST = "EAF2F5"
GREY = "5B6B74"      # darker than the brand grey so small text passes AA on white
MID = "8A99A3"
LINE = "C9D5DA"
INK = "1A1A1A"
WHITE = "FFFFFF"
AMBER = "9A5B00"     # warning accent for "before" examples, AA on white
AMBER_BG = "FBF1E0"
OK_ORANGE = "D55E00" # Okabe-Ito vermillion
OK_BLUE = "0072B2"   # Okabe-Ito blue

LEFT, RIGHT, TOP, BOTTOM = 34, 926, 96, 482
WIDTH = RIGHT - LEFT


def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self):
        self.p = Presentation(str(TEMPLATE))
        ids = self.p.slides._sldIdLst
        for sld in list(ids):
            self.p.part.drop_rel(sld.rId)
            ids.remove(sld)
        self.layouts = {l.name: l for l in self.p.slide_layouts}

    def _add(self, layout):
        return self.p.slides.add_slide(self.layouts[layout])

    def title_slide(self, title, subtitle, date_text, notes):
        s = self._add("Title Slide")
        s.shapes.title.text = title
        for r in s.shapes.title.text_frame.paragraphs[0].runs:
            r.font.size = Pt(36)
        s.placeholders[1].text = subtitle
        for ph in s.placeholders:
            if ph.placeholder_format.type == 16:  # date
                ph.text = date_text
        set_notes(s, notes)
        return s

    def section(self, title, sub, notes):
        s = self._add("Section Header")
        s.shapes.title.text = title
        for r in s.shapes.title.text_frame.paragraphs[0].runs:
            r.font.size = Pt(32)
        for ph in s.placeholders:
            if ph.placeholder_format.idx not in (0,) and ph.placeholder_format.type == 2:
                ph.text = sub
                for r in ph.text_frame.paragraphs[0].runs:
                    r.font.color.rgb = rgb(GREY)
        set_notes(s, notes)
        return s

    def slide(self, headline, notes, source=None, fictional=False):
        """A content slide. The headline states the slide's message."""
        s = self._add("Title Only")
        t = s.shapes.title
        t.text = headline
        size = 24 if len(headline) <= 66 else 21
        for r in t.text_frame.paragraphs[0].runs:
            r.font.size = Pt(size)
        foot = []
        if fictional:
            foot.append("Fictional teaching data, not a real study.")
        if source:
            foot.append(source)
        if foot:
            text(s, LEFT, 466, WIDTH, 22, " ".join(foot), size=12, color=GREY, anchor="bottom", name="Source note")
        set_notes(s, notes)
        return s

    def closing(self, notes):
        s = self._add("Closing - Copyright")
        set_notes(s, notes)
        # The closing layout has no title placeholder; add an off-slide-free accessible name.
        return s

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        cp = self.p.core_properties
        cp.author = cp.last_modified_by = "Neudata Consulting Ltd"
        cp.title = Path(path).stem.replace("_", " ")
        cp.subject = "Scientific Communication: Writing, Slide Design and Presentation Skills"
        cp.comments = cp.keywords = ""
        self.p.save(str(path))


def set_notes(slide, notes):
    slide.notes_slide.notes_text_frame.text = notes.strip()


def alt(shape, description):
    el = shape._element
    nv = el.xpath(".//p:cNvPr")[0]
    nv.set("descr", description)
    return shape


def _fill_par(par, s, size, color, bold, italic=False):
    """Write text with **bold** spans into a paragraph."""
    parts = re.split(r"(\*\*.+?\*\*)", s)
    for part in parts:
        if not part:
            continue
        r = par.add_run()
        is_b = part.startswith("**") and part.endswith("**")
        r.text = part[2:-2] if is_b else part
        r.font.size = Pt(size)
        r.font.color.rgb = rgb(color)
        r.font.bold = True if (bold or is_b) else False
        if italic:
            r.font.italic = True


def _write(tf, content, size, color, bold, align, spacing, line_spacing, italic=False):
    tf.word_wrap = True
    items = content if isinstance(content, (list, tuple)) else [content]
    for i, item in enumerate(items):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if isinstance(item, dict):
            _fill_par(par, item["t"], item.get("size", size), item.get("color", color), item.get("bold", bold), item.get("italic", italic))
            par.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[item.get("align", align)]
        else:
            _fill_par(par, item, size, color, bold, italic)
            par.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if i:
            par.space_before = Pt(spacing)
        if line_spacing:
            par.line_spacing = line_spacing


def text(s, x, y, w, h, content, size=18, color=INK, bold=False, align="l", anchor="top", spacing=6, line_spacing=None, name=None, italic=False):
    b = s.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    if name:
        b.name = name
    tf = b.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    _write(tf, content, size, color, bold, align, spacing, line_spacing, italic)
    return b


def box(s, x, y, w, h, content=None, fill=MIST, line=None, size=16, color=INK, bold=False, align="l", anchor="middle",
        margin=10, spacing=4, shape="rect", weight=1.0, name=None, line_spacing=None):
    kind = {"rect": MSO_SHAPE.RECTANGLE, "oval": MSO_SHAPE.OVAL, "chevron": MSO_SHAPE.PENTAGON}[shape]
    b = s.shapes.add_shape(kind, Pt(x), Pt(y), Pt(w), Pt(h))
    if name:
        b.name = name
    b.shadow.inherit = False
    if fill:
        b.fill.solid()
        b.fill.fore_color.rgb = rgb(fill)
    else:
        b.fill.background()
    if line:
        b.line.color.rgb = rgb(line)
        b.line.width = Pt(weight)
    else:
        b.line.fill.background()
    tf = b.text_frame
    tf.margin_left = tf.margin_right = Pt(margin)
    tf.margin_top = tf.margin_bottom = Pt(min(margin, 6))
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    if content is not None:
        _write(tf, content, size, color, bold, align, spacing, line_spacing)
    return b


def rule(s, x1, y1, x2, y2, color=LINE, weight=1.0, arrow=False, dash=False, name=None):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(weight)
    st = c._element.find(qn("p:style"))
    if st is not None:
        c._element.remove(st)  # the theme's connector style adds a shadow
    ln = c.line._get_or_add_ln()
    if dash:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", "dash")
    if arrow:
        t = etree.SubElement(ln, qn("a:tailEnd"))
        t.set("type", "triangle")
    if name:
        c.name = name
    return c


def table(s, x, y, w, rows, widths, row_h=30, size=15, header=True, name="Table", bold_first=False, fills=None):
    nrows, ncols = len(rows), len(rows[0])
    gf = s.shapes.add_table(nrows, ncols, Pt(x), Pt(y), Pt(w), Pt(row_h * nrows))
    gf.name = name
    t = gf.table
    tblPr = t._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "1" if header else "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is not None:
        sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # No style, no grid
    total = sum(widths)
    for i, wd in enumerate(widths):
        t.columns[i].width = Pt(w * wd / total)
    for r, row in enumerate(rows):
        t.rows[r].height = Pt(min(row_h, 36) if header and r == 0 else row_h)
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.margin_left = cell.margin_right = Pt(8)
            cell.margin_top = cell.margin_bottom = Pt(3)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            is_head = header and r == 0
            colr = WHITE if is_head else INK
            _write(tf, val, size, colr, is_head or (bold_first and c == 0), "l", 2, None)
            cell.fill.solid()
            f = NAVY if is_head else (fills[r][c] if fills and fills[r] and fills[r][c] else WHITE)
            cell.fill.fore_color.rgb = rgb(f)
            if not is_head:
                _cell_bottom(cell)
    return gf


def _cell_bottom(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    ln = etree.SubElement(tcPr, qn("a:lnB"), w="9525", cap="flat", cmpd="sng", algn="ctr")
    sf = etree.SubElement(ln, qn("a:solidFill"))
    c = etree.SubElement(sf, qn("a:srgbClr"))
    c.set("val", LINE)
    # schema order: borders must precede the fill
    fill = tcPr.find(qn("a:solidFill"))
    if fill is not None:
        tcPr.remove(ln)
        fill.addprevious(ln)


def bar_chart(s, x, y, w, h, cats, series, colors=None, ymin=0, ymax=None, major=None, number_format="0.0", labels=True,
              horizontal=False, legend=False, gap=60, font=14, axis_title=None, point_colors=None, three_d=False, gridlines=False,
              name="Chart", value_axis_visible=True):
    data = CategoryChartData()
    data.categories = cats
    for nm, vals in series:
        data.add_series(nm, vals)
    kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = s.shapes.add_chart(kind, Pt(x), Pt(y), Pt(w), Pt(h), data)
    gf.name = name
    ch = gf.chart
    ch.font.size = Pt(font)
    ch.font.color.rgb = rgb(INK)
    ch.has_title = False
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
    va = ch.value_axis
    va.minimum_scale = ymin
    if ymax is not None:
        va.maximum_scale = ymax
    if major:
        va.major_unit = major
    va.has_major_gridlines = gridlines
    if gridlines:
        va.major_gridlines.format.line.color.rgb = rgb(LINE)
    va.format.line.color.rgb = rgb(MID)
    va.tick_labels.font.size = Pt(font - 1)
    va.tick_labels.number_format = "0" if not number_format else number_format
    va.tick_labels.number_format_is_linked = False
    va.visible = value_axis_visible
    if axis_title:
        va.has_title = True
        va.axis_title.text_frame.text = axis_title
        va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(font - 1)
        va.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    ca = ch.category_axis
    ca.format.line.color.rgb = rgb(MID)
    ca.has_major_gridlines = False
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.tick_labels.font.size = Pt(font)
    pl = ch.plots[0]
    pl.gap_width = gap
    pl.overlap = 0
    if labels:
        pl.has_data_labels = True
        dl = pl.data_labels
        dl.number_format = number_format
        dl.number_format_is_linked = False
        dl.show_value = True
        dl.font.size = Pt(font)
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
    for i, ser in enumerate(pl.series):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb((colors or [DEEP, BLUE, MID])[i])
        ser.invert_if_negative = False
        if point_colors and i == 0:
            for j, col in enumerate(point_colors):
                pt = ser.points[j]
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb = rgb(col)
    if three_d:
        _to_3d(ch)
    return gf


def _to_3d(ch):
    """Turn a clustered column chart into a 3-D one. Used only for the bad-example slide."""
    root = ch._chartSpace
    c_chart = root.find(qn("c:chart"))
    bar = c_chart.find(qn("c:plotArea")).find(qn("c:barChart"))
    bar.tag = qn("c:bar3DChart")
    ov = bar.find(qn("c:overlap"))
    if ov is not None:
        bar.remove(ov)
    view = etree.Element(qn("c:view3D"))
    for tag_, val in (("c:rotX", "15"), ("c:rotY", "20"), ("c:rAngAx", "1")):
        etree.SubElement(view, qn(tag_)).set("val", val)
    atd = c_chart.find(qn("c:autoTitleDeleted"))
    atd.addnext(view)


def line_chart(s, x, y, w, h, cats, series, colors, ymin=0, ymax=None, major=None, font=14, axis_title=None, markers=None,
               legend=False, dashes=None, widths=None, name="Chart", number_format="0", gridlines=True):
    data = CategoryChartData()
    data.categories = cats
    for nm, vals in series:
        data.add_series(nm, vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Pt(x), Pt(y), Pt(w), Pt(h), data)
    gf.name = name
    ch = gf.chart
    ch.font.size = Pt(font)
    ch.font.color.rgb = rgb(INK)
    ch.has_title = False
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
    va = ch.value_axis
    va.minimum_scale = ymin
    if ymax is not None:
        va.maximum_scale = ymax
    if major:
        va.major_unit = major
    va.has_major_gridlines = gridlines
    if gridlines:
        va.major_gridlines.format.line.color.rgb = rgb(LINE)
    va.format.line.color.rgb = rgb(MID)
    va.tick_labels.number_format = number_format
    va.tick_labels.number_format_is_linked = False
    if axis_title:
        va.has_title = True
        va.axis_title.text_frame.text = axis_title
        va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(font - 1)
        va.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    ca = ch.category_axis
    ca.format.line.color.rgb = rgb(MID)
    ca.major_tick_mark = XL_TICK_MARK.NONE
    from pptx.enum.chart import XL_MARKER_STYLE
    mk = markers or ["circle"] * len(series)
    style = {"circle": XL_MARKER_STYLE.CIRCLE, "square": XL_MARKER_STYLE.SQUARE, "diamond": XL_MARKER_STYLE.DIAMOND, "triangle": XL_MARKER_STYLE.TRIANGLE}
    for i, ser in enumerate(ch.plots[0].series):
        ser.smooth = False
        ser.format.line.color.rgb = rgb(colors[i])
        ser.format.line.width = Pt(widths[i] if widths else 2.5)
        ser.marker.style = style[mk[i]]
        ser.marker.size = 9
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = rgb(colors[i])
        ser.marker.format.line.color.rgb = rgb(colors[i])
    return gf


def ci_plot(s, x, y, w, rows, xmin, xmax, ticks, axis_label, label_w=250, row_h=44, ref=0.0, size=15, value_w=190, color=DEEP):
    """Point-and-interval plot in native shapes. rows: (label, point, lo, hi, value_text)."""
    px0 = x + label_w
    px1 = x + w - value_w
    sx = lambda v: px0 + (v - xmin) / (xmax - xmin) * (px1 - px0)
    top = y
    bottom = y + row_h * len(rows)
    rule(s, sx(ref), top - 4, sx(ref), bottom + 2, color=GREY, weight=1.25, dash=True, name="No difference line")
    for i, (label, pt, lo, hi, val) in enumerate(rows):
        cy = y + row_h * i + row_h / 2
        text(s, x, cy - row_h / 2, label_w - 12, row_h, label, size=size, anchor="middle", align="l")
        rule(s, sx(lo), cy, sx(hi), cy, color=color, weight=3, name=f"Interval {i + 1}")
        d = box(s, sx(pt) - 7, cy - 7, 14, 14, fill=color, shape="oval", name=f"Estimate {i + 1}")
        text(s, px1 + 12, cy - row_h / 2, value_w - 12, row_h, val, size=size - 1, anchor="middle")
    rule(s, px0, bottom + 4, px1, bottom + 4, color=MID, weight=1)
    for t in ticks:
        rule(s, sx(t), bottom + 4, sx(t), bottom + 9, color=MID, weight=1)
        lab = f"{t:g}".replace("-", "−")
        text(s, sx(t) - 30, bottom + 11, 60, 18, lab, size=13, align="c", color=GREY)
    text(s, px0 - 40, bottom + 30, px1 - px0 + 80, 20, axis_label, size=13, align="c", color=GREY)
    return bottom + 50


def label(s, x, y, w, content, kind="before"):
    """Small heading for before and after panels."""
    col = {"before": AMBER, "after": DEEP}[kind]
    txt = {"before": "BEFORE", "after": "AFTER"}[kind] if content is None else content
    return text(s, x, y, w, 20, txt, size=14, color=col, bold=True)


def activity_bar(s, minutes, what):
    """Consistent strip marking participant work."""
    box(s, LEFT, 96, WIDTH, 34, f"**Activity, {minutes} minutes.** {what}", fill=DEEP, color=WHITE, size=16, margin=12, name="Activity strip")
