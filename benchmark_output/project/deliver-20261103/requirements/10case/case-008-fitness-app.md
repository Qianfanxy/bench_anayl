# Fitness App（10case / case-008）

- 原始模板（只读）：https://www.figma.com/design/MW0UgeOT43xqVhoSAzNMPH/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/MW0UgeOT43xqVhoSAzNMPH/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Fitness App — workouts and daily activity

Design a fitness app: get started, pick a workout or continue today’s plan, explore programs, open a workout to see its rounds, and review today’s activity report. Canvas 390 × 844, iPhone. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 5 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The two brand colors and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the photos, the map and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Onboarding

02_Home

Goal: Feel motivated and start.

Goal: Pick a popular workout or continue today’s plan.

MUST INCLUDE

MUST INCLUDE

• Actions: “Get Started”
• Copy: “Wherever you are, health is number one” · “There is no instant way to a healthy life”
• Media: Photo_Onboarding

• Greeting: “Good Morning 🔥” · “Pramuditya Uzumaki”
• Main navigation: tab bar Home / Explore / Analytics / Profile · current: Home
• Popular Workouts: “Popular Workouts” · Lower Body Training · Hand Training, each with photo, kcal (Icon_Fire), minutes (Icon_Timer) and play (Icon_Play) (see DATA)
• Search: “Search” (Icon_Search)
• Today Plan: “Today Plan” · Push Up · Sit Up · Knee Push Up, each with photo, daily goal, progress and level (see DATA)

LINKS

→ Get Started → 02_Home

LINKS

→ Lower Body Training → 04_Workout
→ Explore tab → 03_Explore
→ Analytics tab → 05_Analytics

03_Explore

04_Workout

Goal: Discover programs and challenges.

Goal: Understand a workout and start it.

MUST INCLUDE

MUST INCLUDE

• Banner: “Best Quarantine Workout” · “See more” (Icon_Chevron_Right, Photo_Quarantine_Workout)
• Best for you: “Best for you” · 4 programs, each with photo, minutes and level (see DATA)
• Challenge: “Challenge” · Plank Challenge · Sprint Challenge · Squat Challenge
• Fast Warmup: “Fast Warmup” · 2 programs, each with photo, minutes and level (see DATA)
• Main navigation: tab bar · current: Explore

• Actions: back (Icon_Back) · “Let’s Workout”
• Description: see DATA
• Header: “Workout”
• Media: Photo_Lower_Body_Training
• Rounds: “Rounds” · 1/3 · Jumping Jacks 00:30 · Squats 01:00 · Backward Lunge 00:30, each with photo and play (Icon_Play)
• Stats: “Time” 50 min (Icon_Timer) · “Burn” 500 kcal (Icon_Fire)
• Title: “Lower Body Training”

LINKS

LINKS

→ Home tab → 02_Home
→ Analytics tab → 05_Analytics

→ back → 02_Home

05_Analytics

Goal: Review today’s activity.

MUST INCLUDE

• Calendar: “July 2022” · S 10 – S 17 · current: T 12
• Main navigation: tab bar · current: Analytics
• Report: “Today Report” · Active calories · Training time · Cycling (Map_Cycling_Route, Icon_Cycling) · Heart Rate (Icon_Heart_Rate) · Steps (Icon_Steps) · “Keep it Up! 💪” · Sleep (Icon_Sleep) · Water (Icon_Water) (see DATA)

LINKS

→ Home tab → 02_Home
→ Explore tab → 03_Explore

Navigation structure

• Bottom tab bar on 02, 03 and 05 with 4 tabs in this order: Home (Icon_Home), Explore (Icon_Explore), Analytics (Icon_Analytics), Profile (Icon_Profile). Current: Home on 02, Explore on 03, Analytics on 05. How the current tab looks is yours.
• 01_Onboarding → Get Started → 02_Home. 04_Workout is pushed from the Lower Body Training card on 02 and has no tab bar.
• Entry only (no frame): Profile tab, search, Hand Training, plan rows, See more, programs, challenges, rounds, Let’s Workout, calendar days, report tiles.

Fixed data & copy

Use these values verbatim.

User

Popular workouts

Today Plan

Pramuditya Uzumaki · greeting “Good Morning 🔥”

Lower Body Training · 500 Kcal · 50 Min (Photo_Lower_Body_Training)
Hand Training · 600 Kcal · 40 Min (Photo_Hand_Training)

Push Up · 100 push ups a day · 45% · Intermediate (Photo_Push_Up)
Sit Up · 20 sit ups a day · 75% · Beginner (Photo_Sit_Up)
Knee Push Up · 20 knee push ups a day · 45% · Beginner (Photo_Knee_Push_Up)

Explore · Best for you

Explore · Fast Warmup

Explore · Challenge

Belly fat burner · 10 min · Beginner (Photo_Belly_Fat_Burner)
Lose Fat · 10 min · Beginner (Photo_Lose_Fat)
Plank · 5 min · Expert (Photo_Plank)
Build Wider Biceps · 30 min · Intermediate (Photo_Build_Wider_Biceps)

Leg exercises · 10 min · Beginner (Photo_Leg_Exercises)
Backward lunges · 5 min · Beginner (Photo_Backward_Lunges)

Plank Challenge · Sprint Challenge · Squat Challenge

Workout (04)

Analytics · July 2022

Lower Body Training · Time 50 min · Burn 500 kcal
“The lower abdomen and hips are the most difficult areas of the body to reduce when we are on a diet. Even so, in this area, especially the legs as a whole, you can reduce weight even if you don’t use tools.”
Rounds 1/3: Jumping Jacks 00:30 (Photo_Jumping_Jacks) · Squats 01:00 (Photo_Squats) · Backward Lunge 00:30 (Photo_Backward_Lunges)

Days: S 10 · M 11 · T 12 (current) · W 13 · T 14 · F 15 · S 16 · S 17
Active calories 645 Cal · Training time 80%
Heart Rate 79 Bpm · Steps 999/2000 · Keep it Up! 💪
Water 6/8 Cups · Sleep (chart, values illustrative)

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand colors #BBF246 + #192126 and Lato
• Media: photos, map, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces, analytics tiles, level tags, progress, error / disabled
• Type scale, spacing, radii, elevation
• All states: current tab, current day, pressed, playing, disabled
• Headers, tab bar, workout cards, plan rows, level tags, stat chips, round rows, day strip, analytics tiles, charts
• How photos are cropped and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, current day, plan progress, round list)

Deliverable: the link to your own Figma file containing the 5 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Fitness App

Fixed: the two brand colors and the typeface below — the brand relies on the lime and charcoal pair. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces, the colors of the analytics tiles (heart rate, steps, sleep, water…), level tags, progress, error and disabled, type scale, spacing, radii and elevation.

Brand colors

Brand primary · lime

Brand dark · charcoal

#BBF246

#192126

The app’s signature accent. Where and how much to use it is your decision.

The brand’s second color, paired with the lime. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  500 Kcal

Use Lato for all UI text (Regular / Bold / Black available; the source also used Poppins on a few labels — use Lato instead). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 390 × 844 (iPhone 13 / 14). 02_Home, 03_Explore, 04_Workout and 05_Analytics may scroll vertically. Light or dark surfaces per screen are your decision.
