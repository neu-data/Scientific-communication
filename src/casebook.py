"""Fictional teaching cases for the neu-data Scientific Communication course.

This file is the single source of truth for every number in the course.
Slides, documents and the website import from here, and scripts/check_numbers.py
recomputes the results independently. Nothing here is a real study result.

Case A, CareCall: fictional hospital follow-up calls (health services).
Case B, CoolRoom: fictional reflective roof pilot in classrooms (engineering, education).
"""
from dataclasses import dataclass
from math import sqrt

Z95 = 1.959964
T22_95 = 2.073873  # two-sided 95% critical value of t with 22 degrees of freedom

FICTION_LABEL = "Fictional teaching data. Not a real study."


@dataclass(frozen=True)
class Group:
    events: int
    n: int

    @property
    def risk(self):
        return self.events / self.n


def risk_difference(a, b):
    """Wald risk difference a minus b, in proportion units, with 95% CI."""
    rd = a.risk - b.risk
    se = sqrt(a.risk * (1 - a.risk) / a.n + b.risk * (1 - b.risk) / b.n)
    return rd, rd - Z95 * se, rd + Z95 * se


def pct(x, dp=1):
    return f"{100 * x:.{dp}f}"


def signed_pp(x, dp=1):
    """Percentage points with a proper minus sign, for tables and labels."""
    v = 100 * x
    return f"−{abs(v):.{dp}f}" if v < 0 else f"{v:.{dp}f}"


# ---------------------------------------------------------------- Case A
FLOW = {
    "discharged": 1037,
    "transferred": 62,
    "palliative": 41,
    "no_phone": 84,
    "analysed": 850,
}
CALL = Group(60, 412)
USUAL = Group(94, 438)
STRATA = {
    "High": (Group(32, 120), Group(59, 198)),
    "Lower": (Group(28, 292), Group(35, 240)),
}
ED_CALL = Group(40, 412)
ED_USUAL = Group(47, 438)
HOSPITALS = {"Hospital A": Group(95, 540), "Hospital B": Group(59, 310)}
MINUTES_PER_CALL = 20


def mantel_haenszel_rd():
    """Mantel-Haenszel risk difference across strata, with Greenland-Robins variance."""
    num = den = var = 0.0
    for a, b in STRATA.values():
        w = a.n * b.n / (a.n + b.n)
        num += w * (a.risk - b.risk)
        den += w
        var += (a.n * b.n) ** 2 / (a.n + b.n) ** 2 * (
            a.risk * (1 - a.risk) / a.n + b.risk * (1 - b.risk) / b.n
        )
    rd = num / den
    se = sqrt(var) / den
    return rd, rd - Z95 * se, rd + Z95 * se


RD_CRUDE, RD_CRUDE_LO, RD_CRUDE_HI = risk_difference(CALL, USUAL)
RD_ADJ, RD_ADJ_LO, RD_ADJ_HI = mantel_haenszel_rd()
RD_ED, RD_ED_LO, RD_ED_HI = risk_difference(ED_CALL, ED_USUAL)
RD_HIGH, RD_HIGH_LO, RD_HIGH_HI = risk_difference(*STRATA["High"])
RD_LOW, RD_LOW_LO, RD_LOW_HI = risk_difference(*STRATA["Lower"])
RR_CRUDE = CALL.risk / USUAL.risk
TOTAL_EVENTS = CALL.events + USUAL.events
TOTAL_N = CALL.n + USUAL.n
HIGH_SHARE_CALL = STRATA["High"][0].n / CALL.n
HIGH_SHARE_USUAL = STRATA["High"][1].n / USUAL.n
CALL_HOURS = CALL.n * MINUTES_PER_CALL / 60

# ---------------------------------------------------------------- Case B
ROOF_N = 12
ROOF_MEAN_COATED = 29.4
ROOF_MEAN_STANDARD = 30.6
ROOF_SD_COATED = 1.5
ROOF_SD_STANDARD = 1.6
ROOF_MONTHS = ["May", "June", "July", "August"]
ROOF_MONTHLY_COATED = [28.5, 29.3, 30.0, 29.8]
ROOF_MONTHLY_STANDARD = [29.8, 30.4, 31.3, 30.9]
assert abs(sum(ROOF_MONTHLY_COATED) / 4 - ROOF_MEAN_COATED) < 1e-9
assert abs(sum(ROOF_MONTHLY_STANDARD) / 4 - ROOF_MEAN_STANDARD) < 1e-9
ROOF_DIFF = ROOF_MEAN_COATED - ROOF_MEAN_STANDARD
ROOF_SE = sqrt(ROOF_SD_COATED ** 2 / ROOF_N + ROOF_SD_STANDARD ** 2 / ROOF_N)
ROOF_LO = ROOF_DIFF - T22_95 * ROOF_SE
ROOF_HI = ROOF_DIFF + T22_95 * ROOF_SE


def facts():
    """Formatted values for text. Keys are used in str.format templates."""
    f = {
        "disch": f"{FLOW['discharged']:,}",
        "excl": str(FLOW["discharged"] - FLOW["analysed"]),
        "transferred": str(FLOW["transferred"]),
        "palliative": str(FLOW["palliative"]),
        "nophone": str(FLOW["no_phone"]),
        "total_n": str(TOTAL_N),
        "total_ev": str(TOTAL_EVENTS),
        "call_n": str(CALL.n),
        "call_ev": str(CALL.events),
        "call_pct": pct(CALL.risk),
        "usual_n": str(USUAL.n),
        "usual_ev": str(USUAL.events),
        "usual_pct": pct(USUAL.risk),
        "rd": f"{abs(100 * RD_CRUDE):.1f}",
        "rd_lo": f"{abs(100 * RD_CRUDE_LO):.1f}",
        "rd_hi": f"{abs(100 * RD_CRUDE_HI):.1f}",
        "rr": f"{RR_CRUDE:.2f}",
        "rrr": f"{100 * (1 - RR_CRUDE):.0f}",
        "adj": f"{abs(100 * RD_ADJ):.1f}",
        "adj_lo": f"{abs(100 * RD_ADJ_LO):.1f}",
        "adj_hi": f"{abs(100 * RD_ADJ_HI):.1f}",
        "ed_call_ev": str(ED_CALL.events),
        "ed_call_pct": pct(ED_CALL.risk),
        "ed_usual_ev": str(ED_USUAL.events),
        "ed_usual_pct": pct(ED_USUAL.risk),
        "ed_rd": f"{abs(100 * RD_ED):.1f}",
        "ed_lo": f"{abs(100 * RD_ED_LO):.1f}",
        "ed_hi": f"{abs(100 * RD_ED_HI):.1f}",
        "hi_call_ev": str(STRATA["High"][0].events),
        "hi_call_n": str(STRATA["High"][0].n),
        "hi_call_pct": pct(STRATA["High"][0].risk),
        "hi_usual_ev": str(STRATA["High"][1].events),
        "hi_usual_n": str(STRATA["High"][1].n),
        "hi_usual_pct": pct(STRATA["High"][1].risk),
        "lo_call_ev": str(STRATA["Lower"][0].events),
        "lo_call_n": str(STRATA["Lower"][0].n),
        "lo_call_pct": pct(STRATA["Lower"][0].risk),
        "lo_usual_ev": str(STRATA["Lower"][1].events),
        "lo_usual_n": str(STRATA["Lower"][1].n),
        "lo_usual_pct": pct(STRATA["Lower"][1].risk),
        "hi_share_call": pct(HIGH_SHARE_CALL, 0),
        "hi_share_usual": pct(HIGH_SHARE_USUAL, 0),
        "hosp_a_ev": str(HOSPITALS["Hospital A"].events),
        "hosp_a_n": str(HOSPITALS["Hospital A"].n),
        "hosp_a_pct": pct(HOSPITALS["Hospital A"].risk),
        "hosp_b_ev": str(HOSPITALS["Hospital B"].events),
        "hosp_b_n": str(HOSPITALS["Hospital B"].n),
        "hosp_b_pct": pct(HOSPITALS["Hospital B"].risk),
        "call_hours": f"{CALL_HOURS:.0f}",
        "mins": str(MINUTES_PER_CALL),
        "roof_n": str(ROOF_N),
        "roof_c": f"{ROOF_MEAN_COATED:.1f}",
        "roof_s": f"{ROOF_MEAN_STANDARD:.1f}",
        "roof_diff": f"{abs(ROOF_DIFF):.1f}",
        "roof_lo": f"{abs(ROOF_LO):.1f}",
        "roof_hi": f"{abs(ROOF_HI):.1f}",
        "fiction": FICTION_LABEL,
    }
    return f


if __name__ == "__main__":
    for k, v in facts().items():
        print(f"{k:16}{v}")
    print("ROOF hi signed", ROOF_HI, "ADJ hi", RD_ADJ_HI, "ED", RD_ED_LO, RD_ED_HI)
    assert FLOW["discharged"] - FLOW["transferred"] - FLOW["palliative"] - FLOW["no_phone"] == FLOW["analysed"]
    assert TOTAL_N == FLOW["analysed"]
    assert sum(g.n for g in HOSPITALS.values()) == TOTAL_N
    assert sum(g.events for g in HOSPITALS.values()) == TOTAL_EVENTS
    for i, g in enumerate((CALL, USUAL)):
        assert sum(s[i].n for s in STRATA.values()) == g.n
        assert sum(s[i].events for s in STRATA.values()) == g.events
