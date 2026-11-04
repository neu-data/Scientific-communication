"""Builds the one-hour talk deck. A standalone subset of the workshop content."""
from pathlib import Path

import course as c
import examples as ex
from slides_lib import *

OUT = Path(__file__).parents[1] / "materials" / "talk_1h" / "Scientific_Communication_Talk_1h.pptx"
d = D()
B = [b[0] for b in c.TALK]

d.set_block(B[0])
d._tick(0.5)
d.title_slide("Clear Claims, Clear Slides, Clear Delivery", "Scientific communication in one hour\nA talk with audience activity and questions", "Version 1.0, November 2026",
              timed(0.5, N("Welcome. In the next hour I will show you how to decide what to say, how to say it without overstating your evidence, how to show it on a slide, and how to deliver it and handle questions. You will do one short exercise with your neighbour, and we will leave time for your questions.",
                           do="This is a standalone talk. It needs no workbook. A one-page handout (the rehearsal checklist) is optional.")))
s = d.s("The same fictional result can inform or mislead, depending on how it is told", 3, N(
    f"Here is one finding, told three ways. The numbers come from a fictional case I will use throughout, CareCall, about nurse phone calls after hospital discharge. The first version is a topic: it says nothing. The second is exciting and wrong: it claims cause and gives only a relative figure. The third says what was found and how far to trust it. It is less dramatic, and it is the one you could defend. That is the whole talk in one slide. Everything else is how to get to the third version.",
    ask="Which would you trust as a reader? Which would you rather write? Take a show of hands.",
    watch="Make clear from the start that CareCall is fictional."), fictional=True)
for i, (a, b, col, fl) in enumerate((("Says nothing", ex.HEADLINE_WEAK, GREY, MIST), ("Overstates", "Calls slash readmissions by a third", AMBER, AMBER_BG), ("Informs", ex.HEADLINE, DEEP, MIST))):
    text(s, LEFT, 104 + i * 118, 170, 104, a, size=19, bold=True, color=col, anchor="middle")
    box(s, 210, 104 + i * 118, 716, 104, b, fill=fl, size=23, margin=18, color=NAVY)
s = d.s("One hour, four decisions", 1.5, N(
    "Four decisions, in this order. Decide your audience and your message. Make claims that match your evidence. Show the evidence on slides. Deliver it, rehearse it and answer questions. You will practise one small piece, a headline, around the middle. This is an introduction. If you want to practise with feedback, the three-hour workshop does that.",
    do="Keep this brisk."))
items = [("Decide", "Who is it for, and what is your message?"), ("Claim", "Does your wording match your evidence?"), ("Show", "Does each slide make its point?"), ("Deliver", "Can you say it in time and answer honestly?")]
w = 208
for i, (a, b) in enumerate(items):
    x = LEFT + i * (w + 20)
    box(s, x, 130, w, 60, a, fill=DEEP, color=WHITE, size=22, bold=True, align="c", margin=4)
    box(s, x, 190, w, 150, b, fill=MIST, size=19, margin=14)
    if i < 3:
        rule(s, x + w + 1, 160, x + w + 19, 160, color=TEAL, weight=2.5, arrow=True)
text(s, LEFT, 366, WIDTH, 70, f"Fictional case throughout: nurse calls after discharge, {F['total_n']} patients, calls not randomised.", size=19, color=NAVY)

d.set_block(B[1])
s_audience_chain(d, 3.5, N(
    "Most weak talks fail before the first slide. Work left to right. Who is in the room, what do they know, what do they need, and what should change afterwards? Then write one sentence. Researchers: this is the sentence you want people to repeat in the coffee queue. Students: the examiner's question is whether the work is yours and sound. Professionals: what should the person with the budget do on Monday?",
    ask="Think of your next talk. Who matters most in that room? What should they do afterwards? Ten seconds of silence.",
    basis="Advice: Bourne 2007. The CDC Clear Communication Index asks for audience, objective and main message, but is built for public health materials. The chain is a neu-data teaching recommendation."))
s_topic_message(d, 3, N(
    "A topic names an area. A message makes a claim someone could challenge. Use these three checks on your own sentence. Notice the caution inside the message: 'linked to', and 'not yet justify'. A good message carries its own limit.",
    ask="Is 'Barriers to antibiotic stewardship' a topic or a message? Expected: a topic."))
s_three_rooms(d, 3.5, N(
    f"Same data, three rooms. A conference wants a new idea. A thesis committee wants to see your contribution and your reasoning. Management wants a decision, so the recommendation comes first. The evidence does not change, and neither does the uncertainty: even the management message says the benefit could be {F['adj_lo']} fewer to {F['adj_hi']} more per hundred. Thesis formats differ widely, from a private viva to a public defence with an opponent, so always check your own regulations.",
    ask="Which room is yours?",
    basis="Institutional examples in the workshop: Imperial College, UCLA Neuroscience, Halmstad University."))

d.set_block(B[2])
s_denominators(d, 2, N(
    f"Claims first need the right numbers. On the left, Hospital A has {F['hosp_a_ev']} readmissions and Hospital B {F['hosp_b_ev']}. On the right, as rates, the picture reverses: {F['hosp_a_pct']} per hundred against {F['hosp_b_pct']}. Always give the numerator and denominator.",
    basis="Reporting guidance: SAMPL."))
s_size_uncertainty(d, 3, N(
    f"Three ways to state one result. {F['rrr']} percent sounds large. A Cochrane review found that relative figures look bigger and persuade more than absolute ones, with no difference in understanding, so do not give the relative figure alone. {F['rd']} per hundred gives the size. {F['rd_hi']} to {F['rd_lo']} gives the uncertainty. And see what happens when we compare like with like within risk groups: now the interval crosses zero. An experiment with UK public audiences found that a numeric range cost little trust, and vague verbal uncertainty cost more. That was not a clinical audience, so treat it as a pointer.",
    basis="Research finding: Akl et al. 2011, van der Bles et al. 2020. Guidance: SAMPL, STROBE."))
s_verbs(d, 2.5, N(
    "Match the verb to the design. CareCall is observational, so 'associated with' fits and 'prevented' does not. Even a trial supports 'reduced, in this population', and does not support 'proves'. Be aware that the word 'association' is no shield: many readers still hear a causal claim. State the design and the main alternative explanation.",
    basis="Research finding: Haber 2018, 2022. Commentary: Hernan 2018. Ladder: neu-data teaching recommendation."))
s_non_significant(d, 2.5, N(
    f"Two results that missed the usual threshold. Neither shows no effect. Emergency visits: {F['ed_rd']} fewer per hundred, and the data fit {F['ed_lo']} fewer to {F['ed_hi']} more. Classrooms: {F['roof_diff']} degrees cooler, and the data fit {F['roof_lo']} cooler to {F['roof_hi']} warmer. Say what the study can and cannot tell us. Absence of evidence is not evidence of absence.",
    basis="Review: Altman and Bland 1995, Greenland et al. 2016, ASA statement 2016."))

d.set_block(B[3])
s = d.s("Your turn: fix these three headlines", 5, N(
    "Seven minutes in all, starting now. Two minutes alone: choose one headline and rewrite it as an honest full sentence. Three minutes with your neighbour: compare, and improve one. Use the facts at the bottom of the slide. In a large room people can do this in the row. Online, they can type into chat. Then I will take a few and show three models.",
    do="Start a visible timer. Call 'talk to your neighbour' at 2 minutes. In a room of 100 or more, take examples from the front rows or use a poll.",
    watch="Headlines that drop the caution. Ask: is it still true for an observational study?"), fictional=True)
activity_bar(s, 5, "Alone (2), then with a neighbour (3).")
y = 146
for a, b in ex.HEADLINE_TASK:
    box(s, LEFT, y, 440, 62, f"\"{a}\"", fill=AMBER_BG, size=18, margin=12, color=INK, bold=True)
    box(s, LEFT + 440, y, WIDTH - 440, 62, b, fill=WHITE, line=LINE, size=16, margin=12)
    y += 70
text(s, LEFT, 362, WIDTH, 90, [f"**Facts:** readmissions {F['call_ev']} of {F['call_n']} ({F['call_pct']}%) with a call, {F['usual_ev']} of {F['usual_n']} ({F['usual_pct']}%) without. Not randomised.",
                               f"Emergency visits {F['ed_call_pct']}% and {F['ed_usual_pct']}%, difference {F['ed_rd']} fewer per 100 ({F['ed_lo']} fewer to {F['ed_hi']} more)."], size=17, spacing=6)
s = d.s("A good headline is a sentence, gives the size and keeps the caution", 2, N(
    "Two minutes. Take two or three from the room. Then show these. There are many good answers. Each has a verb, gives the size or the limit, and is no stronger than the evidence.",
    ask="What did you find hardest to keep?"), fictional=True, source="Model answers: neu-data. Other good versions exist.")
y = 106
for (weak, _), model in zip(ex.HEADLINE_TASK, ex.HEADLINE_MODELS):
    text(s, LEFT, y, WIDTH, 26, f"Instead of \"{weak}\"", size=16, color=AMBER, bold=True)
    box(s, LEFT, y + 28, WIDTH, 68, model, fill=MIST, size=20, margin=14, color=NAVY, bold=True)
    y += 116

d.set_block(B[4])
s_assertion_evidence(d, 2.5, N(
    "A slide has one job: to support what you are saying. This approach uses a sentence headline with visual evidence, and you explain the rest. In one randomised experiment with 110 engineering students, a recorded talk built this way gave better comprehension and recall than topic headlines with bullets. But that study changed several things at once, and critics say the comparison slides were weak. So treat it as a strong default, and do not read it as proof that all text is bad. Mayer and Moreno's review found that with no competing animation, narration with text did better than narration alone.",
    basis="Research finding: Garner and Alley 2013. Critique: Farkas 2010. Review: Mayer and Moreno 2003."))
s_numeric_rules(d, 1.5, N(
    "You will hear these quoted as facts. We searched and did not find an experiment that sets any of these numbers. Bourne's limit is a personal rule of thumb. Published font advice ranges from 18 to 32 points. Legibility depends on letter size at the eye, so it depends on the screen and the distance. The honest test is to stand at the back of the actual room.",
    basis="Professional advice: Bourne 2007, Naegle 2021, Microsoft, WBU summary, W3C. Review: Legge and Bigelow 2011."))
BA_PAIRS[0][1](d, 0.5, N("Before. Every number is correct, and nothing stands out."))
BA_PAIRS[0][2](d, 1.5, N("After. The headline says what it means. The evidence is on the chart, the caution stayed, and the words dropped sharply. All the numbers are still available, on the chart or in your speech.", basis="Worked example by neu-data."))
s_mislead(d, 2, N(
    "Same numbers. On the left the axis starts at 14, so one bar looks about twelve times as tall. On the right it starts at zero. Experiments show truncated bars make differences seem larger, even when people can read the values. Bars encode length, so they must start at zero. Dots and lines encode position, so a narrower labelled range can be right where small changes matter.",
    basis="Research finding: Pandey et al. 2015, Correll et al. 2020. Both online samples. Guidance: Wilke 2019."))
BA_PAIRS[3][1](d, 0.5, N("Before. Red and green, a legend, and no meaning in 'Group 1'. Colour is the only signal."))
BA_PAIRS[3][2](d, 1, N("After. Colours from the Okabe and Ito palette, different marker shapes, labels on the lines. Colour is no longer the only signal, and the headline states the claim and its limit.", basis="Guidance: Okabe and Ito; standard: WCAG 2.2 SC 1.4.1 (for web content)."))
s_figure_five(d, 2.5, N(
    "Before you show any data figure, check these five. What are the axes? What are the units? Out of how many? What do the bars mean? Where do the data come from? 'Error bars' could mean three different things. Say which.",
    ask="Which of these is most often missing in your field?"))

d.set_block(B[5])
s_four_moves(d, 1.5, N(
    "When you show a figure, avoid 'as you can see'. Use four moves. What it shows. Where to look. What you see. Why it matters. This also helps anyone who cannot see the slide well.",
    do="Demonstrate on one figure.",
    basis="Guidance: W3C Making Events Accessible. Moves: neu-data teaching recommendation."))
s_rehearse(d, 2, N(
    "Say it aloud, with the clicker, against the real limit. If you run over, cut content rather than speaking faster. Mark what you must keep and what you can drop. Then rehearse for a listener and ask where they stopped following. This is professional advice: we found no study that sets how much rehearsal is enough. If you present in English as an additional language, work on pace, pauses and signposting. Accent is not the issue; being understood is. A small study found strong accents did not necessarily reduce how well speech was understood.",
    basis="Advice: Bourne 2007, Naegle 2021. Research finding: Munro and Derwing 1995, abstract only."))
s_questions(d, 2, N(
    "Questions are part of the talk. Listen to the end, repeat, answer briefly, check. Repeating helps everyone hear and gives you thinking time. A critical question: find the valid part. Unclear: ask what they mean. Out of scope: say so and offer a route. Unknown: say so plainly. A bluff costs more than an honest 'I do not know'.",
    basis="Guidance: Streeter and Miller 2011, Dunphy 2007, University of Waterloo."))
s_ai(d, 1.5, N(
    "One last point on accuracy. AI tools can help you edit and rehearse. You verify every fact, reference and claim, and you keep confidential data out of tools your organisation has not approved. In hospitals, removing a name is often not enough: a rare case on a small ward can identify someone. And credit your sources and collaborators.",
    basis="Research finding: Walters and Wilder 2023, Peters and Chin-Yee 2025. Policy: ICMJE 2026, COPE."))

d.set_block(B[6])
s = d.s("Your questions", 7, N(
    "Seven minutes of questions. Use the four steps yourself: this is a live demonstration. If there are no questions, use these: How do I handle a slide my supervisor insists on? What if my data are not significant? How many slides for a ten-minute talk?",
    do="Repeat each question. Keep answers short. Keep an eye on the clock: stop questions at minute 58.",
    watch="If you do not know, say so. The audience will notice that you practised what you taught."))
text(s, LEFT, 150, WIDTH, 80, "What would you like to ask?", size=38, bold=True, color=TEAL, align="c")
text(s, LEFT, 250, WIDTH, 120, ["If it would help to start somewhere:", "A slide your supervisor insists on", "A result that is not significant", "How many slides you really need"], size=20, align="c", spacing=8)
s = d.s("Before your next talk: one sentence, one honest headline, one timed run", 2, N(
    "Close here. Three things to do before your next talk. Write your message in one sentence. Check every headline against your evidence. Run it aloud once against the clock, with a listener. Thank you.",
    do="Leave this slide on screen as people leave. Mention the references and the three-hour workshop."))
for i, (a, b) in enumerate((("One sentence", "Your message, with its caution."), ("One honest headline", "On every slide, no stronger than the data."), ("One timed run", "Aloud, with a listener, against the limit."))):
    box(s, LEFT + i * 304, 120, 284, 220, [{"t": a, "bold": True, "color": DEEP, "size": 24}, b], fill=MIST, size=20, margin=18, spacing=12, align="c")
text(s, LEFT, 372, WIDTH, 60, "References and the three-hour workshop materials are in the course repository.", size=18, color=GREY, align="c")
d.closing(N("Closing slide."))

d.save(OUT)
import json
json.dump({"first_slide": d.first_slide, "total": len(d.p.slides._sldIdLst)}, open(Path(__file__).parent / "_talk_slides.json", "w"))
for st, en, title, mins, *_ in c.clock(c.TALK):
    got = d.minutes.get(title, 0)
    assert abs(got - mins) < 1e-6, (title, got, mins)
print("talk slides:", len(d.p.slides._sldIdLst), sum(d.minutes.values()))
