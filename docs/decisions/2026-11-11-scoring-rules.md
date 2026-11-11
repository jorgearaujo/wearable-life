# Scoring rules on paper

- **Date:** 2026-11-11
- **Status:** **partly decided** (2026-11-11). Questions 3 to 8 in section 10 are answered and applied to `docs/spec.md`. How the Mood score counts Sleep and Energy (questions 1 and 2) is still open. Nothing is built.
- **Question:** The spec describes the meters in words. What exact rules turn health records and the time into meter values, reasons, the Mood score and the level?
- **Answer so far:** every meter can be worked out from steps and sleep duration alone, with each richer input adding one clearly bounded part. Writing the rules down exposed seven places where the spec is silent or pulls against rule 2 (hidden values never grade the player). They are listed in section 10 with the owner's answers.
- **Evidence:** `docs/spec.md`; the shapes of real records in `docs/findings/2026-11-11-health-connect-data.md`. No rule here has been run against data.
- **About the numbers:** every weight, rate and limit below is a **starting value**. They exist so the rules are complete enough to argue with. Phase 1 tunes them against the recorded data in `fixtures/`. No number compares HRV, resting heart rate or breathing rate with a population value; those are only ever compared with the player's own usual.

## 1. Shared definitions

**The night and the day**
- A **night** is the main sleep that ends on a calendar day, in the time zone the records carry.
- Sleep sessions with less than 60 minutes between them are one night (a split night).
- The **main sleep** is the longest such group ending between 02:00 and 14:00. Any other session of 15 minutes or more is a **nap**.
- The **game day** starts when the main sleep ends and its data has arrived (the morning reveal), and ends at the next one. Steps use the calendar day, because Health Connect's total is per calendar day.

**Usual values (baselines)**
- Kept per input and per source. One figure per night: HRV is reduced to the night's median when a source writes many values.
- The usual value is the median of the last 30 nights that have the input, not counting last night. The usual spread is measured the same way.
- At least 5 nights are needed before an input is used at all. Between 5 and 14 nights it counts for less (section 8).
- "How far from usual" is the difference from the usual value, measured in usual spreads and limited to two spreads either way. This one figure, written **d** below, is the only form in which a hidden value enters any rule.
- When the source of an input changes, its baseline starts again.

**Which inputs count as present**
- Judged per input from the last 7 days of data, not from which apps have ever written something.

**Not arrived yet**
- Until last night's sleep arrives, the character stays asleep and yesterday's world is shown.
- If nothing has arrived 4 hours after the usual wake time, the day starts anyway from the player's usual values (question 7).
- Every rule can be run again on the same night with the same result. Late or rewritten data may raise a settled day's result, never lower it (rule 1).

## 2. Sleep

**Sleep need for tonight** = base need + debt repayment + extra after a hard day.
- Base need: 7 hours to start. It moves slowly toward the longer nights in the player's last 30 (the upper quarter), never below 7 and never above 9 hours (question 5).
- Sleep debt: each morning, debt = debt + base need − time asleep, kept between 0 and 2 hours. Naps reduce it by their length.
- Debt repayment: at most 30 minutes a night.
- Extra after a hard day: up to 30 minutes, growing as the day's load passes the Activity target.

**Recommended bedtime** = wake time − sleep need, stretched by the player's usual time awake in bed. Wake time is the next phone alarm if one is set within 18 hours, otherwise the usual wake time. It is worked out again whenever new activity data arrives.

**Sleep score for last night** (0 to 100), from the parts that are available:

| Part | Needs | Full marks when | Share |
| --- | --- | --- | --- |
| Hours | Sleep duration | Time asleep reaches last night's need | 50 |
| Consistency | Sleep duration | Bedtime and wake time within 30 minutes of usual; none at 2 hours off | 20 |
| Efficiency | Stages | 90% of the time in bed asleep; none at 70% | 10 |
| Deep and REM | Stages | Their share of the night is at or above the player's usual | 20 |

- With steps and sleep duration only, Hours and Consistency share the full 100 (70 and 30).
- Time asleep is the session minus awake stages when stages exist, otherwise the session length.

**The Sleep meter**
- Morning value: the sleep score.
- It falls in a straight line to 0 at the recommended bedtime + 1 hour. When the bedtime moves, the line is redrawn from the current value.
- A nap adds 1 point per 3 minutes, at most 25.
- Fog: morning fog thickness is 100 − sleep score; night fog starts at the recommended bedtime.

## 3. Energy

**Morning value** (30 to 100; 70 is an ordinary morning).
- Sleep part: 30 + 0.7 × sleep score.
- Body part, only from hidden inputs that are present: 70 + 20 × d for each, limited to 30 to 100, then averaged with HRV counting 3, resting heart rate 2, breathing rate 1. HRV above usual is good; resting heart rate and breathing rate above usual are not.
- With at least one hidden input: morning value = 60% body part + 40% sleep part. With none: the sleep part alone.
- SpO2 is not used in the first release: it was written on 6 nights in 10, and no visible feature needs it.

**During the day**
- A slow fall of 1 point an hour awake.
- Load: 60 points for a full Activity target's worth of load, spread as the load arrives.
- Overdoing it: load beyond the day's target costs twice as much.
- It cannot go below 0.

**Getting some back** (each is small on purpose)

| Lever | Needs | Gain |
| --- | --- | --- |
| Nap | Sleep sessions | 1 point per 5 minutes, at most 15 a day |
| Quiet period | Heart rate | 2 points per 20 minutes awake with heart rate near the resting value, at most 10 a day |
| Mindfulness or breathing session | Session records (not requested yet, see store drafts) | 1 point per 2 minutes, at most 10 a day |

**The forecast** extends today's fall so far to the recommended bedtime and shows whether it reaches 0 first. It is redrawn when data arrives.

## 4. Activity

**Load** is one number for how much the body did today.
- Step load: 1 unit per 100 steps, from Health Connect's daily total.
- Heart load, when heart rate is present: each minute scores by how far heart rate sits between the player's own resting value and the player's own highest sustained value from history. Under 30% of that range: 0. 30 to 50%: 1. 50 to 70%: 2. 70 to 85%: 4. Above: 6. No age formula is used; the game does not know the player's age.
- Day's load = the larger of the two + a quarter of the smaller. A long walk at low heart rate counts through steps; a hard run counts through heart rate; neither is counted twice in full.

**Target**
- Standard target: the player's own median daily load over the last 30 days, never below 5,000 steps' worth and never above 12,000 steps' worth. It rises by at most 5% a week.
- Today's target: the standard target scaled by the morning Energy value, from 60% of standard on the lowest morning to 115% on the best. This is where hidden values shape the day.
- With steps only, there is no heart load and the target is in steps.

**The Activity meter**
- Carries over from yesterday, so it has no fixed start value.
- Rising: load moves it from where the day started toward 100, reaching 100 exactly when today's target is met.
- Falling: 2 points an hour while awake and no load is being added (no steps for 30 minutes). It does not fall during sleep. A full meter is empty after about three days of doing practically nothing, a typical one after about two.
- The dog's restlessness follows the "awake and still" time, not the meter value.

## 5. Mood score, weather, dormancy

**Day result** (0 to 100), only from things the player controls:
- Sleep (proposed, question 2): the Hours and Consistency parts of the sleep score, scaled so that meeting both is 100. Efficiency and Deep and REM are left out.
- Activity: load ÷ target, at most 1, using the **smaller** of the standard target and today's target. A good morning never makes the day harder to pass (question 3).
- Energy (proposed, question 1): full marks when Energy did not run out before the recommended bedtime; less for each hour spent at 0. It counts how Energy was looked after, never where it started.
- Day result = the average of the three parts. A day with all three met is 100, and a week of them is a Mood score of 100.
- Design constraint on section 3: on any morning, meeting today's target and going to bed on time must leave Energy above 0. The starting numbers there do not yet guarantee this on the lowest mornings and must be tuned so they do.
- A day with no sleep data counts Activity and Energy only. A day with no data at all is left out, not counted as zero.

**Mood score** = the average day result over the last 7 days that have one, plus 5 for each weekly goal completed this week, at most 100. Fewer than 3 days: the Mood score is held at 60.

**Weather**, in the season's look: 75 and up is the good day; 55 to 75 fair; 35 to 55 cloudy or light rain; under 35 the bad day; under 15 the very bad day (hail in summer). It changes once a day, at the morning reveal.

**Dormancy** follows the last 3 days, so it answers faster than the weather: when their average day result is under 40, animals hide and flowers close; they return at 50.

**Rest mode:** the Activity part is replaced by full marks on any day the load stays at or under the target. Sleep counts as usual. Resting is rewarded.

## 6. Level

- Each day adds growth: its day result ÷ 100. Each completed weekly goal adds 3.
- A day is settled at the next morning reveal. Growth already given is never taken back; late data can only add.
- Level thresholds grow slowly, so early levels come within days and later ones take weeks. The exact curve is a Phase 1 tuning question.
- An unreadable or missing store never lowers the level (encryption decision).

## 7. One sentence for every change

Each rule that moves something the player can see has a sentence. All are within the 75-letter limit. None shows a number or makes a medical claim.

| When | Sentence |
| --- | --- |
| Sleep high: hours met | Sleep starts full: you slept as long as you needed. |
| Sleep lower: short night | Sleep starts lower today: you slept less than you needed. |
| Sleep lower: timing off | Sleep starts lower today: you went to bed later than usual. |
| Sleep lower: restless (stages) | Sleep starts lower today: you were awake a lot in the night. |
| Sleep lower: little Deep and REM | Sleep starts lower today: less deep sleep than usual. |
| Nap | A nap gave Sleep a little back. |
| Bedtime earlier: debt | Bedtime is a bit earlier: you are catching up on sleep. |
| Bedtime earlier: hard day | Bedtime is a bit earlier: today was a hard day. |
| Energy high | Energy starts high: you slept well and your body is rested. |
| Energy lower: HRV | Energy starts lower today: your body is less rested than usual. |
| Energy lower: resting heart rate | Energy starts lower today: your resting heart rate is higher than usual. |
| Energy lower: breathing rate | Energy starts lower today: your breathing was faster than usual. |
| Energy lower: sleep only | Energy starts lower today: last night was short. |
| Energy falling fast | Energy is dropping fast: you have done a lot today. |
| Energy: overdoing it | Energy is dropping faster: you are past today's goal. |
| Energy regained | A quiet moment gave Energy a little back. |
| Activity target lower | Today asks for less: your body is less rested than usual. |
| Activity target met | Activity is full: you reached today's goal. |
| Activity falling | Activity is slipping: you have been still for a while. |
| Morning fog | Misty morning: you slept less than you needed last night. |
| Good weather | Sunny today: you have slept and moved well this week. |
| Poor weather | Rain today: sleep and movement have slipped this week. |
| Dormant | The animals are hiding: the last few days were quiet. |
| No sleep data | No sleep data for last night, so today starts from your usual. |
| Calibrating | Still getting to know you: the meters move gently for now. |

When several causes apply, the one with the largest effect is shown.

## 8. While the baseline is forming

- Calibration lasts at least 24 hours, as in the spec.
- From 5 to 14 nights of an input, its distance from usual counts for nights ÷ 14 of its full effect. Before 5 nights it is not used and the meter works as if the input were absent.
- History reads usually fill 30 nights on the first day, so most players with a wearable skip this.

## 9. What each input adds

| Present | Sleep | Energy | Activity |
| --- | --- | --- | --- |
| Steps, sleep duration | Hours, Consistency | Sleep part; naps | Steps against a step target |
| + stages | + Efficiency, Deep and REM | (through the sleep score) | |
| + heart rate | | + quiet periods; load from effort | + heart load |
| + resting heart rate | | + body part | + target follows the morning |
| + breathing rate | | sharper body part | |
| + HRV | | sharpest body part | |

## 10. Questions and answers

Answered by the project owner on 2026-11-11 unless marked open.

1. **Energy in the Mood score: open, new proposal.** The owner's aim: the Mood score shows how the week went on all three meters, and a player who does everything right every day gets 100. A morning Energy value cannot be something to "do right", because hidden values set it (rule 2). *Proposed:* Energy counts by how it was looked after, not where it started: full marks on a day Energy did not run out before the recommended bedtime. Because the Activity target shrinks with a low morning, this is reachable on every morning, which section 3's numbers must guarantee.
2. **Sleep stages in the Mood score: open, same proposal.** *Proposed:* the Sleep part is Hours and Consistency, scaled so that meeting both is 100. Stages still shape the Sleep meter and the fog.
3. **Target follows morning Energy: decided.** The Mood score counts against the smaller of the standard target and today's, so a good morning never makes the day harder to pass. (Applied as recommended; the owner's answer confirmed the target rule and did not speak to this detail.)
4. **Activity meter carries over: decided.** It rises as load builds, falls when none is added, and reaches 0 after about 48 to 72 hours of doing practically nothing. *Recommended on the owner's open point:* 100 means today's target is met, not several days' worth. One good day can then always fill it, the sentence stays simple ("you reached today's goal"), and the carry-over already rewards the days before by giving a head start.
5. **Sleep need: decided.** Starts at 7 hours. It may learn from history: *proposed* that it moves slowly toward the longer nights in the player's last 30 (the upper quarter), never below 7 and never above 9 hours.
6. **Sleep meter is a straight line: decided** for the prototype; judged by feel in Phase 1.
7. **A night that never arrives: decided.** After 4 hours the character wakes, meters start from the player's usual values, and the night is left out of the Mood score.
8. **Weekly goal weight: agreed** as a starting value (5 Mood points, 3 growth each), revisited when the goals are designed.

## 11. Not covered

- HealthKit differences (SDNN instead of RMSSD, no reads while locked): the baseline rule handles the first; the second is a data layer matter.
- The level curve, the weekly event, rewards.
- Blood oxygen and skin temperature: not used.
- Time-zone travel and daylight-saving nights: the records carry their own offsets, but Consistency will need a rule for travel days.
