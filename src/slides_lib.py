"""Slides shared by the workshop deck, the talk deck and the examples file.

Each function draws one slide and takes its speaker notes, so the same picture can be
explained differently in each version. Numbers come from casebook only.
"""
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.util import Pt

import casebook as cb
import examples as ex
from casebook import facts
from deck_kit import *

F = facts()


class D(Deck):
    """Deck that records planned minutes per schedule block."""

    def __init__(self):
        super().__init__()
        self.block = None
        self.minutes = {}

    def set_block(self, name):
        self.block = name
        self.minutes.setdefault(name, 0)
        self.first_slide = getattr(self, "first_slide", {})
        self.first_slide[name] = len(self.p.slides._sldIdLst) + 1

    def s(self, headline, mins, notes, source=None, fictional=False):
        return self.slide(headline, timed(mins, notes), source, fictional) if self._tick(mins) else None

    def _tick(self, mins):
        self.minutes[self.block] = self.minutes.get(self.block, 0) + mins
        return True

    def sec(self, title, sub, mins, notes):
        self._tick(mins)
        return self.section(title, sub, timed(mins, notes))


def timed(mins, notes):
    return f"Timing: {mins:g} min.\n{notes.strip()}"


def N(say, ask=None, watch=None, basis=None, do=None):
    """Structured speaker notes."""
    parts = [f"Say: {say}"]
    if do:
        parts.append(f"Do: {do}")
    if ask:
        parts.append(f"Ask: {ask}")
    if watch:
        parts.append(f"Watch for: {watch}")
    if basis:
        parts.append(f"Basis: {basis}")
    return "\n".join(parts)


def tag(s, kind):
    txt, col = {"before": ("BEFORE", AMBER), "after": ("AFTER", DEEP)}[kind]
    box(s, 846, 10, 80, 22, txt, fill=col, color=WHITE, size=12, bold=True, align="c", margin=2, name=f"{txt} marker")
    t = s.shapes.title
    t.left, t.top, t.width, t.height = Pt(30), Pt(18), Pt(806), Pt(58)


def contrast(a, b):
    def lum(h):
        vals = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        vals = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in vals]
        return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# ------------------------------------------------------------ Audience
def s_audience_chain(d, mins, notes):
    s = d.s("Every talk starts with people who must do something afterwards", mins, notes,
            source="Teaching recommendation, drawing on Bourne 2007 and the CDC Clear Communication Index (professional guidance).")
    steps = [("Who is in the room?", "Roles, field, seniority, language"),
             ("What do they already know?", "Assume less method, more context"),
             ("What do they need?", "To trust it, to judge it, to decide"),
             ("What should change?", "Understand, decide or act"),
             ("What is your one sentence?", "The claim you want them to repeat")]
    w, gap = 164, 18
    for i, (a, b) in enumerate(steps):
        x = LEFT + i * (w + gap)
        fill = DEEP if i == 4 else MIST
        box(s, x, 150, w, 118, a, fill=fill, color=WHITE if i == 4 else NAVY, size=17, bold=True, align="c", margin=8)
        text(s, x + 2, 280, w - 4, 62, b, size=15, color=GREY, align="c")
        if i < 4:
            rule(s, x + w + 1, 209, x + w + gap - 1, 209, color=TEAL, weight=2, arrow=True)
    text(s, LEFT, 372, WIDTH, 60, "Work left to right. If you cannot fill a box, you are not ready to make slides.", size=20, color=NAVY, align="c")
    return s


def s_topic_message(d, mins, notes):
    s = d.s("A topic names an area; a message makes a claim someone could challenge", mins, notes,
            source="neu-data teaching recommendation.", fictional=True)
    text(s, LEFT, 104, 420, 22, "TOPIC", size=14, color=AMBER, bold=True)
    box(s, LEFT, 130, 420, 150, "Telephone follow-up after hospital discharge", fill=AMBER_BG, size=24, color=INK, margin=18)
    text(s, 506, 104, 420, 22, "MESSAGE", size=14, color=DEEP, bold=True)
    box(s, 506, 130, 420, 150, "A nurse call is linked to fewer readmissions, but the evidence does not yet justify full roll-out", fill=MIST, size=22, color=NAVY, bold=True, margin=18)
    text(s, LEFT, 306, WIDTH, 26, "Three checks for your sentence", size=18, color=NAVY, bold=True)
    for i, (h, b) in enumerate((("Is it a full sentence?", "It has a verb and says something happened."),
                                ("Could someone disagree?", "If nobody could, it is still a topic."),
                                ("Could you say it in a corridor?", "It should work without slides."))):
        x = LEFT + i * 304
        text(s, x, 338, 284, 110, [{"t": h, "bold": True, "color": TEAL, "size": 17}, b], size=16)
    return s


def s_three_rooms(d, mins, notes):
    s = d.s("One finding needs a different message in each room", mins, notes, fictional=True,
            source="neu-data teaching examples.")
    rows = [["Room", "Who they are", "What they should do", "Your message"]]
    for r in ex.ROOMS:
        rows.append([r[0], r[1], r[2], r[3]])
    table(s, LEFT, 100, WIDTH, rows, [15, 21, 19, 45], row_h=98, size=15, bold_first=True, name="Three rooms table")
    return s


# ------------------------------------------------------------ Claims
def s_denominators(d, mins, notes):
    s = d.s("A count without a denominator can reverse the picture", mins, notes, fictional=True,
            source="Reporting guidance: SAMPL (Lang & Altman 2015).")
    ha, hb = cb.HOSPITALS["Hospital A"], cb.HOSPITALS["Hospital B"]
    text(s, LEFT, 100, 430, 24, "Counted: Hospital A looks worse", size=18, bold=True, color=NAVY)
    alt(bar_chart(s, LEFT, 128, 430, 290, ["Hospital A", "Hospital B"], [("Readmissions", [ha.events, hb.events])], ymax=120, number_format="0", colors=[MID],
                  value_axis_visible=False, gap=80, name="Readmission counts"),
        f"Bar chart of readmission counts: Hospital A {ha.events}, Hospital B {hb.events}.")
    text(s, 496, 100, 430, 24, "As a rate: Hospital B is higher", size=18, bold=True, color=NAVY)
    alt(bar_chart(s, 496, 128, 430, 290, [f"A: {ha.events} of {ha.n}", f"B: {hb.events} of {hb.n}"], [("Readmitted per 100", [round(100 * ha.risk, 1), round(100 * hb.risk, 1)])], ymax=25, colors=[DEEP],
                  value_axis_visible=False, gap=80, name="Readmission rates"),
        f"Bar chart of readmission rates: Hospital A {F['hosp_a_pct']} per 100, Hospital B {F['hosp_b_pct']} per 100.")
    text(s, LEFT, 426, WIDTH, 30, "Give numerator and denominator every time: 95 of 540, not just 95 and not just 17.6%.", size=18, color=INK)
    return s


def plot_rows_main():
    return [
        ("All patients, crude", 100 * cb.RD_CRUDE, 100 * cb.RD_CRUDE_LO, 100 * cb.RD_CRUDE_HI, f"{F['rd']} fewer ({F['rd_hi']} to {F['rd_lo']} fewer)"),
        ("Within risk groups", 100 * cb.RD_ADJ, 100 * cb.RD_ADJ_LO, 100 * cb.RD_ADJ_HI, f"{F['adj']} fewer ({F['adj_lo']} fewer to {F['adj_hi']} more)"),
    ]


def s_size_uncertainty(d, mins, notes):
    s = d.s("Report the size of the difference and how uncertain it is", mins, notes, fictional=True,
            source="Professional guidance: SAMPL, STROBE. Research finding: Akl et al. 2011 (Cochrane), van der Bles et al. 2020.")
    box(s, LEFT, 100, 280, 100, [{"t": f"{F['rrr']}%", "size": 34, "bold": True, "color": AMBER}, "relative reduction alone: sounds large, hides the base"], fill=AMBER_BG, size=14, margin=12, align="c")
    box(s, 330, 100, 280, 100, [{"t": f"{F['rd']} per 100", "size": 34, "bold": True, "color": DEEP}, f"absolute difference: {F['usual_pct']}% v {F['call_pct']}%"], fill=MIST, size=14, margin=12, align="c")
    box(s, 626, 100, 300, 100, [{"t": f"{F['rd_hi']} to {F['rd_lo']}", "size": 34, "bold": True, "color": DEEP}, "95% confidence interval: the range the data fit"], fill=MIST, size=14, margin=12, align="c")
    y = 224
    text(s, LEFT, y - 8, 240, 20, "Difference in readmissions", size=14, color=GREY, bold=True)
    ci_plot(s, LEFT, y + 16, WIDTH, plot_rows_main(), -14, 4, [-12, -8, -4, 0, 4], "Readmissions per 100 patients, call minus no call. Left of zero: fewer with a call.",
            label_w=180, value_w=300, row_h=52)
    return s


def s_verbs(d, mins, notes):
    s = d.s("Choose the verb your design can support", mins, notes,
            source="Research findings: Haber 2018, 2022. Guidance: STROBE, GRADE 26 (for reviews). Wording ladder: neu-data teaching recommendation.")
    rows = [["What you have", "Verbs that fit", "Too strong for it"],
            ["Observational comparison, as in CareCall", "was associated with, was higher among", "led to, reduced, prevented"],
            ["Comparison with adjustment", "remained lower after stratifying by risk", "the effect of, independently caused"],
            ["Well-conducted randomised comparison", "reduced, in this population", "proves, works everywhere"],
            ["Any single study, in the conclusion", "may, suggests, is consistent with", "shows conclusively, will improve"]]
    table(s, LEFT, 102, WIDTH, rows, [38, 33, 29], row_h=56, size=16, bold_first=True, name="Verb ladder")
    box(s, LEFT, 384, WIDTH, 68, "**The word \"association\" is not a shield.** Many readers still hear a causal claim, so state the design and the main alternative explanation as well.", fill=MIST, size=17, margin=14)
    return s


def s_non_significant(d, mins, notes):
    s = d.s("A non-significant result is rarely proof of no effect", mins, notes, fictional=True,
            source="Review: Altman & Bland 1995, Greenland et al. 2016, ASA statement 2016.")
    text(s, LEFT, 100, 430, 24, "CareCall: emergency visits", size=18, bold=True, color=NAVY)
    ci_plot(s, LEFT, 138, 430, [("", 100 * cb.RD_ED, 100 * cb.RD_ED_LO, 100 * cb.RD_ED_HI, "")], -8, 8, [-8, -4, 0, 4, 8], "Visits per 100 patients, call minus no call",
            label_w=10, value_w=10, row_h=56, size=14)
    text(s, LEFT, 256, 420, 60, f"{F['ed_rd']} fewer per 100, but anything from {F['ed_lo']} fewer to {F['ed_hi']} more fits the data.", size=16)
    text(s, 496, 100, 430, 24, "CoolRoom: classroom temperature", size=18, bold=True, color=NAVY)
    ci_plot(s, 496, 138, 430, [("", cb.ROOF_DIFF, cb.ROOF_LO, cb.ROOF_HI, "")], -3, 1, [-3, -2, -1, 0, 1], "Degrees Celsius, coated minus standard",
            label_w=10, value_w=10, row_h=56, size=14, color=BLUE)
    text(s, 496, 256, 420, 60, f"{F['roof_diff']} °C cooler, with {F['roof_lo']} °C cooler to {F['roof_hi']} °C warmer fitting the data.", size=16)
    box(s, LEFT, 334, WIDTH, 116, [{"t": "Do not write: \"The calls had no effect.\"", "color": AMBER, "bold": True},
                                   {"t": "Write: \"The study cannot tell us whether calls change emergency visits. The interval includes a useful benefit and a small harm.\"", "color": NAVY, "bold": True}],
        fill=MIST, size=18, margin=16, spacing=8)
    return s


def s_four_forms(d, mins, notes):
    s = d.s("One finding takes four forms, and the strength of the claim stays the same", mins, notes, fictional=True,
            source="Worked examples: neu-data. Abstract structure: MIT Communication Lab; STROBE.")
    cols = [("Paragraph", f"{len(ex.PARA_AFTER.split())} words", "Full reasoning for a reader who can reread."),
            ("Abstract passage", f"{len(ex.ABSTRACT_PASSAGE.split())} words", "Result, adjusted result and a cautious conclusion."),
            ("Slide headline", f"{len(ex.HEADLINE.split())} words", ex.HEADLINE),
            ("Spoken explanation", f"{len(ex.SPOKEN.split())} words", "\"For every hundred patients, those who got a call had about seven fewer readmissions...\"")]
    w, gap = 208, 20
    for i, (h, n, b) in enumerate(cols):
        x = LEFT + i * (w + gap)
        box(s, x, 104, w, 44, h, fill=NAVY, color=WHITE, size=16, bold=True, align="c", margin=4)
        box(s, x, 148, w, 34, n, fill=MIST, color=NAVY, size=15, align="c", margin=4)
        text(s, x + 6, 192, w - 12, 170, b, size=16)
        if i < 3:
            rule(s, x + w + 1, 126, x + w + gap - 1, 126, color=TEAL, weight=2, arrow=True)
    box(s, LEFT, 372, WIDTH, 78, "**Keep in every version:** the size of the difference, who was studied, that calls were not randomised, and that the result is uncertain. Words can go. These cannot.", fill=MIST, size=17, margin=14)
    return s


# ------------------------------------------------------------ Slides
def s_assertion_evidence(d, mins, notes):
    s = d.s("A slide headline states the claim; the body shows the evidence", mins, notes,
            source="Research finding: Garner & Alley 2013 (a bundle of changes, recorded talk, students). Critique: Farkas 2010. Method: Alley, Penn State.")
    # anatomy panel
    box(s, LEFT, 104, 470, 346, fill=WHITE, line=LINE, name="Example slide frame")
    text(s, LEFT + 16, 114, 438, 62, "Readmissions were lower among patients who received a call", size=19, bold=True, color=TEAL)
    rule(s, LEFT + 14, 180, LEFT + 456, 180, color=TEAL, weight=1.25)
    alt(bar_chart(s, LEFT + 14, 188, 442, 214, [f"Call ({F['call_ev']} of {F['call_n']})", f"No call ({F['usual_ev']} of {F['usual_n']})"], [("Readmitted per 100", [14.6, 21.5])], ymax=28, colors=[DEEP],
                  value_axis_visible=False, gap=70, font=13, name="Example chart"),
        f"Bar chart: {F['call_pct']} readmitted per 100 with a call, {F['usual_pct']} without.")
    text(s, LEFT + 16, 406, 438, 36, "Not randomised. Fictional data.", size=13, color=GREY)
    items = [("Headline", "A full sentence that makes the claim."),
             ("Evidence", "A chart, diagram, photo or table that supports it."),
             ("Spoken detail", "You explain. Secondary detail goes in your notes."),
             ]
    y = 108
    for h, b in items:
        text(s, 526, y, 400, 66, [{"t": h, "bold": True, "color": TEAL, "size": 18}, b], size=16, spacing=2)
        y += 74
    box(s, 526, 332, 400, 118, [{"t": "What the evidence shows", "bold": True, "color": NAVY},
                                "In one experiment this bundle beat topic headlines with bullets. It has critics, and no study tests each part alone. Treat it as a strong default."], fill=MIST, size=15, margin=12)
    return s


def s_numeric_rules(d, mins, notes):
    s = d.s("Slide-count, word-count and font-size rules are rules of thumb, not findings", mins, notes,
            source="Our search found no experiment setting these numbers. Sources in the notes. Guidance labelled as such.")
    rows = [["Rule you may hear", "What sources actually say", "Use it like this"],
            ["One slide per minute", "Bourne: more than one visual a minute is too many, as his rule of thumb. Naegle: a minute or less. Other tested talks ran faster.", "A planning check. A dense slide needs longer; a build needs less."],
            ["Six words, six lines", "No primary source found. Advice varies. The direction (less text while you speak) has reasoned support.", "Ask what must be read, and cut the rest to your notes."],
            ["Minimum 24 or 30 point", "Published advice ranges from 18 to 32 pt. Legibility depends on screen size and distance.", "Stand at the back of the actual room, or test at reduced size."]]
    table(s, LEFT, 100, WIDTH, rows, [20, 46, 34], row_h=102, size=15, bold_first=True, name="Numeric rules table")
    return s


def s_readable(d, mins, notes):
    s = d.s("Readable means tested: type, spacing, contrast and layout", mins, notes,
            source="Standard: WCAG 2.2 SC 1.4.3 (web; W3C notes apply it to documents). Guidance: W3C Making Events Accessible.")
    pairs = [(WHITE, TEAL, "Heading teal on white"), (WHITE, GREY, "Dark grey on white"), (WHITE, MID, "Brand mid-grey on white"), (NAVY, WHITE, "White on navy"), (MIST, NAVY, "Navy on mist")]
    text(s, LEFT, 100, 430, 24, "Contrast is measurable", size=18, bold=True, color=NAVY)
    y = 132
    for bg, fg, nm in pairs:
        r = contrast(bg, fg)
        box(s, LEFT, y, 300, 44, nm, fill=bg, color=fg, size=15, line=LINE, margin=10)
        ok = "passes" if r >= 4.5 else "large text only" if r >= 3 else "fails"
        text(s, LEFT + 312, y, 130, 44, [f"**{r:.1f}:1**", ok], size=14, anchor="middle", spacing=0)
        y += 54
    text(s, LEFT, 408, 430, 44, "Level AA asks for 4.5:1, or 3:1 for large text. Check in the actual room too.", size=15, color=GREY)
    text(s, 510, 100, 416, 24, "Four habits that cost nothing", size=18, bold=True, color=NAVY)
    items = [("One typeface family.", "Two sizes for text, one for headlines."),
             ("Same place, every slide.", "Headline, evidence, source."),
             ("Space separates ideas.", "Use it before you use boxes."),
             ("Back-of-room test.", "Can a colleague read it from the last row?")]
    y = 134
    for a, b in items:
        text(s, 510, y, 416, 70, [{"t": a, "bold": True, "color": TEAL, "size": 18}, b], size=17, spacing=2)
        y += 78
    return s


def s_chart_choice(d, mins, notes):
    s = d.s("Choose the chart from the question you are asking", mins, notes,
            source="Research finding: Heer & Bostock 2010, Weissgerber 2015. Guidance: Wilke 2019. Table: neu-data teaching recommendation.")
    rows = [["Your question", "Good default", "Be careful"],
            ["How do groups compare?", "Bars from zero, or dots with intervals", "Bars hide spread in small continuous data"],
            ["How does it change over time?", "Line, with real time spacing", "Short windows can flatter a trend"],
            ["How spread out are values?", "Individual points, box plot", "A mean alone hides the shape"],
            ["How do two measures relate?", "Scatter plot", "A pattern is not a cause"],
            ["What share of the whole?", "Ordered bars; stacked bar for few parts", "Readers judge angle and area poorly"]]
    table(s, LEFT, 100, WIDTH, rows, [33, 35, 32], row_h=52, size=16, bold_first=True, name="Chart choice table")
    text(s, LEFT, 408, WIDTH, 50, "In perception experiments, people judged position better than length, and length better than angle or area.", size=17, color=NAVY)
    return s


def s_figure_five(d, mins, notes):
    s = d.s("Every data figure must answer five questions for the audience", mins, notes, fictional=True,
            source="Teaching checklist: neu-data, drawing on SAMPL and Rougier et al. 2014.")
    ci_plot(s, LEFT, 118, 560, [("Call v no call,\ncrude", 100 * cb.RD_CRUDE, 100 * cb.RD_CRUDE_LO, 100 * cb.RD_CRUDE_HI, ""),
                                ("Call v no call,\nwithin risk groups", 100 * cb.RD_ADJ, 100 * cb.RD_ADJ_LO, 100 * cb.RD_ADJ_HI, "")],
            -14, 4, [-12, -8, -4, 0, 4], "Readmissions per 100 patients, call minus no call", label_w=170, value_w=16, row_h=72, size=14)
    text(s, LEFT, 330, 560, 44, f"Adults discharged from medical wards at two hospitals, n = {F['total_n']}. Bars show 95% CI. Source: fictional CareCall data.", size=14, color=GREY)
    items = [("Axes", "What is on each axis?"), ("Units", "Per 100? Degrees? Days?"), ("Denominators", "Out of how many?"), ("Uncertainty", "What do the bars mean?"), ("Source", "Where did the data come from?")]
    y = 104
    for i, (a, b) in enumerate(items, 1):
        box(s, 618, y, 34, 34, str(i), fill=DEEP, color=WHITE, size=16, bold=True, align="c", shape="oval", margin=0)
        text(s, 664, y - 3, 262, 56, [{"t": a, "bold": True, "color": NAVY, "size": 17}, b], size=15, spacing=0)
        y += 69
    return s


def s_mislead(d, mins, notes):
    s = d.s("The same numbers can look dramatic or modest, so choose honestly", mins, notes, fictional=True,
            source="Research findings: Pandey et al. 2015, Correll et al. 2020 (online samples). Guidance: Wilke 2019.")
    text(s, LEFT, 100, 430, 24, "Axis starts at 14: the gap looks huge", size=17, bold=True, color=AMBER)
    alt(bar_chart(s, LEFT, 126, 430, 250, ["Call", "No call"], [("Readmitted per 100", [14.6, 21.5])], ymin=14, ymax=22, major=2, colors=[AMBER], number_format="0.0", gap=70, name="Truncated chart"),
        "Bar chart with a vertical axis from 14 to 22, which exaggerates the gap between 14.6 and 21.5.")
    text(s, 496, 100, 430, 24, "Axis starts at 0: the gap is in proportion", size=17, bold=True, color=DEEP)
    alt(bar_chart(s, 496, 126, 430, 250, ["Call", "No call"], [("Readmitted per 100", [14.6, 21.5])], ymin=0, ymax=25, major=5, colors=[DEEP], number_format="0.0", gap=70, name="Full axis chart"),
        "Bar chart with a vertical axis from 0 to 25 showing 14.6 and 21.5 in true proportion.")
    box(s, LEFT, 386, WIDTH, 66, "**Bars encode length, so bars start at zero.** Dots and lines encode position and may use a narrower range, if the range is labelled and the change is meaningful.", fill=MIST, size=16, margin=14)
    return s


# ------------------------------------------------------------ Before and after pairs
def ba1_before(d, mins, notes):
    s = d.s("Results", mins, notes, fictional=True)
    tag(s, "before")
    lines = [f"Total sample size was {F['total_n']} patients discharged from medical wards at Hospitals A and B during the study period",
             f"{F['call_n']} patients received a nurse telephone call and {F['usual_n']} patients did not receive a nurse telephone call",
             f"In the call group {F['call_ev']} patients ({F['call_pct']}%) had an unplanned readmission within 30 days",
             f"In the no-call group {F['usual_ev']} patients ({F['usual_pct']}%) had an unplanned readmission within 30 days",
             f"The risk difference was {F['rd']} percentage points (95% CI {F['rd_hi']} to {F['rd_lo']})",
             f"Patients at high discharge risk made up {F['hi_share_call']}% of the call group and {F['hi_share_usual']}% of the no-call group",
             f"After stratification by discharge risk the difference was {F['adj']} points ({F['adj_lo']} lower to {F['adj_hi']} higher)",
             "This suggests that the intervention may have had a beneficial impact on readmission outcomes"]
    text(s, LEFT, 100, WIDTH, 356, [f"•  {x}" for x in lines], size=17, spacing=8)
    return s


def ba1_after(d, mins, notes):
    s = d.s("Patients who got a call had fewer readmissions, but the gap narrowed after accounting for risk", mins, notes, fictional=True)
    tag(s, "after")
    alt(bar_chart(s, LEFT, 100, 400, 350, [f"Call ({F['call_ev']} of {F['call_n']})", f"No call ({F['usual_ev']} of {F['usual_n']})"], [("Readmitted within 30 days, per 100", [14.6, 21.5])], ymax=26, colors=[DEEP],
                  value_axis_visible=False, gap=70, font=14, axis_title=None, name="Readmission risk"),
        f"Bar chart: {F['call_pct']} per 100 readmitted with a call, {F['usual_pct']} per 100 without.")
    text(s, 460, 100, 466, 24, "Difference in readmissions per 100 patients", size=16, bold=True, color=NAVY)
    ci_plot(s, 460, 136, 466, [("Crude", *[100 * v for v in (cb.RD_CRUDE, cb.RD_CRUDE_LO, cb.RD_CRUDE_HI)], ""),
                               ("Within risk groups", *[100 * v for v in (cb.RD_ADJ, cb.RD_ADJ_LO, cb.RD_ADJ_HI)], "")],
            -14, 4, [-12, -8, -4, 0, 4], "Call minus no call, with 95% CI", label_w=136, value_w=10, row_h=60, size=14)
    text(s, 460, 306, 466, 140, [f"High-risk patients were harder to reach: {F['hi_share_call']}% of those called, {F['hi_share_usual']}% of those not called.",
                                 "Calls were not randomised."], size=17, spacing=10)
    return s


def ba2_before(d, mins, notes):
    s = d.s("Methods", mins, notes, fictional=True)
    tag(s, "before")
    lines = ["Retrospective observational cohort study", "Two hospitals, medical wards, one calendar year",
             "Inclusion criteria: adults discharged home", f"Exclusion criteria: transfer (n={F['transferred']}), palliative pathway (n={F['palliative']}), no working phone number (n={F['nophone']})",
             "Exposure: nurse telephone call within 72 hours of discharge", "Outcome: unplanned readmission within 30 days",
             "Statistical analysis: risk differences, 95% Wald confidence intervals, Mantel-Haenszel stratification by discharge risk (high or lower)"]
    text(s, LEFT, 100, WIDTH, 350, [f"•  {x}" for x in lines], size=18, spacing=9)
    return s


def flow_diagram(s, y0=104):
    bw = 280
    cx = 290
    box(s, cx - bw / 2, y0, bw, 56, [f"**{F['disch']}** adults discharged from medical wards, two hospitals"], size=15, align="c", fill=MIST, color=NAVY)
    rule(s, cx, y0 + 56, cx, y0 + 112, color=TEAL, weight=2, arrow=True)
    rule(s, cx, y0 + 84, cx + 160, y0 + 84, color=TEAL, weight=1.5)
    box(s, cx + 160, y0 + 60, 228, 62, [f"**{F['excl']}** excluded: {F['transferred']} transferred, {F['palliative']} palliative, {F['nophone']} no phone"], size=14, fill=WHITE, line=LINE, color=INK, anchor="middle", margin=8)
    box(s, cx - bw / 2, y0 + 112, bw, 44, f"**{F['total_n']}** analysed", size=16, align="c", fill=MIST, color=NAVY)
    lx, rx = cx - 130, cx + 130
    rule(s, cx, y0 + 156, cx, y0 + 174, color=TEAL, weight=2)
    rule(s, lx, y0 + 174, rx, y0 + 174, color=TEAL, weight=2)
    rule(s, lx, y0 + 174, lx, y0 + 196, color=TEAL, weight=2, arrow=True)
    rule(s, rx, y0 + 174, rx, y0 + 196, color=TEAL, weight=2, arrow=True)
    box(s, lx - 120, y0 + 196, 240, 58, [f"**{F['call_n']}** with a call within 72 h"], size=16, align="c", fill=DEEP, color=WHITE)
    box(s, rx - 120, y0 + 196, 240, 58, [f"**{F['usual_n']}** with no call"], size=16, align="c", fill=BLUE, color=WHITE)


def ba2_after(d, mins, notes):
    s = d.s(f"We compared {F['total_n']} patients who did or did not get a call within 72 hours", mins, notes, fictional=True)
    tag(s, "after")
    flow_diagram(s)
    box(s, 696, 104, 230, 200, [{"t": "Why it matters", "bold": True, "color": NAVY},
                                "Nurses called when free and when a patient could be reached, so groups may differ."], fill=AMBER_BG, size=15, margin=12)
    text(s, LEFT, 372, WIDTH, 80, ["**Outcome:** unplanned readmission within 30 days.", "**Analysis:** risk difference, overall and within discharge-risk groups."], size=17, spacing=6)
    return s


def ba3_before(d, mins, notes):
    s = d.s("Calls produce a massive drop in readmissions!", mins, notes, fictional=True)
    tag(s, "before")
    alt(bar_chart(s, 120, 96, 720, 360, ["Call", "No call"], [("Readmissions", [14.6, 21.5])], ymin=14, ymax=22, major=2, colors=[AMBER], number_format="0.0", gap=60, three_d=True, labels=False, font=16, name="3-D truncated chart"),
        "Three-dimensional bar chart with a vertical axis from 14 to 22, no units and no denominators.")
    return s


def ba3_after(d, mins, notes):
    s = d.s(f"Readmissions were {F['rd']} per 100 lower with a call, but the data allow a wide range", mins, notes, fictional=True)
    tag(s, "after")
    ci_plot(s, LEFT + 10, 130, 870, [("Crude difference", *[100 * v for v in (cb.RD_CRUDE, cb.RD_CRUDE_LO, cb.RD_CRUDE_HI)], f"{F['rd']} fewer ({F['rd_hi']} to {F['rd_lo']} fewer)"),
                                     ("Within risk groups", *[100 * v for v in (cb.RD_ADJ, cb.RD_ADJ_LO, cb.RD_ADJ_HI)], f"{F['adj']} fewer ({F['adj_lo']} fewer to {F['adj_hi']} more)")],
            -14, 4, [-12, -8, -4, 0, 4], "Readmissions per 100 patients, call minus no call, with 95% CI", label_w=190, value_w=300, row_h=76, size=15)
    text(s, LEFT, 352, WIDTH, 80, [f"Risk of readmission: {F['call_ev']} of {F['call_n']} ({F['call_pct']}%) with a call, {F['usual_ev']} of {F['usual_n']} ({F['usual_pct']}%) without.",
                                   "The dot uses position, so the axis can focus on the range of the differences."], size=17, spacing=8)
    return s


def ba4_before(d, mins, notes):
    s = d.s("Temperature comparison by month", mins, notes, fictional=True)
    tag(s, "before")
    alt(line_chart(s, 110, 100, 740, 350, cb.ROOF_MONTHS, [("Group 1", cb.ROOF_MONTHLY_COATED), ("Group 2", cb.ROOF_MONTHLY_STANDARD)], ["2E8B2E", "D62828"], ymin=26, ymax=33, major=1,
                   legend=True, markers=["circle", "circle"], name="Red and green lines"),
        "Line chart with a red line and a green line, told apart only by a colour legend labelled Group 1 and Group 2.")
    return s


def ba4_after(d, mins, notes):
    s = d.s(f"Coated classrooms averaged {F['roof_diff']} °C cooler, but the interval includes no difference", mins, notes, fictional=True)
    tag(s, "after")
    gf = line_chart(s, 34, 100, 800, 352, cb.ROOF_MONTHS, [("Standard roof", cb.ROOF_MONTHLY_STANDARD), ("Coated roof", cb.ROOF_MONTHLY_COATED)], [OK_ORANGE, OK_BLUE], ymin=27, ymax=32, major=1,
                    axis_title="Mean afternoon temperature (°C)", markers=["square", "circle"], name="Direct labelled lines", number_format="0")
    alt(gf, "Line chart from May to August. The standard roof line sits above the coated roof line by about one degree each month.")
    for ser, name, col in zip(gf.chart.plots[0].series, ("Standard", "Coated"), (OK_ORANGE, OK_BLUE)):
        dl = ser.points[3].data_label
        dl.has_text_frame = True
        dl.text_frame.text = name
        r = dl.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = rgb(col)
        dl.position = XL_LABEL_POSITION.ABOVE
    text(s, 800, 196, 126, 200, [f"{F['roof_n']} rooms in each group.", f"Mean difference {F['roof_diff']} °C (95% CI {F['roof_lo']} cooler to {F['roof_hi']} warmer)."], size=14, color=GREY)
    return s


def ba5_before(d, mins, notes):
    s = d.s("Conclusions", mins, notes, fictional=True)
    tag(s, "before")
    text(s, LEFT, 104, WIDTH, 240, [f"•  {x}" for x in ("Nurse telephone follow-up is a promising intervention", "Further research is needed", "Limitations of this study include its observational design", "The team would like to acknowledge everybody who helped")], size=24, spacing=14)
    text(s, LEFT, 372, WIDTH, 70, "Thank you! Any questions?", size=34, bold=True, color=TEAL, align="c")
    return s


def ba5_after(d, mins, notes):
    s = d.s("Recommendation: test calls on two wards for six months before funding full roll-out", mins, notes, fictional=True)
    tag(s, "after")
    box(s, LEFT, 104, 286, 200, [{"t": "What we know", "bold": True, "color": NAVY, "size": 18},
                                 f"{F['adj']} fewer readmissions per 100 within risk groups.", f"The data fit {F['adj_lo']} fewer to {F['adj_hi']} more."], fill=MIST, size=16, margin=14)
    box(s, 337, 104, 286, 200, [{"t": "What it costs", "bold": True, "color": NAVY, "size": 18},
                                f"About {F['call_hours']} nurse hours for {F['call_n']} calls at {F['mins']} minutes each."], fill=MIST, size=16, margin=14)
    box(s, 640, 104, 286, 200, [{"t": "What we do not know", "bold": True, "color": NAVY, "size": 18},
                                "Whether calls caused the difference, because reachable patients were healthier."], fill=MIST, size=16, margin=14)
    box(s, LEFT, 320, WIDTH, 126, [{"t": "Decision needed today", "bold": True, "size": 18},
                                   "Approve a staggered six-month trial on two wards, so that allocation no longer depends on who can be reached. Decide on full roll-out from its results."], fill=DEEP, color=WHITE, size=18, margin=16, spacing=6)
    return s


def bax_before(d, mins, notes):
    s = d.s("Subgroup analysis", mins, notes, fictional=True)
    tag(s, "before")
    rows = [["Stratum", "Call events", "Call n", "Call %", "No-call events", "No-call n", "No-call %", "p"],
            ["High", F["hi_call_ev"], F["hi_call_n"], F["hi_call_pct"], F["hi_usual_ev"], F["hi_usual_n"], F["hi_usual_pct"], "NS"],
            ["Lower", F["lo_call_ev"], F["lo_call_n"], F["lo_call_pct"], F["lo_usual_ev"], F["lo_usual_n"], F["lo_usual_pct"], "NS"]]
    fills = [None, [None, "D9F2D9", None, "D9F2D9", "F7D4D4", None, "F7D4D4", None], [None, "D9F2D9", None, "D9F2D9", "F7D4D4", None, "F7D4D4", None]]
    table(s, LEFT, 104, WIDTH, rows, [11, 13, 10, 11, 16, 13, 14, 7], row_h=46, size=15, name="Dense subgroup table", fills=fills)
    text(s, LEFT, 258, WIDTH, 190, [f"•  {x}" for x in ("Green = good, red = bad", "No significant difference in either stratum, so calls had no effect in subgroups",
                                                             "However the overall analysis was significant", "See table for further details")], size=20, spacing=8)
    return s


def bax_after(d, mins, notes):
    s = d.s("In both risk groups fewer patients who got a call were readmitted, and the intervals are wide", mins, notes, fictional=True)
    tag(s, "after")
    gf = bar_chart(s, LEFT, 100, 480, 352, ["High risk", "Lower risk"], [("Call", [26.7, 9.6]), ("No call", [29.8, 14.6])], ymax=36, colors=[DEEP, MID], value_axis_visible=False, legend=True, gap=70, font=15, name="Risk by stratum")
    alt(gf, f"Paired bars. High risk: {F['hi_call_pct']} with a call, {F['hi_usual_pct']} without. Lower risk: {F['lo_call_pct']} with a call, {F['lo_usual_pct']} without.")
    text(s, 536, 100, 390, 24, "Difference per 100 (95% CI)", size=16, bold=True, color=NAVY)
    ci_plot(s, 536, 134, 390, [("High", *[100 * v for v in (cb.RD_HIGH, cb.RD_HIGH_LO, cb.RD_HIGH_HI)], ""), ("Lower", *[100 * v for v in (cb.RD_LOW, cb.RD_LOW_LO, cb.RD_LOW_HI)], "")],
            -16, 8, [-16, -8, 0, 8], "Call minus no call", label_w=74, value_w=10, row_h=52, size=15)
    text(s, 536, 292, 390, 160, [f"High risk: {F['hi_call_ev']} of {F['hi_call_n']} v {F['hi_usual_ev']} of {F['hi_usual_n']}.", f"Lower risk: {F['lo_call_ev']} of {F['lo_call_n']} v {F['lo_usual_ev']} of {F['lo_usual_n']}.",
                                 "Too few patients to separate these groups."], size=16, spacing=6)
    return s


BA_PAIRS = [
    ("Results slide: text wall to claim and chart", ba1_before, ba1_after),
    ("Methods slide: bullets to flow diagram", ba2_before, ba2_after),
    ("Chart: 3-D and truncated to honest interval plot", ba3_before, ba3_after),
    ("Colour: red and green legend to direct labels", ba4_before, ba4_after),
    ("Conclusion: generic close to a recommendation", ba5_before, ba5_after),
    ("Exercise slide: subgroup table to claim and chart", bax_before, bax_after),
]


# ------------------------------------------------------------ Delivery
def s_four_moves(d, mins, notes):
    s = d.s("Explain every figure in four moves", mins, notes, fictional=True,
            source="Teaching recommendation, drawing on W3C Making Events Accessible and the assertion-evidence tutorial.")
    moves = [("1  What it shows", "\"Each dot is the difference in readmissions, per hundred patients.\""),
             ("2  Where to look", "\"Look at the top line, and the dashed line at zero.\""),
             ("3  What you see", f"\"With a call there were about {round(float(F['rd']))} fewer. The interval stays below zero.\""),
             ("4  Why it matters", "\"So there is a signal. The next line shows how much survives comparing like with like.\"")]
    y = 104
    for h, b in moves:
        box(s, LEFT, y, 230, 76, h, fill=NAVY, color=WHITE, size=18, bold=True, margin=12)
        box(s, LEFT + 230, y, WIDTH - 230, 76, b, fill=MIST, size=18, margin=14)
        y += 86
    return s


def s_clarity(d, mins, notes):
    s = d.s("Clear speech is about being understood, not sounding like someone else", mins, notes,
            source="Research finding: Munro & Derwing 1995 (abstract, small study). Review: Derwing & Munro 2009. Guidance: W3C Making Events Accessible.")
    terms = [("Accent", "How your speech differs from what a listener expects. Not a fault, and never scored here."),
             ("Intelligibility", "How much of your message the listener actually recovers."),
             ("Comprehensibility", "How easy your speech is to follow. Pace, pauses and structure all help.")]
    y = 104
    for a, b in terms:
        fill = AMBER_BG if a == "Accent" else MIST
        box(s, LEFT, y, 420, 90, [{"t": a, "bold": True, "color": AMBER if a == "Accent" else DEEP, "size": 18}, b], fill=fill, size=15, margin=12, spacing=2)
        y += 100
    text(s, 490, 104, 436, 26, "Habits that help every listener", size=18, bold=True, color=NAVY)
    habits = ["Pause after each key number.", "Say long numbers slowly and show them.", "Signpost: \"Two results. First...\"", "Stress the word that carries the point.", "Rehearse your technical terms aloud."]
    text(s, 490, 138, 436, 260, habits, size=18, spacing=13)
    return s


def s_rehearse(d, mins, notes):
    s = d.s("Rehearse against the real clock and decide in advance what to cut", mins, notes,
            source="Professional advice: Bourne 2007, Naegle 2021, Penn State. We found no study of rehearsal timing itself.")
    steps = [("Say it aloud", "Full run, standing, with the clicker. Silent reading does not count."),
             ("Time it", "Use the real limit. Note the time at each section."),
             ("Cut", "Remove before you speed up."),
             ("Run for a listener", "Use the feedback prompts. Then revise."),
             ]
    w = 208
    for i, (h, b) in enumerate(steps):
        x = LEFT + i * (w + 20)
        box(s, x, 104, w, 48, h, fill=DEEP, color=WHITE, size=17, bold=True, align="c", margin=4)
        text(s, x + 4, 162, w - 8, 92, b, size=16)
        if i < 3:
            rule(s, x + w + 1, 128, x + w + 19, 128, color=TEAL, weight=2, arrow=True)
    text(s, LEFT, 268, WIDTH, 26, "Mark your slides before you rehearse", size=18, bold=True, color=NAVY)
    table(s, LEFT, 298, WIDTH, [["Must keep", "Should keep", "Can cut"],
                                ["Question, main result, limit, conclusion", "Second result, method detail", "Extra examples, background already known"]],
          [1, 1, 1], row_h=46, size=16, name="Cut list")
    text(s, LEFT, 408, WIDTH, 44, "If you run over on the day, jump to your conclusion. Never skip it.", size=18, color=NAVY)
    return s


def s_questions(d, mins, notes):
    s = d.s("Listen, repeat, answer briefly, then check", mins, notes,
            source="Professional and teaching guidance: Streeter & Miller 2011, Dunphy 2007, NIU, W3C Making Events Accessible.")
    steps = ["Listen to the end", "Repeat or rephrase", "Answer briefly", "Check it landed"]
    w = 208
    for i, h in enumerate(steps):
        x = LEFT + i * (w + 20)
        box(s, x, 102, w, 50, h, fill=NAVY, color=WHITE, size=17, bold=True, align="c", margin=4)
        if i < 3:
            rule(s, x + w + 1, 127, x + w + 19, 127, color=TEAL, weight=2, arrow=True)
    rows = [["Question type", "What to do", "You could say"],
            ["Critical", "Find the valid part and answer that", "\"That is a fair concern. Reachability may explain part of this.\""],
            ["Unclear", "Check what they mean", "\"Do you mean the crude result or the stratified one?\""],
            ["Out of scope", "Say so and offer a route", "\"We did not study cost per patient. I can follow up afterwards.\""],
            ["Unknown", "Say so plainly", "\"I do not know. I will check and reply by email.\""]]
    table(s, LEFT, 170, WIDTH, rows, [17, 31, 52], row_h=62, size=16, bold_first=True, name="Question types")
    return s


def s_ai(d, mins, notes):
    s = d.s("AI can help you edit and rehearse; you verify every fact, reference and claim", mins, notes,
            source="Research findings: Walters & Wilder 2023, Peters & Chin-Yee 2025. Policy: ICMJE 2026, COPE. Check your journal and institution.")
    text(s, LEFT, 100, 280, 24, "Useful for", size=18, bold=True, color=DEEP)
    text(s, LEFT, 130, 280, 210, ["Tightening sentences you wrote", "Finding hard-to-say phrases", "Suggesting likely questions", "Timing a script"], size=17, spacing=10)
    text(s, 340, 100, 290, 24, "Check by hand", size=18, bold=True, color=AMBER)
    text(s, 340, 130, 290, 210, ["Every number against your table", "Every reference: open it", "Every verb: did the claim grow?", "Every summary against the source"], size=17, spacing=10)
    text(s, 650, 100, 276, 24, "Do not", size=18, bold=True, color=NAVY)
    text(s, 650, 130, 276, 210, ["Paste patient or confidential data into tools your organisation has not approved", "List AI as an author", "Skip disclosure when required"], size=17, spacing=10)
    box(s, LEFT, 356, WIDTH, 96, "In one 2025 study, most language models tested widened scientific claims when summarising, and asking for accuracy did not help. A polished sentence can still be an overstated one.", fill=MIST, size=17, margin=14)
    return s
