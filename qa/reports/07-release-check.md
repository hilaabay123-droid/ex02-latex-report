# QA report 07: release check (prompt 07 part 3)      build d969d17 (3 tracked files modified: fix/tests/s24img-*.png, prompts/log/2026-11-21.md)      2026-11-21

Tool: `qa/scripts/release_check.py --history` (secrets are masked in all output). Detector only: nothing in the repository was edited. Raw output: `qa/tmp/rel_out.txt` (not tracked).

## Summary
**Blockers 0. Majors 0 real (5 flagged by the script, all false positives or accepted; see below). Minor 2.** The release is clean for the four requested checks, with one open decision for master-se: what is in the git history (REL4-history).

## REL1: fresh clone of HEAD, 4-command build  **PASS**
`git clone . qa/tmp/rel` then `lualatex --disable-installer main`, `biber main`, `lualatex ...`, `lualatex ...`: exit codes 0, 0, 0, 0; 0 errors, 0 undefined. Pages: clone **46** = committed `main.pdf` **46**. `pdftotext -layout` of the clone PDF is byte-identical to the committed `main.pdf`.

## REL2: required files tracked  **PASS**
Tracked (314 files in total): `main.tex`, `closettwin.cls`, `references.bib`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md`, `main.pdf`, and tracked files under `chapters/` (11 `.tex`), `prompts/`, `.claude/skills/`, `python/`, `figures/`, `fonts/`.

## REL3: .gitignore, junk, gitlinks  **PASS**
- No gitlink (mode 160000) is tracked. `qa/tmp`, `qa/build`, `qa/b4out*` are no longer tracked (the tracked count fell from 586 to 314), and `.gitignore` has entries for them, for `fix/bld`, `art/test`, `ref/` and the LaTeX build files.
- 0 tracked build-junk files (`*.aux *.log *.bbl *.bcf *.blg *.toc *.lof *.lot *.out *.run.xml`), 0 files in `ref/`, no tracked file over 5 MB.
- Minor (not a defect): 3 tracked files are modified in the working tree (`fix/tests/s24img-1.png`, `fix/tests/s24img-2.png`, `prompts/log/2026-11-21.md`; the log is rewritten by the hook on every prompt). They do not affect the build.

## REL4: ID numbers, e-mails, tokens, passwords
### Tracked files at HEAD (314 files)  **PASS, no real secret**
- E-mails: 1, `@example.invalid` in `qa/tests/run_selftest.py` (a test fixture). The user's own address is not in any tracked file.
- Tokens/passwords: the script's 4 "password-like" hits are not secrets: `closettwin.cls:257` and `writer/test/closettwin.cls:220` are TeX code (`token: float...`), `qa/scripts/release_check.py:19` is my own regular expression, and `prompts/sessions/2026-11-21_qa-se_d1f5cb40.md:108` is the text `token=[redacted]`. No API key, private key or credential string was found.
- Nine-digit numbers (the course number 875523402 and `sg00ha11` are allowed): 0 personal IDs. All hits were looked at with digits masked: 37 + 4 are session pipe names (`\pipe\LOCAL\cc-msg-...`) in `prompts/log/`, 1 is a google/fonts commit hash and 4 are font-file sizes/hashes in `fonts/SOURCES.md`, 1 is a DOI part in `references.bib`, 1 is in `fix/cls-feasibility.md` (same font hash), 1 is a masked fake value `0…0` in `prompts/log/2026-11-20.md`, and `qa/tests/run_selftest.py` and `qa/reports/05-qa-super-round3.md` contain my fabricated test values (123456780 and similar, accepted by master-se in round 3).

### Git history (all commits, added lines)  **OPEN, for master-se's decision; no rewrite done**
56 distinct hits (masked): 42 nine-digit numbers, 8 token-like strings, 6 e-mails. Only the 3 groups below matter; the rest are the same fake test values and font/DOI numbers as above.
1. **Third-party web-page copies, commit fedf4b3 (no longer in HEAD, but in history):** `qa/tmp/src/cs.dat` (Coresight; 14 hits), `nrf.dat` (4), `p3.dat` (2), `kings.dat` (2), `imarc.dat` (1), `appriss.txt` (1). They hold publisher contact e-mails (coresight, nrf, kingsresearch, appriss: 6 addresses, all company addresses), 2 `token="..."` strings embedded in the pages (one starts with a JWT prefix) and many numbers that are page data. They look like public page content, not the team's secrets, but they are also copies of copyrighted pages.
2. **Fabricated test fixtures:** `qa/tmp/planted/*`, `qa/tests/run_selftest.py` (5 hits, from commit 904c663), `qa/reports/05-qa-super-round3.md`: fake nine-digit values made by me for the scanner self-test (not real IDs).
3. **TeX/other false positives:** `closettwin.cls` (b36ac78, fedf4b3) and `writer/test/closettwin.cls`: the word "token" in TeX code.
No hit is the user's e-mail address or a real ID number. Real ID/e-mail/token exposure: none found. If the user wants the third-party page copies out of the public history, that is a history rewrite (the user's decision, pending).

## REL5: README links and images, exact case  **PASS**
66 relative links and image paths in `README.md` (including `docs/screenshots/agents-working.png`, which is tracked as `docs/screenshots/agents-working.png`, same case) all resolve to tracked files or folders with a tracked file. 0 case mismatches, 0 missing targets. External `http(s)` links were not fetched (the check is about the repository).

## Findings
- **F-rel-01 [minor]** REL4-history: third-party page copies and their e-mails/tokens remain in history (fedf4b3). Owner: master-se (user decision, no action unless the user asks for a rewrite). Status: open, accepted as "report only".
- **F-rel-02 [minor]** working tree: 3 tracked files modified (see REL3). Owner: master-se (commit or ignore before the final push). Status: open.

## Tool note
The 5 "major" lines of the script (4 password-like words in TeX/regex/redacted text and the history summary) were checked by hand and are false positives or the item above; I will tighten the patterns in `release_check.py`.
