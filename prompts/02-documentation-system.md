Save this prompt to prompts/02-documentation-system.md, then execute it.

Goal: every word I type to ANY agent of this project is documented automatically.
1. Add "ref/" to .gitignore (course PDFs are copyrighted, never push them).
   Add docs/screenshots/01-mesh-check.png to git.
2. Create tools/log_prompt.py - a Claude Code UserPromptSubmit hook.
   It reads the hook JSON from stdin (prompt, cwd, session_id).
   If cwd is not inside C:\biu\02 -> exit 0 silently.
   Map cwd to agent: root=master-se, writer=writer-se, art=art-se, qa=qa-se, fix=fix-se.
   Append to C:\biu\02\prompts\log\YYYY-MM-DD.md a block:
   "### HH:MM - <agent>" followed by the prompt in a fenced block. UTF-8.
   It must never block me: no stdout, everything in try/except, always exit 0.
3. Register it in my USER settings (%USERPROFILE%\.claude\settings.json)
   under hooks -> UserPromptSubmit, command: python C:\biu\02\tools\log_prompt.py
   (user level, because the agents run in different sub-folders).
   Keep every existing setting. Show me the diff before saving.
4. Create prompts/README.md explaining the documentation system:
   prompts/NN-*.md = curated prompts; prompts/log/ = automatic log of every
   prompt; prompts/sessions/ = full transcripts exported with /export;
   incidents/ = incident investigations; .claude/skills/ = skills.
5. Commit and push.
