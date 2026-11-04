"""Course structure: outcomes, schedules and alignment. Single source for every timing."""

COURSE = "Scientific Communication: Writing, Slide Design and Presentation Skills"
VERSION = "Version 1.0, November 2026"
ORG = "Neudata Consulting Ltd"

OUTCOMES = {
    "LO1": "Define their audience, purpose and main message.",
    "LO2": "Build an argument that connects a question, evidence, interpretation and implications.",
    "LO3": "Write clear scientific paragraphs, abstracts and slide headlines without overstating findings.",
    "LO4": "Design readable slides and explain figures accurately.",
    "LO5": "Deliver a timed presentation and respond to questions.",
    "LO6": "Use structured feedback to revise and rehearse their work.",
}

# (block title, minutes, kind, what happens, what participants produce, outcomes)
WORKSHOP = [
    ("Welcome and working pairs", 8, "teach", "Goals, ground rules, confidentiality, form pairs", "", []),
    ("Module 1: Audience, purpose and message", 20, "practice", "Teach 7, Worksheet 1 for 10, pair check 3", "Audience-and-message worksheet", ["LO1"]),
    ("Module 2: Scientific writing", 30, "practice", "Teach 13, paragraph edit 12, debrief 5", "Revised paragraph", ["LO2", "LO3"]),
    ("Module 3: Presentation structure", 20, "practice", "Teach 8, storyboard 10, share 2", "Short presentation storyboard", ["LO2"]),
    ("Break", 12, "break", "Short break", "", []),
    ("Module 4: Slide design and data communication", 34, "practice", "Teach 16, critique and redesign 13, debrief 5", "One redesigned slide", ["LO3", "LO4"]),
    ("Module 5: Delivery skills", 10, "practice", "Teach and demonstrate 5, opening and transition drill 5", "Spoken opening line", ["LO5"]),
    ("Timed rehearsal in trios", 22, "practice", "Brief 2, three 6-minute rounds, whole-group debrief 2", "Rehearsed explanation, peer feedback", ["LO4", "LO5", "LO6"]),
    ("Question-and-answer practice", 12, "practice", "Teach and brief 3, three 3-minute rounds", "Practised answers", ["LO5", "LO6"]),
    ("Module 6: Accuracy and responsible use", 7, "practice", "Teach 4, accuracy check on own slide 3", "Checked slide", ["LO3", "LO4"]),
    ("Close: revise and commit", 5, "practice", "Choose one revision, write next step, course feedback", "Personal revision plan", ["LO6"]),
]

TALK = [
    ("Opening: one finding, three rooms", 5, "teach", "Same fictional finding told three ways", "", []),
    ("Decide the audience and the message", 10, "teach", "Audience, purpose, one-sentence message", "", ["LO1"]),
    ("Claims that match the evidence", 10, "teach", "Effect sizes, denominators, uncertainty, causal language", "", ["LO3"]),
    ("Audience activity: fix the headline", 7, "practice", "Think 2, pairs 3, debrief 2", "One rewritten headline", ["LO3"]),
    ("Slides and charts that explain", 12, "teach", "Headline plus evidence, three redesigns, misleading axis", "", ["LO4"]),
    ("Delivery, rehearsal and responsible use", 7, "teach", "Timing, explaining a figure, honest answers, AI checks", "", ["LO5"]),
    ("Questions and close", 9, "qa", "Questions 7, close 2", "", ["LO5"]),
]

# Anchored feedback rubric. A course feedback tool, not a validated assessment instrument.
RUBRIC = [
    ("Message", "No single claim can be identified, or the listener names a different one from the speaker.",
     "A claim is present, but it drifts, or the listener needs help to repeat it.",
     "One clear claim. The listener can repeat it, and it suits this audience and purpose."),
    ("Structure", "Reads as a list of topics. Steps do not follow from each other.",
     "Most steps link. One gap between question, evidence, interpretation or implication.",
     "Question, evidence, interpretation and implication connect, with clear transitions."),
    ("Writing", "Vague, wordy or overstated. Results and interpretation are mixed.",
     "Clear in most places. Some vague wording, or one claim slightly too strong.",
     "Clear and direct. Each sentence is no stronger than its evidence."),
    ("Evidence", "Numbers without context, or a claim with no numbers. Non-significance read as no effect.",
     "Most of size, denominator and uncertainty are given. Design only partly stated.",
     "Size, denominator and uncertainty are given where relevant, with honest limits."),
    ("Visual clarity", "Hard to read from the back. Message not visible. Colour used as the only signal.",
     "Readable, but cluttered, or the headline is a topic. Axes or units partly explained.",
     "Readable, one claim visible, figure explained, and nothing relies on colour alone."),
    ("Timing", "Over the limit by more than a quarter, or stopped before the main point.",
     "Within a quarter of the limit, but the ending was rushed or reached only just.",
     "Within the limit, with the main point and conclusion delivered at an even pace."),
    ("Responses to questions", "Avoids, bluffs or argues. Does not state uncertainty.",
     "Answers part of the question, or answers at length. Limits partly stated.",
     "Listens, checks, answers briefly, states limits and says when something is unknown."),
]

# Outcome alignment: which activity teaches it and how feedback is gathered.
ALIGNMENT = [
    ("LO1", "Module 1 and Worksheet 1", "Audience-and-message worksheet, pair check", "Message"),
    ("LO2", "Modules 2 and 3, storyboard", "Revised paragraph and storyboard", "Message, Structure, Evidence"),
    ("LO3", "Module 2 exercise, Worksheet 2, Module 6 check", "Revised paragraph, redesigned slide headline", "Writing, Evidence"),
    ("LO4", "Module 4 exercise, Worksheet 4, trio rehearsal", "Redesigned slide, spoken figure explanation", "Visual clarity, Evidence"),
    ("LO5", "Module 5 drill, trio rehearsal, Q&A practice", "Timed explanation, practised answers", "Timing, Responses to questions"),
    ("LO6", "Feedback prompts in rehearsal and Q&A, closing plan", "Feedback notes, personal revision plan", "All criteria"),
]


def clock(items):
    """Yield (start, end, *block) in minutes from the start."""
    t = 0
    for b in items:
        yield (t, t + b[1], *b)
        t += b[1]


def fmt(m):
    return f"{m // 60}:{m % 60:02d}"


assert sum(b[1] for b in WORKSHOP) == 180
assert sum(b[1] for b in TALK) == 60
