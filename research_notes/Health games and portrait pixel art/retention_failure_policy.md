# Cross-cutting evidence for health-data-driven games: retention, failure, non-punishing design, platform policy

All web pages were accessed on 2026-11-11. Policy quotes were extracted from the live pages by a fetch tool that summarises pages; they are marked "verbatim per fetch" and should be re-checked against the linked page before being copied into a store submission. Anything marked UNVERIFIED comes from a search snippet, a secondary source, or memory, and was not confirmed against the primary source.

## 1. Retention: what keeps people for months versus novelty that fades in weeks

### Takeaway
The published evidence is consistent: health games and gamified health apps produce a real but small boost that shrinks sharply within 6 to 14 weeks, and typical 30-day retention for health and fitness apps is in the low single digits to about 8%. No source found gives audited long-term retention for a passive, health-data-driven game, so any retention target for this project is a guess.

### Cited Findings

**Pokémon GO (the best-studied health-adjacent game)**
- BMJ 2016 (Howe et al.): players took on average 955 extra steps a day in the first week (about 11 minutes of walking); the increase tapered and by week six step counts were back to pre-game levels. Sample was 560 players and 622 non-players, US young adults, iPhone-recorded steps. — [Medical Xpress summary of the BMJ paper](https://medicalxpress.com/news/2016-12-pokemon-moderately-physical-adults-effect.html); [Smithsonian](https://www.smithsonianmag.com/smart-news/pokemon-go-craze-had-health-benefits-little-while-180961486/); [STAT](https://www.statnews.com/2016/12/13/pokemon-go/)
- The BMJ authors attributed the fade to two things: fewer people still playing, and remaining players walking less. — [Medical Xpress](https://medicalxpress.com/news/2016-12-pokemon-moderately-physical-adults-effect.html)
- JMIR 2016 (Althoff, White, Horvitz; Microsoft Band data, about 32,000 users, 3 months): highly engaged players increased activity by 1,473 steps a day, more than 25% over prior levels, over 30 days. The authors say long-term effects need further study. — [JMIR 2016;18(12):e315](https://www.jmir.org/2016/12/e315); [PMC copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC5174727)

**Gamification meta-analyses**
- Mazeas et al., JMIR 2022 (16 RCTs, 2,407 participants): gamified interventions had a small-to-medium effect on physical activity (Hedges g = 0.42); at follow-up averaging 14 weeks after the intervention ended the effect was g = 0.15 (95% CI 0.07–0.23). The authors read the residual effect as evidence that it is "not just a novelty effect"; the size still fell by about two thirds. (Figures from abstract/search snippet, full text not opened.) — [JMIR 2022;24(1):e26779](https://www.jmir.org/2022/1/e26779)
- Yu et al., JMIR Serious Games 2025 (cardiovascular populations, 5 studies): short-term g = 0.32, maintenance g = 0.20 at about 2.5 months after the intervention. (From abstract.) — [JMIR Serious Games 2025;13:e68151](https://games.jmir.org/2025/1/e68151/XML)

**Wearables and trackers**
- The often-quoted "a third stop within six months" figure comes from a single industry survey: Endeavour Partners, September 2013, 500 US wearable owners (screened from 6,223 consumers); more than half no longer used the device at all. — [MobiHealthNews](https://www.mobihealthnews.com/news/survey-one-third-wearable-device-owners-stopped-using-them-within-six-months)
- A survey study of tracker abandonment lists the top reasons as lack of usefulness, boredom and device malfunction. — [arXiv 1904.13226](https://arxiv.org/pdf/1904.13226)
- TRIPPA trial (Finkelstein et al., Lancet Diabetes & Endocrinology 2016; 800 employees in Singapore, Fitbit Zip with or without cash or charity incentives for 6 months, followed to 12 months): only the cash group raised steps at 6 months; at 12 months, after incentives stopped, the cash group did 23 fewer MVPA bout-minutes per week than the plain-Fitbit group, and no health outcomes improved. — [WU research portal record](https://research.wu.ac.at/en/publications/effectiveness-of-activity-trackers-with-and-without-incentives-to-13/); [TCTMD](https://www.tctmd.com/news/money-gadgets-incentivizing-healthy-behaviors-questioned-once-again)
- A news report on TRIPPA says about 10% of participants were still wearing the device at the end (UNVERIFIED against the paper). — [HealthDay](https://www.healthday.com/healthpro-news/exercise-and-fitness/no-evidence-activity-tracker-devices-raise-fitness-levels-715516.html)
- UbiComp 2016 (Epstein et al., 141 lapsed Fitbit users): half felt guilty about having stopped, and nearly all of those wanted to return to tracking; the authors argue one-size-fits-all tracker design misses different user types. — [UW News / ScienceDaily](https://www.sciencedaily.com/releases/2016/09/160908141724.htm); [paper PDF](https://homes.cs.washington.edu/~jfogarty/publications/ubicomp2016.pdf)

**App retention benchmarks (vendor data, methods differ)**
- Health and fitness app benchmarks cluster around Day 1 20–28%, Day 7 8–18%, Day 30 3–8%. Braze reports Day 30 of 3.9% (iOS) and 3.4% (Android) for Health & Fitness. — [Braze](https://www.braze.com/resources/articles/mobile-app-retention); [Adjust](https://www.adjust.com/blog/what-makes-a-good-retention-rate/); [Stream, citing OneSignal](https://getstream.io/blog/app-retention-guide)
- Objective panel data for 93 mental health apps (Baumel et al., JMIR 2019): median 15-day retention 3.9% and median 30-day retention 3.3%. A preprint reports tracker apps (6.1%) and peer-support apps (8.9%) above mindfulness (4.7%) and breathing apps (0.0%) at day 30 (subgroup figures UNVERIFIED in the published version). — [JMIR 2019;21(9):e14567](https://www.jmir.org/2019/9/e14567/)

**Incentive trials (what happens when the external push stops)**
- Patel et al., Annals of Internal Medicine 2016 (281 employees, 13-week intervention, 13-week follow-up): only the loss-framed incentive beat control (goal met on 45% of participant-days versus 30%); no group showed a lasting effect after incentives ended. — [Penn Today](https://penntoday.upenn.edu/2016-03-24/research/prospect-losing-money-pushes-people-achieve-fitness-goals); [Penn CHIBE](https://chibe.upenn.edu/blog/move-it-or-lose-it/)

**Developer statements (Duolingo, the most documented retention program)**
- Decoupling the streak from the daily goal (one lesson extends the streak) raised Day 14 retention by 3.3%, daily active learners by 1%, and the share of daily learners on a streak by 10.5% (relative). — [Duolingo blog: Improving the streak](https://blog.duolingo.com/improving-the-streak)
- Allowing two Streak Freezes at once raised daily active learners by 0.38%. — [Duolingo blog: streak research](https://blog.duolingo.com/duolingo-streak-research/)
- Streak milestone animations raised the chance that a new learner was active seven days later by 1.7%. — [Duolingo blog: how the streak builds habit](https://blog.duolingo.com/how-duolingo-streak-builds-habit)

### Inferences
- The pattern across Pokémon GO, gamification trials and incentive trials is the same: the behaviour change is driven by novelty or an external push and decays once that fades. A game that asks nothing of the player and only reflects what already happened avoids promising behaviour change at all, which sidesteps the weakest part of the evidence. This is inference, not a tested result.
- Since tracker and peer-support apps retained better than exercise-instruction apps in the Baumel panel, "something to look at that changes every day" may retain better than "something to do every day". Weak inference from one preprint figure.
- Benchmarks imply that even a well-executed product should expect more than 90% of installs to be gone by day 30. Design for the small fraction who stay, and make returning after a gap cheap (the Epstein finding that lapsed users feel guilty and want to return supports a no-penalty return).
- Duolingo's measured wins are small single-digit relative lifts per experiment. Large retention claims for any single mechanic should be treated with suspicion.

### Gaps
- No published Day 1/7/30 or multi-month retention figures were found for passive health-driven games as a class. Per-product figures are being covered by the other researchers.
- The Mazeas and Yu effect sizes were taken from abstracts; full texts were not opened.
- I did not find a long-term (12+ month) follow-up of sustained Pokémon GO players; the Althoff paper explicitly leaves it open.
- The Endeavour Partners figure is from 2013 and a single survey; no current equivalent with a clear method was found. A "42% after six months" figure circulates without a traceable primary source.

## 2. Failure: why these products shut down or were abandoned

### Takeaway
The stated reasons are almost always commercial or platform-level, not design-level: revenue below the cost of a live service, an owner changing strategy, a reward economy that could not sustain itself, or an upstream API being withdrawn. An on-device game with no backend and no third-party wearable API removes most of these, but stays exposed to platform API changes and to background-sync limits.

### Cited Findings

**Live-service cost versus revenue (Niantic)**
- June 2023: Niantic laid off about 230 people, closed its Los Angeles studio, cancelled Marvel World of Heroes and shut down NBA All-World, which had launched in January 2023. CEO John Hanke wrote that the company had "allowed our expenses to grow faster than revenue", that recent games had not delivered revenue matching the investment, and that the mobile market is crowded, with app store and mobile advertising changes making it harder to launch new games at scale. — [NME](https://www.nme.com/news/pokemon-go-developer-confirms-230-layoffs-cancels-marvel-game-3463283); [mobilegamer.biz](https://mobilegamer.biz/niantic-lays-off-230-staff-cancels-two-games-closes-la-studio/); [TechRadar](https://techradar.com/gaming/consoles-pc/pokemon-go-a-top-priority-for-niantic-as-it-cancels-two-games-and-lays-off-staff)
- Harry Potter: Wizards Unite closed on 31 January 2022. Niantic gave no explicit reason beyond the story arc ending; press cited Sensor Tower estimates of $39.4M lifetime revenue and roughly $100,000 in a month when Pokémon GO made an estimated $29M. — [TechCrunch](https://techcrunch.com/2021/11/02/harry-potter-wizards-unite-shut-down-niantic/); [Game World Observer](https://gameworldobserver.com/2021/11/03/niantic-shutting-down-harry-potter-wizards-unite-as-its-revenue-falls-short-compared-to-pokemon-go)

**Reward economies (move-to-earn)**
- STEPN: daily active users fell from a reported peak of 58,000 on 21 June 2022 to 5,800 on 15 September 2022 (Decrypt); Dune data show monthly actives falling from 702,649 in May to 237,780 in July 2022. Other trackers report much higher peaks, so absolute numbers disagree while the direction does not. Causes cited: falling token earnings, copycat competitors, and withdrawal from mainland China. — [Decrypt](https://decrypt.co/111809/crypto-fitness-app-stepn-denies-layoff-reports); [CoinJournal](https://coinjournal.net/news/gmt-price-at-risk-as-stepn-monthly-and-daily-users-plunge)
- A later review concludes that rewarding healthy habits can attract users but is rarely enough to keep them. — [Traders Union](https://tradersunion.com/news/editors-picks/show/2931420-move-earn-after-hype/)

**Owner strategy changes (Fitbit under Google)**
- Fitbit removed Challenges, Adventures and open groups on 27 March 2023; earned trophies were lost. Stated reasons were that the features had "a limited number of active users compared to other offerings" and a wish to "streamline" the app during Google integration. Users protested on the community forum. — [9to5Google](https://9to5google.com/2023/03/27/fitbit-challenges-groups-removed/); [Engadget](https://engadget.com/fitbit-removing-open-groups-adventures-challenges-app-140024841.html); [Fitbit community thread](https://community.fitbit.com/t5/Product-Feedback/Don-t-remove-Challenges-amp-Adventures/idi-p/5335785/page/38)

**API withdrawal**
- Google Fit APIs: no new developer sign-ups since 1 May 2024; Google's migration FAQ says the Fit APIs, including the REST API, will be deprecated in 2026 and that there is no direct replacement for the REST API. No exact shutdown date was found on Google's pages. — [Google Fit Migration FAQ](https://developer.android.com/health-and-fitness/health-connect/migration/fit/faq); [Fit migration guide](https://developer.android.com/health-and-fitness/health-connect/migration/fit)
- Legacy Fitbit Web API: dev.fitbit.com states support ends on 30 September 2026 and directs developers to the Google Health API. Different versions of Google's page list an API turn-off of 30 October or 2 November 2026 (HTTP 410 afterwards). The dates conflict and the current status was not confirmed. — [dev.fitbit.com](https://dev.fitbit.com/build/); [Google Health API: About](https://developers.google.com/health/about)
- Third-party integrators report that existing Fitbit OAuth tokens cannot be reused, so every user must reconnect (UNVERIFIED, vendor blogs). — [Terra](https://tryterra.co/blog/fitbit-api-shutdown-september-2026-migration)
- Health Connect itself changed an identifier mid-2026: "Starting with the Health Connect update in June 2026, on-device steps are attributed to a device-specific Synthetic Package Name (SPN) instead of the generic "android" package name" (verbatim per fetch). Apps that filtered by data origin had to change. — [Health Connect: read data](https://developer.android.com/health-and-fitness/health-connect/read-data)

**Background sync limits**
- Apple: "the device encrypts the HealthKit store when the user locks the device. As a result, your app may not be able to read data from the store when it runs in the background." (verbatim per fetch) — [HealthKit: Protecting user privacy](https://developer.apple.com/documentation/healthkit/protecting-user-privacy)
- Apple: "If your app fails to respond three times, HealthKit assumes your app can't receive data and stops sending background updates." (verbatim per fetch) — [enableBackgroundDelivery](https://developer.apple.com/documentation/healthkit/hkhealthstore/enablebackgrounddelivery(for:frequency:withcompletion:))
- Developer reports: observer queries do not deliver while the phone is locked; one developer reports sleep data only arriving when the app is in the foreground; another that sleep data reaches HealthKit many minutes or longer after waking. Anecdotal, some old. — [Apple forum 824819](https://developer.apple.com/forums/thread/824819); [Apple forum 763329](https://developer.apple.com/forums/thread/763329); [Apple forum 856115](https://developer.apple.com/forums/thread/856115); [Apple forum 825304](https://developer.apple.com/forums/thread/825304)

### Inferences
- Niantic's and Fitbit's closures are about cost and strategy at companies with servers and staff to pay. A single-developer, offline, no-backend game cannot be "shut down" in the same way; its failure mode is neglect or a platform API change breaking it.
- The Fitbit and Google Fit withdrawals show that reading a vendor's cloud API is the fragile path. Reading only the two OS health stores is the most durable choice available, though the June 2026 step-attribution change shows it still needs maintenance.
- Move-to-earn shows that external rewards attract people who leave when the reward shrinks. This matches the incentive trials in section 1.
- Because overnight data cannot reliably be read in the background on iOS, "data not arrived yet" on first morning open is the normal case, not an edge case. This matches the project's existing architecture rule.

### Gaps
- Niantic did not publish a reason for the Wizards Unite closure; revenue figures are third-party estimates. A reported CEO remark calling the game "mediocre" was seen only as a headline and not verified.
- No formal post-mortem from a small indie health game was found in this pass.
- Android background execution limits by manufacturer (battery optimisers killing workers) were not researched here; no source collected.
- The current live status of the legacy Fitbit Web API on 2026-11-11 was not confirmed.

## 3. Non-punishing design: staying motivating without loss or streaks

### Takeaway
There is solid evidence that loss aversion works on engagement numbers (Duolingo's experiments, loss-framed incentive trials) and solid qualitative evidence that it produces guilt, anxiety and guilty abandonment in health tracking. I found no controlled study showing that a no-loss design retains as well as a streak design; the case for it rests on wellbeing evidence, on successful cozy games, and on the fact that streak effects vanish once pressure is removed.

### Cited Findings

**Counter-evidence first: loss aversion does raise engagement**
- A Duolingo retention PM states that once users reach a seven-day streak, loss aversion takes hold and retention rises markedly (secondary summary of a podcast interview). — [Lenny's Podcast summary](https://rosetta.to/u/lennyspodcast/behind-the-product-duolingo-streaks-jackson-shuttleworth-group-pm-retention-team)
- Loss-framed money (lose $1.40 per missed day from a pre-allocated sum) was the only incentive design that beat control in the Patel 2016 trial, 45% versus 30% of days at goal. — [Penn Today](https://penntoday.upenn.edu/2016-03-24/research/prospect-losing-money-pushes-people-achieve-fitness-goals)
- Duolingo's Streak Wager (betting in-game currency on keeping a streak) made learners return more often. A +14% Day 7 figure circulates but was not verified against Duolingo's own write-up. — [Duolingo: how streaks keep learners committed](https://making.duolingo.com/how-streaks-keep-duolingo-learners-committed-to-their-language-goals)

**But the same company's wins came from softening the loss**
- Duolingo's largest reported streak gains came from making streaks easier to keep (one lesson counts: +3.3% Day 14 retention) and from more forgiveness (two Streak Freezes: +0.38% daily actives). — [Improving the streak](https://blog.duolingo.com/improving-the-streak); [Streak research](https://blog.duolingo.com/duolingo-streak-research/)
- The loss-framed incentive effect did not persist after the incentive ended. — [Penn CHIBE](https://chibe.upenn.edu/blog/move-it-or-lose-it/)

**Tracker guilt, anxiety and orthosomnia**
- "Orthosomnia" was coined in a 2017 Journal of Clinical Sleep Medicine case series (Baron et al.): patients sought treatment because of tracker data, trackers reinforced sleep-related anxiety or perfectionism, and all three described patients spent excessive time in bed to raise the tracker's number, which may have worsened their insomnia. It is not a recognised disorder. — [Sleep Foundation](https://www.sleepfoundation.org/insomnia/orthosomnia)
- A 2026 SLEEP conference abstract from a nationally representative US survey reports 30.9% of sleep trackers screening positive for orthosomnia risk (adapted screening tool; abstract only). — [SLEEP 2026 supplement](https://academic.oup.com/sleep/article/49/Supplement_1/A246/8674102)
- Half of 141 lapsed Fitbit users felt guilty about stopping. — [ScienceDaily](https://www.sciencedaily.com/releases/2016/09/160908141724.htm)
- A Newcastle University systematic review links fitness technology use to anxiety, body dissatisfaction and rumination, and to excessive exercise to relieve guilt over missed goals. — [Newcastle University](https://from.ncl.ac.uk/the-dark-side-of-fitness-technology)
- First-person journalism describes anxiety about closing Apple Watch rings and frantic exercise to keep a streak (essay, not research). — [TechRadar](https://techradar.com/health-fitness/smartwatches/my-apple-watch-is-going-to-hate-this-our-wearables-are-making-us-anxious-and-obsessive-heres-what-we-can-all-do-about-it)

**Self-determination theory (SDT)**
- SDT (autonomy, competence, relatedness) is the usual framework for gamification's motivational effects; a systematic review found that health gamification mostly relies on positive reinforcement and extrinsic rewards and is often not grounded in behaviour change theory. — [PMC6096297](https://pmc.ncbi.nlm.nih.gov/articles/PMC6096297); [JMIR 2021;23(8):e24546](https://www.jmir.org/2021/8/e24546/XML)
- A fitness-app experiment reported that gamification raised stress, and that a self-exploration-based variant reduced that effect (search snippet, UNVERIFIED in full text). — [PMC11347891](https://pmc.ncbi.nlm.nih.gov/articles/PMC11347891)

**How cozy and idle games handle absence**
- Animal Crossing before New Horizons penalised absence with weeds, cockroaches, unhappy villagers and villagers moving away; Wild World's villagers are described as harsh about absences. — [CBR](https://www.cbr.com/animal-crossing-how-the-games-have-punished-time-travelers/); [MetaFilter thread](https://metafilter.com/185548/But-youre-back-to-stay-right-At-least-for-one-more-day)
- New Horizons softened this: villagers no longer leave while the player is away, bedhead fixes itself, and what remains is weeds, a few cockroaches and villagers remarking on the time passed. — [Destructoid](https://www.destructoid.com/animal-crossing-new-horizons-returning-player-neglected-island/); [Kotaku](https://kotaku.com/what-happens-when-you-abandon-your-animal-crossing-new-1844574997); [CBR](https://www.cbr.com/animal-crossing-how-the-games-have-punished-time-travelers/)
- Even the softened version drew criticism when Nintendo emailed lapsed players that their island missed them. — [TheGamer](https://www.thegamer.com/nintendo-animal-crossing-new-horizons-hiatus-guilt-trip-email/)
- Neko Atsume: the series supervisor says it was built to be enjoyed in a relaxed manner with "healing" as a major theme; critics note it has no win state and does not beg for attention. — [Meta interview with Ryo Shintani](https://www.meta.com/blog/neko-atsume-interview/); [Ludus Novus](https://ludusnovus.net/2015/07/30/the-feline-grace-of-neko-atsume)
- Tamagotchi: Japanese toys showed a ghost and headstone at death; English versions showed an angel or a UFO returning the pet to its home planet; many later toys have the pet run away or leave on a journey, and the 2009 Tamagotchi iD partly removed death (wiki-level sources). — [Wikipedia mirror](https://cavac.at/cavacopedia/Tamagotchi); [TV Tropes](https://www.tvtropes.org/pmwiki/pmwiki.php/Toys/Tamagotchi)

**Products built on non-punishment**
- Gentler Streak's designers say it came "from our own struggles with burnout due to improper activity levels", that "Most apps focus on constant improvement, setting records, and unrealistic challenges", and that the tone goal was "supportive but not cheesy, motivating but not fake-hyped" (verbatim per fetch). Users can set a status of sick, injured or on a break. — [Sketch interview](https://www.sketch.com/blog/gentler-streak/)
- Gentler Streak counts rest days toward the streak and ties suggestions to recovery state; its Activity Path needs about three to four weeks of data to become accurate (reviews and store listing). — [App Store listing](https://apps.apple.com/us/app/gentler-streak-workout-tracker/id1576857102); [Lifestack review](https://lifestack.ai/blog/gentler-streak)
- Finch: founded by two friends who struggled with anxiety and depression; a design analysis describes its core idea as presence, the pet living a life while the user is away, to build emotional investment. — [Finch FAQ](https://befinch.notion.site/Finch-FAQ-474652d0123d4883ac7a0cd6c8f5aa70); [Deconstructor of Fun](https://www.deconstructoroffun.com/blog/x0hd2ssr80y5n7gv0w967pg7hwd7tl)

### Inferences
- Loss aversion measurably lifts engagement while it is applied, and the lift disappears when the pressure stops; meanwhile the health-tracking literature documents guilt and anxiety as costs. For a product whose stated values exclude grading and shame, the trade is defensible, but it should be expected to cost some short-term retention compared with a streak design. This is inference; no head-to-head study was found.
- Animal Crossing's history is the closest precedent for "dormant, not dead": each release reduced the absence penalty, and the surviving elements (weeds, a remark from a villager) are cosmetic and reversible in minutes. The backlash to the "your island misses you" email suggests even gentle guilt messaging outside the game is risky.
- Duolingo's best results came from making progress easier to keep. That is weak support for the idea that forgiveness, not threat, is where the retention gains are.
- Orthosomnia research is a direct argument for the project's rule of showing only three coarse meters and never raw sleep numbers: the documented harm comes from chasing a displayed number.
- What replaces loss as a reason to return, in the products above, is curiosity (what changed while I was away), attachment to a character, and accumulation that only goes up. This is my synthesis, not a cited finding.

### Gaps
- No controlled study comparing a no-loss design against a streak design on retention was found.
- No peer-reviewed study of Snapchat streaks and adolescent stress turned up; only parenting and opinion pieces. Not included as evidence.
- From memory and NOT verified in this pass: Silverman and Barasch, "On or Off Track: How (Broken) Streaks Affect Consumer Decisions" (Journal of Consumer Research, about 2023), reported that a broken streak reduces subsequent engagement; and Ryan, Rigby and Przybylski (2006) applied SDT to video game motivation. The report writer should confirm both before citing.
- No founder statement from Finch on a no-death or no-punishment decision, and no retention figures from Finch or Gentler Streak, were found. One opinion piece claims Finch has a streak-loss mechanic; unverified.
- Stardew Valley's handling of absence was not researched.
- No peer-reviewed study specific to Apple Watch ring guilt was found, only journalism.

## 4. Platform policy: Apple and Google rules on health data, claims and permissions

### Takeaway
Google explicitly lists games as an approved Health Connect use case, so the Android path is permitted in principle but gated by a declaration with per-data-type justification. Apple has no such category: HealthKit must be used "for health and fitness purposes", clearly shown in both the UI and the marketing text, and the most common documented rejection is Guideline 2.5.1 for not making Health use visible. One open risk on Google Play is whether a health-data-reading app from a personal developer account is pushed to an organization account.

### Cited Findings

**Apple: App Store Review Guidelines (verbatim per fetch, accessed 2026-11-11; the page shows no last-updated date)** — [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- 1.4.1: "Medical apps that could provide inaccurate data or information, or that could be used for diagnosing or treating patients may be reviewed with greater scrutiny." And: "Apps must clearly disclose data and methodology to support accuracy claims relating to health measurements, and if the level of accuracy or methodology cannot be validated, we will reject your app." And: "Apps should remind users to check with a doctor in addition to using the app and before making medical decisions."
- 2.5.1: "HealthKit should be used for health and fitness purposes and integrate with the Health app."
- 2.5.18: ads "may not engage in targeted or behavioral advertising based on sensitive user data such as health/medical data (such as from the HealthKit APIs)".
- 5.1.1(i): "All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner."
- 5.1.1(ii): "Ensure your purpose strings clearly and completely describe your use of the data." Also: "Paid functionality must not be dependent on or require a user to grant access to this data."
- 5.1.1(iii): "Apps should only request access to data relevant to the core functionality of the app and should only collect and use data that is required to accomplish the relevant task."
- 5.1.2(vi): "Data gathered from the HomeKit API, HealthKit, Clinical Health Records API, MovementDisorder APIs, ClassKit or from depth and/or facial mapping tools ... may not be used for marketing, advertising or use-based data mining, including by third parties."
- 5.1.3(i): "Apps may not use or disclose to third parties data gathered in the health, fitness, and medical research context—including from the Clinical Health Records API, HealthKit API, Motion and Fitness, MovementDisorder APIs, or health-related human subject research—for advertising, marketing, or other use-based data mining purposes other than improving health management, or for the purpose of health research, and then only with permission." And: "You must disclose the specific health data that you are collecting from the device."
- 5.1.3(ii): "Apps must not write false or inaccurate data into HealthKit or any other medical research or health management apps, and may not store personal health information in iCloud."

**Apple: HealthKit framework documentation (verbatim per fetch)** — [Protecting user privacy](https://developer.apple.com/documentation/healthkit/protecting-user-privacy)
- Apps must not access HealthKit APIs unless "the use is for health or fitness purposes and this usage is clear in both your marketing text and your user interface."
- "To prevent possible information leaks, an app isn't aware when the user denies permission to read data. From the app's point of view, no data of that type exists."
- "Apps must include usage descriptions, or it will crash when you request authorization to access HealthKit data. Include the NSHealthShareUsageDescription key to read, and NSHealthUpdateUsageDescription key to write data to Healthkit."
- "You must also provide a privacy policy for any app that uses the HealthKit framework."
- "Your app may not use information gained through the use of the HealthKit framework for advertising or similar services. Note that you may still serve advertising in an app that uses the HealthKit framework, but you can't use data from the HealthKit store to serve ads."
- "You must not disclose any information gained through HealthKit to a third party without express permission from the user. Even with permission, you can only share information to a third party if they also provide a health or fitness service to the user."
- "You must clearly disclose to the user how you and your app will use their HealthKit data."

**Apple: background delivery (verbatim per fetch)** — [enableBackgroundDelivery](https://developer.apple.com/documentation/healthkit/hkhealthstore/enablebackgrounddelivery(for:frequency:withcompletion:))
- "The system wakes your app at most once per time period defined by the specified frequency. Some sample types have a maximum frequency of hourly." And: "on iOS, stepCount samples have an hourly maximum frequency."
- "For iOS 15 and watchOS 8 and later, you must enable the HealthKit Background Delivery by adding the com.apple.developer.healthkit.background-delivery entitlement to your app. If your app doesn't have this entitlement, the enableBackgroundDelivery(for:frequency:withCompletion:) method fails with an errorAuthorizationDenied error."
- "If you don't call the update's completion handler, HealthKit continues to attempt to launch your app using a backoff algorithm ... If your app fails to respond three times, HealthKit assumes your app can't receive data and stops sending background updates."
- "Background server queries aren't supported on the Simulator."

**Apple: Human Interface Guidelines for HealthKit (verbatim per fetch)** — [HIG: HealthKit](https://developer.apple.com/design/human-interface-guidelines/healthkit)
- "If your app doesn't provide health and fitness functionality, don't request access to people's private health data."
- "It makes sense to request access to weight information when people log their weight, for example, but not immediately after your app launches."
- "Avoid adding custom screens that replicate the standard permission screen's behavior or content."
- "People expect to globally manage access to their health information in Settings > Privacy. Don't confuse people by building additional screens in your app that affect the flow of health data."
- "Refer to the Health app as Apple Health or the Apple Health app." And: "Don't use the term HealthKit. HealthKit is a developer-facing term".
- "Don't display Health app images or screenshots."
- Apple Health icon: use only the Apple-provided icon, unaltered, never as a button.
- Activity rings: "Use Activity rings for Move, Exercise, and Stand information only ... Never show Move, Exercise, and Stand progress in another ring-like element." Also never in the app icon, marketing or notifications.

**Apple: documented rejections**
- A step-count fitness app was rejected in September 2025 under 2.5.1 with: "The app uses the HealthKit or CareKit APIs but does not clearly identify the HealthKit and CareKit functionality in the app's user interface." The developer added a permission prompt, a HealthKit indicator in the UI and onboarding text and was still rejected; App Review staff replied in October 2025 that they were investigating. No resolution recorded. — [Apple forum 802626](https://developer.apple.com/forums/thread/802626)
- The same 2.5.1 wording goes back years; developers report fixing it by naming the Health integration in the UI and in the App Store description. — [Apple forum 28627](https://developer.apple.com/forums/thread/28627); [Apple forum 698081](https://developer.apple.com/forums/thread/698081)
- Apps have been rejected under 2.5.1 with no HealthKit calls at all, because a third-party framework linked HealthKit. — [Apple forum 762128](https://developer.apple.com/forums/thread/762128); [Apple forum 803775](https://developer.apple.com/forums/thread/803775)
- A July 2026 forum question on whether uploading HealthKit data to the developer's own backend raises scrutiny under 5.1.1/5.1.3 has no replies. — [Apple forum 838022](https://developer.apple.com/forums/thread/838022)

**Google Play: is a game an accepted Health Connect use case? Yes.**
- The Play help page titled "Android Health Permissions: Guidance and FAQs" lists approved use cases as: Fitness, wellness and coaching; Rewards; Corporate wellness; Medical care; Human-subjects research; Health-integrated games. Access is "strictly limited to apps providing clear user benefit within specific, approved use cases." For games: "The primary purpose must remain gaming," and the app "should not function as an unregulated medical tool." (verbatim fragments per fetch) — [Play Console Help 12991134](https://support.google.com/googleplay/android-developer/answer/12991134)
- The permissions policy lists approved use cases including "fitness and wellness, rewards, fitness coaching, corporate wellness," plus "medical care, health research, and games." (fragments per fetch) — [Play policy: Permissions and APIs that access sensitive information](https://support.google.com/googleplay/android-developer/answer/9888170)
- The Health Content and Services policy names games as in scope: "games apps that collect a user's activity data as a way to advance game play etc." Such apps must make the link between core functionality and health data collection clear, and reflect the limited use in the privacy policy. — [Play policy 16679511](https://support.google.com/googleplay/android-developer/answer/16679511)

**Google Play: Health Connect requirements (fragments verbatim per fetch)** — [Play policy 9888170](https://support.google.com/googleplay/android-developer/answer/9888170)
- Limited use: "Data use should be limited to providing or improving the appropriate use case or features visible" in the app's interface.
- "User data may only be transferred to third parties with explicit user consent".
- Prohibited: "Transferring, selling, or using user data for serving ads, including personalized or interest-based advertising".
- Minimum scope: "You must only request access to the permissions that are necessary to implementing your product's features or services."
- Prohibited: "Transferring, selling, or using user data with any product or service that may qualify as a medical device" unless regulatory requirements are met and the user consents.
- "Data accessed through Health Connect Permissions is regarded as personal and sensitive user data". — [Play policy 16679511](https://support.google.com/googleplay/android-developer/answer/16679511)

**Google Play: declaration and review**
- "All developers that have an app published on Google Play must complete the Health apps declaration", including apps with no health features. "If your app provides health features or accesses health data to support non-health features, you must declare" the relevant features. — [Play Console Help 14738291](https://support.google.com/googleplay/android-developer/answer/14738291)
- The form's Health and fitness options are: Activity and fitness; Nutrition and weight management; Period tracking; Sleep management; Stress management, relaxation, mental acuity; Diseases and conditions management. Then each Health Connect data type needs its own written justification. The declaration is repeated whenever data types change and "may be reviewed again" on new versions. — [Publish your health app on Google Play](https://developer.android.com/health-and-fitness/health-connect/publish)
- Stated rejection reasons: "Lack of clear justification for the requested permissions."; "Requesting a bulk list of permissions when not necessary."; "Insufficient detail about data collection, usage, and sharing practices."; misalignment with approved use cases. High-sensitivity categories are "subject to heightened scrutiny." — [Play Console Help 12991134](https://support.google.com/googleplay/android-developer/answer/12991134)
- Without an approved declaration, users of a published app see a "can't access Health Connect" dialog. — [Publish your health app](https://developer.android.com/health-and-fitness/health-connect/publish)
- The manifest must contain an activity that shows the privacy policy for the permissions rationale intent, and "The activity must display the same privacy policy you provide for your app in the Google Play Console." — [Health Connect: get started](https://developer.android.com/health-and-fitness/health-connect/get-started)
- Medical disclaimer wording in the Health policy: "not a medical device and does not diagnose, treat, cure, or prevent any medical condition." (fragment; the exact conditions under which it is required were not captured) — [Play policy 16679511](https://support.google.com/googleplay/android-developer/answer/16679511)
- Integrator advice: the Play declaration must match the manifest's permissions; an SDK that declares every Health Connect permission triggers review questions. — [Terra docs](https://docs.tryterra.co/faq/help-topics/data-api-sdk/mobile-sdk-setup-permissions-and-crashes/strip-unused-health-permissions-store-review)

**Google Play: organization account risk (unresolved)**
- "You must choose an organization account if you provide any of the following services" includes "Health apps, such as medical apps and human subjects research apps." An organization account requires a D-U-N-S number. — [Play Console Help 13634885](https://support.google.com/googleplay/android-developer/answer/13634885)
- The health categories article describes medical apps as "developed by a healthcare provider (such as a HIPAA covered entity) or similar institution" and does not say health-and-fitness apps need an organization account. — [Play Console Help 13996367](https://support.google.com/googleplay/android-developer/answer/13996367)
- A developer reports Google repeatedly rejecting an app and finally stating that, for the health data collected and declared, it needs to be an organizational app (mirrored Reddit snapshot, could not be opened, UNVERIFIED). A secondary blog states existing health apps had to move to a verified organization account by 28 January 2026 (UNVERIFIED). The Reddit thread itself has no working URL to cite (the fetch failed), so treat the anecdote as unsourced. — [Play Console Help 13634885](https://support.google.com/googleplay/android-developer/answer/13634885) (the primary rule only); [webtoapp.design blog](https://webtoapp.design/blog/requirements-organization-account)

**Health Connect platform behaviour** — [Health Connect: read data](https://developer.android.com/health-and-fitness/health-connect/read-data); [get started](https://developer.android.com/health-and-fitness/health-connect/get-started)
- "Starting Android 14 (API Level 34), Health Connect is part of the Android Framework." On Android 13 and lower it is a separate app from the Play Store. The SDK supports Android 8+, the Health Connect app Android 9+.
- "Foreground reads: You can normally read data from Health Connect when your app is in the foreground." "Background reads: By requesting an extra permission from the user, you can read data after the user or system places your app in the background." The permission is `android.permission.health.READ_HEALTH_DATA_IN_BACKGROUND`, and availability must be checked with the feature status API.
- "Features tied to the system module remain unavailable on Android 13 and lower, even with the APK."
- "By default, all applications can read data from Health Connect for up to 30 days prior to when any permission was first granted." Beyond that needs `PERMISSION_READ_HEALTH_DATA_HISTORY`; "without this permission, an attempt to read records older than 30 days results in an error."
- "If a user deletes your app, all permissions, including the history permission, are revoked."
- "Because users can grant or revoke permissions at any time, your app needs to check for permissions every time before using them".
- With Android 14 and SDK extension 20+, Health Connect counts steps on the phone itself once any app holds `READ_STEPS`; written at most about once a minute.
- For cumulative types such as steps, use `aggregate()` "to avoid double counting from multiple sources".

**2025–2026 changes**
- Android 16 (apps targeting API 36): APIs that needed `BODY_SENSORS` now need granular `android.permission.health.*` permissions: `BODY_SENSORS` maps to `READ_HEART_RATE`, `READ_OXYGEN_SATURATION` and `READ_SKIN_TEMPERATURE`; `BODY_SENSORS_BACKGROUND` maps to `READ_HEALTH_DATA_IN_BACKGROUND`. Mobile apps using these must also declare the privacy-policy activity. — [Android 16 behavior changes](https://developer.android.com/about/versions/16/behavior-changes-16)
- Developers who used the old Health Connect API request form had to redeclare in Play Console by 22 January 2025. — [Publish your health app](https://developer.android.com/health-and-fitness/health-connect/publish)
- Health apps declaration mandatory for all apps after 31 August 2024. — [Play Console Help 14738291](https://support.google.com/googleplay/android-developer/answer/14738291)
- Google Fit APIs deprecated in 2026; Fitbit Web API support ended 30 September 2026 (see section 2). — [Fit migration FAQ](https://developer.android.com/health-and-fitness/health-connect/migration/fit/faq); [dev.fitbit.com](https://dev.fitbit.com/build/)
- June 2026: on-device steps attribution changed to a per-device synthetic package name. — [Health Connect: read data](https://developer.android.com/health-and-fitness/health-connect/read-data)

**Medical device versus wellness**
- FDA issued a revised final "General Wellness: Policy for Low Risk Devices" guidance on 6 January 2026, superseding the 2019 version. The two tests are unchanged: intended only for general wellness use, and low risk. The revision is more explicit that non-invasive sensor wearables measuring physiological metrics can qualify. (Law-firm summaries; FDA document itself not opened.) — [Covington](https://www.cov.com/news-and-insights/insights/2026/01/fda-issues-revised-guidance-on-general-wellness-products); [Foley](https://www.foley.com/insights/publications/2026/01/digital-health-policy-fda-relaxes-restrictions-over-wearables-and-ai-decision-ma/); [King & Spalding](https://www.kslaw.com/news-and-insights/fda-updates-general-wellness-and-clinical-decision-support-guidance-documents)
- EU: under MDCG 2019-11 (Rev.1, June 2025) qualification as medical device software turns on the manufacturer's intended purpose, meaning what is claimed, not how the software works; lifestyle and well-being software is outside the MDR. (Consultancy summaries; MDR recital and MDCG PDF not opened.) — [OpenRegulatory](https://openregulatory.com/mdcg/mdcg-2019-11); [Emergo](https://www.emergobyul.com/news/european-revision-primary-software-guidance-mdcg-2019-11-revision-1-small-changes-meaningful)
- Apple 1.4.1 rejects unvalidated accuracy claims about health measurements; Google says a health-integrated game "should not function as an unregulated medical tool." — [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/); [Play Console Help 12991134](https://support.google.com/googleplay/android-developer/answer/12991134)

### Inferences
- Apple is the harder store for this concept. There is no "game" category for HealthKit; the app must read as a health-and-fitness use, and that must be visible in the UI and the store description. A cozy game that hides all health numbers is in tension with the 2.5.1 reviewer expectation that HealthKit functionality be "clearly identified". Likely mitigations (inference, untested): a plain "Connected to Apple Health" line in settings and onboarding, the three meters explained as coming from Apple Health, a store description that says so in the first paragraph, and App Review notes explaining the mapping from data to world.
- On Google the concept is explicitly allowed as a health-integrated game, but each data type needs a justification. Heart rate variability, resting heart rate, respiratory rate and SpO2 are closer to "clinical vitals" than steps and sleep; expect them to draw more scrutiny. The project's rule that the game is fully playable on steps and sleep alone gives a fallback: ship those first, add the richer types in a later declaration.
- Never knowing whether read access was denied on iOS means the game cannot say "you declined sleep access"; it can only say "no sleep data yet" and offer a link to settings. This matches the project's "not arrived yet is normal" rule and its tier model.
- The 30-day default history window on Android is enough for rolling baselines but not for seeding a long baseline at install. Asking for the history permission adds a declaration item; inference is to skip it at first.
- On-device-only storage satisfies Apple 5.1.3(ii) (no personal health information in iCloud) only if saved game state that embeds health-derived values is kept out of iCloud backup/CloudKit. Whether derived meter values count as "personal health information" is not stated; safest reading is to exclude them. Inference.
- Avoid Apple's Activity ring look for the three meters; the HIG forbids ring-like elements for move/exercise/stand data.
- Wording to avoid (inference from the intended-purpose tests and the store rules): diagnose, treat, cure, prevent, monitor a condition, detect, clinical, medical-grade, accuracy claims, "improves your sleep/HRV/health", naming any disease, and any phrase implying the app measures the body itself. Safer: "reflects", "inspired by", "your day", "rest", "for fun and general wellness". Not legal advice; no regulator text was read directly.

### Gaps
- Whether a game on a personal Google Play developer account that declares "Activity and fitness" and "Sleep management" is forced onto an organization account (D-U-N-S) is NOT resolved. The rule text names only medical and research apps as examples, but one developer anecdote says otherwise. This should be confirmed with Play Console support before Phase 1, since it affects a solo developer directly.
- No documented case was found of a game specifically being approved or rejected for Health Connect or HealthKit use. The other researchers' product profiles (shipping step and sleep games) are the practical proof that approval is possible.
- The exact Play policy sentence defining when the "not a medical device" disclaimer is mandatory was not captured.
- Play policy quotes for 9888170 and 12991134 came back as fragments; the full paragraphs should be read on the live page.
- The current revision date of the App Store Review Guidelines is not shown on the page; the final 14,000 characters of the page were not read (unlikely to contain health rules).
- Per-data-type sensitivity tiers in Health Connect (how sleep and heart rate are classed) were not found stated beyond "high-sensitivity categories (such as reproductive health, substance use, clinical vitals, and self-reported symptoms)".
- The FDA guidance and the MDR/MDCG texts were read only through law-firm and consultancy summaries.
- Apple's rules on HealthKit background delivery behaviour for sleep analysis specifically (frequency cap) were not confirmed.
- No Google-side developer rejection thread could be opened and read in full.

## 5. Gaps in the market: what nobody seems to be doing

### Takeaway
Everything in this section is INFERENCE from the cross-cutting evidence above, not from a product census; the product-by-product researchers are better placed to confirm or refute each point. The evidence suggests the open space is a passive, multi-signal, no-loss, on-device world, and that the main reason it is open may be that it is hard to monetise and hard to get through Apple review.

### Cited Findings
- Google's own description of the games category assumes activity data drives gameplay: "games apps that collect a user's activity data as a way to advance game play". Sleep and recovery signals are not mentioned. — [Play policy 16679511](https://support.google.com/googleplay/android-developer/answer/16679511)
- The one product found that adjusts targets to recovery state (Gentler Streak) is a tracker, not a game, and still frames progress as a streak. — [App Store listing](https://apps.apple.com/us/app/gentler-streak-workout-tracker/id1576857102)
- The documented failures were products dependent on servers, token economies or vendor cloud APIs. — [NME on Niantic](https://www.nme.com/news/pokemon-go-developer-confirms-230-layoffs-cancels-marvel-game-3463283); [Decrypt on STEPN](https://decrypt.co/111809/crypto-fitness-app-stepn-denies-layoff-reports); [dev.fitbit.com](https://dev.fitbit.com/build/)
- Health gamification mostly relies on extrinsic rewards and positive reinforcement. — [PMC6096297](https://pmc.ncbi.nlm.nih.gov/articles/PMC6096297)

### Inferences
- Passive multi-signal worlds: studied and shut-down products are driven by one signal, almost always steps or location. Combining sleep, recovery and activity into one world state, with no player input required, did not appear in any source read here. INFERENCE.
- Recovery-aware targets inside a game: adjusting what counts as a good day to the body's state appears in one tracker and in no game found. INFERENCE.
- No-loss progression: even the gentle products keep a streak or a currency. A level that never drops, with dormancy as the only consequence, has a precedent in cozy games (New Horizons) but not, in what was found, in a health-driven product. INFERENCE.
- On-device only: the failures above were all cloud-dependent. No source described a health game that states it sends nothing off the device; this may simply be because such products are small and unreported. INFERENCE, low confidence.
- Hidden numbers: the orthosomnia and tracker-guilt literature argues for not showing raw values, yet trackers compete on showing more of them. A product that deliberately shows only coarse meters is unusual. INFERENCE.
- Possible reasons the gap exists (INFERENCE): no backend means no accounts, social features or server-side monetisation; no loss mechanic means giving up the best-measured retention lever; Apple's requirement that HealthKit use be visibly "health and fitness" pulls products toward dashboards; and background-read limits make a passive world feel stale unless the app is opened.

### Gaps
- This section cannot establish absence. A claim that "nobody does X" needs the per-product profiles from the other researchers; treat every line above as a hypothesis to test against them.
- No market-size or willingness-to-pay evidence for a calm, no-loss health game was found.
