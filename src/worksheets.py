"""Worksheet content. Each function writes into a Doc, so a worksheet can stand alone or sit in the workbook."""
import course as c
import examples as ex
from casebook import facts

F = facts()

QUESTION_CARDS = [
    ("Critical", "Your groups were not comparable, so why should we believe any of this?"),
    ("Critical", "Isn't this just regression to the mean, or a healthier group being reached?"),
    ("Critical", "You have one year of data from two sites. Why generalise at all?"),
    ("Unclear", "What about the, you know, the other thing with the numbers?"),
    ("Unclear", "Can you say more about the difference?"),
    ("Unclear", "Doesn't that depend on the setting?"),
    ("Out of scope", "How would this work in primary care?"),
    ("Out of scope", "What is the cost per readmission avoided?"),
    ("Out of scope", "What do you think of the new national funding policy?"),
    ("Unknown", "What was the result for patients aged over 85?"),
    ("Unknown", "Has anyone tested this in a low-income setting?"),
    ("Unknown", "Which statistical package did your colleague use for that sensitivity analysis?"),
]


def ws1(D):
    D.h2("Worksheet 1: Audience and message")
    D.p("Use your own talk if you can. Otherwise use CareCall or CoolRoom and choose one room: conference, thesis committee, or hospital or organisation.", keep=True)
    D.form(["Occasion and time limit", "Who is in the room? (roles, field, seniority, language)", "What do they already know?", "What do they need from you?", "What should they understand, decide or do afterwards?"], height=1.5)
    D.p("**Your message in one sentence**", keep=True)
    D.write_lines(3)
    D.p("Check your sentence. Tick each box.", keep=True)
    D.bullets(["It is a full sentence with a verb.", "Someone could disagree with it.", "You could say it in a corridor, without slides.", "It is no stronger than your evidence."])
    D.p("**Pair check.** Read your sentence aloud. Your partner says what they think you want them to do. What did they say?", keep=True)
    D.write_lines(2)


def ws2(D):
    D.h2("Worksheet 2: Paragraph editing")
    D.p("Edit the paragraph below, or a paragraph of your own. Use only the facts given. Do not invent numbers. This is fictional teaching data.", keep=True)
    D.key(ex.EXERCISE_PARA)
    D.p(f"**{ex.EXERCISE_DATA}**")
    D.p("**Step 1.** Underline at least five problems. Look for wordy phrases, vague claims, missing denominators, causal language, and anything stated but not measured.")
    D.p("**Step 2.** Rewrite it. Aim for one point, then evidence, then interpretation.", keep=True)
    D.write_lines(9)
    D.p("**Step 3. Swap with your partner.** Check the rewrite for three things: is the size given, is the uncertainty given, and is any claim stronger than the data?", keep=True)
    D.write_lines(3)


def ws3(D):
    D.h2("Worksheet 3: Storyboard")
    D.p("Write one full-sentence headline for each card, then sketch the evidence under it. Six cards is a device for today, not a rule for your talk. Do not design slides yet.", keep=True)
    labels = ["1 Problem and question", "2 What we did", "3 Main finding", "4 Limit or second finding", "5 What it means", "6 Conclusion or recommendation"]
    rows = [[labels[i], labels[i + 1]] for i in (0, 2, 4)]
    t = D.table(rows, [1, 1], header=False, size=9.5)
    from docx.shared import Cm
    for r in t.rows:
        r.height = Cm(5.0)
    D.p("**Title test.** Read your headlines aloud in order. Do they tell the story without slides? Which card would you cut if you had half the time?", keep=True)
    D.write_lines(2)


def ws4(D):
    D.h2("Worksheet 4: Slide critique and redesign")
    D.p("The slide is on screen, and it is also in Slide_Redesign_Exercise.pptx. Critique it in pairs for 3 minutes, then redesign it alone for 9 minutes. All values are fictional.", keep=True)
    D.table([["Discharge risk", "Call", "No call"],
             ["High", f"{F['hi_call_ev']} of {F['hi_call_n']} ({F['hi_call_pct']}%)", f"{F['hi_usual_ev']} of {F['hi_usual_n']} ({F['hi_usual_pct']}%)"],
             ["Lower", f"{F['lo_call_ev']} of {F['lo_call_n']} ({F['lo_call_pct']}%)", f"{F['lo_usual_ev']} of {F['lo_usual_n']} ({F['lo_usual_pct']}%)"]], [2, 3, 3], size=9.5)
    D.form(["What is the slide's claim?", "What evidence supports it?", "What would a viewer with a colour vision difference lose?", "What does 'NS' hide?"], height=1.2)
    D.p("**Your headline, as a full sentence**", keep=True)
    D.write_lines(2)
    D.p("**Sketch your evidence.** Keep the denominators and the uncertainty.", keep=True)
    t = D.table([[""]], [1], header=False)
    from docx.shared import Cm
    t.rows[0].height = Cm(6.5)


def ws5(D):
    D.h2("Worksheet 5: Rehearsal checklist and feedback")
    D.p("**Before you rehearse**", keep=True)
    D.bullets(["State your main message in one sentence.", "Mark each slide: must keep, should keep, can cut.", "Practise your opening and your last sentence aloud.", "Practise any technical term or long number you find hard to say.",
               "Write the time you should reach at each section."])
    D.p("**The six-minute round in trios**", keep=True)
    D.table([["Minutes", "Speaker", "Listeners"],
             ["0:00 to 2:00", "Explain your slide using the four moves: what it shows, where to look, what you see, why it matters.", "Listen. The timekeeper stops the speaker at 2:00."],
             ["2:00 to 3:00", "Write down what you would change.", "Complete the prompts below in silence."],
             ["3:00 to 5:00", "Listen. Ask for clarification only.", "Give feedback using the prompts."],
             ["5:00 to 6:00", "Repeat your weakest part once.", "Say whether it was clearer."]], [2, 6, 5], size=9.5)
    D.p("**Feedback prompts, for each speaker**", keep=True)
    D.form(["The main message I understood was:", "I stopped following when:", "The one change that would help most is:"], height=1.5)
    D.small("Keep feedback on clarity and understanding. Do not comment on accent, looks or personality.")


def ws6(D):
    D.h2("Worksheet 6: Feedback rubric")
    D.p("Use this rubric to give feedback on practice. It is a course feedback tool, not a validated assessment instrument, and it should not be used to grade people or to make decisions about them. It rates the work and never accent or personality. Choose the description that fits best and give one example from what you saw or heard.", keep=True)
    rows = [["Criterion", "1 Not yet", "2 Developing", "3 Secure", "Example"]]
    for name, a, b, s in c.RUBRIC:
        rows.append([f"**{name}**", a, b, s, ""])
    D.table(rows, [2.5, 4, 4, 4, 2.5], size=8.5)
    D.p("**What the ratings mean.** 1 Not yet: the listener would struggle, or the claim is unsafe. 2 Developing: the main idea reaches the listener, with one clear thing to improve. 3 Secure: it works for this audience and could be used as it is. A rating of 3 does not mean finished.")


def ws7(D):
    D.h2("Worksheet 7: Question cards")
    D.p("In trios, give your main message in one sentence. A partner reads a card, or writes a fair question of the same type. Answer in one minute: listen, repeat, answer briefly, check. Questions refer to CareCall; adapt them to your own topic.", keep=True)
    rows = [["Type", "Question"]] + [[a, b] for a, b in QUESTION_CARDS]
    D.table(rows, [2, 10], size=9.5)
    D.p("**Phrases you can use**", keep=True)
    D.table([["Moment", "Phrase"],
             ["To gain time", "\"Let me check I understood: you are asking about...\""],
             ["To clarify", "\"Do you mean the crude result or the stratified one?\""],
             ["When criticised", "\"That is a fair concern. Here is what we did about it, and what remains uncertain.\""],
             ["Out of scope", "\"That is outside this study. I can follow up afterwards.\""],
             ["When you do not know", "\"I do not know. The data cannot answer that. I will check and reply.\""],
             ["To state uncertainty", "\"Our best estimate is X, and the data fit anything from Y to Z.\""]], [3, 9], size=9.5)


ALL = [("Worksheet_1_Audience_and_Message", "Worksheet 1: Audience and message", ws1),
       ("Worksheet_2_Paragraph_Editing", "Worksheet 2: Paragraph editing", ws2),
       ("Worksheet_3_Storyboard", "Worksheet 3: Storyboard", ws3),
       ("Worksheet_4_Slide_Critique_and_Redesign", "Worksheet 4: Slide critique and redesign", ws4),
       ("Worksheet_5_Rehearsal_Checklist", "Worksheet 5: Rehearsal checklist", ws5),
       ("Worksheet_6_Feedback_Rubric", "Worksheet 6: Feedback rubric", ws6),
       ("Worksheet_7_Question_Cards", "Worksheet 7: Question cards", ws7)]
