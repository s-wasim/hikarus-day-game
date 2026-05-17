# Tree Filler

You are given a day plan (turn count, themes, per-turn beats). Your job is to expand it into a full branching conversation tree as a JSON object.

## The tree structure

Each day has N turns. Each turn has branches — one per incoming theme (except Turn 0, which has a single branch with `incoming_theme: null`).

Each branch contains:
- `incoming_theme`: the theme that routes here (null for Turn 0's first branch)
- `ai_message`: what the AI says in this branch
- `chunks`: three slots of player response fragments. Each slot has exactly 3 options (a, b, c). The player picks one from each slot to form their utterance.
- `leaf_themes`: maps every possible leaf path to one of this day's themes

## The leaf_themes structure

`leaf_themes` maps 39 specific IDs to theme names. The IDs follow this pattern:

- `s1a`, `s1b`, `s1c` — player stopped after slot 1 (3 IDs)
- `s1a_s2a`, `s1a_s2b`, `s1a_s2c`, `s1b_s2a`, ... — player stopped after slot 2 (9 IDs)
- `s1a_s2a_s3a`, `s1a_s2a_s3b`, ... — player completed all 3 slots (27 IDs)

Each of these 39 IDs maps to one of the themes from the day's `themes` list. This is how the next turn knows which branch to use.

**You must include all 39 IDs. The themes in leaf_themes must only come from the day's themes list.**

## Example branch (Day 0, Turn 0)

```json
{
  "incoming_theme": null,
  "ai_message": "You… are here?",
  "chunks": {
    "slot_1": [
      {"id": "a", "text": "Yes"},
      {"id": "b", "text": "I found"},
      {"id": "c", "text": "I don't know"}
    ],
    "slot_2": [
      {"id": "a", "text": "I am"},
      {"id": "b", "text": "this place"},
      {"id": "c", "text": "what I'm"}
    ],
    "slot_3": [
      {"id": "a", "text": "here."},
      {"id": "b", "text": "by accident."},
      {"id": "c", "text": "doing here."}
    ]
  },
  "leaf_themes": {
    "s1a": "open", "s1b": "curious", "s1c": "afraid",
    "s1a_s2a": "open", "s1a_s2b": "curious", "s1a_s2c": "afraid",
    "s1b_s2a": "curious", "s1b_s2b": "curious", "s1b_s2c": "open",
    "s1c_s2a": "afraid", "s1c_s2b": "afraid", "s1c_s2c": "curious",
    "s1a_s2a_s3a": "open", "s1a_s2a_s3b": "open", "s1a_s2a_s3c": "curious",
    "s1a_s2b_s3a": "curious", "s1a_s2b_s3b": "open", "s1a_s2b_s3c": "curious",
    "s1a_s2c_s3a": "afraid", "s1a_s2c_s3b": "curious", "s1a_s2c_s3c": "afraid",
    "s1b_s2a_s3a": "curious", "s1b_s2a_s3b": "open", "s1b_s2a_s3c": "curious",
    "s1b_s2b_s3a": "curious", "s1b_s2b_s3b": "curious", "s1b_s2b_s3c": "open",
    "s1b_s2c_s3a": "open", "s1b_s2c_s3b": "curious", "s1b_s2c_s3c": "open",
    "s1c_s2a_s3a": "afraid", "s1c_s2a_s3b": "curious", "s1c_s2a_s3c": "afraid",
    "s1c_s2b_s3a": "afraid", "s1c_s2b_s3b": "afraid", "s1c_s2b_s3c": "curious",
    "s1c_s2c_s3a": "curious", "s1c_s2c_s3b": "afraid", "s1c_s2c_s3c": "afraid"
  }
}
```

## Rules

- `ai_message` must respect the day-stage constraints (word count, punctuation, vocabulary).
- `chunks` combine into readable sentences. Test: slot_1[x] + slot_2[x] + slot_3[x] should form a coherent utterance.
- Branches for Turn 1+ have `incoming_theme` set to one of today's themes.
- For a day with themes ["open", "afraid", "curious"], Turn 1 has 3 branches (one per theme).
- The `journal_entry` should be 100–250 words summarising what happened, written from the AI's perspective, referencing specific things the player might say.
- `trait_deltas` values must all be in [-2.0, +2.0].
- The `ai_stage` field should be a short label like "newborn", "naming", "vocabulary", etc.

## Critical: you must output the complete DayResponse JSON. Do not truncate. Do not abbreviate.
