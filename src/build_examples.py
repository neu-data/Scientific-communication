"""Builds the standalone before-and-after slide file and the redesign exercise file."""
from pathlib import Path

import casebook as cb
from slides_lib import *

ROOT = Path(__file__).parents[1] / "materials"

why = [
    ("A wall of text. The audience reads ahead and the point is buried in the last line.",
     "The headline makes the claim, the chart carries the main numbers, and the interval plot shows what happens within risk groups. The caution stayed."),
    ("A methods section pasted onto a slide. The audience cannot see how the groups relate.",
     "A flow diagram shows denominators and design at once. Analysis detail moves to speech or to a backup slide."),
    ("Truncated axis, 3-D perspective, no units or denominators, a causal headline with an exclamation mark.",
     "Dots and intervals encode position, so the scale can fit the differences. Size and uncertainty are both visible."),
    ("Red and green alone separate the lines, and a viewer must decode 'Group 1' and 'Group 2'.",
     "Colours from the Okabe and Ito palette, different markers and direct labels. The headline states the claim and its limit."),
    ("A generic close that fits any talk, and it asks nothing of a decision-maker.",
     "For a management audience: what we know, what it costs, what we do not know, and the decision needed."),
    ("A table with no message, colour as the only signal, 'NS' in place of intervals, and 'no effect' reasoning.",
     "The headline states the pattern and its uncertainty, paired bars keep the denominators nearby, and intervals replace 'NS'."),
]
d = D()
d.set_block("Examples")
d._tick(0)
d.title_slide("Before and After Slides", "Six worked redesigns. All data are fictional.", "Version 1.0, November 2026",
              "Each pair shows a slide before and after redesign. The notes explain what changed and why. All objects are native PowerPoint shapes and charts, so you can adapt them.")
for (nm, fb, fa), (wb, wa) in zip(BA_PAIRS, why):
    fb(d, 0, N(f"{nm}. {wb}"))
    fa(d, 0, N(f"{nm}. {wa}"))
d.closing("Closing slide.")
d.save(ROOT / "examples" / "Before_After_Slides.pptx")

d = D()
d.set_block("Exercise")
d._tick(0)
d.title_slide("Slide Redesign Exercise", "Worksheet 4 companion file\nAll data are fictional", "Version 1.0, November 2026",
              "Slide 2 is the slide to critique. Slide 3 is a blank slide for your redesign. Slide 4 gives the data. The model answer is held in the facilitator guide and shown in the workshop debrief.")
bax_before(d, 0, N("Critique this slide using Worksheet 4. What is the claim? What is the evidence? What would a viewer with a colour vision difference lose? What does NS hide?"))
s = d.s("Write your headline here as a full sentence", 0, N("Replace this title with your claim. Add one visual as evidence. Keep denominators and uncertainty. Use the data on the next slide. Insert a chart with Insert, Chart in PowerPoint."), fictional=True)
s = d.s("Data for your redesign", 0, N("All values are fictional. Differences are call minus no call, per 100 patients, with Wald 95% confidence intervals."), fictional=True)
rows = [["Discharge risk", "Call", "No call", "Difference per 100 (95% CI)"],
        ["High", f"{F['hi_call_ev']} of {F['hi_call_n']} ({F['hi_call_pct']}%)", f"{F['hi_usual_ev']} of {F['hi_usual_n']} ({F['hi_usual_pct']}%)", f"{abs(100*cb.RD_HIGH):.1f} fewer ({abs(100*cb.RD_HIGH_LO):.1f} fewer to {100*cb.RD_HIGH_HI:.1f} more)"],
        ["Lower", f"{F['lo_call_ev']} of {F['lo_call_n']} ({F['lo_call_pct']}%)", f"{F['lo_usual_ev']} of {F['lo_usual_n']} ({F['lo_usual_pct']}%)", f"{abs(100*cb.RD_LOW):.1f} fewer ({abs(100*cb.RD_LOW_LO):.1f} fewer to {100*cb.RD_LOW_HI:.1f} more)"],
        ["All patients", f"{F['call_ev']} of {F['call_n']} ({F['call_pct']}%)", f"{F['usual_ev']} of {F['usual_n']} ({F['usual_pct']}%)", f"{F['rd']} fewer ({F['rd_hi']} to {F['rd_lo']} fewer)"]]
table(s, LEFT, 110, WIDTH, rows, [17, 24, 24, 35], row_h=66, size=16, bold_first=True, name="Exercise data")
text(s, LEFT, 370, WIDTH, 70, "Calls were not randomised. Patients at high risk were harder to reach.", size=18, color=NAVY)
d.closing("Closing slide.")
d.save(ROOT / "exercises" / "Slide_Redesign_Exercise.pptx")
print("ok")
