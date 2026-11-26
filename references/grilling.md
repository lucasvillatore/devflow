# Grilling

Adapted from Matt Pocock's `grilling` skill (MIT, see `THIRD_PARTY_NOTICES.md`).

Interview the user relentlessly until you reach a shared understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask now without guessing at answers you have not heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format of a round:

```
❓ **Q1** - **<question title>**: <question body, with the options when there are any>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

Each round reshapes the tree: settled decisions push the frontier outward. Recompute the frontier and ask the next round. A question that depends on another question still open in this round belongs to a later round.

**Facts and decisions.** Decisions are the user's: put each to them and wait.
Facts you find yourself only where it is cheap and quiet: the Issue workspace, the Vault, a file the user pointed to. Do not send agents to explore code. When a decision needs a fact from the code, ask the user, or ask to do a targeted search (one grep, one file) and do it only when they agree.

When the user pastes a real data sample (a JSON payload, an API response), treat it as the source of truth for that contract.

The interview is done when the frontier is empty: every branch visited, nothing silently assumed. Do not act on it until the user confirms you are aligned.
