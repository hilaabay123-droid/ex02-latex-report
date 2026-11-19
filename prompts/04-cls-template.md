Save this prompt to prompts/04-cls-template.md, then execute it.

CONTEXT: online today: master-se, fix-se, art-se (qa-se will join for the
final stress test - tell me when to open it). fix-se has UNCOMMITTED work
from yesterday (closettwin.cls and fix/). fix-se: first review it, commit
what is good, and continue from it - do not start over. Also finish the
pythonbox environment (T20.5).

Build closettwin.cls for LuaLaTeX (MiKTeX) according to PRD.md (latest version).
Roles: fix-se writes the class; art-se reviews every stage visually;
qa-se runs the final stress test; you (master-se) coordinate and report to me.
Maximum 2 review rounds per stage.

Work in 6 stages. After EACH stage: compile a test page, render it to PNG
with PyMuPDF into docs/screenshots/cls-stage-N.png, show me, wait for my OK.
If a stage is already done in the existing work, show its image and move on.
1. Skeleton: fonts from fonts/ (Playfair Display = English headings,
   Rubik = body and ALL Hebrew text, Latin Modern Math = formulas only,
   JetBrains Mono = code box only). White page background. English LTR
   default + a Hebrew RTL environment for the executive-summary page,
   safe language switching.
2. Magazine typography: chapter openers (large Playfair title, chapter
   number, thin mocha rule, generous white space), sections, lists,
   palette incl. dark mocha #6B4B3D and pale mocha #D3BBAE.
3. Banner (header) and footer: brand name, chapter title, "Page N of M".
4. Components: styled tables, figure/table captions, a "key number" stat
   callout, a magazine pull-quote box, an insight box (ivory), a Python
   code box.
5. Cover page in fashion-magazine-cover style, drawn with TikZ only
   (no internet images), with the cover details from PRD.md.
6. biblatex IEEE style, docs/cls-commands.md (every command + one example),
   a template README, version number and CHANGELOG.md from v0.1.
Rules: one purpose per command; nothing hard-coded in the class that belongs
to the document; no Hebrew inside English units.
Finally qa-se runs course book Prompt B4 (stress test page) - show me the image.
Commit and push after each approved stage.
