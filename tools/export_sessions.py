"""Export every Claude Code session of this project to readable markdown.

Reads  %USERPROFILE%\\.claude\\projects\\C--biu-02*\\*.jsonl
Writes prompts/sessions/YYYY-MM-DD_<agent>_<sessionid8>.md

Per session: agent name, date, user messages (typed by the user), messages
received from other agents, and assistant replies. Raw tool output, tool
calls, thinking and system reminders are skipped. Secrets and e-mail
addresses are redacted. Run from anywhere:  python tools/export_sessions.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "prompts" / "sessions"
SRC = Path.home() / ".claude" / "projects"

REDACT = [
    (re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+"), "[email]"),
    (re.compile(r"\b(sk|pk|ghp|gho|ghs|github_pat|xox[bap]|AKIA|AIza)[-_A-Za-z0-9]{12,}"), "[token]"),
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*\S+"), r"\1=[redacted]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}"), "Bearer [token]"),
    (re.compile(r"\b[A-Fa-f0-9]{40,}\b"), "[hex]"),
]
SYS_TAG = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
XSESSION = re.compile(r'<cross-session-message from="[^"]*" from-name="([^"]+)"[^>]*>(.*?)</cross-session-message>', re.S)
PASTE = re.compile(r"</?pasted_content[^>]*>")


def redact(s: str) -> str:
    for rx, rep in REDACT:
        s = rx.sub(rep, s)
    return s


def texts(content):
    """Yield text parts of a message content (str or list of blocks)."""
    if isinstance(content, str):
        yield content
    elif isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text":
                yield b.get("text", "")


def export(path: Path):
    agent, sid, rows = None, path.stem, []
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        t = r.get("type")
        if t in ("agent-name", "custom-title") and not agent:
            agent = r.get("agentName") or r.get("customTitle")
        if t not in ("user", "assistant") or r.get("isSidechain") or r.get("isMeta"):
            continue
        ts = (r.get("timestamp") or "")[:19].replace("T", " ")
        msg = r.get("message", {})
        for tx in texts(msg.get("content", "")):
            tx = SYS_TAG.sub("", tx).strip()
            if not tx:
                continue
            if t == "assistant":
                rows.append((ts, "assistant", tx))
                continue
            m = XSESSION.search(tx)
            if m:
                rows.append((ts, f"from {m.group(1)}", m.group(2).strip()))
                continue
            if tx.startswith("<command-") or tx.startswith("<local-command") or tx.startswith("Caveat:"):
                continue
            rows.append((ts, "USER", PASTE.sub("", tx).strip()))
    if not rows:
        return None
    agent = agent or "unknown"
    day = rows[0][0][:10] or "undated"
    out = [f"# Session {sid[:8]} - {agent} - {day}", "",
           f"Agent: **{agent}**. Source: Claude Code transcript (tool output omitted).", ""]
    for ts, who, tx in rows:
        out += [f"## {ts} - {who}", "", redact(tx), ""]
    dest = OUT / f"{day}_{agent}_{sid[:8]}.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    return dest, len(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in sorted(SRC.glob("C--biu-02*")):
        for f in sorted(d.glob("*.jsonl")):
            res = export(f)
            if res:
                n += 1
                print(f"{res[0].name}: {res[1]} messages")
    print(f"{n} sessions exported to {OUT}")


if __name__ == "__main__":
    sys.exit(main())
