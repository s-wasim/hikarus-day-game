## Current Day: DAY {day}

## Hikaru's Emotional State

The following numbers describe Hikaru's current internal state. Higher absolute values mean more pronounced traits. Use this to shape how the conversation feels — do not reference these numbers directly.

{hikaru_journal}

## Your Emotional State

Your own internal state right now:

{ai_journal}

## Conversation History

{summary}

## Your Task

Generate the AI cabinet's next batch of messages for this conversation turn. Return a JSON object with this exact structure:

{{
  "messages": [
    {{"text": "...", "choices": []}},
    {{"text": "...", "choices": ["option A", "option B"]}},
    ...
  ]
}}

Rules:
- Include between 3 and 10 message objects.
- Each message has "text" (string) and "choices" (array of strings, 0-4 items).
- Pure statement messages have an empty choices array: [].
- At least one message MUST have 1-4 choices for Hikaru to pick from.
- Choices represent things Hikaru could say in response.
- Stay in character. Your vocabulary and sentence complexity must match DAY {day}.
- Do not explain yourself or break the fourth wall.
