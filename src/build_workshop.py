"""Builds the three-hour workshop deck."""
from pathlib import Path

import casebook as cb
import course as c
import examples as ex
from slides_lib import *

OUT = Path(__file__).parents[1] / "materials" / "workshop_3h" / "Scientific_Communication_Workshop_3h.pptx"
d = D()
B = [b[0] for b in c.WORKSHOP]

# ------------------------------------------------------------------ Welcome
d.set_block(B[0])
d._tick(1)
d.title_slide("Scientific Communication", "Writing, slide design and presentation skills\nA three-hour practical workshop", "Version 1.0, November 2026",
              timed(1, N("Welcome. This is three hours of practice with a little teaching in between. You already know your subject. Today is about helping other people understand it, and about making sure your claims are no stronger than your evidence.",
                         do="Have the workbook open, the timer visible and the groups plan ready. Slides are 16:9 and the notes carry timing for each slide.")))

s = d.s("You will leave with four things you made yourself", 3, N(
    "The bar is the whole session, drawn to scale. Green blocks are modules with practice. More than half of the session is your own work, and much of that comes after the break. By the end you will have a revised paragraph, a short storyboard, one redesigned slide and an explanation you have rehearsed against a clock. This is an introduction with guided practice. Nobody masters scientific writing or public speaking in three hours, and we do not claim you will.",
    ask="What would make today useful for you? Take two answers.",
    watch="People hoping for a full talk rehearsal. Explain that you rehearse one explanation, because that is what fits."))
total = 180
x = LEFT
for st, en, title, mins, kind, what, out, los in c.clock(c.WORKSHOP):
    w = WIDTH * mins / total
    col = {"teach": MID, "practice": DEEP, "break": "D5DDE1"}[kind]
    box(s, x, 112, w - 2, 44, fill=col, name=f"Schedule: {title}, {mins} min")
    x += w
for lab, xm in (("0:00", 0), ("1:00", 60), ("2:00", 120), ("3:00", 180)):
    text(s, LEFT + WIDTH * xm / total - (28 if xm == 180 else 0), 160, 60, 18, lab, size=13, color=GREY)
text(s, LEFT, 184, WIDTH, 24, "Green: modules with practice. Grey: welcome. Pale: 12-minute break.", size=14, color=GREY)
items = [("Revised paragraph", "Claim, evidence and caution in the right order"), ("Storyboard", "A short talk planned as an argument"),
         ("Redesigned slide", "Headline plus evidence"), ("Rehearsed explanation", "Two timed minutes, with feedback")]
for i, (a, b) in enumerate(items):
    bx = LEFT + i * 228
    box(s, bx, 224, 208, 150, [{"t": a, "bold": True, "color": NAVY, "size": 18}, b], fill=MIST, size=15, margin=14, anchor="top", spacing=8)
text(s, LEFT, 392, WIDTH, 60, "You also take away a workbook, worksheets, a rehearsal checklist and a feedback rubric.", size=18, color=INK)

s = d.s("We give feedback on clarity and understanding, never on accent or personality", 2, N(
    "Four ground rules. First, feedback here is about whether the message reached the listener. Accent and personality are off the table. Many of us present in English as an additional language, and that is an asset in an international field. Second, use fictional data or your own non-confidential work. Do not bring identifiable patient, staff or client details into this room. Third, what is shared here stays here. Fourth, this is practice, so expect things to be unfinished.",
    do="Point to the fictional-data label on slides. Ask anyone using their own work to remove identifiers now.",
    basis="Teaching recommendation, informed by Derwing and Munro 2009 on intelligibility and Hattie and Timperley 2007 on task-focused feedback."))
rules_ = [("Feedback on the work", "Clarity, evidence and understanding. Never accent, looks or personality."), ("No confidential data", "Fictional cases, or your own work with identifiers removed."),
          ("What is said here stays here", "Share ideas freely, including unfinished ones."), ("Practice, not performance", "Expect rough drafts. Nothing today is graded.")]
for i, (a, b) in enumerate(rules_):
    bx, by = LEFT + (i % 2) * 456, 108 + (i // 2) * 170
    box(s, bx, by, 436, 150, [{"t": a, "bold": True, "color": DEEP, "size": 20}, b], fill=MIST, size=18, margin=18, spacing=8)

s = d.s("One fictional study runs through the session, told to three different rooms", 2, N(
    f"CareCall is invented for this course. Two hospitals looked at nurse telephone calls within 72 hours of discharge. {F['total_n']} patients were analysed and {F['call_n']} got a call. Calls were not randomised: a patient got one if a nurse was free and the patient could be reached. Keep that in mind, because it matters to everything we say later. We use a second fictional case from outside health, CoolRoom, on classroom temperature, so that non-clinical colleagues have a home too. If you have your own result, use it in the exercises.",
    ask="Before we see any analysis: why might patients who get a call differ from those who do not? Expected: reachable patients may be healthier or better supported.",
    watch="Anyone treating CareCall as a real study. Repeat that it is fictional."), fictional=True)
stats = [(F["total_n"], "patients analysed, two hospitals"), (f"{F['call_pct']}%", f"readmitted with a call ({F['call_ev']} of {F['call_n']})"), (f"{F['usual_pct']}%", f"readmitted with no call ({F['usual_ev']} of {F['usual_n']})")]
for i, (a, b) in enumerate(stats):
    bx = LEFT + i * 304
    text(s, bx, 104, 284, 56, a, size=44, bold=True, color=DEEP)
    text(s, bx, 164, 284, 50, b, size=16)
box(s, LEFT, 224, WIDTH, 50, "Calls were **not randomised**. Nurses called when free, and only patients who could be reached.", fill=AMBER_BG, size=18, margin=14)
text(s, LEFT, 290, WIDTH, 24, "The three rooms", size=18, bold=True, color=NAVY)
for i, (a, b) in enumerate((("Conference", "Researchers presenting to peers"), ("Thesis defence", "Students facing examiners"), ("Hospital or organisation", "Professionals briefing decision-makers"))):
    box(s, LEFT + i * 304, 320, 284, 96, [{"t": a, "bold": True, "color": NAVY, "size": 18}, b], fill=MIST, size=15, margin=12, align="c")
text(s, LEFT, 426, WIDTH, 26, "A second fictional case, CoolRoom, covers classroom temperature for non-clinical colleagues.", size=15, color=GREY)

# ------------------------------------------------------------------ Module 1
d.set_block(B[1])
d.sec("Audience, purpose and message", "Module 1: 20 minutes", 0.5, N("First module. By the end you will have a one-sentence message for your own talk."))
s_audience_chain(d, 2, N(
    "Most weak talks fail before the first slide, because the speaker never decided who the talk is for or what should change. Work through these five boxes from left to right. Who is in the room? What do they already know? What do they need from you? What should change afterwards: should they understand something, decide something or do something? Only then write your one sentence.",
    ask="Think of your next talk. Who is the most important person in the room, and what should they do afterwards?",
    basis="Advice: Bourne 2007 on knowing your audience. The CDC Clear Communication Index asks authors to state audience, objective and main message first, but it is built for public health materials. The chain itself is a neu-data teaching recommendation."))
s_topic_message(d, 2, N(
    "This is the most useful distinction today. The left box is a topic. You could give a talk on it and say anything. The right box is a message. It says something, it has a verb, and someone could disagree. Notice that it also carries its caution: linked to, not caused. Apply the three checks to your own sentence.",
    ask="Is 'Barriers to antibiotic stewardship' a topic or a message? Expected: a topic. Ask someone to turn it into a claim.",
    watch="Messages that are true but empty, such as 'communication is important'."))
s_three_rooms(d, 2.5, N(
    f"Same data, three messages. The conference audience wants a new idea, and the claim is about what the evidence suggests. The thesis committee wants to see your contribution and your reasoning. Hospital management wants a decision, so the recommendation comes first and the numbers support it. None of these changes the evidence. Each changes what you lead with. All three keep the uncertainty: the management message still gives {F['adj_lo']} fewer to {F['adj_hi']} more.",
    ask="Which room is closest to your next talk?",
    watch="Thinking that managers need less honesty. They need less method detail and the same honesty."))
s = d.s("Fill in Worksheet 1 for your own talk", 13, N(
    "Ten minutes alone on Worksheet 1, then three minutes in pairs. Use your own work if you can. If you cannot, use CareCall or CoolRoom and choose one of the three rooms. In the pair check, read your one-sentence message aloud. Your partner says back what they think you want them to do. If that does not match, revise.",
    do="Start the timer. Circulate. Call the switch to pairs at 10 minutes. Look for topic-style sentences and ask 'what is the claim?'",
    watch="Sentences with no verb, sentences with three ideas joined by 'and', and audiences described as 'everyone'. CDC's guide does not accept 'general public' as an audience, which is a useful prompt."))
activity_bar(s, 13, "Worksheet 1 alone (10), then pair check (3). Workbook page: Worksheet 1.")
for i, (a, b) in enumerate((("Alone, 10 minutes", ["Name your audience and what they know", "State what should change afterwards", "Write your message in one sentence"]),
                            ("In pairs, 3 minutes", ["Read your sentence aloud", "Partner says back what they think you want them to do", "Revise if it does not match"]))):
    text(s, LEFT + i * 456, 150, 436, 26, a, size=20, bold=True, color=NAVY)
    text(s, LEFT + i * 456, 186, 436, 220, b, size=19, spacing=12)
text(s, LEFT, 396, WIDTH, 50, "No current talk? Use CareCall or CoolRoom and pick one room.", size=18, color=GREY)

# ------------------------------------------------------------------ Module 2
d.set_block(B[2])
d.sec("Scientific writing", "Module 2: 30 minutes", 0.5, N("Now the writing. Clear slides and clear talks depend on clear sentences. We will move quickly and then you will edit a paragraph."))

s = d.s("A clear paragraph makes one point, then supports it", 1.5, N(
    "Read the paragraph in four colours of meaning. The first sentence gives the point. The second gives evidence, with numbers. The third interprets. The last says what follows. Readers should be able to read only the first sentence of each paragraph and follow your argument. In English academic prose, also try to start sentences with what the reader already knows and finish with what is new, because readers tend to look to the end of a sentence for the emphasis. That idea comes from Gopen and Swan. It is reasoned advice, and they say themselves that these are not rules.",
    basis="Teaching resource: Gopen and Swan 1990, an essay with worked revisions and no reader testing."), fictional=True,
    source="Teaching resource: Gopen & Swan 1990 (argued essay, not rules). Example: neu-data.")
rows = [("Point", f"Patients who got a nurse call were readmitted less often."),
        ("Evidence", f"Readmission within 30 days was {F['call_pct']}% with a call and {F['usual_pct']}% without ({F['call_ev']} of {F['call_n']} and {F['usual_ev']} of {F['usual_n']})."),
        ("Interpretation", "The gap may partly reflect who was reached, as high-risk patients received fewer calls."),
        ("Implication", "A randomised evaluation is needed before roll-out.")]
y = 104
for a, b in rows:
    box(s, LEFT, y, 170, 64, a, fill=NAVY, color=WHITE, size=17, bold=True, margin=12)
    box(s, LEFT + 170, y, WIDTH - 170, 64, b, fill=MIST, size=17, margin=14)
    y += 70
text(s, LEFT, 392, WIDTH, 60, "Within a sentence: start with what the reader knows, and end with what is new.", size=19, color=NAVY)

s = d.s("Most unclear sentences are vague, wordy or full of needless jargon", 1, N(
    "Three repairs. Vague: replace 'considerably' with the number. Wordy: 'due to the fact that a large number of' is 'because many'. Jargon: keep a technical term when it carries meaning that a plain word would lose. Here, it does not. Plain language means fitting words to your reader. It does not mean oversimplifying, and a specialist audience can have specialist terms. The workbook has eight of these repairs with explanations.",
    ask="Spot the real verb hiding in 'the implementation of calls was undertaken'. Expected: nurses called patients.",
    basis="Professional guidance: Federal Plain Language Guidelines and the digital.gov guide. Written for government documents, so treat as defaults."), fictional=True,
    source="Professional guidance: Federal Plain Language Guidelines; digital.gov plain language guide.")
rows = [["Problem", "Before", "After"]]
for kind, before, after, why in ex.SENTENCE_FIXES[:3]:
    rows.append([kind, before, after])
table(s, LEFT, 102, WIDTH, rows, [12, 47, 41], row_h=100, size=16, bold_first=True, name="Sentence repairs")

s = d.s("Keep what you found separate from what you think it means", 1.5, N(
    "Results and interpretation need separate sentences, and often separate paragraphs. On the left: what the data show. A sceptical colleague could check it. On the right: what you think it means, marked with words like 'may' or 'suggests'. 'The calls worked' mixes the two and overstates. Hedge where real uncertainty remains, and only there: too many hedges are as unhelpful as none. Manchester's Academic Phrasebank is a useful resource for this, especially for writers using English as an additional language.",
    ask="Is 'readmissions were lower in the call group' a result or an interpretation? Expected: result. 'The calls reduced readmissions'? Interpretation, and a causal one.",
    basis="Teaching resource: Manchester Academic Phrasebank. Guidance: STROBE on balanced abstracts."), fictional=True,
    source="Teaching resource: Manchester Academic Phrasebank. Guidance: STROBE.")
text(s, LEFT, 104, 436, 26, "RESULT: what the data show", size=16, bold=True, color=DEEP)
box(s, LEFT, 132, 436, 196, [f"{F['call_ev']} of {F['call_n']} patients with a call ({F['call_pct']}%) were readmitted, and {F['usual_ev']} of {F['usual_n']} without ({F['usual_pct']}%).", f"{F['hi_share_call']}% of those called were at high risk, against {F['hi_share_usual']}% of those not called."], fill=MIST, size=18, margin=16, spacing=10)
text(s, 490, 104, 436, 26, "INTERPRETATION: what you think it means", size=16, bold=True, color=BLUE)
box(s, 490, 132, 436, 196, ["The call **may** have helped some patients.", "The gap **may also reflect** who could be reached, because healthier patients were easier to contact."], fill=WHITE, line=BLUE, size=18, margin=16, spacing=10)
box(s, LEFT, 344, WIDTH, 100, [{"t": "Avoid mixing them", "bold": True, "color": AMBER}, f"\"The calls worked, with only {F['call_pct']}% readmitted.\""], fill=AMBER_BG, size=20, margin=16)

s_denominators(d, 1, N(
    f"A fast demonstration. Left: {F['hosp_a_ev']} readmissions at Hospital A, {F['hosp_b_ev']} at Hospital B. Hospital A looks worse. Right: Hospital A saw far more patients, and its rate is {F['hosp_a_pct']} per hundred against {F['hosp_b_pct']}. The picture reverses. So always report the numerator and the denominator together.",
    watch="Do not over-interpret the small gap between hospitals. The point is only that counts mislead.",
    basis="Reporting guidance: SAMPL asks for numerators and denominators for all percentages."))
s_size_uncertainty(d, 1.5, N(
    f"Three ways to state the same result. {F['rrr']} percent sounds impressive, and a Cochrane review found that relative figures look larger and persuade more than absolute ones, with no difference in understanding. So do not give the relative figure alone. {F['rd']} per hundred tells us the size. And {F['rd_hi']} to {F['rd_lo']} shows how uncertain that is. The plot shows the crude estimate and the estimate within risk groups. Now the interval crosses zero. In an experiment with UK public audiences, numeric ranges cost little trust, whereas vague verbal uncertainty cost more. That was not a clinical audience, so treat it as a useful pointer.",
    watch="A strict reading: a 95% CI is a property of the procedure, not a 95% chance that the truth is inside this interval. Say it once, then speak of the range the data fit.",
    basis="Research finding: Akl et al. 2011 (Cochrane, search to 2007), van der Bles et al. 2020. Guidance: SAMPL. Review: Greenland et al. 2016."))
s_verbs(d, 1.5, N(
    "Match the verb to the design. For an observational comparison such as CareCall: associated with, higher among. 'Led to' and 'prevented' are claims of cause. Even a good trial supports 'reduced, in this population', and does not support 'proves'. Two cautions. First, swapping in 'associated' does not solve the problem. In one large review many readers still heard some causal meaning in it, and recommendations often implied more causality than the sentence did. Second, some methodologists argue that if your aim is causal you should say so and state your assumptions. So name your aim, keep Results descriptive, and check your journal's preference.",
    ask="Rewrite 'smoking cessation classes reduce relapse' for a survey of past attendees.",
    basis="Research finding: Haber 2018, 2022. Commentary: Hernan 2018. Guidance: STROBE (adjustment does not by itself establish causation). GRADE 26 wording ('may', 'likely') applies to systematic reviews with a certainty rating. The ladder is a neu-data teaching recommendation."))
s_non_significant(d, 1.5, N(
    f"Two fictional results that did not reach conventional significance. For emergency visits the estimate is {F['ed_rd']} fewer per hundred, and the interval runs from {F['ed_lo']} fewer to {F['ed_hi']} more. For classrooms it is {F['roof_diff']} degrees cooler, from {F['roof_lo']} cooler to {F['roof_hi']} warmer. Neither shows no effect. Both show that the study cannot say. Altman and Bland made this point in 1995: absence of evidence is not evidence of absence. To claim two things are equivalent you need a study designed for that, with a pre-specified margin.",
    ask="What would you need to know to decide whether 1.2 degrees matters? Expected: what difference is meaningful in a classroom.",
    basis="Review and consensus: Altman and Bland 1995, Greenland et al. 2016, ASA statement 2016. The ASA statement does not ban p-values."))
s = d.s("Rewriting made this result longer, and much more honest", 1.5, N(
    "The before version is short and confident, and it overstates. Here are the seven edits; the workbook shows the full 'after' paragraph. Note that the rewrite is longer. Clear writing does not always mean fewer words. It means every word earns its place, and in a results paragraph the numbers earn theirs.",
    do="Read the before paragraph aloud once. Then walk quickly down the edits. Do not read them all out; pick two or three."), fictional=True,
    source="Worked example: neu-data. Full rewrite in the workbook.")
label(s, LEFT, 102, 380, None, "before")
box(s, LEFT, 126, 380, 324, ex.PARA_BEFORE, fill=AMBER_BG, size=17, margin=16, anchor="top")
label(s, 434, 102, 492, "WHAT WE CHANGED", "after")
y = 128
for a, b in ex.PARA_NOTES[:6]:
    text(s, 434, y, 492, 26, a, size=16, color=INK, bold=True, anchor="middle")
    rule(s, 434, y + 40, 926, y + 40, color=LINE, weight=0.75)
    y += 53
s_four_forms(d, 1.5, N(
    f"One finding, four forms. The paragraph has room for reasoning. The abstract passage compresses it. The headline makes the claim in {len(ex.HEADLINE.split())} words. The spoken version uses everyday numbers: about seven per hundred. What must survive every step? The size, the population, the design and the uncertainty. If a shorter version sounds more certain than the long one, it has changed the science. Your workbook has all four in full.",
    do="Read the spoken version aloud slowly, as a model.",
    basis="Teaching resource: MIT Communication Lab and UNC on abstracts. Guidance: STROBE item 1b."))

s = d.s("Edit the CoolRoom paragraph, or a paragraph of your own", 12, N(
    "Twelve minutes on Worksheet 2. Work alone for eight, then swap with your partner for four. The paragraph has at least seven problems: wordiness, two meanings of significant, a vague 'number of classrooms', missing numbers, a causal claim, an outcome nobody measured, and a non-significant result read as proof. You may use only the facts on the worksheet. If you brought your own paragraph, you may use that.",
    do="Start the timer. Circulate. At 8 minutes call the swap. Read over shoulders for 'no effect' and 'improves exam results'.",
    watch="Participants inventing a p-value or a claim that is not in the facts. Say: only what the data allow."), fictional=True)
activity_bar(s, 12, "Worksheet 2. Alone (8), then swap and comment (4).")
box(s, LEFT, 142, 560, 310, ex.EXERCISE_PARA, fill=AMBER_BG, size=18, margin=16, anchor="top")
text(s, 612, 142, 314, 310, [{"t": "Facts you may use", "bold": True, "color": NAVY, "size": 17},
                             f"{F['roof_n']} coated and {F['roof_n']} standard rooms", f"{F['roof_c']} °C and {F['roof_s']} °C on average", f"95% CI of the difference: {F['roof_lo']} °C cooler to {F['roof_hi']} °C warmer", "Head teachers chose the rooms", "Exam results not measured"], size=16, spacing=8)

s = d.s("A strong edit reports the data, names the limits and drops the unsupported claims", 5, N(
    f"Debrief for five minutes. Ask two pairs to read out their opening sentence, then show this version. Point out what went: 'significant' as an adjective for the problem, 'will improve exam results', and 'does not work'. Point out what arrived: the group sizes, the difference, the interval and how rooms were chosen. There are many acceptable versions. Yours need not match this one, as long as it says nothing stronger than the data.",
    ask="Which edit was hardest? Debrief questions: What did you delete first? Where did you want a stronger verb than the evidence allows? What would you need before claiming the coating works?",
    do="The facilitator guide lists all seven problems with explanations."), fictional=True, source="Model answer: neu-data. Other good versions exist.")
box(s, LEFT, 102, WIDTH, 240, ex.EXERCISE_MODEL, fill=MIST, size=18, margin=18)
text(s, LEFT, 354, WIDTH, 100, ["**Removed:** wordy opening, \"significant\" for importance, \"will improve exam results\", \"does not work\".", "**Added:** sizes of groups, means, difference, interval, how rooms were chosen."], size=17, spacing=8)

# ------------------------------------------------------------------ Module 3
d.set_block(B[3])
d.sec("Presentation structure", "Module 3: 20 minutes", 0.5, N("We now turn writing into a talk. A talk is one argument, spoken."))

s = d.s("A talk is one argument: question, evidence, interpretation, implication", 1, N(
    "Four steps, and each one must lead to the next. If your slide does not serve one of these four boxes, ask why it is in the talk. The chain is the same in every room. What changes is how long you spend in each box and where you begin.",
    ask="Which box do people usually spend too long on? Expected: background and methods.",
    basis="neu-data teaching recommendation."), fictional=True, source="neu-data teaching recommendation.")
steps = [("Question", "Are nurse calls linked to fewer readmissions?"), ("Evidence", f"{F['call_pct']}% v {F['usual_pct']}%. Within risk groups, {F['adj']} fewer per 100."),
         ("Interpretation", "A signal, partly explained by who was reached."), ("Implication", "Test on two wards before full roll-out.")]
w = 208
for i, (a, b) in enumerate(steps):
    bx = LEFT + i * (w + 20)
    box(s, bx, 130, w, 56, a, fill=DEEP, color=WHITE, size=19, bold=True, align="c", margin=4)
    box(s, bx, 186, w, 170, b, fill=MIST, size=18, margin=14)
    if i < 3:
        rule(s, bx + w + 1, 158, bx + w + 19, 158, color=TEAL, weight=2.5, arrow=True)
text(s, LEFT, 378, WIDTH, 60, "If a slide serves none of the four boxes, cut it.", size=22, color=NAVY, align="c")

s = d.s("Open with the problem and the question, not with an outline", 1, N(
    "Compare the two. The first is what many of us were taught. It spends your best thirty seconds on administration. The second tells the room why this matters and what you asked, in under thirty seconds. Then you can give a one-line roadmap if the talk is long. The number here is fictional, like the rest of the case.",
    do="Read the second opening aloud as a model. Pause after the question."), fictional=True,
    source="Teaching recommendation, consistent with Bourne 2007 and Naegle 2021 (professional advice).")
label(s, LEFT, 104, 436, "A WEAK OPENING", "before")
box(s, LEFT, 130, 436, 240, "\"Good morning. Thank you for having me. Today I will first give some background, then the methods, then results, discussion and conclusion...\"", fill=AMBER_BG, size=19, margin=18)
label(s, 490, 104, 436, "A STRONGER OPENING", "after")
box(s, 490, 130, 436, 240, f"\"Last year, about {round(cb.TOTAL_EVENTS / cb.TOTAL_N * 100)} in every 100 patients on our medical wards came back within a month. Nurses started phoning some of them after discharge. We asked: did those calls make a difference?\"", fill=MIST, size=19, margin=18)
text(s, LEFT, 388, WIDTH, 60, "Problem, then question. Then a one-line roadmap if the talk is long.", size=19, color=NAVY)

s = d.s("Show only the methods your audience needs to judge the evidence", 1, N(
    "Methods on slides are not your methods section. Ask: what must this audience know to judge my result? Usually four things: who was studied, what was compared, what was measured, and the main threat to validity. A flow diagram shows the first two and the denominators at once. A thesis committee will want more, and a management team less. Everything else goes in your backup slides.",
    ask="What is the main threat to validity in CareCall? Expected: who received a call was not random."), fictional=True,
    source="neu-data teaching recommendation. Backup slides: Naegle 2021.")
flow_diagram(s, 104)
text(s, 690, 104, 236, 180, [{"t": "Four things to show", "bold": True, "color": NAVY, "size": 17}, "Who", "What was compared", "What was measured", "Main threat to validity"], size=16, spacing=6)
text(s, LEFT, 374, WIDTH, 70, "Everything else goes to backup slides, ready for questions.", size=19, color=NAVY)

s = d.s("Lead with your main finding, then give the limits that change what it means", 1, N(
    "Do not present every table. Choose one main finding. Then choose the limits that actually change how the audience should read it. Reciting every limitation is a ritual. Saying 'this result weakens once you account for risk' is an argument. In CareCall the second finding is the limit, so it deserves a slide. A short word on 'limitations' at the end does not do that job.",
    watch="Speakers who hide limits at the end in small print. Limits belong next to the finding they affect."), fictional=True,
    source="neu-data teaching recommendation.")
rows = [["Priority", "CareCall", "Time"], ["Main finding", f"{F['rd']} fewer readmissions per 100 with a call", "Most"],
        ["Limit that changes the reading", f"Within risk groups, {F['adj']} fewer, and the data fit {F['adj_lo']} fewer to {F['adj_hi']} more", "Most"],
        ["Secondary finding", "Emergency visits: too uncertain to say", "Brief"], ["Detail", "Hospital breakdown, sensitivity checks", "Backup"]]
table(s, LEFT, 104, WIDTH, rows, [28, 58, 14], row_h=62, size=17, bold_first=True, name="Priority table")

s = d.s("The room changes where you start and where you spend your time", 1, N(
    "These bars are a planning starting point that we suggest, not findings or rules. A conference talk spends most of its time on findings and what they mean. A defence spends more on your methods and your reasoning, because that is what is being examined. A briefing puts the recommendation first, then the evidence, then the risks, and it usually leaves more time for discussion.",
    ask="If your manager says 'you have five minutes', what goes first? Expected: the recommendation."), fictional=False,
    source="Illustrative proportions: neu-data teaching suggestion, not a finding. Adjust to your setting.")
shapes_ = [("Conference talk", [("Problem", 15), ("Methods", 15), ("Findings", 45), ("Meaning", 25)]),
           ("Thesis defence", [("Problem", 15), ("Methods and choices", 35), ("Findings", 30), ("Contribution", 20)]),
           ("Organisational briefing", [("Recommendation", 25), ("Evidence", 30), ("Risks and options", 25), ("Decision", 20)])]
cols = [DEEP, BLUE, "3B6E8F", NAVY]
y = 112
for nm, parts in shapes_:
    text(s, LEFT, y, 190, 72, nm, size=17, bold=True, color=NAVY, anchor="middle")
    x = LEFT + 196
    for i, (lab_, pc) in enumerate(parts):
        w = (WIDTH - 196) * pc / 100
        box(s, x, y, w - 2, 72, lab_, fill=cols[i], color=WHITE, size=14, align="c", margin=3)
        x += w
    y += 104

s = d.s("A defence examines your contribution and your choices, so check your own rules first", 1.5, N(
    "Requirements vary a great deal, so read your own regulations first. A UK viva is usually private, and a talk may not be required at all. Many North American programmes have a public talk and then a closed session. In Sweden there may be an external opponent and a public defence of two to three hours. Whatever the format, three things recur: state your own contribution, justify your methodological choices against the alternatives, and prepare backup slides for the questions you expect. Build background for the whole room, and organise for clarity rather than the order you did the work.",
    ask="What is the format at your institution? Who could tell you?",
    basis="Policy and teaching resources: Imperial College viva procedure 2026, University of Minnesota ECE handbook, UCLA Neuroscience, Halmstad University, MIT Biological Engineering Communication Lab. Each covers one institution only."),
    source="Institutional examples: Imperial College, University of Minnesota ECE, UCLA Neuroscience, Halmstad University. Each covers one institution.")
rows = [["Format example", "Public?", "Talk?"], ["UK viva (Imperial)", "No", "Not required by the procedure"], ["US defence (UCLA Neuroscience)", "Yes, then closed session", "45 to 60 minutes"], ["Sweden (Halmstad)", "Yes, with opponent", "About 20 minutes, in most fields"]]
table(s, LEFT, 102, 520, rows, [42, 29, 29], row_h=66, size=15, bold_first=True, name="Defence formats")
text(s, 576, 102, 350, 250, [{"t": "Prepare for any format", "bold": True, "color": NAVY, "size": 18}, "**Contribution:** what is new, and what is yours", "**Choices:** why this method and not the alternatives", "**Backup slides:** expected challenges, tables, sensitivity results"], size=16, spacing=9)
box(s, LEFT, 356, WIDTH, 94, "CareCall example: \"I chose stratification over a simple comparison because reachable patients differ. A randomised design was not possible for this retrospective data.\"", fill=MIST, size=17, margin=14)

s = d.s("End with what the evidence supports, not with \"thank you\"", 1, N(
    "Your last slide stays on screen during questions, so make it work. The end of the talk is the moment people remember. Restate the message, with the caution included. If you need to thank people, do that just before this slide. Then stop. Do not add a new idea in the last thirty seconds.",
    ask="What would stay on screen during questions in your talk?"), fictional=True, source="Teaching recommendation, consistent with Naegle 2021 (professional advice).")
for i, (a, b, c_) in enumerate((("Conference", "Calls were linked to fewer readmissions, but much of the gap may reflect who was reached.", "Test it in a randomised design."),
                                ("Thesis defence", "This thesis shows why reachability must be handled in evaluations of follow-up calls.", "Next: a design that removes it."),
                                ("Hospital briefing", "We recommend a six-month staggered trial on two wards.", "Decision needed today."))):
    bx = LEFT + i * 304
    box(s, bx, 110, 284, 50, a, fill=NAVY, color=WHITE, size=18, bold=True, align="c")
    box(s, bx, 160, 284, 210, [b, {"t": c_, "bold": True, "color": DEEP}], fill=MIST, size=18, margin=14, spacing=12)
text(s, LEFT, 388, WIDTH, 60, "Claim, caution, next step. Then stop.", size=22, color=NAVY, align="c")

s = d.s("Draft your storyboard on six cards", 12, N(
    "Ten minutes on Worksheet 3, then two minutes showing your partner. Write only headlines, in full sentences, one per card, and a quick sketch of the evidence. Do not design slides yet. When you have finished, read your headlines in order. They should tell the story with no slides at all. That is the test some communication advisers call the title test.",
    do="Start the timer. At 10 minutes say 'read your headlines aloud to your partner'. Circulate and ask what each slide adds to the argument.",
    watch="Six topics rather than six claims. Too many cards: six is a device for today, not a rule for your talk.",
    basis="The title test is advised by the MIT Biological Engineering Communication Lab."))
activity_bar(s, 12, "Worksheet 3. Storyboard (10), then read your headlines to a partner (2).")
for i, lab_ in enumerate(("1  Problem and question", "2  What we did", "3  Main finding", "4  Limit or second finding", "5  What it means", "6  Conclusion or recommendation")):
    bx, by = LEFT + (i % 3) * 304, 146 + (i // 3) * 112
    box(s, bx, by, 284, 100, lab_, fill=WHITE, line=TEAL, size=17, color=NAVY, margin=12, weight=1.25, anchor="top")
text(s, LEFT, 374, WIDTH, 74, ["Write each headline as a full sentence. Sketch the evidence below it.", "**Title test:** read the headlines in order. Do they tell the story alone?"], size=17, spacing=6)

# ------------------------------------------------------------------ Break
d.set_block(B[4])
s = d.s("Break: 12 minutes", 12, N("Twelve minutes. Stretch, have a drink, and ignore your email. Restart on time, because the rehearsal needs every minute.",
                                   do="Put a visible countdown on screen. Check the rooms and groups for the rehearsal. Note any changes needed to the groups."))
text(s, LEFT, 180, WIDTH, 80, "Back in 12 minutes", size=44, bold=True, color=TEAL, align="c")
text(s, LEFT, 270, WIDTH, 60, "Next: making slides that show your evidence.", size=22, color=INK, align="c")

# ------------------------------------------------------------------ Module 4
d.set_block(B[5])
d.sec("Slide design and data communication", "Module 4: 34 minutes", 0.5, N("Welcome back. Everything in this section is shown on real slides, including some bad ones that we built on purpose."))
s_assertion_evidence(d, 2.5, N(
    "This is the approach used in this deck. The headline is a sentence that makes the claim. The body is evidence: a chart, diagram or photo. You explain the rest aloud. Be honest about how far the evidence goes. In one randomised experiment with 110 engineering students, the assertion-evidence version of a recorded eight-minute talk gave better comprehension and recall, and less reported effort, than topic headlines with bullets. But that study changed several things at once, used one recorded talk, and was run by the method's advocate. A critic argues the comparison slides were weak. No study we found tests sentence headlines alone. So treat this as a strong default. Also, the old advice that text on slides always harms learning is not what the research says. In Mayer and Moreno's review, with no competing animation, narration plus text did better than narration alone.",
    ask="When would a topic heading be fine? Expected: agenda slides, or section dividers.",
    basis="Research finding: Garner and Alley 2013. Descriptive: Garner et al. 2009, which found about 80% of slides used phrase headlines. Critique: Farkas 2010. Review: Mayer and Moreno 2003. Learning studies do not automatically transfer to research talks."))
s_numeric_rules(d, 1.5, N(
    "You will hear these rules quoted as facts. We looked, and we did not find an experiment that sets any of these numbers. That does not prove none exists, but they are not findings. Bourne says more than one visual a minute is too many, as a personal rule of thumb. Naegle says a minute or less per slide. The experiment we just discussed used about 1.4 slides a minute and got good results, though rate was not what it tested. Published font advice runs from Microsoft's 18 point to 32 point for audiences with print impairment. Legibility depends on the size of the letters at the eye, so it depends on the screen and the distance. WCAG's 18 point defines 'large text' for contrast; it is not a font minimum. The practical test is to stand at the back of the actual room.",
    watch="People who want a number. Offer this: start with 24 points or more for body text as a house habit if you need one, then test in the room. Be clear that it is our choice, not a finding.",
    basis="Professional advice: Bourne 2007, Naegle 2021, Microsoft, Penn State instruction set, WBU summary, W3C Making Events Accessible. Review: Legge and Bigelow 2011 on angular size."))
s_readable(d, 1.5, N(
    "Contrast is one thing you can actually measure. These ratios are calculated from the colours on screen. The WCAG standard is written for the web, and W3C's guidance for non-web documents treats the same ratios as applicable to files such as slides, without requiring compliance. Our brand's mid-grey fails on white for small text, so we use a darker grey. A ratio on your laptop does not guarantee a good result on a washed-out projector in a bright room. Check the actual room. In lit rooms, dark text on a light background tends to work. In dark rooms, the reverse may work better.",
    do="Point to the mid-grey line as an honest example from our own brand palette.",
    basis="Standard: WCAG 2.2 SC 1.4.3, Understanding page. WCAG2ICT note (informative). W3C Making Events Accessible."))
s_chart_choice(d, 1, N(
    "Start from your question, not from the software's menu. Groups: bars from zero, or dots with intervals. Time: lines. Spread: show the individual points where you have few. Relationships: scatter. Shares: ordered bars usually beat a pie, because in perception experiments people judged position better than length, and length better than angle and area. Those experiments were about judging proportions online, so this is a guide, not a law.",
    basis="Research finding: Heer and Bostock 2010 replicating Cleveland and McGill 1984. Weissgerber 2015 on bar charts hiding the data. Guidance: Wilke 2019."))
s_figure_five(d, 1, N(
    "Five questions that every data figure must answer. What are the axes? What are the units? Out of how many? What do the bars mean? Where do the data come from? 'Error bars' could be standard deviation, standard error or a confidence interval, and the audience cannot guess which. Say it, and label it.",
    ask="Which of these five is most often missing in your field?"))
s_mislead(d, 1.5, N(
    "Same data, two charts. On the left the axis starts at 14, so one bar looks about twelve times the height of the other. On the right it starts at zero, and the true proportion is visible. Experiments confirm that truncated bars make differences seem larger, even when people can read the values correctly. Note the nuance. Correll and colleagues reject a blanket rule that every chart must start at zero. Bars must, because you read their length. Dots and lines use position, so a narrower range can be right when a small change is meaningful, such as body temperature. Label the range clearly.",
    ask="When would you not start at zero? Expected: temperature, or a narrow clinical range where small changes matter.",
    basis="Research finding: Pandey et al. 2015, Correll et al. 2020, both online samples. Guidance: Wilke 2019."))

ba_notes = [
    (0.5, "Before. What would you do to this slide? Everything is here and nothing stands out. The audience reads ahead of you. All the numbers are correct.",
     1, "After. The headline says what the slide means. The chart carries the main result, the interval plot shows the narrowing, and the confounder is stated. All the numbers on the old slide are still available: two in the chart, the rest in your speech or your notes. Fewer words, and the caution stayed."),
    (0.5, "Before. A complete methods list, written for a reader. The audience cannot see how the numbers relate.",
     1, "After. The flow diagram gives the denominators and the design at a glance, and the box says why it matters. Statistical detail moved to a backup slide, where a thesis committee can ask for it."),
    (0.5, "Before. Three problems. A truncated axis, 3-D perspective that makes values hard to read, and a headline that claims cause. There are no units or denominators.",
     0.5, "After. The dot and interval show the size and the uncertainty honestly. The headline is less exciting, and it is true. It is still a clear claim."),
    (0.5, "Before. About one man in twelve in some populations has a red-green colour vision difference, and the prevalence varies. Red and green with a legend is the classic failure. 'Group 1' and 'Group 2' also force the audience to look away to decode the chart.",
     0.5, "After. The colours come from the Okabe and Ito palette, and they differ in lightness. Marker shapes differ too, and labels sit on the lines. Colour is no longer the only signal. Turn the slide to greyscale and it still works. The headline also makes the claim and its limit."),
    (0.5, "Before. This could be the end of any talk on any subject. 'Further research is needed' tells a manager nothing.",
     1, "After. For a management audience: what we know, what it costs, what we do not know, and the decision needed. It stays up during discussion. The cost figure is simple arithmetic from the fictional case and should be replaced with real costs in practice."),
]
for (bm, bn, am, an), (nm, fb, fa) in zip(ba_notes, BA_PAIRS[:5]):
    fb(d, bm, N(bn))
    fa(d, am, N(an, basis="Worked example by neu-data."))

s = d.s("Critique the next slide, then redesign it", 1, N(
    "The next slide is yours to fix. Critique it in pairs for three minutes using the five figure questions and the headline test. Then redesign it alone for nine minutes, on paper or in the exercise file. Write the headline first. You do not need artistic skill. A sketch with a clear claim beats a polished slide without one. If you have your own slide, redesign that instead.",
    do="Hand out Worksheet 4 and share Slide_Redesign_Exercise.pptx if people have laptops. Show the next slide during the exercise."))
activity_bar(s, 13, "Worksheet 4. Critique in pairs (3), redesign alone (9).")
for i, (a, b) in enumerate((("Critique, 3 minutes", ["What is the claim?", "What is the evidence?", "What would a colour-blind viewer lose?", "What does 'NS' hide?"]),
                            ("Redesign, 9 minutes", ["Write the headline as a sentence", "Choose one visual for the evidence", "Keep the denominators", "Keep the uncertainty"]))):
    text(s, LEFT + i * 456, 150, 436, 26, a, size=20, bold=True, color=NAVY)
    text(s, LEFT + i * 456, 186, 436, 240, b, size=19, spacing=11)
text(s, LEFT, 410, WIDTH, 40, "Paper is fine. A clear sketch beats a polished slide with no claim.", size=18, color=GREY)
BA_PAIRS[5][1](d, 12, N("Leave this on screen during the exercise. Problems to look for: a topic title, a table with no message, colour as the only signal with green and red, 'NS' instead of intervals, 'no effect' reasoning, and an unexplained conflict with the overall result.",
                        do="Circulate. Ask each person: what is your claim? Warn at 3 minutes to move from critique to redesign. Warn again with 2 minutes left."))
BA_PAIRS[5][2](d, 5, N(
    f"Debrief for five minutes. Ask two volunteers to show their sketches, starting with the headline. Then show this model. The stratum-specific differences have wide intervals, and that is why 'NS' misleads: neither stratum alone has much power, and that does not mean no effect in subgroups. The chart keeps denominators and uses shades plus a legend, so colour is not the only signal.",
    ask="Debrief questions: What did you remove first? What did you refuse to remove? What would a colleague at the back of the room still not see?"))

# ------------------------------------------------------------------ Module 5
d.set_block(B[6])
d.sec("Delivery skills", "Module 5: 10 minutes", 0.5, N("Now we say it aloud. Short teaching, then you speak."))
s_four_moves(d, 1.5, N(
    "Most speakers point at a figure and say 'as you can see'. The audience often cannot see. Use four moves. Say what the figure shows, including the axes. Say where to look. Say what you see there. Say why it matters. This also helps anyone with low vision, because you are describing the visual rather than relying on a pointer.",
    do="Demonstrate on the CareCall interval plot, slowly.",
    basis="Guidance: W3C Making Events Accessible asks speakers to cover information in graphics. Moves are a neu-data teaching recommendation."))
s_clarity(d, 1.5, N(
    "Three terms worth separating. Accent is how your speech differs from what a listener expects. It is not an error, and we never score it. Intelligibility is how much of the message gets through. Comprehensibility is how easy that is for the listener. One small study found that even strong accents did not necessarily reduce either, and the field has moved towards intelligibility as the goal. So work on what you control: pace, pauses, signposts and stress on key words. These help every listener. Speak from understanding: if you know what each slide claims, you can say it in your own words, and you do not need to read a script. Keep brief notes for the path.",
    do="Model a pause after a number.",
    basis="Research finding: Munro and Derwing 1995 (abstract only, small study). Review: Derwing and Munro 2009 (abstract only). Habits are guidance and teaching recommendations."))
s_rehearse(d, 1.5, N(
    "Say it aloud, standing, with the clicker. Time it against the real limit. Silent reading underestimates length. If you run over, cut content rather than speaking faster. Mark your slides now: must keep, should keep, can cut. Then rehearse with a listener. All of this is professional advice. We found no study that sets how much rehearsal is enough. One Penn State guide suggests about five times the talk length, as a rule of thumb. If nerves are a serious problem for you, structured support does exist: a meta-analysis of 30 trials found psychological interventions reduced fear of public speaking, though that is not what a short workshop provides.",
    basis="Advice: Bourne 2007, Naegle 2021, Penn State instruction set. Review: Ebrahimi et al. 2019 (fear, not talk quality)."))
s = d.s("Say your opening and one transition aloud", 5, N(
    "Five minutes in your pairs. Each person has two minutes. Say your opening: the problem and the question. Then say one transition sentence that joins two storyboard cards. For example: 'That is the overall result. But were these patients really alike?' Your partner tells you one thing they remember. Then swap. Transitions are where listeners get lost, so they deserve practice.",
    do="Start the timer. Say 'swap' at 2 minutes 30 seconds. Everyone should be speaking at once, which makes it less exposed."))
activity_bar(s, 5, "Pairs. Each person has 2 minutes, plus 30 seconds to swap.")
for i, (a, b) in enumerate((("Opening", "State the problem and your question, in under 30 seconds."), ("Transition", "Join two storyboard cards with one sentence."), ("Partner", "Say one thing you remember."))):
    box(s, LEFT + i * 304, 150, 284, 180, [{"t": a, "bold": True, "color": NAVY, "size": 20}, b], fill=MIST, size=18, margin=14, spacing=8, anchor="top")
box(s, LEFT, 348, WIDTH, 96, "\"That is the overall result. But were these patients really alike?\"", fill=WHITE, line=TEAL, size=22, color=NAVY, align="c")

# ------------------------------------------------------------------ Rehearsal
d.set_block(B[7])
s = d.s("Useful feedback says what happened to you as a listener", 2, N(
    "Two minutes to brief. You will use three prompts. What was the main message, as you understood it? Where did you get lost, or stop following? What one change would help most? Notice what these do not ask: whether the speaker was confident or charming. Feedback about the task helps more than feedback about the person, according to a large review, though most of that evidence comes from schools. Peer assessment improved performance on average in a meta-analysis, with a smaller estimate for university students. It was not studied for talks specifically, so treat today as a reasonable use of a general finding.",
    do="Point to the rubric on Worksheet 6. Form trios. If the group does not divide by three, make one or two groups of four: they use the 4.5-minute round in the facilitator guide.",
    basis="Review: Hattie and Timperley 2007, Double et al. 2020. The rubric is a course feedback tool and is not a validated instrument."),
    source="Review: Hattie & Timperley 2007, Double et al. 2020. Both extrapolated to adult talks.")
for i, (a, b) in enumerate((("What was the main message?", "Say it back in your own words."), ("Where did you stop following?", "Name the moment, the term or the number."), ("What one change would help most?", "Choose one. Make it specific."))):
    box(s, LEFT, 104 + i * 90, WIDTH, 80, f"**{a}**  {b}", fill=MIST, size=20, margin=18)
box(s, LEFT, 378, WIDTH, 72, "Off limits: accent, looks, personality, or \"you should be more confident\".", fill=AMBER_BG, size=20, margin=18, color=AMBER, bold=True)

s = d.s("Each trio has three rounds of exactly six minutes", 18, N(
    "Three rounds, six minutes each. The speaker has two minutes to explain their redesigned slide or one figure, using the four moves. The timekeeper stops them at two minutes, even mid-sentence. Then one minute of silent writing on the feedback sheet. Then two minutes of spoken feedback using the three prompts. In the last minute the speaker repeats their weakest part, once. Then rotate. The roles are speaker, timekeeper and listener; the timekeeper also gives feedback.",
    do="Start a global timer and call the changes loudly, or display the bar. Move round the room listening. Protect the two-minute limit: stopping on time is the skill being practised. Do not join in the rounds.",
    watch="Feedback drifting towards personality or accent: redirect to the prompts. Speakers apologising: say the time is theirs. Groups running ahead: ask for one more question."))
activity_bar(s, 18, "Trios. Three rounds. Use the rehearsal checklist and Worksheet 5.")
pieces = [("Speak", 2, DEEP), ("Write", 1, MID), ("Discuss", 2, BLUE), ("Redo", 1, NAVY)]
x = LEFT
for a, m, col in pieces:
    w = WIDTH * m / 6
    box(s, x, 146, w - 3, 92, [{"t": a, "bold": True, "size": 22}, f"{m} min"], fill=col, color=WHITE, align="c", size=17, margin=4)
    x += w
text(s, LEFT, 256, WIDTH, 124, ["**Speak:** explain your redesigned slide with the four moves. The timekeeper stops you at 2:00.", "**Write:** both listeners complete the feedback prompts in silence.",
                                "**Discuss:** message, where they stopped following, one change.", "**Redo:** repeat your weakest part once."], size=17, spacing=6)
text(s, LEFT, 410, WIDTH, 40, "Then rotate speaker, timekeeper and listener.", size=19, color=NAVY)
s = d.s("What changed between your first attempt and your redo?", 2, N(
    "Two minutes as a whole group. Take two or three contributions. Keep them about the method. What did you change in the redo? What surprised you about your partner's account of your message? Then move straight on.",
    ask="Debrief questions: Where did the two minutes go? What did you hear that your slide did not show? What will you cut?",
    do="Note any common confusion for the closing."))
text(s, LEFT, 160, WIDTH, 200, ["Where did your two minutes go?", "What did a listener hear differently from what you meant?", "What will you cut first?"], size=26, color=NAVY, spacing=22, align="c")

# ------------------------------------------------------------------ Q and A
d.set_block(B[8])
s_questions(d, 3, N(
    "Questions are part of the talk. Four steps: listen to the end of the question, repeat or rephrase it, answer briefly, then check it landed. Repeating helps everyone hear, helps you check, and gives you time to think, which is especially useful in a second language. Then handle each type differently. For a critical question, find the valid part and answer that. Do not argue. For an unclear one, ask what they mean. If it is out of scope, say so and offer a route. If you do not know, say so plainly and offer to follow up. A bluff costs more than an honest 'I do not know'.",
    do="Demonstrate the four steps once with a co-facilitator or a volunteer.",
    basis="Guidance and teaching resources: Streeter and Miller 2011, Dunphy 2007, Northern Illinois University, University of Waterloo, W3C Making Events Accessible. Experience-based, not tested."))
s = d.s("Practise three kinds of question in three-minute rounds", 9, N(
    "Stay in your trios. Three rounds, three minutes each. The speaker gives their main message in one sentence. A partner reads a card from Worksheet 7: critical, unclear or out of scope. You may write your own in a similar style. The speaker gets one minute to answer with the four steps. The two listeners then give one minute of feedback: was the question answered, and was the uncertainty honest? Rotate, and try a different question type in each round.",
    do="Call time every three minutes. If people finish early they should try the 'I do not know' card.",
    watch="Speakers who fill silence with long answers: they should stop at one minute. Questioners who are aggressive: this is practice, so keep questions fair."))
activity_bar(s, 9, "Trios. Three rounds of 3 minutes. Question cards on Worksheet 7.")
for i, (a, b) in enumerate((("Question", "30 seconds: a partner reads a card."), ("Answer", "60 seconds: listen, repeat, answer, check."), ("Feedback", "90 seconds: was it answered? Was the uncertainty honest?"))):
    box(s, LEFT + i * 304, 150, 284, 150, [{"t": a, "bold": True, "color": NAVY, "size": 20}, b], fill=MIST, size=18, margin=14, spacing=8, anchor="top")
text(s, LEFT, 320, WIDTH, 130, [{"t": "Useful phrases", "bold": True, "color": NAVY, "size": 18}, "\"Let me check I understood: you are asking about...\"", "\"I do not know. The data cannot answer that.\"", "\"That is outside this study. I can follow up afterwards.\""], size=17, spacing=5)

# ------------------------------------------------------------------ Module 6
d.set_block(B[9])
d.sec("Accuracy and responsible use", "Module 6: 7 minutes", 0.5, N("Last module, brief and important: simplifying without distorting, giving credit, keeping confidences, and using AI carefully."))
s = d.s("Simplify the words, and keep the claim the same size", 1, N(
    "When you simplify, words may change. Four things may not: the size, the population, the direction and the certainty. A study of 462 university press releases found about a third made stronger causal claims than the journal article they described, and when releases exaggerated, news stories were much more likely to do so as well. The study is observational, and it was one country and year. But it reminds us that exaggeration often begins with us. Before your next talk, read your slide and the original table side by side.",
    ask="If a communications officer wrote your press release, who is responsible for it? Expected: you approve it, so you share responsibility.",
    basis="Research finding: Sumner et al. 2014, retrospective observational study, correlational."),
    source="Research finding: Sumner et al. 2014 (observational, UK, 2011).", fictional=True)
rows = [["Check", "Original", "Over-simplified", "Honest and simple"],
        ["Size", f"{F['rd']} points lower", "Far fewer", f"About 7 fewer in every 100"],
        ["Population", "Adults, medical wards", "All patients", "Adults on medical wards"],
        ["Direction of claim", "Associated with", "Calls cut readmissions", "Patients with a call came back less often"],
        ["Certainty", f"{F['adj_lo']} fewer to {F['adj_hi']} more", "Proven", "We cannot yet rule out no benefit"]]
table(s, LEFT, 102, WIDTH, rows, [18, 24, 22, 36], row_h=76, size=16, bold_first=True, name="Simplification check")
s = d.s("Credit the people, and protect the people in your data", 1.5, N(
    "Two duties. Credit: name collaborators and data sources, cite figures you did not make, and get permission for anyone you acknowledge, because naming a person can imply endorsement. Authorship has criteria; in medical journals, those of ICMJE. Confidentiality, particularly in hospital settings: do not show names, initials, hospital numbers or dates that identify people. Removing a name is often not enough. A rare case on a small ward can identify someone, and small numbers in a table can expose a patient or a single clinician. Thresholds differ between organisations, so ask yours. And be careful with vocabulary: data with codes in place of names are generally pseudonymised, not anonymous.",
    ask="A slide says 'the 94-year-old readmitted on Ward 7 in March'. What is the problem? Expected: age, place and date together may identify the patient.",
    basis="Policy: ICMJE 2026 sections II.A and II.E. HHS de-identification guidance (US law, no small-cell rule). GDPR Recital 26. Guidance: Public Health Scotland disclosure protocol v2.2, one agency's thresholds."),
    source="Policy: ICMJE; HHS de-identification guidance (US); GDPR Recital 26 (EU). Guidance: Public Health Scotland protocol.")
text(s, LEFT, 102, 436, 26, "Credit", size=20, bold=True, color=DEEP)
text(s, LEFT, 136, 436, 300, ["Cite figures and data you did not make", "Name collaborators and their roles", "Ask before you acknowledge someone", "Use your field's authorship criteria"], size=18, spacing=12)
text(s, 490, 102, 436, 26, "Confidentiality", size=20, bold=True, color=DEEP)
text(s, 490, 136, 436, 200, ["No names, initials or record numbers", "Rare case + ward + date can identify", "Small cells can expose a patient or clinician", "Coded data are usually not anonymous"], size=18, spacing=12)
box(s, LEFT, 356, WIDTH, 80, "Find your organisation's rule. Thresholds differ, and legal rules differ by country.", fill=MIST, size=17, margin=14)
s_ai(d, 1, N(
    "Used carefully, AI tools can help you tighten your own sentences, find phrases that are hard to say aloud, and suggest likely questions. You then verify everything. An audit of 2023 models found many fabricated references, which shows the failure mode, though current rates will differ. A 2025 study found most language models widened claims when summarising science, and asking for accuracy did not help. Authors remain responsible. AI tools cannot be authors. Disclosure is required by many journals, and ICMJE and COPE differ on where, so check your target journal. Do not paste confidential data into tools your organisation has not approved.",
    basis="Research finding: Walters and Wilder 2023, Peters and Chin-Yee 2025, both of which will age. Policy: ICMJE 2026, COPE 2023."))
s = d.s("Check your own slide against your source", 3, N(
    "Three minutes alone. Take your redesigned slide. Compare it with your source, or with the worksheet facts. Tick each item. Fix anything that fails. If you find nothing to fix, swap with a neighbour.",
    do="Start the timer. This is quiet work, and it is a good moment to look at the room."))
activity_bar(s, 3, "Alone. Tick each item on your redesigned slide.")
items = ["Every number matches the source table", "Denominators and units are shown", "Uncertainty is shown", "The verb fits the design", "Headline is no stronger than the data", "No identifiable person", "Sources and collaborators credited", "AI use disclosed, if required"]
for i, it in enumerate(items):
    bx, by = LEFT + (i % 2) * 456, 150 + (i // 2) * 74
    box(s, bx, by + 8, 26, 26, fill=WHITE, line=TEAL, weight=1.5, name="Tick box")
    text(s, bx + 40, by, 390, 44, it, size=19, anchor="middle")

# ------------------------------------------------------------------ Close
d.set_block(B[10])
s = d.s("Choose one revision, and book one rehearsal", 5, N(
    "Five minutes. Write on the back page of your workbook: the one thing you will revise first, and the date of a rehearsal with a real listener. Then complete the course feedback form. You came with a subject you know. You leave with a clear message, a revised paragraph, a storyboard, a redesigned slide and a rehearsed explanation. That is a start. Remember that this was an introduction, and that the rubric is a tool for feedback, not a test.",
    do="Collect feedback forms. Point to the references and the source map. Thank the group. Show the closing slide.",
    ask="One volunteer: what will you do differently in your next talk?"))
for i, (a, b) in enumerate((("One revision", "What will you change first?"), ("One rehearsal", "With whom, and on what date?"), ("One check", "Which claim will you verify?"))):
    box(s, LEFT + i * 304, 112, 284, 170, [{"t": a, "bold": True, "color": DEEP, "size": 24}, b], fill=MIST, size=19, margin=16, spacing=10, align="c")
text(s, LEFT, 306, WIDTH, 120, ["Write them on your personal plan in the workbook, then complete the course feedback form.", "Keep the rubric, rehearsal checklist and references for your next talk."], size=20, color=NAVY, spacing=10)
d.closing(N("Closing slide. Leave the message slide or this slide on screen as people leave.", do="Note that the copyright notice is the Neudata standard for this template."))

# ------------------------------------------------------------------ Backup
d.set_block("Backup")
s = d.s("Backup: the feedback rubric at a glance", 0, N("Use this slide if a participant asks what 'good' means. The full anchored rubric is on Worksheet 6. It is a course feedback tool, not a validated instrument."))
rows = [["Criterion", "1 Not yet", "2 Developing", "3 Secure"],
        ["Message", "No clear claim", "Claim present, drifts", "One claim, listener repeats it"],
        ["Structure", "List of topics", "One gap in the chain", "Question to implication connects"],
        ["Writing", "Vague or overstated", "Clear in most places", "Clear, no stronger than evidence"],
        ["Evidence", "Numbers without context", "Most context given", "Size, denominator, uncertainty"],
        ["Visual clarity", "Hard to read", "Readable, cluttered", "Readable, claim visible"],
        ["Timing", "Over by more than a quarter", "Rushed ending", "Within the limit, even pace"],
        ["Questions", "Bluffs or argues", "Partly answers", "Answers, states limits"]]
table(s, LEFT, 98, WIDTH, rows, [18, 26, 26, 30], row_h=44, size=14, bold_first=True, name="Rubric summary")
s = d.s("Backup: how the CareCall numbers were calculated", 0, N(
    "For anyone who asks. Risks are events divided by patients. Differences use Wald 95% intervals. The stratified estimate is a Mantel-Haenszel risk difference across the two discharge-risk strata, with the Greenland-Robins variance. The classroom interval uses a pooled two-sample approach with 22 degrees of freedom. All numbers are recalculated by scripts/check_numbers.py in the course repository."), fictional=True)
rows = [["Quantity", "Calculation", "Result"],
        ["Risk with a call", f"{F['call_ev']} / {F['call_n']}", f"{F['call_pct']}%"],
        ["Risk with no call", f"{F['usual_ev']} / {F['usual_n']}", f"{F['usual_pct']}%"],
        ["Crude difference", "Wald 95% CI", f"{F['rd']} lower ({F['rd_hi']} to {F['rd_lo']})"],
        ["Within risk groups", "Mantel-Haenszel, Greenland-Robins variance", f"{F['adj']} lower ({F['adj_lo']} lower to {F['adj_hi']} higher)"],
        ["Emergency visits", f"{F['ed_call_ev']}/{F['call_n']} v {F['ed_usual_ev']}/{F['usual_n']}", f"{F['ed_rd']} lower ({F['ed_lo']} lower to {F['ed_hi']} higher)"],
        ["Nurse hours", f"{F['call_n']} calls x {F['mins']} min / 60", f"About {F['call_hours']} hours"]]
table(s, LEFT, 100, WIDTH, rows, [24, 40, 36], row_h=48, size=15, bold_first=True, name="Calculations")
s = d.s("Backup: where the guidance in this workshop comes from", 0, N(
    "The full reference list and source-to-content map are in the course folder. Each source is labelled by type, so you can see which claims are research findings and which are professional advice or our own teaching recommendations."))
rows = [["Type", "Examples", "How to read it"],
        ["Research finding", "Garner & Alley 2013; Akl 2011; Pandey 2015; Sumner 2014", "One study or review. Check its setting and limits."],
        ["Review or consensus", "Altman & Bland 1995; ASA 2016; Greenland 2016", "Expert summary, usually reliable on principle."],
        ["Standard or policy", "WCAG 2.2; ICMJE 2026; COPE; institutional defence rules", "Binding only where it applies."],
        ["Professional guidance", "Bourne 2007; Naegle 2021; SAMPL; CDC Index", "Experience-based. Useful, not proven."],
        ["Our recommendation", "Chain, cut list, four moves, rubric", "Teaching devices, labelled as ours."]]
table(s, LEFT, 100, WIDTH, rows, [22, 44, 34], row_h=58, size=15, bold_first=True, name="Evidence types")

d.save(OUT)
import json
json.dump({"first_slide": d.first_slide, "total": len(d.p.slides._sldIdLst)}, open(Path(__file__).parent / "_workshop_slides.json", "w"))
for st, en, title, mins, *_ in c.clock(c.WORKSHOP):
    got = d.minutes.get(title, 0)
    assert abs(got - mins) < 1e-6, (title, got, mins)
print("workshop slides:", len(d.p.slides._sldIdLst), "minutes", sum(v for k, v in d.minutes.items()))
