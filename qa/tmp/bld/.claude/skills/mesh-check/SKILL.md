---
name: mesh-check
description: Check that every Claude session on the team can message every other one (a full PING/PONG mesh), then report who-knows-whom, who-reached-whom and an "X of N links work" verdict. Use when the user asks for a mesh check, a connectivity test, or "can all agents talk to each other". Run only by master-se.
version: 1.0
---

# mesh-check

Tests the SendMessage mesh between all team sessions. With S sessions there are S × (S − 1) directed links
(5 sessions → 20). A link **A → B works** when A sent `PING` to B and received `PONG B` back.

## Steps (master-se)
1. Save the user's prompt to `prompts/NN-<slug>.md` (shared rule).
2. Run `ListAgents` and write down the peer names. This is master-se's row of "who knows whom".
3. In **one turn**, send every peer this message with SendMessage (replace `<name>` and the peer list):
   ```
   PING from master-se: mesh check. Please:
   (1) Reply to master-se with "PONG <name>" and your own peer list from ListAgents (names only).
   (2) Send "PING from <name>" to every other session, including master-se.
   (3) Answer every PING you receive with "PONG <name>" to its sender.
   (4) When you have the PONGs back, send master-se one line: "MESH <name>: got PONG from <names>".
   Do not wait in a loop. Replies arrive as new messages. No file edits are needed.
   ```
4. **End the turn.** Do not poll or sleep. Replies arrive as new messages.
5. As messages arrive:
   - `PONG <x>` with a peer list: fill row x of "who knows whom", and mark master-se → x as working.
   - `PING from <x>`: reply `PONG master-se` to x right away.
   - `MESH <x>: got PONG from ...`: fill row x of "who reached whom". If a later MESH line from x arrives, it replaces the earlier one
     (a "pending" PONG often just arrives late).
6. Stop when every peer has sent its MESH line, or after **5 minutes** (if you have no timer, the user nudges you).
   A missing MESH line counts as failed links for that row, and the report says so.
7. Write `docs/mesh-check.md` with:
   - **Who knows whom**: an S×S table (row = the session, ✅ = that peer is in its ListAgents)
   - **Who reached whom**: an S×S table (row = the PING sender, ✅ = it got the PONG back, ❌ = it did not)
   - the MESH lines received, verbatim, plus notes on any delays
   - the verdict line: `Full mesh: X of N links work`
8. Show both tables and the verdict to the user, then `git add` / commit / push (only master-se commits).

## If a link fails
- The peer is missing from ListAgents: that session isn't running. Ask the user to start it.
- `[Cross-session delivery notice]` (held or refused): the session uses a different permission mode or refuses
  messages. Tell the user, and don't try to route around it.
- One direction works and the other doesn't: re-send just that PING once, then report it.
