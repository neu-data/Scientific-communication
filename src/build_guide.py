"""Builds the facilitator guide."""
import json
from pathlib import Path

import casebook as cb
import course as c
import examples as ex
import worksheets as ws
from casebook import facts
from doc_kit import Doc

F = facts()
ROOT = Path(__file__).parents[1] / "materials"
HERE = Path(__file__).parent
W = json.load(open(HERE / "_workshop_slides.json"))
T = json.load(open(HERE / "_talk_slides.json"))


def ranges(info, order):
    fs = info["first_slide"]
    out = {}
    for i, k in enumerate(order):
        start = fs[k]
        end = (fs[order[i + 1]] - 1) if i + 1 < len(order) else (fs.get("Backup", info["total"] + 1) - 1)
        out[k] = f"{start}-{end}" if end > start else str(start)
    return out


WR = ranges(W, [b[0] for b in c.WORKSHOP])
TR = ranges(T, [b[0] for b in c.TALK])


def clock_at(m, start=9 * 60):
    t = start + m
    return f"{t // 60:02d}:{t % 60:02d}"


D = Doc("Facilitator Guide", c.COURSE, f"{c.ORG}  ·  {c.VERSION}", toc=True)

# ------------------------------------------------------------------ 1
D.h1("Using this guide")
D.p("This guide lets a trainer who did not write the course run it. It covers two standalone versions: a three-hour practical workshop for 12 to 24 people and a one-hour talk for any size of audience. Exact timings are in the run sheets. The decks carry speaker notes for every slide, with a suggested script, a question for the room, things to watch for, and the basis for each claim.")
D.key("Keep the promise modest. This is an introduction with guided practice. Participants will leave with four products and some useful habits, and not with mastery of scientific writing or public speaking.")
D.h2("Who it is for")
D.p("Participants know their subject but may struggle to communicate it. They are researchers preparing conference presentations, students preparing thesis defences, and professionals in hospitals and other organisations presenting evidence or recommendations. Many will present in English as an additional language. Examples include health and research settings, and the CoolRoom case gives non-clinical participants a home. No prerequisite statistics are needed beyond the idea of a percentage and a confidence interval. Facilitators should be comfortable explaining those two ideas.")
D.h2("What you must not claim")
D.bullets(["That rules such as one slide per minute, six words per line or a minimum font size are research findings. They are rules of thumb.",
           "That the assertion-evidence approach is proven. One experiment supports a bundle of changes, on a recorded talk, with students.",
           "That the rubric is a validated instrument. It is a course feedback tool, so do not use it to grade people.",
           "That any fictional number is real. CareCall and CoolRoom are invented."])
D.p("Each slide's notes end with a Basis line. If a participant challenges a claim, read that line and refer to References_and_Source_Map.")

# ------------------------------------------------------------------ 2
D.h1("Preparing")
D.h2("Two weeks before")
D.bullets(["Confirm numbers, room and equipment. A flat room with movable chairs suits trios far better than fixed rows.",
           "Check the deck on the real projector if you can. Run the back-of-room test on slides 34 to 38.",
           "Ask for an assistant if the group is above 18.",
           "Send participants this note: \"Please bring one result from your own work, or a paragraph you are writing, with identifiers removed. If you do not have one, we provide fictional cases. Do not bring confidential or identifiable data.\""])
D.h2("On the day")
D.table([["Item", "Quantity", "Used in"],
         ["Workshop deck (PowerPoint, PDF as backup)", "1", "Whole session"],
         ["Participant workbook, or printed Worksheets 1 to 7", "1 each", "Whole session"],
         ["Worksheet 6 rubric and Worksheet 5 rehearsal sheet", "3 spare per trio", "Rehearsal"],
         ["Question cards (Worksheet 7), cut up if you wish", "1 set per trio", "Q&A practice"],
         ["Slide_Redesign_Exercise.pptx", "Shared link", "Module 4"],
         ["Blank paper and pens", "1 each", "Storyboard, redesign"],
         ["Visible countdown timer", "1", "All activities"]], [9, 3, 4.6], size=9.5)
D.h2("Forming groups for 12 to 24 people")
D.p("Pairs work through Modules 1 to 4. Trios work on the rehearsal and Q&A, formed by joining pairs at the break. Mix fields and, if possible, first languages, so that each listener has to rely on clear explanation.")
D.table([["Participants", "Trios", "Groups of four", "Facilitators"],
         ["12", "4", "0", "1"], ["13", "3", "1", "1"], ["14", "2", "2", "1"], ["15", "5", "0", "1"], ["16", "4", "1", "1"], ["17", "3", "2", "1"], ["18", "6", "0", "1"],
         ["19", "5", "1", "1 plus assistant"], ["20", "4", "2", "1 plus assistant"], ["21", "7", "0", "1 plus assistant"], ["22", "6", "1", "1 plus assistant"], ["23", "5", "2", "1 plus assistant"], ["24", "8", "0", "1 plus assistant"]], [3, 3, 4, 5], size=9.5)
D.p("A group of four does not get extra time, so it uses a shorter round: see the rehearsal section.")

# ------------------------------------------------------------------ 3
D.h1("Three-hour workshop run sheet")
D.p("The session totals exactly 180 minutes, including a 12-minute break. Slide numbers refer to the workshop deck. Clock times assume a 09:00 start.")
rows = [["Start", "Elapsed", "Min", "Block", "Slides", "How the time is spent"]]
for st, en, title, mins, kind, what, out, los in c.clock(c.WORKSHOP):
    rows.append([clock_at(st), f"{c.fmt(st)} to {c.fmt(en)}", str(mins), title, WR[title], what])
rows.append(["12:00", "3:00", "180", "**End**", "", ""])
D.table(rows, [1.3, 2.2, 1.3, 5, 1.4, 5.8], size=8.5)
D.p(f"Slides {W['first_slide']['Backup']} to {W['total'] } are backups: the rubric at a glance, how the numbers were calculated, and evidence types. They carry no time allowance.")
D.h2("If you fall behind")
D.p("Protect the rehearsal and Q&A. They are the reason to hold this workshop in person. Cut in this order.")
D.table([["If you are behind by", "Do this", "Saves"],
         ["Up to 5 minutes", "Merge slides 23 and 24, and take only one before-and-after pair in detail in Module 4.", "3 to 5"],
         ["6 to 10 minutes", "Show only pairs 1, 3 and 4 in Module 4, and shorten Module 3 by dropping slide 26. Keep the defence slide if students are present.", "6 to 8"],
         ["More than 10 minutes", "Drop the module-level pair share at the end of Module 3, and reduce Module 6 to the accuracy checklist.", "4 to 5 more"]], [4, 10, 2.6], size=9.5)
D.p("Do not shorten the trio rounds. If you must lose a round, tell groups to run two rounds, and have the third speaker go first in the Q&A practice.")

# ------------------------------------------------------------------ 4
D.h1("Block-by-block instructions")
b = {x[0]: x for x in c.WORKSHOP}


def block(title, purpose, steps, debrief=None, problems=None):
    D.h2(f"{title} ({b[title][1]} minutes, slides {WR[title]})")
    D.p(f"**Purpose.** {purpose}")
    D.table([["Min", "What happens"]] + [[str(a), x] for a, x in steps] + [[str(sum(a for a, _ in steps)), "**Total**"]], [1.2, 15.4], size=9.5)
    assert sum(a for a, _ in steps) == b[title][1], title
    if debrief:
        D.p("**Debrief questions**", keep=True)
        D.bullets(debrief)
    if problems:
        D.p("**Common problems**", keep=True)
        D.bullets(problems)


block("Welcome and working pairs", "Set expectations, make feedback safe and introduce the fictional cases.",
      [(1, "Title slide. Welcome. Timer visible."), (3, "Four products and the schedule bar. Take two answers to 'what would make today useful?'"), (2, "Ground rules. Point out that accent and personality are never assessed, and ask people to remove identifiers."), (2, "Introduce CareCall and CoolRoom. Ask why called patients might differ. Pair people with a neighbour.")],
      problems=["Late arrivals. Pair them with each other rather than waiting.", "Someone has brought real patient data. Ask them to use the fictional case today."])
block("Module 1: Audience, purpose and message", "Each person writes a one-sentence message for a real audience.",
      [(7, "Teach: section slide, audience chain, topic v message, three rooms."), (10, "Worksheet 1, alone. Circulate and ask 'what is the claim?'"), (3, "Pair check. Partner says back what they think they are being asked to do.")],
      debrief=["What did your partner think you wanted?", "What did you have to drop from your sentence?"],
      problems=["Topics in place of claims. Ask for a verb.", "Audience of 'everyone'. Ask who matters most in the room.", "Messages stronger than the evidence. Ask what the data would say to that sentence."])
block("Module 2: Scientific writing", "Each person revises one paragraph so that it says no more than the data allow.",
      [(13, "Teach: paragraph anatomy, three repairs, result v interpretation, denominators, size and uncertainty, verbs, non-significance, worked rewrite, four forms."), (12, "Worksheet 2. Alone for 8, swap and comment for 4."), (5, "Debrief. Two pairs read their opening sentence. Show the model answer.")],
      debrief=["What did you delete first?", "Where did you want a stronger verb than the evidence allows?", "What would you need before claiming the coating works?"],
      problems=["Time. This module is dense. If short, skip the sentence repairs slide, which is in the workbook.", "Participants worried by statistics. Say that you need the ideas of size and range, not the formula.", "Debates over p-values. Keep to the point: report the estimate and interval, and do not read p above 0.05 as no effect."])
block("Module 3: Presentation structure", "Each person drafts a short storyboard built as an argument.",
      [(8, "Teach: one argument, openings, selecting methods, prioritising, three shapes, defences, endings."), (10, "Worksheet 3. Headlines on six cards, with a sketch of the evidence."), (2, "Read headlines to a partner: the title test.")],
      debrief=["Do your headlines tell the story alone?", "Which card would you cut with half the time?"],
      problems=["Students anxious about defence rules. Stress that formats vary, and that they should read their own regulations and ask their supervisor.", "Managers who think this is too academic. Point to the briefing shape, with the recommendation first."])
block("Break", "Rest. Rearrange chairs and form trios.", [(12, "Break. Display the countdown. Check groups and rooms.")])
block("Module 4: Slide design and data communication", "Each person redesigns one slide, with a claim and honest evidence.",
      [(16, "Teach: assertion-evidence and its limits, numeric rules, readability, chart choice, the five questions, misleading charts, five before-and-after pairs."), (1, "Introduce the exercise."), (12, "Critique in pairs for 3, redesign alone for 9. Leave slide 50 on screen."), (5, "Debrief. Two volunteers show sketches. Show the model.")],
      debrief=["What did you remove first?", "What did you refuse to remove?", "What would someone at the back of the room still not see?"],
      problems=["People polishing in PowerPoint. Paper is fine, and the headline comes first.", "Requests for 'the correct font size'. Explain the range and the room test. If pressed, say that 24 points for body text is a reasonable personal habit, not a finding.", "Removing uncertainty to simplify a slide. Ask whether the claim is still true without it."])
block("Module 5: Delivery skills", "Each person says their opening and one transition aloud.",
      [(5, "Teach and demonstrate: four moves, clarity not accent, rehearsal and cutting."), (5, "Pair drill: opening and transition, 2 minutes each, plus 30 seconds to swap, and 30 seconds' spare.")],
      problems=["Reluctance to speak. Everyone speaks at once, which reduces exposure.", "Self-criticism about accent. Repeat that intelligibility and comprehensibility are the goals. Accent is not assessed."])
block("Timed rehearsal in trios", "Each person gives a timed explanation and receives structured feedback.",
      [(2, "Brief: feedback prompts and the rubric. Form trios."), (18, "Three rounds of 6 minutes: speak 2, write 1, discuss 2, redo 1."), (2, "Whole-group debrief.")],
      debrief=["Where did your two minutes go?", "What did a listener hear differently from what you meant?", "What will you cut first?"],
      problems=["Rounds running over. Use one global timer and call each change loudly. Stopping on time is the skill.", "Feedback about confidence or accent. Redirect to the three prompts.", "Silent listeners. The write minute exists so that everyone has something to say."])
D.p("**Groups of four** run four rounds of 4.5 minutes: speak 2, write 0.5, discuss 1.5, redo 0.5. That is 18 minutes, so they finish with the trios.")
block("Question-and-answer practice", "Each person answers one difficult question and says what they do not know.",
      [(3, "Teach and brief: four steps, question types, one demonstration."), (9, "Three rounds of 3 minutes: question 0.5, answer 1, feedback 1.5.")],
      problems=["Long answers. One minute is the limit.", "Unfair questions. Keep it practice: fair, not hostile."])
D.p("**Groups of four** run four rounds of 2.25 minutes: question 0.25, answer 1, feedback 1.")
block("Module 6: Accuracy and responsible use", "Each person checks their slide for accuracy and responsible use.",
      [(4, "Teach: simplify the words and keep the claim, credit and confidentiality, AI."), (3, "Accuracy checklist on the participant's own slide.")],
      problems=["Requests for legal advice. Say that the rules differ by country and organisation, and refer people to their governance office.", "Strong views on AI. Keep to the verifiable points: humans are responsible, verify everything, keep confidential data out of unapproved tools."])
block("Close: revise and commit", "Each person chooses one revision, one rehearsal and one check.",
      [(5, "Personal plan, course feedback form, one volunteer, thanks.")])

# ------------------------------------------------------------------ 5
D.h1("Model answers")
D.h2("Worksheet 1: example for CareCall")
D.table([["Field", "Hospital management"], ["Occasion and limit", "Quality committee, 10 minutes"], ["Who", "Medical director, finance lead, nursing lead. Busy. Mixed statistics knowledge."],
         ["What they know", "Readmissions are a concern. They have not seen these data."], ["What they need", "A decision on funding, with honest risks."], ["What should change", "Approve a staggered trial."], ["Message", ex.ROOMS[2][3]]], [4, 12.6], size=9.5)
D.p("Good answers for the other rooms:", keep=True)
D.bullets([f"Conference: {ex.ROOMS[0][3]}", f"Thesis committee: {ex.ROOMS[1][3]}"])
D.h2("Worksheet 2: model paragraph")
D.key(ex.EXERCISE_MODEL)
D.table([["Text in the exercise", "Problem", "Repair"]] + [list(x) for x in ex.EXERCISE_PROBLEMS], [5.5, 6, 5], size=9.5, caption="The seven problems. Expect participants to find at least five.")
D.p("Accept other versions if they keep the means, the difference, the interval, the number of rooms and the way rooms were chosen, and if they make no claim about exam results.")
D.h2("Worksheet 3: model storyboard for CareCall")
D.table([["Card", "Headline", "Evidence"],
         ["1 Problem", "Nearly one in five patients came back within a month, so we asked whether a nurse call would help", f"{cb.TOTAL_EVENTS} of {cb.TOTAL_N} patients ({100 * cb.TOTAL_EVENTS / cb.TOTAL_N:.1f}%)"],
         ["2 What we did", f"We compared {F['total_n']} patients who did or did not receive a call within 72 hours", "Flow diagram"],
         ["3 Main finding", f"Readmissions were {F['rd']} per 100 lower among those called", "Bars with denominators"],
         ["4 Limit", f"The gap narrows to {F['adj']} per 100 within risk groups, and the interval crosses zero", "Interval plot"],
         ["5 Meaning", "Calls may help, but reachable patients were healthier, so we cannot yet separate the two", "Risk mix: " + f"{F['hi_share_call']}% v {F['hi_share_usual']}% high risk"],
         ["6 Conclusion", "Test calls in a staggered trial before funding full roll-out", "Decision box"]], [3, 9, 4.6], size=9.5)
D.h2("Worksheet 4: critique and model redesign")
D.p("Problems in the slide: a topic title; a table with no message; green and red as the only signal; 'NS' with no sizes or intervals; the claim that calls 'had no effect in subgroups'; and an unexplained contrast with the overall result. The model redesign is slide 51 of the workshop deck and pair 6 of Before_After_Slides.pptx.")
D.key(f"Model headline: In both risk groups fewer patients who got a call were readmitted, and the intervals are wide. Evidence: paired bars ({F['hi_call_pct']} v {F['hi_usual_pct']} per 100 at high risk, {F['lo_call_pct']} v {F['lo_usual_pct']} at lower risk), with intervals for each difference ({abs(100 * cb.RD_HIGH):.1f} fewer, {abs(100 * cb.RD_HIGH_LO):.1f} fewer to {100 * cb.RD_HIGH_HI:.1f} more; and {abs(100 * cb.RD_LOW):.1f} fewer, {abs(100 * cb.RD_LOW_LO):.1f} fewer to {100 * cb.RD_LOW_HI:.1f} more).")
D.p("Accept any honest alternative, such as a dot plot of the differences alone. Do not accept a headline that drops 'not randomised' from the talk altogether, or one that says calls worked in both groups.")
D.h2("Question cards: what a good answer sounds like")
D.table([["Type", "Good answer"],
         ["Critical", "\"That is a fair concern. Calls were not randomised, and patients reached were healthier. Stratifying by risk reduced the gap, which is why we recommend a randomised evaluation.\""],
         ["Unclear", "\"Do you mean the overall difference, or the difference within risk groups?\" Then answer the one they mean."],
         ["Out of scope", "\"We did not study costs per readmission avoided. We have nurse time only. I can share that afterwards.\""],
         ["Unknown", "\"I do not know. We did not analyse patients over 85 separately. I can check whether the numbers allow it and reply by email.\""]], [3, 13.6], size=9.5)

# ------------------------------------------------------------------ 6
D.h1("One-hour talk run sheet")
D.p("The talk stands alone. It needs no workbook, and it covers a realistic subset of the workshop: fewer slides, one audience activity, and no rehearsal. Do not try to rush through the workshop deck. The schedule totals exactly 60 minutes.")
rows = [["Start", "Elapsed", "Min", "Block", "Slides", "How the time is spent"]]
for st, en, title, mins, kind, what, out, los in c.clock(c.TALK):
    rows.append([clock_at(st), f"{c.fmt(st)} to {c.fmt(en)}", str(mins), title, TR[title], what])
rows.append(["10:00", "1:00", "60", "**End**", "", ""])
D.table(rows, [1.3, 2.2, 1.3, 5, 1.4, 5.8], size=8.5)
D.h2("What the talk leaves out")
D.p("Paragraph editing, storyboarding, slide redesign, rehearsal, Q&A practice and detailed defence guidance are all workshop content. The talk mentions defences briefly under audience and says that requirements vary. It keeps the ideas with the highest value for a single hour: a one-sentence message, claims that match the evidence, a headline plus evidence, honest charts, timed rehearsal and honest answers.")
D.h2("Running the audience activity")
D.p("Seven minutes: 2 alone, 3 with a neighbour, 2 for debrief. Works in fixed rows. With more than 100 people, take examples from a few rows or use a poll. Online, ask for headlines in chat, then read three aloud.")
D.h2("Handling questions")
D.p("Seven minutes are reserved. Model the four steps as you answer: listen, repeat, answer briefly, check. If nobody asks, use the prompts on slide 25. Stop questions at minute 58 and close on slide 26.")

# ------------------------------------------------------------------ 7
D.h1("Adaptations")
D.h2("Larger groups")
D.table([["Group size", "Change", "Rehearsal"],
         ["25 to 40", "Two facilitators. Tables of 6, holding two trios each. Worksheets as in the standard version.", "Trios, standard timings. Facilitators sample tables and do not try to hear everyone."],
         ["41 to 60", "Three facilitators or table leaders briefed in advance. Debriefs are sampled from three tables only.", "Trios, standard timings. Print the round on each table and use a loud timer."],
         ["More than 60", "Use the one-hour talk, or split into parallel workshops. If neither is possible, keep the schedule and run pairs.", "Pairs: two rounds of 9 minutes (speak 2, write 1, discuss 3, redo 1, change 2). That is 18 minutes."]], [3, 7.3, 6.3], size=9.5)
D.h2("Online delivery")
D.p("The online version keeps the 180-minute total. It uses the same deck. Assign trios in advance, and name breakout rooms. Ask for cameras on during rehearsal if people are comfortable, and allow a voice-only option. Tell participants to have the PDF workbook and a second window or a phone timer. Breakout moves cost time, so the online timings below take that from the briefs and debriefs and keep the trio rounds intact.")
rows = [["Block", "Min", "Online change"],
        ["Welcome", "8", "Use chat for 'what would make today useful'. Assign pairs for the morning."],
        ["Module 1", "20", "Worksheet alone with cameras off. Pair check in two-person rooms: 3 minutes includes moving."],
        ["Module 2", "30", "Share the exercise paragraph in chat. Swap by chat or shared document."],
        ["Module 3", "20", "Storyboard in the worksheet or on paper. Read headlines in rooms."],
        ["Break", "12", "Leave a countdown on screen."],
        ["Module 4", "34", "Redesign in Slide_Redesign_Exercise.pptx, or on paper with a phone photo. Debrief by screen share."],
        ["Module 5", "10", "Drill in pair rooms: 4 minutes plus 1 minute to move."],
        ["Timed rehearsal", "22", "Brief 2, open rooms 1, three rounds of 6 minutes, rooms close and debrief 1. Use the broadcast message to call each change."],
        ["Q&A practice", "12", "Teach 2, open rooms 1, three rounds of 3 minutes. Stay in the same rooms if the platform allows."],
        ["Module 6", "7", "Accuracy check alone."],
        ["Close", "5", "Feedback by online form."],
        ["**Total**", "**180**", ""]]
assert sum(int(r[1].strip("*")) for r in rows[1:-1]) == 180
D.table(rows, [3.4, 1.6, 11.6], size=9.5)
D.p("For more than 24 people online, add a co-host to manage rooms. Check before the session that participants can enter breakout rooms from their device. If the connection fails, send everyone the PDFs and restart with the next timed block.")
D.h2("Presenting in English as an additional language")
D.bullets(["Send the workbook before the session, so that people can read it in advance.", "Speak at a steady pace. Pause after numbers, and write key terms on the board.", "Allow writing in another language first, then a move to English.", "Offer the phrases on Worksheet 7. Set phrases help when thinking time is short.", "Never correct accent. Correct a word only if the listener has misunderstood it, and do so privately."])
D.h2("Accessibility")
D.bullets(["Offer materials in advance, and PDF or Word on request. The slide titles are unique, and charts carry alt text.", "Describe each figure aloud using the four moves. Do not refer to things by colour alone.", "Use a microphone where available, and repeat questions from the room.", "Offer a seated or written alternative for anyone who prefers not to rehearse aloud. They can act as timekeeper and give written feedback."])

# ------------------------------------------------------------------ 8
D.h1("Alignment and feedback")
D.h2("Outcomes, activities and feedback")
rows = [["Outcome", "Taught and practised in", "Product", "Rubric criteria"]]
for lo, act, prod, rub in c.ALIGNMENT:
    rows.append([f"**{lo}.** {c.OUTCOMES[lo]}", act, prod, rub])
D.table(rows, [6, 4, 3.6, 3], size=9)
D.h2("Using the rubric")
D.p("Worksheet 6 is a feedback tool for practice, built for this course. It has not been validated. It focuses on seven criteria: message, structure, writing, evidence, visual clarity, timing and responses to questions. In the rehearsal, ask listeners to use only the rows that apply to what they heard. The ratings help a speaker choose one thing to change, so do not collect or total them. Nobody should comment on accent or personality.")
D.h2("Why the feedback is built this way")
D.p("Hattie and Timperley's review found that information about the task and how to improve it has more value than comments on the person, and that feedback can also do harm. A meta-analysis by Double and colleagues found a modest average benefit from peer assessment, with a smaller estimate for university students. Most of that evidence comes from school or university study and not from talks, so we are extrapolating. The timed redo is our own teaching recommendation.")

# ------------------------------------------------------------------ 9
D.h1("Fictional data sheet")
D.p(f"{F['fiction']} All figures below are generated by src/casebook.py, and scripts/check_numbers.py recalculates them independently. Use this sheet to answer questions.")
D.p(ex.CASE_A_BRIEF)
D.table(ex.CASE_A_TABLE, [7, 3, 3, 3], size=9.5)
D.table([["Quantity", "Result"],
         ["Crude risk difference, call minus no call", f"{F['rd']} points lower (95% CI {F['rd_hi']} to {F['rd_lo']} lower)"],
         ["Relative risk", f"{F['rr']}, a relative reduction of {F['rrr']}%"],
         ["Within risk groups (Mantel-Haenszel)", f"{F['adj']} points lower (95% CI {F['adj_lo']} lower to {F['adj_hi']} higher)"],
         ["Emergency visits without admission", f"{F['ed_call_ev']}/{F['call_n']} ({F['ed_call_pct']}%) v {F['ed_usual_ev']}/{F['usual_n']} ({F['ed_usual_pct']}%); {F['ed_rd']} lower (95% CI {F['ed_lo']} lower to {F['ed_hi']} higher)"],
         ["Hospital A", f"{F['hosp_a_ev']} of {F['hosp_a_n']} ({F['hosp_a_pct']}%)"], ["Hospital B", f"{F['hosp_b_ev']} of {F['hosp_b_n']} ({F['hosp_b_pct']}%)"],
         ["Nurse time", f"{F['call_n']} calls at {F['mins']} minutes: about {F['call_hours']} hours. A simple illustration, not a costing."]], [6, 10.6], size=9.5)
D.p(ex.CASE_B_BRIEF)
D.p(ex.EXERCISE_DATA)
D.p("Intervals use Wald standard errors for risk differences, the Greenland-Robins variance for the Mantel-Haenszel difference, and a t distribution with 22 degrees of freedom for the classroom difference.")
D.save(ROOT / "facilitator" / "Facilitator_Guide.docx")
print("guide built")
