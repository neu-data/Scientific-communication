"""Recalculates every fictional number from raw counts, independently of src/casebook.py,
then confirms that the expected values appear in the built materials and stale values do not.

    python scripts/check_numbers.py
"""
from math import sqrt
from pathlib import Path

import fitz
from scipy import stats

ROOT = Path(__file__).parents[1]
Z = stats.norm.ppf(0.975)


def wald(e1, n1, e0, n0):
    p1, p0 = e1 / n1, e0 / n0
    d = p1 - p0
    se = sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    return 100 * d, 100 * (d - Z * se), 100 * (d + Z * se)


# Raw counts, typed here on purpose rather than imported
call, usual = (60, 412), (94, 438)
strata = [((32, 120), (59, 198)), ((28, 292), (35, 240))]
ed = ((40, 412), (47, 438))
hosp = {"A": (95, 540), "B": (59, 310)}

assert 1037 - 62 - 41 - 84 == 850 == call[1] + usual[1]
assert sum(h[0] for h in hosp.values()) == call[0] + usual[0] == 154
assert sum(h[1] for h in hosp.values()) == 850
assert sum(s[0][0] for s in strata) == 60 and sum(s[1][0] for s in strata) == 94
assert sum(s[0][1] for s in strata) == 412 and sum(s[1][1] for s in strata) == 438

crude = wald(*call, *usual)
edd = wald(*ed[0], *ed[1])
hi = wald(*strata[0][0], *strata[0][1])
lo = wald(*strata[1][0], *strata[1][1])

# Mantel-Haenszel risk difference with Greenland-Robins variance
w = [a[1] * b[1] / (a[1] + b[1]) for a, b in strata]
rds = [a[0] / a[1] - b[0] / b[1] for a, b in strata]
mh = sum(x * y for x, y in zip(w, rds)) / sum(w)
var = sum(
    (a[1] * b[1] / (a[1] + b[1])) ** 2
    * (a[0] / a[1] * (1 - a[0] / a[1]) / a[1] + b[0] / b[1] * (1 - b[0] / b[1]) / b[1])
    for a, b in strata
) / sum(w) ** 2
mh_lo, mh_hi = 100 * (mh - Z * sqrt(var)), 100 * (mh + Z * sqrt(var))

# Classroom case
n, m1, m0, s1, s0 = 12, 29.4, 30.6, 1.5, 1.6
se = sqrt(s1 ** 2 / n + s0 ** 2 / n)
t = stats.t.ppf(0.975, 2 * n - 2)
roof = (m1 - m0, m1 - m0 - t * se, m1 - m0 + t * se)
assert abs(sum([28.5, 29.3, 30.0, 29.8]) / 4 - 29.4) < 1e-9
assert abs(sum([29.8, 30.4, 31.3, 30.9]) / 4 - 30.6) < 1e-9

expected = {
    "call risk": (f"{100 * 60 / 412:.1f}", "14.6"),
    "no-call risk": (f"{100 * 94 / 438:.1f}", "21.5"),
    "crude difference": (f"{-crude[0]:.1f}", "6.9"),
    "crude CI far": (f"{-crude[1]:.1f}", "12.0"),
    "crude CI near": (f"{-crude[2]:.1f}", "1.8"),
    "relative reduction": (f"{100 * (1 - (60 / 412) / (94 / 438)):.0f}", "32"),
    "within-strata difference": (f"{-100 * mh:.1f}", "4.3"),
    "within-strata CI far": (f"{-mh_lo:.1f}", "9.4"),
    "within-strata CI near": (f"{mh_hi:.1f}", "0.8"),
    "emergency call": (f"{100 * 40 / 412:.1f}", "9.7"),
    "emergency no call": (f"{100 * 47 / 438:.1f}", "10.7"),
    "emergency difference": (f"{-edd[0]:.1f}", "1.0"),
    "emergency CI far": (f"{-edd[1]:.1f}", "5.1"),
    "emergency CI near": (f"{edd[2]:.1f}", "3.0"),
    "high-risk difference": (f"{-hi[0]:.1f}", "3.1"),
    "high-risk CI": (f"{-hi[1]:.1f} {hi[2]:.1f}", "13.3 7.0"),
    "lower-risk difference": (f"{-lo[0]:.1f}", "5.0"),
    "lower-risk CI": (f"{-lo[1]:.1f} {lo[2]:.1f}", "10.6 0.6"),
    "high-risk share called": (f"{100 * 120 / 412:.0f}", "29"),
    "high-risk share not called": (f"{100 * 198 / 438:.0f}", "45"),
    "hospital A": (f"{100 * 95 / 540:.1f}", "17.6"),
    "hospital B": (f"{100 * 59 / 310:.1f}", "19.0"),
    "roof difference": (f"{-roof[0]:.1f}", "1.2"),
    "roof CI cooler": (f"{-roof[1]:.1f}", "2.5"),
    "roof CI warmer": (f"{roof[2]:.1f}", "0.1"),
    "nurse hours": (f"{412 * 20 / 60:.0f}", "137"),
    "overall risk": (f"{100 * 154 / 850:.1f}", "18.1"),
}
bad = [k for k, (got, want) in expected.items() if got != want]
for k, (got, want) in expected.items():
    print(f"{'ok ' if got == want else 'BAD'} {k:30} recalculated {got:12} expected {want}")
assert not bad, bad

# Rounded values subtract cleanly, so nobody can catch the slides out
assert round(21.5 - 14.6, 1) == 6.9 and round(10.7 - 9.7, 1) == 1.0 and round(30.6 - 29.4, 1) == 1.2
assert round(29.8 - 26.7, 1) == 3.1 and round(14.6 - 9.6, 1) == 5.0

# Search built PDFs
texts = {}
for pdf in sorted((ROOT / "materials").rglob("*.pdf")):
    texts[pdf.name] = " ".join(p.get_text() for p in fitz.open(pdf)).replace("\n", " ")
must_have = {
    "Scientific_Communication_Workshop_3h.pdf": ["14.6", "21.5", "6.9", "4.3", "60 of 412", "94 of 438", "850", "1,037"],
    "Scientific_Communication_Talk_1h.pdf": ["14.6", "21.5", "6.9", "4.3", "60 of 412", "94 of 438"],
    "Participant_Workbook.pdf": ["14.6", "21.5", "60 of 412", "94 of 438", "29.4", "30.6"],
    "Facilitator_Guide.pdf": ["14.6", "21.5", "137 hours", "154 of 850"],
}
for fn, items in must_have.items():
    for it in items:
        assert it in texts[fn], (fn, it)
stale = ["6.4 percentage", "15.0%", "62 of 412", "33 fewer", "41 of 412", "96 of 540", "60 of 310", "156 of 850", "about five times the height", "five times as tall"]
for fn, tx in texts.items():
    for s in stale:
        assert s not in tx, (fn, s)
print(f"\nAll numbers recalculated and {len(texts)} PDFs searched. No stale values.")
