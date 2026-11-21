Save this prompt to prompts/07-readme-and-release.md, then execute it.
Online: master-se, art-se, fix-se, qa-se (writer-se may stay closed).

PART 1 - Screenshots (art-se): render at 150 dpi into docs/screenshots/:
 cover, Hebrew executive summary, Contents, Chapter 1 opener with the
 key numbers, one market chart page, the competition table page,
 Figure 8.1 page, the risk matrix page, the code appendix.
 Also make a 2x4 "gallery" PNG of the best 8 pages.

PART 2 - README.md (you write it, art-se reviews the look). The lecturer
wants a professional, informative README that shows the depth of the
work. In English, in our magazine style (cover image as a banner).
 1. Title, one-line pitch, links: final PDF (main.pdf), PRD, prompts.
 2. The report at a glance: page counts, chapters, the gallery image.
 3. The agent team: a Mermaid diagram of the 5 agents and who talks to
    whom; roles and model per agent (opus/sonnet, why - resource
    management); screenshots 01-mesh-check.png and agents-working.png.
 4. How we worked: PRD -> PLAN -> TODO -> CLS -> skills -> draft ->
    QA loop -> incidents -> red team (a Mermaid flow), with one line per
    stage and a link to the matching prompts/NN-*.md.
 5. Design system: fonts, palette swatch, components; the CLS version
    and its CHANGELOG.
 6. Skills table: every skill in .claude/skills/ with one-line purpose.
 7. Quality: the incident list (incidents/) with root cause in one line
    each; the red-team table (point -> decision); QA reports.
 8. Documentation of our dialogue with the agents:
    prompts/MY-DIALOGUE-WITH-THE-AGENTS.md, prompts/log/, prompts/sessions/.
 9. Build it yourself: MiKTeX + LuaLaTeX, the 4 commands, python
    requirements; folder tree.
 10. Authors (Hila Abay, Shirel Giladi), group sg00ha11, course
    Generative AI for Management (875523402), Dr. Yoram Segal.
 Check every link and image path works on GitHub.

PART 3 - Release check (qa-se):
 - Fresh git clone into a temp folder inside the project, build with the
   4 commands, confirm the same page count (reproducibility).
 - Required files present: main.tex, chapters/*.tex, closettwin.cls,
   references.bib, PRD.md, PLAN.md, TODO.md, README.md, main.pdf,
   prompts/, .claude/skills/, python/, figures/.
 - .gitignore excludes ref/, build junk (*.aux, *.log...), tmp folders.
 - No ID numbers, e-mails, tokens or passwords anywhere in the repo.

PART 4 - Wait until docs/screenshots/agents-working.png exists (I am
taking it now). Then re-run tools/export_sessions.py, update
prompts/MY-DIALOGUE-WITH-THE-AGENTS.md, commit, push, and tell me the
README link and anything that failed.
