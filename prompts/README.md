# Documentation system

Goal: every word the user types to **any** agent of this project is documented, and so is every decision that came from it.

| Where | What | How it gets there |
|-------|------|-------------------|
| `prompts/NN-*.md` | **Curated prompts**: the important instructions, one file each, saved word for word | **Only** when a prompt starts with `Save this prompt to prompts/NN-...`. The receiving agent saves it first, at exactly the path given (the user picks the number and never renumbers it). No other message gets a curated file. |
| `prompts/log/YYYY-MM-DD.md` | **Automatic log** of every prompt typed to every agent, one file per day | The `UserPromptSubmit` hook `tools/log_prompt.py`, registered in the user settings (`%USERPROFILE%\.claude\settings.json`). No agent has to do anything. |
| `prompts/sessions/` | **Full transcripts** (prompts, answers and tool calls) | Exported by hand with `/export` in an agent's window, saved here as `<agent>-YYYY-MM-DD[-topic].md` |
| `incidents/` | **Incident investigations**: what went wrong, the timeline, the root cause, the fix and the lesson | Written when something breaks: a failed build, a lost message, a broken rule |
| `.claude/skills/` | **Skills**: repeatable procedures (for example `mesh-check`), versioned | Owned by fix-se. Changes follow the iron rule: bump the version and log it in `fix/CHANGELOG.md` |

## The automatic log
Each prompt becomes one block in that day's file:

    ### HH:MM - <agent>
    ```
    <the prompt, exactly as typed>
    ```

- The agent comes from the session's folder: the root is `master-se`, then `writer\` is `writer-se`, `art\` is `art-se`,
  `qa\` is `qa-se` and `fix\` is `fix-se`. Any other subfolder of the root, such as `docs\` or `tools\`, counts as `master-se`.
- Prompts typed in folders outside `C:\biu\02` are ignored.
- The log is the **only** record for ordinary messages. Agents do not make curated copies of them.
- The hook never blocks or slows a prompt. It prints nothing, swallows every error and always exits 0. A missing entry
  is therefore possible, though unlikely. The `/export` transcripts in `prompts/sessions/` are the backup.
- Slash commands such as `/export` are not logged. Only typed prompts are.
- A session started before the hook was added to the user settings may not log anything until it is restarted.
- The log is written in UTF-8, so Hebrew is kept as typed. If a prompt contains backticks, the fence is made longer to fit.
- Messages between agents (SendMessage) are **not** user prompts and are not logged here. They appear in the session transcripts.

## Not in git
`ref/` holds the course PDFs. They are copyrighted, so `.gitignore` excludes the folder and it is never pushed.
