"""Builds the worksheets, workbook, writing examples, and references with source map."""
import csv
from pathlib import Path

import course as c
import examples as ex
import sources as src
import worksheets as ws
from casebook import facts
from doc_kit import Doc

F = facts()
ROOT = Path(__file__).parents[1] / "materials"
V = f"{c.ORG}  ·  {c.VERSION}"


def writing_examples(D, heading):
    heading("Worked example: a results paragraph")
    D.p("All data are fictional. The original paragraph is short and confident, and it overstates.")
    D.p("**Before**", keep=True)
    D.key(ex.PARA_BEFORE)
    D.p("**After**", keep=True)
    D.key(ex.PARA_AFTER)
    D.table([["What changed", "Why"]] + [[a, b] for a, b in ex.PARA_NOTES], [5, 11], size=9.5, caption="Table: what changed and why.")
    heading("One finding in four forms")
    D.p("The same result, rewritten for four uses. Words change between versions. The size, the population, the design and the uncertainty do not.")
    D.table([["Form", "Text"], ["Paragraph", "The 'after' paragraph above."], ["Abstract passage", ex.ABSTRACT_PASSAGE], ["Slide headline", ex.HEADLINE], ["Spoken explanation", ex.SPOKEN]], [3, 13], size=9.5)
    heading("Sentence repairs")
    D.p("Eight common problems, with an explanation of each repair.")
    D.table([["Problem", "Before", "After", "Why"]] + [list(x) for x in ex.SENTENCE_FIXES], [2.2, 5, 6, 3], size=9)


# ---------------------------------------------------------------- Worksheets
for fname, title, fn in ws.ALL:
    D = Doc(title.split(": ")[1].capitalize(), f"{title.split(':')[0]}, Scientific Communication", V)
    D.h2 = lambda t: None  # the document title already names the worksheet
    fn(D)
    D.save(ROOT / "worksheets" / f"{fname}.docx")

# ---------------------------------------------------------------- Writing examples
D = Doc("Before and After Writing Examples", c.COURSE, V)
writing_examples(D, D.h1)
D.save(ROOT / "examples" / "Before_After_Writing_Examples.docx")

# ---------------------------------------------------------------- Workbook
D = Doc("Participant Workbook", c.COURSE, V, toc=True)
D.h1("About this workshop")
D.p("You already know your subject. This workshop helps you explain it clearly and keep your claims in line with your evidence. It is an introduction with guided practice over three hours, so it will not make anyone a finished writer or speaker. You will leave with four things you have made yourself: a revised paragraph, a short presentation storyboard, one redesigned slide and a rehearsed explanation.")
D.p("Use your own work if you can, with any identifiers removed. If you cannot, the two fictional cases in this workbook will serve. Nothing in this workbook comes from a real study.")
D.h2("Learning outcomes")
D.p("By the end of the workshop you should be able to:", keep=True)
D.bullets([(x[0].lower() + x[1:]).replace("their ", "your ") for x in c.OUTCOMES.values()])
D.h2("Schedule")
rows = [["Time", "Min", "Block", "What you will produce"]]
for st, en, title, mins, kind, what, out, los in c.clock(c.WORKSHOP):
    rows.append([f"{c.fmt(st)} to {c.fmt(en)}", str(mins), title, out or "-"])
rows.append(["", "180", "**Total**", ""])
D.table(rows, [2.4, 1.4, 7, 5], size=9.5)
D.h2("How we treat evidence")
D.p("This course separates three things. **Research findings** come from studies, and they have limits. **Professional advice** comes from experience, and most advice about slides is of this kind. **Our recommendations** are teaching devices that we find useful. You will hear each one labelled. Rules such as one slide per minute, six words per line or a minimum font size are rules of thumb. We did not find experiments that set those numbers, so test your slides in the real room.")

D.h1("The two fictional cases")
D.h2("Case A: CareCall")
D.p(ex.CASE_A_BRIEF)
D.table(ex.CASE_A_TABLE, [7, 3, 3, 3], size=9.5, caption=f"Table: unplanned readmission within 30 days. {F['fiction']}")
D.p(f"The risk difference was {F['rd']} percentage points (95% CI {F['rd_hi']} to {F['rd_lo']} lower with a call). Within risk groups, combined by the Mantel-Haenszel method, it was {F['adj']} points lower (95% CI {F['adj_lo']} lower to {F['adj_hi']} higher). Emergency visits without admission were {F['ed_call_ev']} of {F['call_n']} ({F['ed_call_pct']}%) and {F['ed_usual_ev']} of {F['usual_n']} ({F['ed_usual_pct']}%), a difference of {F['ed_rd']} points lower (95% CI {F['ed_lo']} lower to {F['ed_hi']} higher).")
D.h2("Case B: CoolRoom")
D.p(ex.CASE_B_BRIEF)
D.p(ex.EXERCISE_DATA)

D.h1("Module notes")
D.h2("Module 1: Audience, purpose and message")
D.p("Decide who is in the room, what they know, what they need and what should change afterwards. Only then write your message. A topic names an area, and a message makes a claim someone could challenge. The same finding needs a different message for a conference, a thesis committee and a hospital management team, although the evidence and the uncertainty stay the same.")
D.table([["Room", "Who they are", "What they should do", "Message"]] + [list(r) for r in ex.ROOMS], [3, 4, 4, 6], size=9)
D.h2("Module 2: Scientific writing")
D.p("A clear paragraph makes one point, gives evidence, interprets it and says what follows. Keep results apart from interpretation. Give counts with their denominators, report the size of a difference with its uncertainty, and choose verbs your design can support. A non-significant result is rarely proof of no effect: state what the interval allows. Avoid giving a relative figure alone, because relative figures tend to look larger and persuade more.")
D.p("Within a sentence, readers tend to look to the start for context and to the end for what is new. That is reasoned advice from Gopen and Swan, and they do not offer it as a rule. Plain language means fitting words to your reader. Specialists can keep specialist terms where those terms carry meaning.")
writing_examples(D, D.h3)
D.h2("Module 3: Presentation structure")
D.p("A talk is one argument: question, evidence, interpretation, implication. Open with the problem and the question. Show the methods your audience needs to judge the evidence: who, what was compared, what was measured and the main threat to validity. Lead with your main finding, and put a limit that changes its meaning next to it. End with what the evidence supports.")
D.p("A conference talk spends most time on findings and meaning. An organisational briefing leads with the recommendation. A thesis defence examines your contribution and your methodological choices, so prepare to explain why you chose your methods over the alternatives, and build backup slides for expected challenges. Requirements vary a great deal: a UK viva may be private with no required talk, while a public defence in the United States or Sweden may last an hour or several. Read your own regulations first.")
D.h2("Module 4: Slide design and data communication")
D.p("Give each slide a headline that states the claim, and use the body to show evidence. One experiment supports this bundle, and it has critics, so treat it as a strong default. Reduce text by moving detail to your speech and notes, while keeping the numbers needed to judge the claim. Test contrast and legibility in the real room. Do not let colour be the only signal: add labels, shapes or line styles.")
D.p("Choose a chart from your question. Bars encode length, so they start at zero. Dots and lines encode position, so a narrower labelled range can be right. Every figure should tell the audience its axes, units, denominators, uncertainty and source. The file Before_After_Slides.pptx holds six redesigns with notes.")
D.h2("Module 5: Delivery, rehearsal and questions")
D.p("Explain each figure in four moves: what it shows, where to look, what you see and why it matters. Speak from understanding, with brief notes for the route. Rehearse aloud against the real limit, and cut content before you speed up. Accent is not a fault. Being understood is the goal, and pace, pauses, signposts and stress on key words all help.")
D.p("With questions, listen to the end, repeat or rephrase, answer briefly, then check. Find the valid part of a critical question. Ask what an unclear question means. Say when something is out of scope, and offer a route. If you do not know, say so.")
D.h2("Module 6: Accuracy and responsible use")
D.p("When you simplify, keep the size, the population, the direction and the certainty. Credit sources and collaborators, and get permission before you acknowledge someone. Protect people in your data. A rare case on a named ward can identify a patient, small numbers can expose a person, and data with codes in place of names are usually pseudonymised and not anonymous. Find your organisation's rule.")
D.p("AI tools can help you edit and rehearse. You remain responsible for every fact, reference and claim, so open every reference and check every number against your source. Do not paste confidential data into tools your organisation has not approved, and follow your journal's or institution's rules on disclosure.")
D.page()
D.h1("Worksheets")
for i, (fname, title, fn) in enumerate(ws.ALL):
    fn(D)
    if i < len(ws.ALL) - 1:
        D.page()
D.page()
D.h1("Personal plan and course feedback")
D.h2("My plan")
D.form(["The one thing I will revise first", "My rehearsal: with whom, and on what date?", "The claim I will verify"], height=1.6)
D.h2("Accuracy check for any slide")
D.bullets(["Every number matches the source table.", "Denominators and units are shown.", "Uncertainty is shown.", "The verb fits the design.", "The headline is no stronger than the data.", "No person can be identified.", "Sources and collaborators are credited.", "AI use is disclosed, if required."])
D.h2("Course feedback")
D.table([["Please tick one for each statement", "Disagree", "Neutral", "Agree"],
         ["The session was useful for my work.", "", "", ""], ["The exercises fitted the time.", "", "", ""], ["Feedback focused on clarity and understanding.", "", "", ""], ["I would recommend this workshop.", "", "", ""]], [10, 2, 2, 2], size=9.5)
D.p("What should we change?", keep=True)
D.write_lines(3)
D.h2("Where the guidance comes from")
D.p("The full reference list, with links, is in References_and_Source_Map. Useful starting points are Bourne (2007), Naegle (2021), the assertion-evidence site at assertion-evidence.com, the CDC Clear Communication Index, and Altman and Bland (1995).")
D.save(ROOT / "workbook" / "Participant_Workbook.docx")

# ---------------------------------------------------------------- References and source map
D = Doc("References and Source Map", c.COURSE, V, toc=True)
D.h1("How these sources were checked")
D.p("Every source below was opened and read on 4 November 2026, in full or, where stated, as an abstract or bibliographic record only. Some publisher pages refuse automated access, so a few sources were read through PubMed Central, Europe PMC, an author's copy or a university repository. In those cases the link given is the most stable one for readers. Long pages were sometimes read with text extraction or a summarising tool, so every figure quoted in the course was then checked by eye against the source text. Links were tested by script, and the results are in materials/references/link_check.csv.")
D.h2("Evidence types")
D.table([["Label", "Meaning", "How to use it"],
         [src.RF, "An empirical study or systematic review.", "State the design, the setting and the limits. Learning or online studies do not automatically transfer to research talks."],
         [src.RC, "A narrative or methods review, meta-analysis, or expert statement.", "Reliable on principles. Check how far it applies."],
         [src.PG, "Advice from experienced people or organisations.", "Useful, but not evidence of effect. Most slide advice is of this kind."],
         [src.SP, "A standard, or a policy of an institution or journal group.", "Binding only where it applies, so check yours."],
         [src.TR, "Teaching material from a university or a method's authors.", "Practical. Often written by advocates."],
         ["Teaching recommendation", "Our own device, such as the four moves or the rubric.", "Labelled as ours in the materials. Not a finding."]], [3.4, 6, 7], size=9.5)
D.h2("Rules of thumb in this course")
D.p("We searched for experiments that set a slides-per-minute rate, a six-by-six word limit, or a minimum point size for projected slides, and found none. This was a targeted search, so the materials say that we found no evidence, and they do not say that none exists.")
D.table([["Rule", "What the sources say", "Practical limit"],
         ["One slide per minute", "Bourne 2007 calls more than one visual per minute too many, as a personal rule of thumb. Naegle 2021 advises a minute or less per slide. Garner & Alley 2013 tested a talk at about 1.4 slides per minute, although rate was not the variable tested.", "A planning check only. Density and build matter more than count."],
         ["Six words, six lines", "No primary source found. The closest statement is a summary of World Blind Union guidance, which gives no evidence for its numbers. Less text alongside speech has reasoned and indirect support.", "Decide what must be read, and move the rest."],
         ["Minimum 24 or 30 point", "Published advice ranges from 18 pt (Microsoft) through 18 to 24 pt body text (Penn State) to 32 pt (WBU summary). W3C gives no number. Legge & Bigelow 2011 show that legibility depends on angular size. WCAG's 18 pt defines large text for the contrast rule and is not a font minimum.", "Test from the back of the actual room, or at reduced size."]], [3, 9, 4.6], size=9)
D.h2("Corrections we made to common claims")
D.bullets(["Garner et al. 2009 is a slide audit. The learning experiment is Garner & Alley 2013, which tested a bundle of changes on one recorded talk.",
           "Mayer & Moreno's redundancy effect concerns identical on-screen text with narration and animation. With no animation, narration plus text did better than narration alone. It does not show that text on slides is harmful in general.",
           "Akl et al. 2011 found relative figures looked larger and persuaded more than absolute ones, with no difference in understanding. Its natural-frequency finding applies to diagnostic and screening information.",
           "Gopen & Swan 1990 is an argued essay with no reader testing, and the authors say their principles are not rules.",
           "HHS de-identification guidance gives no rule on small cells. We use the Public Health Scotland protocol as one worked example and tell readers to find their own rule.",
           "The CDC Clear Communication Index score is a percentage of applicable items. CDC gives no validation for its 90 cut-off, and we call it a convention.",
           "The former plainlanguage.gov guidelines page now redirects to digital.gov. The Guidelines are reposted by the Center for Plain Language."])
D.h1("Source-to-content map")
D.p("These tables show which sources support each module, and what each source is used for. M1 to M6 are the course modules. F covers facilitation and feedback design.")
for mod, name in src.MODULE_NAMES.items():
    rows = [["Source", "Type", "What it supports here"]]
    for s in src.SOURCES:
        if mod in s[6].split():
            rows.append([s[0], s[4], s[7]])
    D.table(rows, [3.4, 3, 10.2], size=9, caption=f"{mod}: {name}.")
D.h1("Reference list")
for i, s in enumerate(src.SOURCES, 1):
    link = f"https://doi.org/{s[3]}" if s[3] else s[2]
    D.ref(f"{i}. {s[1]}", link, f"[{s[4]}. {s[5]}.]")
D.h2("Limits of each source")
D.table([["Source", "Limit to keep in mind"]] + [[s[0], s[8]] for s in src.SOURCES], [4, 12.6], size=9)
D.h2("Considered and not used")
D.table([["Item", "Why"]] + [list(x) for x in src.NOT_USED], [7, 9.6], size=9.5)
D.save(ROOT / "references" / "References_and_Source_Map.docx")

# ---------------------------------------------------------------- Plain-text exports of the references
md = ["# References", "", "Opened and checked on 4 November 2026. See References_and_Source_Map for evidence types, limits and the map to modules.", ""]
for i, s in enumerate(src.SOURCES, 1):
    link = f"https://doi.org/{s[3]}" if s[3] else s[2]
    md.append(f"{i}. {s[1]} <{link}> ({s[4]}; {s[5].lower()}; modules {s[6]})")
(ROOT / "references" / "references.md").write_text("\n".join(md) + "\n", encoding="utf8")
with open(ROOT / "references" / "source_map.csv", "w", newline="", encoding="utf8") as f:
    w = csv.writer(f)
    w.writerow(["source", "citation", "url", "doi", "evidence_type", "access", "modules", "supports", "limit"])
    w.writerows(src.SOURCES)
print("docs built")
