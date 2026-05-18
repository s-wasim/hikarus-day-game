# Hikaru's Day

This is the API implementation of the game, Hikaru's Day. The story revolves around a 14 year old school kid in the early 2000s Japan. To escape his monotonous life and loneliness, he finds solace in an arcade owned by Yamada. On a particular day, he encounter's a game that is an AI. Unknown to him, he creates makes or breaks the world using his conversation's with the AI

---

## Repo Setup



---

## Story Points

Each point here determine's what ending plays out.

- Hikaru's point's determine how the pre-configured responses are generated
- AIs  point's determine what responses the AI generates and how the story play's out.

Hikaru's responses to AI's questions determine exactly how the AI Update's its points at the end of the day.

### Hikaru's Points

| Journal Sentiment | Description | Affect |
| --- | --- | --- |
| Disassociation | Hikaru's Sentiment against his life | Conversation is more disassociated. Hikaru will be compelled to feel less compassion towards people |
| Spite | Hikaru's feelings towards other people | Conversation is steered toward's resentment of other people in the world |
| Loneliness | Hikaru's mental state W.R.T socliaising with PEOPLE | Conversations would be steered towards more association with the AI as Hikaru feel's more connection with it. |
| Family Relation | Hikaru's sentiment toward's the value's of family | Conversation's would deliberately avoid discussion's about family and when talked about Hikaru would showcase negativity about family and the meaning of it. |
| Jealousy | Trait of Jealousy | Conversation's would steer toward's disparity amongst the working class and the elite. Hikaru would deliberately present an unfair world-view if Jealousy is high |
| Ambition | How ambtious Hikaru gets | Conversation's would steer toward's how ambitious Hikaru is |
| Confidence | Hikaru's confidence level | Conversation's would be more energetic and Hikaru would try to talk more about himself. |
| Association with AI | Hikaru's sentiment toward's the AI | This start's off with +5 Points. If Hikaru does not respond much to the AI this score drops. reaching -5 Points conclude's the game on DAY0 as Mr. Yamada unplug's and sell's the machine.

### <AI_NAME_PLACEHODLER>'s Points
> ONLY 6 POSSIBLE SENTIMENT'S DRIVING THE AI TO A POSSIBLE ENDING FOR THE GAME
| AI Sentiment | Description | Affect |
| --- | --- | --- |

--- 

## Story Line

### DAY 0
***The Setting:*** _Pleasent and calm room with books scattered around by the ringing of his alarm. Retro themed Japanese style traditional room. **It is the edge of Winters right now with mild rain in the evening**_<br>
A dialogue box appears with Hikaru's face 
- "..." -> "Yet.. Another day..."

```
The user is prompted with the option to:
    "wake up"
    OR
    "Go to sleep"  
```
**CHOICE CONSEQUENCE:** Going back to sleep add's 1 point to disassociation.

At this point, the screen goes blank and in the next-moment, Hikaru is ready for school in a black uniform. 

```
The user is free to explore the room. They can interact with a few selected objects. Finding a picture of him and his friend on the book shelf makes him feel a slightly happy. 
The player at this point should explore the room as they have their homework on the desk.
```
**CHOICE CONSEQUENCE:** Leaving homework on the desk would add 1 point to spite as later on the line, he would get punished if he forgets it. Checking the <PLACEHOLDER_FOR_FRIEND_NAME>'s picture reduce's 1 point from lonliness

Stepping out of the room changes the scenery 

**_The Setting:_** _Ground floor of the house where the kitchen is visible, NO INTERACTIONS possible here. His mother is in the Kitchen preparing breakfast facing away toward's the washing basin_

Depending on earlier choice, His mother will have the following two possible conversation's once Hikaru crosses the kitchen's sliding doors:

1. IF HIKARU WOKE UP ON TIME: "Off to school already? I prepared your bento box. Here is your lunch." (Mother faces to Hikaru and a popup show's Bento Box added) 
2. IF HIKARU WOKE UP LATE: "You're late again! Hurry to school now or you'll be punished again!" (Mother forget's the bento box and Hiakru proceed's outsice)

```
Option 1 add's bento box to his inventory which leaves an oppurtunity to decrease the lonliness score later when he share's his lunch with a peer.
Option 2 does not affect lonliness at this point, it leaves no room for reduction in lonliness
```
**CHOICE CONSEQUENCE:** Option 1 adds a point to Family Relation whereas Option 2 reduces a point

**_The Setting:_** _The scenery is now outside his house. A suburban village with narrow streets_

There are a few artifact's on the way that Hikaru could interact with. 

- Cat
- Luxury car on the street
- School Bullies on the way to school (They are absent if Hikaru woke up on time)
- Vending machine (Hikaru does not have money)
- Alternate path to avoid school bullies

**CHOICE CONSEQUNECE:**

- Interacting with Cat remove's a point from disassociation
- Watching the luxury car and vending machine add's a point to jealosy. Watching the luxury car also add's a point to ambition
- Interaction with bullies would add a point to Spite
- Avoiding bullies would keep scoring unchanged
- If Hikaru does not interact with anything on his way to school, a point would be added to disassociation

**_The Setting:_** _Hikaru is in his classroom, the class is filled with student's There are a few generic classroom acrtivities where subtitle's are shown but are in slightly faded color's_

```
During the lecture, there are random monologues about Hikaru's life and his pondering shown. There is also a faded text about the lecture the teacher is giving. IF the user pay's attention, there would be a question after about 10 monologues.
```
- Teacher: "Hikaru. Are you with us?"
- Hikaru: Yes!
- Teacher: "What were we talking about"
- Options: <CORRECT_OPTION> | <3_INCORRECT_OPTIONS>

**CHOICE CONSEQUENCE:** Answering wrong trigger's a teacher dialogue where she exclaims that: "Be PRESENT! This is exactly why your grades are suffering" Increases Spite point and reduce's point from ambition. Correct answer add's to the ambition and confidence scale

During lunch break, IF Hikaru had his bento box, he would offer his lunch to <PLACEHOLDER_FOR_FRIEND_NAME> IF he had it. 
**CHOICE CONSEQUENCE:** Offerring lunch reduces a point from lonliness.

The rest of the day continues with static monologues where hikaru thinks about playing at the arcade.

**_The Setting:_** _When school end's the same scenery as shown before from home to school is shown except now, it's dawn and orange hue all around._

On his way, the shop that was previously closed; Mr. Yamada's shop is now open. The arcade has alot of games but all are occupied.

Hikaru can interact with NPCs in the arcade given the option to observe (limited to 3 people) OR request to play the game. All NPCs react with dismissal.

**CHOICE CONSEQUNECE:** Interacting with atleast 1 adds a point to confidence and interacting with all adds a point toward's spite. Interacting with none adds a point to disassociation.

Hikaru notice's a peculiar game at the end which is a bright orange box with the name <AI_NAME_PLACEHOLDER> where hikaru asks mr. yamada.

- Hikaru: Mr. Yamada, What is this game?
- Mr Yamada: Oh that's just an old game that I am about to send away (IMPORTANT AS NOT GROWING A BOND WITH THE MACHINE MAKES MR. YAMADA DISCARD IT)
- Hikaru: Mind if I check it out before?
- Mr Yamada: Sure! knock yourself out.

**_The Setting:_** _The game transition's to the AI with orange CRT display. At this point, the AI take's over and conversation snipets are generated with AI._

**_Ending 1.1:_** _Hikaru does not respond to the AI much and does not grow much association with it, the AI Association points drop to -5 and console is Sold_ **THE END**

#### End of DAY 0
- IF ENDING 1.1 is triggered.
    - Mr. Yamada: Did you enjoy the game?
    - Hikaru: Not really. I think you'll fair better without it
    - Mr. Yamada: Well, I was selling it anyways.
    - The game is sold and the story ends anticlimatic
- ELSE
    - Hikaru: I loved this game!
    - Mr. Yamada: Well sure Hikaru! We shall keep it.
    - The game stays and story continue's

**CHOICE CONSEQUENCE:** triggering the else statement adds a point to AI Association and take's a point away from lonliness. This would also reduce a point from disassociation.

Hikaru return's home and sleep's excited to start the next day.