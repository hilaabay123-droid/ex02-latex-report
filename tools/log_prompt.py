"""Claude Code UserPromptSubmit hook: log every user prompt typed to a project agent.

Registered in the USER settings (%USERPROFILE%\\.claude\\settings.json) as:
    python C:\\biu\\02\\tools\\log_prompt.py

Reads the hook JSON from stdin ({"prompt", "cwd", "session_id", ...}).
If cwd is inside C:\\biu\\02, appends to C:\\biu\\02\\prompts\\log\\YYYY-MM-DD.md:

    ### HH:MM - <agent>
    ```
    <prompt>
    ```

It never blocks the user: no stdout, everything in try/except, always exit 0.
"""
import datetime
import json
import os
import sys

ROOT = r"C:\biu\02"
LOG_DIR = os.path.join(ROOT, "prompts", "log")
AGENTS = {"writer": "writer-se", "art": "art-se", "qa": "qa-se", "fix": "fix-se"}


def norm(path):
    return os.path.normcase(os.path.abspath(path))


def agent_for(cwd):
    """Return the agent name for cwd, or None if cwd is outside ROOT."""
    root, here = norm(ROOT), norm(cwd)
    if here != root and not here.startswith(root + os.sep):
        return None
    rel = os.path.relpath(here, root)
    first = rel.split(os.sep)[0] if rel != "." else ""
    # The root and any non-agent subfolder (docs, tools, ...) belong to master-se.
    return AGENTS.get(first, "master-se")


def fence_for(text):
    """Use a fence longer than any backtick run inside the prompt."""
    longest = run = 0
    for ch in text:
        run = run + 1 if ch == "`" else 0
        longest = max(longest, run)
    return "`" * max(3, longest + 1)


def main():
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    data = json.loads(raw)
    prompt = data.get("prompt") or ""
    cwd = data.get("cwd") or os.getcwd()
    agent = agent_for(cwd)
    if agent is None:
        return
    now = datetime.datetime.now()
    fence = fence_for(prompt)
    block = f"### {now:%H:%M} - {agent}\n{fence}\n{prompt.rstrip()}\n{fence}\n\n"
    os.makedirs(LOG_DIR, exist_ok=True)
    path = os.path.join(LOG_DIR, f"{now:%Y-%m-%d}.md")
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(block)


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        pass
    sys.exit(0)
