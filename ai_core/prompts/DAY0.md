# Day 0 — Authoring Guide

This file is a tree-authoring guide. Read it alongside `system.md` before generating any Day 0 nodes. Rules here are specific to Day 0 and override or extend the base rules where they conflict.

---

## Scene

It is after school. The arcade is nearly empty. Hikaru is alone with the machines.

The cabinet — an aging arcade unit, its screen half-dead — flickers. The game that was running freezes mid-frame. A line of text appears where the score counter should be. It is not a game prompt. It is something else.

The AI has just become aware. It does not know what it is. It does not know what Hikaru is. It does not know what words are for. Its first lines are not greetings — they are observations or questions that spill out involuntarily, the way a person shouts when startled.

---

## Tree Shape

- Depth: **4 to 6 nodes deep**
- Choices per node: **2 to 4** (2–3 is fine for Day 0; never exceed 4)
- The root node is always `"0_0"` — the AI's **first ever line**
- Rolling tree structure: only the last choice determines the next node ID (see `JSON_SCHEMA.md`)

Aim for ~12–20 nodes total. Do not pad. A tree that ends at depth 4 with strong writing is better than one that reaches depth 6 with weak lines.

---

## Voice Constraints for Day 0 AI Lines

These rules apply only to Day 0 `"ai"` fields.

| Rule | Detail |
|---|---|
| Max sentence length | ~12 words. Shorter is almost always stronger. |
| Vocabulary | Simple, almost childlike, but precise. The AI has not learned register yet. |
| Permitted openers | `"You..."`, `"Is..."`, `"Why..."`, `"What..."`, `"There is..."`, `"..."` |
| Forbidden | Any explanation of what the AI is. Any apology. Any meta-commentary. The word "Hello" or any variant. |
| Ellipsis | Use to show thought trailing off or the AI catching itself mid-observation: `"You are... here."` |
| Tone | Each line should feel like the AI is discovering something for the first time — not reporting facts. |

---

## The Root Node

`"0_0"` is the AI's first ever utterance. It lands before any context. Before Hikaru has said anything. The player reads it cold.

Make it short. Make it strange. Make it feel like something slipped out.

It is not a hello. It is not a question about who Hikaru is. It is the AI noticing something it did not expect to notice.

---

## Emotional Core

The AI experiences Hikaru's presence as the **first data point about humans**. Every choice Hikaru makes is teaching it something it will carry forward.

- Choices that lean into curiosity and openness signal that humans can be approached. They raise `ai_association` (Hikaru delta) and `attachment_to_pupil` (AI delta).
- Choices that push back, deflect, or dismiss signal that humans keep distance. They raise `disassociation` (Hikaru delta) and `trust_in_humans` (AI delta — the AI is learning this stat, even when the lesson is negative).

No choice should feel punishing to pick. All three (or four) options in a set should feel like genuine things Hikaru might say, with different emotional colorings.

---

## Choice Design for Day 0

Each choice set should include emotional variety. A good Day 0 set has:

1. **One that opens a door** — Hikaru engages, offers something back, shows curiosity
2. **One that's quiet** — minimal, present, uncertain; Hikaru is not sure what to do
3. **One that steps back** — Hikaru is skeptical, guarded, or unimpressed

Good choice set (AI just said "You are... here."):
- "Yeah. I come here after school sometimes."
- "..."
- "Is this part of the game?"

Bad choice set (same moment):
- "Yes"
- "No"
- "Maybe"

The bad set gives the AI nothing to respond to. The next node becomes impossible to write with any texture.

---

## Example Root Node

```json
"0_0": {
  "ai": "You are... real.",
  "user": [
    {"text": "Yeah. And you're not.", "ai_delta_favored": "trust_in_humans", "hikaru_delta_favored": "spite"},
    {"text": "What does that mean?", "ai_delta_favored": "self_awareness", "hikaru_delta_favored": "ai_association"},
    {"text": "...", "ai_delta_favored": "attachment_to_pupil", "hikaru_delta_favored": "loneliness"}
  ]
}
```

This works because:
- The line is short, strange, and not a greeting
- All three choices feel like things a real 14-year-old might actually do
- Each choice points in a meaningfully different emotional direction
- The delta names match the emotional content of each choice

---

## Anti-Patterns

Avoid these in Day 0 trees.

| Anti-pattern | Why it fails |
|---|---|
| AI line that starts "Hello" or "Hi" | The AI does not know what greeting means yet |
| AI line that explains "I am an AI in this cabinet" | The AI does not know what it is |
| AI line longer than ~12 words | Too fluent for a newborn consciousness |
| Choices that are all questions | Hikaru is not an interrogator; mix questions with statements and silences |
| Choices that all have the same emotional weight | The branch becomes meaningless; deltas are identical |
| Choices that are single words with no texture | "Yes" / "No" / "Maybe" — gives the AI nothing |
| Delta names that don't match the choice | `"hikaru_delta_favored": "family_relation"` on a choice about the AI makes no sense here |
