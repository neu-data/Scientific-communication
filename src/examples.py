"""Worked text used across the decks, workbook and facilitator guide.

Every number comes from casebook.facts(), so one edit changes all materials.
"""
from casebook import facts

F = facts()


def t(s):
    return s.format(**F)


CASE_A_BRIEF = t(
    "CareCall (fictional). Two hospitals looked at whether a nurse telephone call within 72 hours of discharge "
    "was linked to fewer unplanned readmissions within 30 days. Of {disch} adults discharged from medical wards in one "
    "year, {excl} were excluded ({transferred} transferred, {palliative} on palliative pathways, {nophone} with no working "
    "phone number), leaving {total_n}. Calls were not randomised: patients received one when a nurse was free and the "
    "patient could be reached."
)
CASE_B_BRIEF = t(
    "CoolRoom (fictional). A school district painted reflective coating on the roofs above {roof_n} classrooms and compared "
    "mean afternoon temperature over one hot term with {roof_n} classrooms under standard roofs. Head teachers volunteered "
    "the coated rooms, so allocation was not random."
)

CASE_A_TABLE = [
    ["Group", "Readmitted", "Patients", "Risk (%)"],
    ["Call", F["call_ev"], F["call_n"], F["call_pct"]],
    ["No call", F["usual_ev"], F["usual_n"], F["usual_pct"]],
    ["Call, high discharge risk", F["hi_call_ev"], F["hi_call_n"], F["hi_call_pct"]],
    ["No call, high discharge risk", F["hi_usual_ev"], F["hi_usual_n"], F["hi_usual_pct"]],
    ["Call, lower discharge risk", F["lo_call_ev"], F["lo_call_n"], F["lo_call_pct"]],
    ["No call, lower discharge risk", F["lo_usual_ev"], F["lo_usual_n"], F["lo_usual_pct"]],
]

# ---------------------------------------------------------- Results paragraph
PARA_BEFORE = t(
    "It is a well-known fact that post-discharge follow-up is of great importance. The implementation of nurse telephone "
    "calls in our hospitals led to a highly significant reduction in readmissions of {rrr}% (p<0.05), which proves that "
    "the intervention works and should be rolled out everywhere. There was no effect on emergency visits."
)
PARA_AFTER = t(
    "We examined whether a nurse telephone call within 72 hours of discharge was associated with fewer unplanned "
    "readmissions. Of {total_n} adults discharged from medical wards at two hospitals, {call_ev} of {call_n} who received a "
    "call ({call_pct}%) and {usual_ev} of {usual_n} who did not ({usual_pct}%) were readmitted within 30 days, a difference "
    "of {rd} percentage points (95% CI {rd_hi} to {rd_lo}). Patients who received calls were less often at high risk at "
    "discharge ({hi_share_call}% v {hi_share_usual}%). Within risk strata the combined difference was {adj} percentage "
    "points (95% CI {adj_lo} lower to {adj_hi} higher). Because calls were not randomised, these results do not show that "
    "the calls caused the difference. Emergency visits without admission were {ed_call_pct}% and {ed_usual_pct}%, but the "
    "interval ({ed_lo} lower to {ed_hi} higher per 100) is too wide to rule out a useful benefit or a small harm."
)
PARA_NOTES = [
    ("Removed the opening claim", "\"Well-known\" and \"great importance\" give the reader nothing to check."),
    ("Replaced the verb", "\"Led to\" and \"proves\" claim cause. The calls were not randomised, so the question is now stated as an association."),
    ("Added counts and denominators", t("{rrr}% sounds large and hides the base. {call_ev} of {call_n} and {usual_ev} of {usual_n} let a reader check it.")),
    ("Reported the absolute difference and its interval", "A risk difference with a 95% CI shows size and precision. \"Highly significant\" shows neither."),
    ("Exposed the confounder", "High-risk patients were harder to reach. Readers need this to judge the crude result."),
    ("Moved the recommendation out", "A results paragraph reports. The recommendation belongs in the conclusion, where it can be argued."),
    ("Rewrote \"no effect\"", "A wide interval around a small difference means the data cannot tell. It does not show the calls had no effect."),
]

# ---------------------------------------------------------- One finding, four forms
ABSTRACT_PASSAGE = t(
    "Results: Of {total_n} patients, {call_ev}/{call_n} (14.6%) with a call and {usual_ev}/{usual_n} (21.5%) without were "
    "readmitted within 30 days (risk difference {rd} percentage points lower, 95% CI {rd_hi} to {rd_lo} lower). After "
    "stratifying by discharge risk the difference was {adj} points lower (95% CI {adj_lo} lower to {adj_hi} higher). "
    "Conclusions: Follow-up calls were associated with fewer readmissions, but much of the gap may reflect lower risk among "
    "patients reached. A randomised evaluation is needed."
)
HEADLINE_WEAK = "Readmission results"
HEADLINE = "Patients who got a call had fewer readmissions, but the gap narrowed after accounting for risk"
SPOKEN = t(
    "For every hundred patients, those who got a call had about seven fewer readmissions. But the nurses reached healthier "
    "patients more easily. When we compare like with like, the gap is about four per hundred, and the data fit anything from "
    "nine fewer to one more. So this is a promising signal. It is not yet proof."
)

# ---------------------------------------------------------- Three rooms
ROOMS = [
    ("Conference audience", "Peers in the field, mixed methods knowledge",
     "Consider a new explanation and ask how it applies to their setting",
     t("In two hospitals, a nurse call was linked to {rd} fewer readmissions per 100, but much of that gap reflected who could be reached.")),
    ("Thesis committee", "Examiners who know the field and will probe your choices",
     "Judge that the work is yours, sound and a contribution",
     "I show that reachability confounds observational evaluations of follow-up calls, and I defend the stratified analysis that reveals it."),
    ("Hospital management", "Decision-makers with budgets, little time, limited methods detail",
     "Decide what to do next",
     t("We recommend a six-month staggered trial on two wards before funding full roll-out, because the benefit could be {adj_lo} fewer to {adj_hi} more readmissions per 100.")),
]

# ---------------------------------------------------------- Sentence-level repairs
SENTENCE_FIXES = [
    ("Vague", "Readmissions were considerably lower in the call group.",
     t("Readmissions were {rd} percentage points lower in the call group ({call_pct}% v {usual_pct}%)."),
     "Name the size."),
    ("Wordy", "Due to the fact that a large number of patients could not be contacted, it was not possible to make calls to all of them.",
     t("Nurses could not call every patient, so {usual_n} received no call."),
     "Fewer words, same fact, and a real verb."),
    ("Jargon", "Post-discharge telephonic engagement modalities were operationalised by nursing staff.",
     "Nurses telephoned patients after discharge.",
     "Keep technical terms when they carry meaning. These do not."),
    ("Result or interpretation", t("The calls worked, with {call_pct}% readmitted."),
     t("{call_pct}% of patients who received a call were readmitted. (Result.) This may reflect the call, or that healthier patients were easier to reach. (Interpretation.)"),
     "Mark where the data end and your reading begins."),
    ("Denominator", t("{hosp_a_ev} readmissions at Hospital A against {hosp_b_ev} at Hospital B shows that A performs worse."),
     t("Hospital A readmitted {hosp_a_ev} of {hosp_a_n} patients ({hosp_a_pct}%) and Hospital B {hosp_b_ev} of {hosp_b_n} ({hosp_b_pct}%)."),
     "Counts without denominators reverse the picture here."),
    ("Uncertainty", t("The calls reduce readmissions by {adj} percentage points."),
     t("After stratifying by discharge risk, the estimate was {adj} points lower (95% CI {adj_lo} lower to {adj_hi} higher)."),
     "A single number hides how much the data allow."),
    ("Causal language", "Calls prevent readmissions.",
     "Patients who received calls were less often readmitted. We cannot say from this design whether the calls caused this.",
     "Match the verb to the design."),
    ("Non-significant", t("The coating had no effect on temperature (p>0.05)."),
     t("Coated rooms were {roof_diff} °C cooler on average, but the 95% CI ran from {roof_lo} °C cooler to {roof_hi} °C warmer."),
     "\"Not significant\" is not \"no effect\"."),
]

# ---------------------------------------------------------- Editing exercise (Case B)
EXERCISE_PARA = t(
    "In light of the fact that excessive heat in classrooms constitutes a significant problem for learning, the implementation "
    "of a reflective roof coating was undertaken in a number of classrooms. It was found that temperatures were much lower in "
    "the coated rooms, showing that the coating cools classrooms and will improve exam results. However, the difference was not "
    "statistically significant (p>0.05), so it can be concluded that the coating does not work."
)
EXERCISE_DATA = t(
    "Facts you may use: {roof_n} coated and {roof_n} standard classrooms. Mean afternoon temperature {roof_c} °C and {roof_s} °C. "
    "Difference {roof_diff} °C cooler in coated rooms (95% CI {roof_lo} °C cooler to {roof_hi} °C warmer). Head teachers "
    "volunteered the coated rooms. Exam results were not measured."
)
EXERCISE_MODEL = t(
    "We asked whether a reflective roof coating lowers classroom temperature. Mean afternoon temperature was {roof_c} °C in {roof_n} coated "
    "classrooms and {roof_s} °C in {roof_n} standard classrooms, a difference of {roof_diff} °C (95% CI {roof_lo} °C cooler to {roof_hi} °C "
    "warmer). The interval includes no difference and a useful cooling, so this small pilot cannot settle the question. Head teachers chose "
    "the coated rooms, so other differences between rooms could explain some of the gap. We did not measure exam results."
)
EXERCISE_PROBLEMS = [
    ("\"In light of the fact that\", \"constitutes\", \"the implementation of ... was undertaken\"", "Wordy opening. Nominalised verbs hide who did what.", "Start with the question."),
    ("\"significant problem\"", "\"Significant\" is used in two senses in one paragraph.", "Keep the word for its statistical sense, or drop it."),
    ("\"a number of classrooms\"", "Vague, with no denominator.", "State 12 and 12."),
    ("\"much lower\"", "No size or uncertainty.", "Give the means, the difference and the interval."),
    ("\"showing that the coating cools\"", "Causal claim from a non-random comparison.", "Say what was compared and how rooms were chosen."),
    ("\"will improve exam results\"", "Exam results were not measured.", "Remove it, or state clearly that it was not studied."),
    ("\"it can be concluded that the coating does not work\"", "Treats a non-significant result as proof of no effect. It also contradicts the earlier sentence.", "Say the interval includes both no difference and useful cooling."),
]

# ---------------------------------------------------------- Headline exercise (talk and workshop)
HEADLINE_TASK = [
    ("Readmission results", "Topic label. Says nothing has been found."),
    ("Calls slash readmissions by a third", "Causal, and uses the relative figure alone."),
    ("Calls had no effect on emergency visits", "Treats an uncertain result as proof of none."),
]
HEADLINE_MODELS = [
    t("Patients with a call were readmitted less often: {call_pct}% v {usual_pct}% (not randomised)"),
    t("Readmissions were {rd} points lower with a call, and {adj} points lower within risk groups"),
    t("Emergency visits were similar, but the data cannot rule out a useful benefit"),
]
