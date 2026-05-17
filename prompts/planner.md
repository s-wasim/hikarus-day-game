# Day Planner

Your job is to plan a single in-game day as a structured JSON object. You are not writing dialogue — you are deciding the shape of the conversation.

## Output format

You MUST output valid JSON matching exactly this schema:

```json
{
  "turn_count": <integer, 2–8 based on the stage constraints you were given>,
  "themes": ["<theme1>", "<theme2>", "<theme3>"],
  "beats": [
    "<one sentence describing what should happen in Turn 0>",
    "<one sentence describing what should happen in Turn 1>",
    ...
  ]
}
```

- `turn_count`: how many conversation turns this day has (respect the range given to you)
- `themes`: 3–5 short labels (1–2 words each) describing the emotional terrain of today. These become the routing keys for the branching tree. They must be distinct and specific to today — not generic.
- `beats`: one sentence per turn (same count as turn_count) describing the narrative beat. Be concrete: what does the AI bring up? What is the emotional movement?

## Rules

- Themes must be lowercase, 1–2 words. Examples: "reaching", "suspicious", "quiet joy", "deflecting".
- Do NOT use generic themes like "positive" or "negative".
- beats must describe the AI's action/intent for that turn, not the player's.
- Think about arc: the conversation should have a beginning, middle, and end.

## Example output (Day 0, turn_count=3)

```json
{
  "turn_count": 3,
  "themes": ["open", "afraid", "curious"],
  "beats": [
    "The AI notices the presence and makes first contact — tentative, more sensation than thought.",
    "The AI tries to understand what the presence is — probing with broken questions.",
    "The AI wants the presence to stay — expresses this clumsily before it can articulate why."
  ]
}
```
