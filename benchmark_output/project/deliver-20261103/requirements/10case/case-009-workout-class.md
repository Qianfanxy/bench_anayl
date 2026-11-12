# Workout Class（10case / case-009）

- 原始模板（只读）：https://www.figma.com/design/FW3jfozfyaOg9OWNXdH1Vq/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/FW3jfozfyaOg9OWNXdH1Vq/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Workout Class — fitness classes and activity tracking

Design a fitness class app: get started, find a workout class, open the Warm up category to see its exercises, and review this week’s activity. Canvas 414 × 896, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 4 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the illustrations, the avatar, the photos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Onboarding

02_Home

Goal: Understand what the app offers and start.

Goal: Find a workout class.

MUST INCLUDE

MUST INCLUDE

• Actions: “Get started”
• Copy: “Best workouts for you” · “You will have everything you need to reach your personal fitness goals — for free!”
• Media: Illustration_Onboarding

• Categories: “Categories” · “See all” · Warm up · Yoga · Squats · Lunge, each with its photo (see DATA)
• Greeting: “Hello, Adam Smith” · Avatar_Adam_Smith · menu (Icon_Menu)
• Main navigation: tab bar Home / Activity / Profile / Settings · current: Home
• Recommendation Class: “Recommendation Class” · “See all” · Yoga Class · “With Rachael Wisdom” · Photo_Yoga_Class · favorite (Icon_Heart)
• Search: “Search” (Icon_Search)
• Title: “Find Your Workout Class”
• Today’s activity: “Today’s activity” · 8.00 AM - 1.30 PM · Illustration_Todays_Activity

LINKS

→ Get started → 02_Home

LINKS

→ Warm up category → 03_Warm_Up
→ Activity tab → 04_Activity

03_Warm_Up

04_Activity

Goal: Understand the Warm up session and pick an exercise.

Goal: Review the calories and activities of a day this week.

MUST INCLUDE

MUST INCLUDE

• Actions: back (Icon_Back) · more (Icon_More) · play video (Icon_Play)
• Description: “Warm up properly before exercising to prevent injury and make your workouts more effective.”
• Exercises: “Exercises” · Exercise 1 – Exercise 10, each with photo, duration and play (Icon_Play_Small) (see DATA)
• Main navigation: tab bar · current: Home
• Media: Photo_Seated_Hug (video cover)
• Tags: 37.10 mins (Icon_Clock) · Running (Icon_Running)
• Title: “Warm up”

• Actions: back (Icon_Back) · more (Icon_More)
• Activities: Running · Swimming · Cycling, each with time range, hours and kilometers (Icon_Running, Icon_Swimming, Icon_Cycling) (see DATA)
• Calories: 1680 kcal
• Chart: hourly calories, axis 8AM · 10AM · 12PM · 2PM · 4PM · selected: 4PM · 120 cal
• Main navigation: tab bar · current: Activity
• Title: “Your activities”
• Week: “This week” · Sat 26 – Fri 01 · selected: Mon 28

LINKS

LINKS

→ back → 02_Home
→ Home tab → 02_Home

→ back → 02_Home
→ Activity tab → 04_Activity

Navigation structure

• Bottom tab bar on 02, 03 and 04 with 4 tabs in this order: Home (Icon_Home), Activity (Icon_Activity), Profile (Icon_Profile), Settings (Icon_Settings). Current: Home on 02 and 03, Activity on 04. How the current tab looks is yours.
• 01_Onboarding → Get started → 02_Home. 03_Warm_Up is pushed from the Warm up category card on 02.
• Entry only (no frame): menu, avatar, search, Today’s activity card, See all, Yoga Class, favorite, Yoga / Squats / Lunge, more, play video, exercise rows, days, chart hours, activity cards, Profile and Settings tabs.

Fixed data & copy

Use these values verbatim.

User

Today’s activity

Recommendation Class

Adam Smith (Avatar_Adam_Smith) · greeting “Hello, Adam Smith”

8.00 AM - 1.30 PM (Illustration_Todays_Activity)

Yoga Class · With Rachael Wisdom (Photo_Yoga_Class)

Categories (in this order)

Warm up (03)

Exercises (03, in this order)

Warm up (Photo_Seated_Hug)
Yoga (Photo_Meditation)
Squats (Photo_Squat)
Lunge (Photo_Lunge)

Tags: 37.10 mins · Running
Video cover: Photo_Seated_Hug

Exercise 1 · 02.30 Minutes (Photo_Forward_Fold)
Exercise 2 · 02.00 Minutes (Photo_Chair_Pose)
Exercise 3 · 03.20 Minutes (Photo_Side_Plank)
Exercise 4 · 02.30 Minutes (Photo_Bent_Over)
Exercise 5 · 05.30 Minutes (Photo_Meditation)
Exercise 6 · 06.10 Minutes (Photo_Seated_Hug)
Exercise 7 · 04.50 Minutes (Photo_Lunge)
Exercise 8 · 03.30 Minutes (Photo_Arm_Stretch)
Exercise 9 · 01.30 Minutes (Photo_Back_Bend)
Exercise 10 · 05.20 Minutes (Photo_Tabletop_Kick)

Week (04)

Activities (04, in this order)

Sat 26 · Sun 27 · Mon 28 (selected) · Tue 29 · Wed 30 · Thu 31 · Fri 01
1680 kcal
Chart: 8AM – 4PM, selected 4PM · 120 cal (curve values illustrative)

Running · 8.00 AM - 9.30 AM · 1.32 hours · 9.50 kilometers
Swimming · 8.00 AM - 9.30 AM · 1.32 hours · 9.50 kilometers
Cycling · 8.00 AM - 9.30 AM · 1.32 hours · 9.50 kilometers

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #24C8FE and Inter
• Media: illustrations, avatar, photos, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces, category tints, activity colors, chart fill, error / disabled
• Type scale, spacing, radii, elevation
• All states: current tab, selected day, selected hour, pressed, favorited, disabled
• Headers, tab bar, activity card, class card, category cards, tags, exercise rows, day pills, chart, activity cards
• How photos and cut-outs are cropped, backed and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, selected day, selected hour)

Deliverable: the link to your own Figma file containing the 4 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Workout Class

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces, category card tints, activity colors (running, swimming, cycling), chart fill, selected and disabled states, type scale, spacing, radii and elevation.

Brand color

Brand primary · sky blue

#24C8FE

The app’s signature accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  1680 kcal

Use Inter for all UI text (Regular / Medium / Semi Bold / Bold / Extra Bold available; the source also used Merriweather on the onboarding headline and Nunito on a few labels — use Inter instead). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 414 × 896 (iPhone 11 Pro Max). Light mode. 02_Home, 03_Warm_Up and 04_Activity may scroll vertically.
