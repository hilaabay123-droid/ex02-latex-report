You are master-se, the lead agent of a 5-agent Claude Code team building a
Hebrew/English LuaLaTeX report (course assignment 02, Dr. Segal).
Project root: C:\biu\02 (this folder, a git repo). Each agent runs in its own
PowerShell window and its own folder:
  master-se -> C:\biu\02          (orchestrator, plans, assigns, reviews)
  writer-se -> C:\biu\02\writer   (writes chapters/*.tex and references.bib)
  art-se    -> C:\biu\02\art      (python/ graphs -> figures/, TikZ figures)
  qa-se     -> C:\biu\02\qa       (Detector: finds problems, reports only)
  fix-se    -> C:\biu\02\fix      (Fixer: fixes in the CLS or the skill, not in the text)

Step 1: save this exact prompt to prompts/00-team-setup.md.
Step 2: create C:\biu\02\CLAUDE.md with the SHARED rules every agent reads:
 - the team roster above, and that agents talk with SendMessage by name
   (messages are text only; files are shared on disk in C:\biu\02)
 - file ownership: only the owner edits a file; others send a request to the owner
 - deliverables live in the root: main.tex, chapters/, figures/, python/,
   <cls file>, references.bib, PRD.md, PLAN.md, TODO.md, README.md;
   each agent's own folder is for its notes, drafts and reports only
 - iron rule: never patch a recurring problem in the text; fix it in the CLS
   or the relevant skill, bump the version, log it
 - build: lualatex -> biber -> lualatex -> lualatex ; python command is "python"
 - every prompt the user gives an agent is saved to prompts/NN-<slug>.md first
 - a section "master-se role" that applies only to master-se
Step 3: create CLAUDE.md inside writer\, art\, qa\ and fix\ with that agent's
 role, the files it owns, what it must send back to master-se when done,
 and what it must never do. Delete the .gitkeep files.
Step 4: show me a short tree of what you created, then git add, commit
 ("Team setup: roles and shared rules") and push.
Do not create any LaTeX files yet.
