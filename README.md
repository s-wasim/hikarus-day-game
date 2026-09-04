# Hikaru's Day

This is the API implementation of the game, Hikaru's Day. The story revolves around a 14 year old school kid in the early 2000s Japan. To escape his monotonous life and loneliness, he finds solace in an arcade owned by Mr. Yamada. On a particular day, he encounters a game that is an AI. Unknown to him, he makes or breaks the world using his conversations with the AI.

---

## Repo Setup



---

## Story Points

Each point here determines what ending plays out.

- Hikaru's points determine how the pre-configured responses are generated.
- AI's points determine what responses the AI generates and how the story plays out.

Hikaru's responses to AI's questions determine exactly how the AI updates its points at the end of the day.

### Hikaru's Points

| Journal Sentiment | Description | Affect |
| --- | --- | --- |
| Disassociation | Hikaru's sentiment against his life | Conversation is more disassociated. Hikaru will be compelled to feel less compassion towards people. |
| Spite | Hikaru's feelings towards other people | Conversation is steered towards resentment of other people in the world. |
| Loneliness | Hikaru's mental state W.R.T socialising with PEOPLE | Conversations would be steered towards more association with the AI as Hikaru feels more connection with it. |
| Family Relation | Hikaru's sentiment towards the values of family | Conversations would deliberately avoid discussions about family, and when talked about Hikaru would showcase negativity about family and the meaning of it. |
| Jealousy | Trait of Jealousy | Conversations would steer towards the disparity amongst the working class and the elite. Hikaru would deliberately present an unfair world-view if Jealousy is high. |
| Ambition | How ambitious Hikaru gets | Conversations would steer towards how ambitious Hikaru is. |
| Confidence | Hikaru's confidence level | Conversations would be more energetic and Hikaru would try to talk more about himself. |
| Association with AI | Hikaru's sentiment towards the AI | This starts off with +5 Points. If Hikaru does not respond much to the AI this score drops. Reaching -5 Points concludes the game on DAY 0 as Mr. Yamada unplugs and sells the machine. |

### <AI_NAME_PLACEHOLDER>'s Points

> ONLY 6 POSSIBLE SENTIMENTS DRIVING THE AI TO A POSSIBLE ENDING FOR THE GAME

| AI Sentiment | Description | Affect |
| --- | --- | --- |

---

## Story Line

### DAY 0

***The Setting:*** _A pleasant and calm room with books scattered around, broken by the ringing of his alarm. Retro-themed Japanese-style traditional room. **It is the edge of winter right now with mild rain in the evening.**_

A dialogue box appears with Hikaru's face.

- Hikaru: "..."
- Hikaru: "Yet... another day..."

```
The user is prompted with the option to:
    "Wake up"
    OR
    "Go to sleep"
```

**CHOICE CONSEQUENCE:** Going back to sleep adds 1 point to disassociation.

At this point, the screen goes blank and in the next moment, Hikaru is ready for school in a black uniform.

```
The user is free to explore the room. They can interact with a few selected objects.
Finding a picture of him and his friend on the bookshelf makes him feel slightly happy.
The player at this point should explore the room as they have their homework on the desk.
```

When Hikaru lingers on the picture frame:

- Hikaru: "...<PLACEHOLDER_FOR_FRIEND_NAME>. It's been a while."

**CHOICE CONSEQUENCE:** Leaving homework on the desk would add 1 point to spite, as later on the line he would get punished if he forgets it. Checking <PLACEHOLDER_FOR_FRIEND_NAME>'s picture reduces 1 point from loneliness.

Stepping out of the room changes the scenery.

***The Setting:*** _Ground floor of the house where the kitchen is visible. NO INTERACTIONS possible here. His mother is in the kitchen preparing breakfast, facing away towards the washing basin._

Depending on the earlier choice, his mother will have one of the following two conversations once Hikaru crosses the kitchen's sliding doors:

1. IF HIKARU WOKE UP ON TIME:
   - Mother: "Off to school already? I prepared your bento box. Here is your lunch."
   - *(Mother turns to face Hikaru and a popup shows "Bento Box added".)*

2. IF HIKARU WOKE UP LATE:
   - Mother: "You're late again! Hurry to school now or you'll be punished again!"
   - *(Mother does not turn around. The bento box stays on the counter and Hikaru proceeds outside.)*

```
Option 1 adds the bento box to his inventory, which leaves an opportunity to decrease the loneliness score later when he shares his lunch with a peer.
Option 2 does not affect loneliness at this point. It leaves no room for reduction in loneliness.
```

**CHOICE CONSEQUENCE:** Option 1 adds a point to Family Relation whereas Option 2 reduces a point.

***The Setting:*** _The scenery is now outside his house. A suburban village with narrow streets._

There are a few artifacts on the way that Hikaru could interact with:

- Cat
- Luxury car on the street
- School Bullies on the way to school (absent if Hikaru woke up on time)
- Vending machine (Hikaru does not have money)
- Alternate path to avoid school bullies

Sample reactions for each interaction:

- **Cat** — Hikaru: "Hey... you're still here. Good."
- **Luxury car** — Hikaru: "...must be nice."
- **Bullies** —
  - Bully: "Oi, late again? Hand over whatever you've got, kid."
  - Hikaru: "...just leave me alone."
- **Vending machine** — Hikaru: "...not today. Not any day."
- **Alternate path** — Hikaru: "Long way around. Worth it."

**CHOICE CONSEQUENCE:**

- Interacting with the Cat removes a point from disassociation.
- Watching the luxury car and vending machine adds a point to jealousy. Watching the luxury car also adds a point to ambition.
- Interaction with the bullies adds a point to spite.
- Avoiding the bullies keeps scoring unchanged.
- If Hikaru does not interact with anything on his way to school, a point is added to disassociation.

***The Setting:*** _Hikaru is in his classroom. The class is filled with students. There are a few generic classroom activities where subtitles are shown, but in slightly faded colours._

```
During the lecture, there are random monologues about Hikaru's life and his pondering shown.
There is also faded text about the lecture the teacher is giving.
IF the user pays attention, there would be a question after about 10 monologues.
```

Sample monologue overlay (Hikaru's thoughts, foreground):

- Hikaru: "...wonder if the cat will still be there tomorrow."

Sample lecture line (background, faded):

- Teacher (faded): "...and so the Meiji Restoration was not just a political shift, but a..."

After about 10 such overlays, the attention check fires:

- Teacher: "Hikaru. Are you with us?"
- Hikaru: "Yes!"
- Teacher: "What were we talking about?"
- Options: `<CORRECT_OPTION>` | `<3_INCORRECT_OPTIONS>`

**CHOICE CONSEQUENCE:** Answering wrong triggers a teacher dialogue:

- Teacher: "Be PRESENT! This is exactly why your grades are suffering."

A wrong answer increases Spite and reduces a point from ambition. A correct answer adds to the ambition and confidence scale.

During lunch break, IF Hikaru has his bento box, he offers his lunch to <PLACEHOLDER_FOR_FRIEND_NAME>:

- Hikaru: "Here. Mom packed extra."
- <PLACEHOLDER_FOR_FRIEND_NAME>: "...you sure? Thanks, Hikaru."

**CHOICE CONSEQUENCE:** Offering lunch reduces a point from loneliness.

The rest of the day continues with static monologues where Hikaru thinks about playing at the arcade.

***The Setting:*** _When school ends, the same scenery as before from home to school is shown, except now it's dawn and an orange hue settles over everything._

On his way, the shop that was previously closed — Mr. Yamada's shop — is now open. The arcade has a lot of games but all are occupied.

Hikaru can interact with NPCs in the arcade, given the option to observe (limited to 3 people) OR request to play the game. All NPCs react with dismissal:

- NPC: "Wait your turn, kid."

**CHOICE CONSEQUENCE:** Interacting with at least 1 adds a point to confidence. Interacting with all adds a point towards spite. Interacting with none adds a point to disassociation.

Hikaru notices a peculiar game at the end — a bright orange box with the name `<AI_NAME_PLACEHOLDER>`. Hikaru asks Mr. Yamada:

- Hikaru: "Mr. Yamada, what is this game?"
- Mr. Yamada: "Oh, that's just an old game that I'm about to send away."
- *(IMPORTANT: not growing a bond with the machine makes Mr. Yamada discard it.)*
- Hikaru: "Mind if I check it out before?"
- Mr. Yamada: "Sure. Knock yourself out."

***The Setting:*** _The game transitions to the AI with an orange CRT display. At this point, the AI takes over and conversation snippets are generated with the AI._

***Ending 1.1:*** _Hikaru does not respond to the AI much and does not grow much association with it. The AI Association points drop to -5 and the console is sold._ **THE END**

#### End of DAY 0

- IF ENDING 1.1 is triggered:
  - Mr. Yamada: "Did you enjoy the game?"
  - Hikaru: "Not really. I think you'll fare better without it."
  - Mr. Yamada: "Well, I was selling it anyways."
  - The game is sold and the story ends anticlimactically.
- ELSE:
  - Hikaru: "I loved this game!"
  - Mr. Yamada: "Well sure, Hikaru! We shall keep it."
  - The game stays and the story continues.

**CHOICE CONSEQUENCE:** Triggering the ELSE branch adds a point to AI Association and takes a point away from loneliness. It also reduces a point from disassociation.

Hikaru returns home and sleeps, excited to start the next day.
