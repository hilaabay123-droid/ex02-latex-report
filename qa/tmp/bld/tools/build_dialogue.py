"""Build prompts/MY-DIALOGUE-WITH-THE-AGENTS.md from prompts/sessions/*.md.

Every message the user typed to any agent, in time order, with date, time and
agent name, followed by a short summary of what the agent answered (the first
sentences of its last reply before the user's next message).
Run after tools/export_sessions.py.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SESS = ROOT / "prompts" / "sessions"
OUT = ROOT / "prompts" / "MY-DIALOGUE-WITH-THE-AGENTS.md"

HDR = re.compile(r"^## (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}):\d{2} - (.+)$", re.M)
SKIP_START = ("<task-notification", "[Request interrupted", "<system-reminder", "Another Claude session",
              "<agent-message")


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"# Session (\w+) - (\S+) - ", text)
    agent = m.group(2) if m else "unknown"
    heads = list(HDR.finditer(text))
    rows = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        rows.append((h.group(1), h.group(2), h.group(3), text[h.end():end].strip()))
    return agent, rows


def summary(txt: str, limit=330) -> str:
    txt = re.sub(r"```.*?```", "", txt, flags=re.S)
    txt = re.sub(r"[#*`|>]", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) <= limit:
        return txt
    cut = txt[:limit]
    k = max(cut.rfind(". "), cut.rfind("? "), cut.rfind(": "))
    return (cut[:k + 1] if k > 120 else cut.rsplit(" ", 1)[0] + " ...")


def main():
    items = []
    for f in sorted(SESS.glob("*_*_*.md")):
        agent, rows = parse(f)
        for i, (d, t, who, body) in enumerate(rows):
            if who != "USER" or body.startswith(SKIP_START) or not body:
                continue
            reply = ""
            for d2, t2, who2, body2 in rows[i + 1:]:
                if who2 == "USER":
                    break
                if who2 == "assistant":
                    reply = body2
            items.append((d, t, agent, body, summary(reply) if reply else "(no reply recorded in this session)"))
    items.sort(key=lambda x: (x[0], x[1]))

    out = ["# My dialogue with the agents", "",
           "One readable record of every message the user typed to any of the five agents "
           "(master-se, writer-se, art-se, qa-se, fix-se), in time order across all days, "
           "each followed by a short summary of what the agent answered or did. "
           "Times are local. The summaries are the opening of the agent's last reply to that message.", "",
           "## Guide: what each prompt stage was for", "",
           "| Stage | Prompt file | Purpose |", "|---|---|---|",
           "| 00 | [prompts/00-team-setup.md](00-team-setup.md) | Create the five-agent team, folders, roles and rules (`CLAUDE.md`) |",
           "| 01 | [prompts/01-mesh-check.md](01-mesh-check.md) | Check that every agent can message every other agent |",
           "| 02 | [prompts/02-documentation-system.md](02-documentation-system.md) | Documentation system: PRD, PLAN, TODO, prompt log |",
           "| 03 | [prompts/03-expert-committee.md](03-expert-committee.md) | Expert committee and red team of the PRD |",
           "| 04 | [prompts/04-cls-template.md](04-cls-template.md) | Build the LuaLaTeX class `closettwin.cls` (cover, Hebrew/English, components) |",
           "| 05 | [prompts/05-skills-and-full-draft.md](05-skills-and-full-draft.md) | QA/production skills and the first full draft |",
           "| 06 | [prompts/06-qa-incidents-redteam.md](06-qa-incidents-redteam.md) | Transcripts, nine user-found incidents, full QA, content red team |", "",
           "Other records: the automatic log of every prompt is in [prompts/log/](log/); full session "
           "transcripts (tool output omitted) are in [prompts/sessions/](sessions/); the skills the team "
           "uses are in [.claude/skills/](../.claude/skills/); incidents are in [incidents/](../incidents/); "
           "QA reports in [qa/reports/](../qa/reports/).", "",
           f"Total: {len(items)} messages.", "", "---", ""]
    cur = None
    for d, t, agent, body, rep in items:
        if d != cur:
            out += [f"## {d}", ""]
            cur = d
        out += [f"### {t} - {agent}", ""]
        if len(body) <= 600:
            out += ["> " + body.replace("\n", "\n> "), ""]
        else:
            first = summary(body, 260)
            out += [f"> {first}", "", "<details><summary>full text</summary>", "", "```text", body, "```", "", "</details>", ""]
        out += [f"**Agent:** {rep}", ""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"{len(items)} messages -> {OUT}")


if __name__ == "__main__":
    main()
