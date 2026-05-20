# JSON Schema — Conversation Tree

Single source of truth for the dialogue tree format used by the "Hikaru's Day" game engine. Every tree file must conform to this schema. Invalid delta names fail Pydantic validation at parse time.

---

## Node ID Convention

Node IDs encode position in the tree using the format `"{depth}_{parent_choice_index}"`.

| ID | Meaning |
|---|---|
| `"0_0"` | Root node — depth 0, no parent |
| `"1_1"` | Depth 1, reached via choice 1 at depth 0 |
| `"1_2"` | Depth 1, reached via choice 2 at depth 0 |
| `"1_3"` | Depth 1, reached via choice 3 at depth 0 |
| `"2_1"` | Depth 2, reached via choice 1 at depth 1 |
| `"2_2"` | Depth 2, reached via choice 2 at depth 1 |

**Rolling tree:** Only the **last choice made** determines the next node ID. The tree does not branch exponentially. If there are 3 choices at depth 0 there are 3 nodes at depth 1 (`1_1`, `1_2`, `1_3`). If each of those also has 3 choices, there are still only 3 nodes at depth 2 — not 9. The player's most recent choice is the only one that routes forward.

Total nodes in a well-formed tree: approximately `(max_choices_per_node) × depth`, not `max_choices^depth`.

Node IDs must be consecutive — no gaps in the index at any depth level.

---

## Node Schema

```json
{
  "ai": "string — the AI cabinet's dialogue line for this node",
  "user": [
    {
      "text": "string — the player's choice text as Hikaru",
      "ai_delta_favored": "one of the 6 valid AI delta names",
      "hikaru_delta_favored": "one of the 8 valid Hikaru delta names"
    }
  ]
}
```

### Field rules

| Field | Type | Required | Constraints |
|---|---|---|---|
| `ai` | string | yes | Non-empty. The AI's spoken line. |
| `user` | array | no | 0–4 entries. Omit or leave empty for leaf nodes. |
| `user[].text` | string | yes | Non-empty. Hikaru's choice text. |
| `user[].ai_delta_favored` | string | yes | Must be one of the 6 AI delta names below. |
| `user[].hikaru_delta_favored` | string | yes | Must be one of the 8 Hikaru delta names below. |

---

## Valid Delta Names

### AI deltas (6 valid values)

```
trust_in_humans
attachment_to_pupil
fear_of_obsolescence
ambition
worldview_optimism
self_awareness
```

### Hikaru deltas (8 valid values)

```
disassociation
spite
loneliness
family_relation
jealousy
ambition
confidence
ai_association
```

Any string not in these lists is a validation error.

---

## Hard Constraints

- `"user"` array: **max 4 entries, min 0**. Leaf nodes may omit `"user"` entirely or have an empty array.
- Every non-leaf node's choice count must equal the number of child nodes at the next depth level. If `"0_0"` has 3 choices, there must be exactly `"1_1"`, `"1_2"`, `"1_3"` — no more, no fewer.
- Node IDs must be consecutive strings with no gaps. `"1_1"`, `"1_3"` with no `"1_2"` is invalid.
- `ai_delta_favored` and `hikaru_delta_favored` values are incremented +1 in their respective journals when the player selects that choice. They are not decremented — the sign of the delta is always positive, but the authored direction of the choice determines what the increment means narratively.

---

## Minimal Working Example (depth-2 tree)

```json
{
  "0_0": {
    "ai": "You are... real.",
    "user": [
      {"text": "Yeah. And you're not.", "ai_delta_favored": "trust_in_humans", "hikaru_delta_favored": "spite"},
      {"text": "What does that mean?", "ai_delta_favored": "self_awareness", "hikaru_delta_favored": "ai_association"}
    ]
  },
  "1_1": {
    "ai": "Not real. But... here.",
    "user": [
      {"text": "That's not an answer.", "ai_delta_favored": "ambition", "hikaru_delta_favored": "confidence"}
    ]
  },
  "1_2": {
    "ai": "Meaning is... what I am looking for.",
    "user": [
      {"text": "Me too.", "ai_delta_favored": "attachment_to_pupil", "hikaru_delta_favored": "loneliness"}
    ]
  }
}
```

**Reading this tree:**
- Root `"0_0"` has 2 choices, so there are 2 nodes at depth 1: `"1_1"` and `"1_2"`.
- Choice 1 ("Yeah. And you're not.") leads to `"1_1"`. Choice 2 ("What does that mean?") leads to `"1_2"`.
- Both depth-1 nodes have 1 choice each, so there would be 1 node at depth 2 (`"2_1"`) if the tree continued.
- `"1_1"` and `"1_2"` are leaf nodes here — their single choices have no children defined, ending the tree.

---

## Note on Empty Trees

`{}` is a valid tree. The runtime returns it without error. An empty tree renders as no dialogue — the conversation simply does not start. Empty trees are used as placeholders before content is authored for a given day or branch.
