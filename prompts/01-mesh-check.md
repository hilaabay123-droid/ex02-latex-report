Save this prompt to prompts/01-mesh-check.md, then run a full mesh check.
Use ListAgents. Send every peer a PING asking it to: (1) reply
"PONG <its name>" with its own peer list, (2) send PING to every other
session including me, (3) answer every PING it gets, (4) finish with one
line: "MESH <name>: got PONG from ...". Send all PINGs in one turn and end
your turn - replies arrive as new messages, do not wait in a loop.
When all replies are in (or after 5 minutes), show two tables:
who-knows-whom and who-reached-whom, and a verdict line
"Full mesh: X of 20 links work". Write the result to docs/mesh-check.md,
turn this procedure into a skill at .claude/skills/mesh-check/SKILL.md,
then git add, commit and push.
