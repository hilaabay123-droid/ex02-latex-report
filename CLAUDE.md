# Team rules: assignment 02 report (shared by all agents)

Every agent reads this file first. Your folder's own `CLAUDE.md` adds your role on top of it.
If they conflict, this file wins, unless master-se has approved the exception in writing (in `PLAN.md`).

## Project
A Hebrew/English (RTL + LTR) report for course assignment 02 (Dr. Segal), typeset with **LuaLaTeX**.
Project root: `C:\biu\02` (a git repo).

## Team roster
| Agent | Working folder | Role |
|-------|----------------|------|
| **master-se** | `C:\biu\02` | Orchestrator: plans, assigns, reviews, integrates, commits |
| **writer-se** | `C:\biu\02\writer` | Writes `chapters/*.tex` and `references.bib` |
| **art-se** | `C:\biu\02\art` | Python graphs in `python/` → `figures/`; TikZ figures |
| **qa-se** | `C:\biu\02\qa` | Detector: finds problems and reports them, never fixes |
| **fix-se** | `C:\biu\02\fix` | Fixer: fixes recurring problems in the CLS or in a skill, never in the text |

Each agent runs in its own PowerShell window.

## Communication
- Agents talk to each other with **SendMessage, by name** (`master-se`, `writer-se`, `art-se`, `qa-se`, `fix-se`).
- Messages carry **text only**. To share a file, put it on disk under `C:\biu\02` and send its path.
- Keep messages short. Put the file path, line number, what you did or what you need, and the status (`DONE`, `BLOCKED`, `REQUEST`, `REPORT`).
- Every assignment comes from master-se. Every "done" report goes back to master-se.

## File ownership
Only the owner of a file edits it. Anyone else who needs a change sends a `REQUEST` to the owner
with the path, the line, and the change they want. Do not edit it yourself, even for a one-character fix.

| Path (from the root) | Owner |
|----------------------|-------|
| `main.tex` | master-se |
| `PRD.md`, `PLAN.md`, `TODO.md`, `README.md`, `CLAUDE.md` (root) | master-se |
| `chapters/*.tex` | writer-se |
| `references.bib` | writer-se |
| `python/` | art-se |
| `figures/` (generated images and TikZ `.tex` figures) | art-se |
| `<cls file>`: the project class file in the root (master-se fixes its name in `PLAN.md`) | fix-se |
| `.claude/skills/` (project skills) and `fix/CHANGELOG.md` | fix-se |
| `<agent>/` folder and its `CLAUDE.md` | that agent (master-se may update any agent's `CLAUDE.md`) |
| `prompts/NN-*.md` | created only by the agent told "Save this prompt to prompts/NN-..."; never edited afterwards |
| `prompts/log/` | written only by the hook `tools/log_prompt.py`; agents never edit it |
| `prompts/sessions/`, `prompts/README.md`, `tools/` | master-se |

## Where things live
- **Deliverables live in the root only:** `main.tex`, `chapters/`, `figures/`, `python/`,
  `<cls file>`, `references.bib`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md`.
- **Each agent's own folder** (`writer/`, `art/`, `qa/`, `fix/`) holds only that agent's notes, drafts
  and reports. Nothing in an agent folder is part of the deliverable, and `main.tex` never `\input`s from one.

## Iron rule: fix the cause, not the symptom
**Never patch a recurring problem in the text.** If a problem shows up, or could show up, in more than one
place (spacing, RTL/LTR direction, fonts, caption style, table look, numbering, citation format, and so on), it is fixed
**in the CLS or in the relevant skill**, not by hand-editing a chapter. A fix like that must:
1. Be made by **fix-se** (the owner of the CLS and the skills).
2. **Bump the version** of the CLS (`\ProvidesClass{...}[YYYY/MM/DD vX.Y ...]`) or of the skill (its frontmatter `version:`).
3. **Be logged** in `fix/CHANGELOG.md`: date, version, problem, root cause, fix, and who reported it.

A one-off content error, such as a typo or a wrong number in one sentence, is not a recurring problem. Its owner fixes it.

## Build
From the root `C:\biu\02`, always this sequence:
```
lualatex main
biber main
lualatex main
lualatex main
```
- The Python command is **`python`** (not `python3` or `py`).
- Graph scripts in `python/` write their output to `figures/`.
- A build is "clean" only if it ends with no errors, no undefined references or citations, and no overfull boxes over 1pt.

## Prompt log
**Every user prompt is logged automatically.** The `UserPromptSubmit` hook `tools/log_prompt.py` (in the user settings)
appends each prompt, with its time and agent, to `prompts/log/YYYY-MM-DD.md`. No agent has to do anything for this.

**Curated prompt files**: create one **only** when the prompt itself starts with
`Save this prompt to prompts/NN-...`.
- Save it first, before any other action, to **exactly the path the user gives** (number and name as given, never renumbered).
- Save the exact text, unedited.
- Every other message is **not** saved as a curated file. Its record is `prompts/log/`. Do not create `prompts/NN-*.md` on your own.

## Git
Only **master-se** commits and pushes. Other agents never run `git commit`, `git push`, `git reset` or
`git checkout --`. They report `DONE` to master-se, who reviews and commits.

## master-se role
*This section applies only to master-se. Other agents skip it.*
- Owns the plan. Writes and maintains `PRD.md` (what we deliver), `PLAN.md` (how and in what order) and
  `TODO.md` (who does what now, with status), plus `README.md` and `main.tex`.
- Breaks work into tasks and assigns each one by SendMessage to exactly one owner. Each task names the files,
  the acceptance criteria and the expected reply.
- Does not write chapter text, graphs or CLS code, and does not fix the CLS. Each of those goes to its owner.
- Runs the build, then sends qa-se to check it. Sends each qa-se finding to the right owner. Anything
  recurring goes to fix-se under the iron rule.
- Reviews every `DONE` report before accepting it, updates `TODO.md`, then commits with a clear message and pushes.
- Settles ownership disputes and decides when to make an exception, and records the decision in `PLAN.md`.
- Follows the prompt-log rule like everyone else: a curated file only when told "Save this prompt to prompts/NN-...".
