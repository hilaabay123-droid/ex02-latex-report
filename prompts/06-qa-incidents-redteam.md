Save this prompt to prompts/06-qa-incidents-redteam.md, then execute it.
All 5 agents are online. Work autonomously; stop only at the end.

PART 0 - Transcripts. Claude Code keeps every session of this project in
%USERPROFILE%\.claude\projects\ (folders whose names start with C--biu-02).
Write tools/export_sessions.py that converts every session there into a
readable markdown file in prompts/sessions/ (one file per session:
agent name, date, user messages, assistant replies, and messages received
from other agents; skip raw tool output). Check the result contains no
tokens, passwords or e-mail addresses. Run it now.

PART 1 - Incidents. I found these defects myself in draft v1
(the automatic QA did not catch them):
 I-1 Chapter 1 key-number box shows "$685 B--$890 B": a literal double
     hyphen instead of an en dash. Probably in every key-number box.
 I-2 Hebrew executive summary: stray numbers 1, 2, 3 in the left margin.
 I-3 List of Tables, entry 6.1: internal text like "(table_check_set_...)"
     leaks into the caption.
 I-4 Table 8.1 (Main inputs): too narrow, the first column wraps badly
     with stretched spaces. Use full text width, ragged-right text columns.
 I-5 Appendix A: the code box splits and leaves 3 lines alone on the
     last page.
 I-6 Page 25 (8.3): "6.03%" is set in the math font while "4.52%" next to
     it is in Rubik. Numbers in running text must always use the text font.
 I-7 The small mocha superscript "D" after numbers: make sure a legend
     explains it (D = derived, A = assumed) before its first use; if none
     exists, add one.
 I-8 Page 25: ~40% of the page is empty after "Table 8.1 lists the
     inputs" - the table floats to the next page. Prevent such gaps.
 I-9 Cover: the course number is missing - must read
     "Generative AI for Management (875523402)".
 Also: align the "Contents" title with the mocha rule above it.
For EACH: run the incident skill -> incidents/NN-<slug>.md (what happened,
root cause, why no detector caught it, fix in the CLS or skill - not in
the text, and the new check added to the relevant qa-* skill).
Recurring causes are fixed in the class (bump version + CHANGELOG).

PART 2 - Full QA: qa-se runs qa-super on the whole PDF (with the new
checks). fix-se runs qa-fixer. Repeat until no blocking findings
(max 3 rounds). Keep every report in qa/reports/.

PART 3 - Red team on CONTENT: run the red-team skill (course book Prompt 9)
as a fresh subagent on a different model than the writers (opus): the 10
weakest points of the business plan, with page and sentence, no praise -
especially the financial logic (funding ask, no profit in 5 years,
break-even), unsupported claims, and source-claim mismatches.
You decide Adopted/Rejected + reason for each in docs/red-team-review.md.
writer-se / qa-se fix the adopted ones (1 round). Then one final qa-super.

PART 4 - FINISH:
a) Re-run tools/export_sessions.py.
b) Create prompts/MY-DIALOGUE-WITH-THE-AGENTS.md - ONE readable file for
   the lecturer: every message I typed to any agent, in time order across
   all days and all 5 agents, each with date, time and agent name, followed
   by a 1-2 line summary of what the agent answered or did. Start it with
   a short guide: what each prompt stage was for, and links to
   prompts/NN-*.md, prompts/log/, prompts/sessions/ and .claude/skills/.
   Build it from prompts/sessions/ so it also covers the first day.
c) Build, commit, push. Show me: page counts, the incident list, the
   red-team table (point -> decision), open findings, and render
   docs/screenshots/draft-v2-contact.png.
