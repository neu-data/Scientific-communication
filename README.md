<div align="center">

<img src="https://raw.githubusercontent.com/neu-data/.github/main/assets/banner.svg" alt="Neudata Consulting Ltd" width="100%" />

# Scientific Communication
### Writing, Slide Design and Presentation Skills

**A complete training package: a three-hour practical workshop and a one-hour talk.**

![Neudata](https://img.shields.io/badge/Neudata-training-055F56?style=flat)
![Status](https://img.shields.io/badge/version-1.0-0B376C?style=flat)

*Neudata · #ClearDataClearImpact*

**Course website:** <https://neu-data.github.io/Scientific-communication/>

</div>

---

## Audience

The course is for people who know their subject and may struggle to communicate it. It uses a shared foundation, with examples adapted to:

- researchers preparing conference presentations
- students preparing thesis defences
- professionals in hospitals and other organisations presenting evidence, findings or recommendations

It is accessible across disciplines, and it accommodates people presenting in English as an additional language. Feedback addresses clarity and understanding, and never accent or personality.

## Learning outcomes

By the end of the workshop, participants should be able to:

1. Define their audience, purpose and main message.
2. Build an argument that connects a question, evidence, interpretation and implications.
3. Write clear scientific paragraphs, abstracts and slide headlines without overstating findings.
4. Design readable slides and explain figures accurately.
5. Deliver a timed presentation and respond to questions.
6. Use structured feedback to revise and rehearse their work.

This is an introduction with guided practice. It does not promise mastery of scientific writing or public speaking.

## Prerequisites

None beyond knowing a subject and being comfortable with percentages. Participants may bring a result or paragraph from their own work, with identifiers removed. Facilitators should be able to explain a confidence interval. Fictional cases are supplied for anyone without their own material.

## The two versions

| | Three-hour workshop | One-hour talk |
|---|---|---|
| Length | 180 minutes, with a 12-minute break | 60 minutes, with a 7-minute activity and 7 minutes of questions |
| Group | 12 to 24, with adaptations for larger groups and online | Any size |
| Slides | 71, including 3 backups | 27 |
| Participants leave with | Revised paragraph, storyboard, redesigned slide, rehearsed explanation | One rewritten headline, and three things to do next |
| Needs | Workbook or printed worksheets, movable chairs, a timer | Slides and a timer |

## How to run each version

**Workshop.** Read [the facilitator guide](materials/facilitator/Facilitator_Guide.pdf), which has the run sheet, block-by-block instructions, debrief questions, model answers and adaptations. Print the [workbook](materials/workbook/Participant_Workbook.pdf). Present [the workshop deck](materials/workshop_3h/Scientific_Communication_Workshop_3h.pptx): the notes on each slide give the timing, a suggested script, a question for the room and the basis for each claim.

**Talk.** Present [the talk deck](materials/talk_1h/Scientific_Communication_Talk_1h.pptx). No workbook is needed. The run sheet is in the facilitator guide.

## File structure

```
materials/
  workshop_3h/    Workshop deck, PowerPoint and PDF
  talk_1h/        Talk deck, PowerPoint and PDF
  facilitator/    Facilitator guide, Word and PDF
  workbook/       Participant workbook, Word and PDF
  worksheets/     Worksheets 1 to 7, including the rehearsal checklist and feedback rubric
  exercises/      Slide redesign exercise file
  examples/       Before-and-after slides and writing examples
  references/     References, source map, CSV exports and link-check results
src/              Editable source: fictional data, slide and document content, builders, brand templates
scripts/          Render and check scripts
docs/             Course website for GitHub Pages
```

## Fictional data

CareCall (hospital follow-up calls) and CoolRoom (classroom temperature) are invented for teaching and labelled as fictional wherever they appear. They are not real study results. Every number comes from [src/casebook.py](src/casebook.py).

## Evidence

The materials separate research findings, professional advice and neu-data teaching recommendations. Rules such as one slide per minute, six words per line and minimum font sizes are presented as rules of thumb, with their limits. See [References and Source Map](materials/references/References_and_Source_Map.pdf).

The feedback rubric is a course feedback tool, not a validated assessment instrument.

## Rebuilding

Requires Windows with Microsoft PowerPoint and Word, because the PDFs are exported by those programs from the editable files, and Python 3 with `python-pptx`, `python-docx`, `pymupdf`, `scipy` and `pillow`.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_all.ps1
```

To change a number, edit `src/casebook.py` and rebuild. Slide content is in `src/build_workshop.py`, `src/build_talk.py` and `src/slides_lib.py`. Document content is in `src/build_docs.py`, `src/build_guide.py` and `src/worksheets.py`.

## Checks

| Script | What it checks |
|---|---|
| `scripts/check_numbers.py` | Recalculates every number from raw counts, and searches the PDFs for expected and stale values |
| `scripts/check_materials.py` | Schedule totals, per-slide minutes, outcome alignment, native objects, notes, PDF page counts, writing standards |
| `scripts/check_links.py` | Tests each link and checks each DOI against Crossref |
| `scripts/render_office.ps1` | Exports PDFs and flags text overflow, using PowerPoint's own measurements |

## Copyright

Copyright Neudata, 2026. All rights reserved. The materials are original, and no third-party course, figure or slide deck is reproduced. Colours and layouts come from the Neudata templates.
