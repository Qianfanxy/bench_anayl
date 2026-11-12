# Budget（10case / case-010）

- 原始模板（只读）：https://www.figma.com/design/2y1tZHHBvy0uiRFSVBBaiH/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/2y1tZHHBvy0uiRFSVBBaiH/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Budget — monthly expenses, bills and credit score

Design a personal budgeting app: see this month’s spending against the budget by category, check the monthly subscriptions, and review the credit score. Canvas 375 × 812, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 3 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only the platform shell (status bar, home indicator) — this task has no primary button and no text input. Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the service logos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Expenses

02_Bill

Goal: See how much of this month’s budget is spent, by category.

Goal: See what I pay for subscriptions each month.

MUST INCLUDE

MUST INCLUDE

• Budget: “Left to spend” $738 · “Monthly budget” $2,550 · progress of spending against the budget
• Categories: Auto & transport · Bill & Utilities, each with icon, total and item rows with amount, amount left and progress (see DATA)
• Header: back (Icon_Back) · “Expenses” · add (Icon_Plus)
• Main navigation: tab bar Overview / This Month / Offers / Setting · current: This Month
• More: more categories (Icon_More)
• Period: “September 2020” (Icon_Chevron_Down) · total spent $1,812

• Header: back (Icon_Back) · “Bill” · add (Icon_Plus)
• Main navigation: tab bar · current: This Month
• Segments: Bills · Payments · Subscription · current: Subscription
• Subscriptions: Patreon membership · Netflix · Apple payment · Spotify, each with logo, monthly price and open (Icon_Chevron_Right) (see DATA)
• Summary: “Your monthly payment for subscriptions” · $58.97

LINKS

→ back → 01_Expenses

LINKS

→ Bill & Utilities card → 02_Bill

03_Credit_Score

Goal: Understand my credit score and what drives it.

MUST INCLUDE

• Factors: On-time payments · Credit Utilization · Age of credit, each with value, rating and detail (see DATA)
• Header: back (Icon_Back) · “Credit Score”
• Main navigation: tab bar · current: This Month
• Score: 660 · “Good” · +6pts · range 400 – 850 · “Last update on 20 Jul 2020”

LINKS

→ back → 01_Expenses

Navigation structure

• Bottom tab bar on all 3 frames with 4 tabs in this order: Overview (Icon_Overview), This Month (Icon_This_Month), Offers (Icon_Offers), Setting (Icon_Setting). Current: This Month on all three. How the current tab looks is yours.
• 01_Expenses is the This Month screen. 02_Bill is pushed from the Bill & Utilities card; back returns to 01.
• 03_Credit_Score: the source shows no entry point — link it from wherever you see fit; its back returns to 01_Expenses.
• Entry only (no frame): period picker, add, more categories, item rows, Bills and Payments segments, subscription rows, factor rows, Overview / Offers / Setting tabs.

Fixed data & copy

Use these values verbatim.

Period and totals

Auto & transport · $600 (Icon_Car)

Bill & Utilities · $320 (Icon_Bill)

September 2020 · spent $1,812
Left to spend $738 · Monthly budget $2,550

Auto & transport · $350 · Left $186
Auto insurance · $250 · Left $120

Subscriptions · $52 · Left $0
House service · $138 · Left $10
Maintenance · $130 · Left $30

Subscriptions (02, in this order)

Credit score (03)

Factors (03, in this order)

Total: Your monthly payment for subscriptions · $58.97
Patreon membership · $19.99/mo (Logo_Patreon)
Netflix · $12/mo (Logo_Netflix)
Apple payment · $19.99/mo (Logo_Apple)
Spotify · $6.99/mo (Logo_Spotify)

660 · Good · +6pts
Range 400 – 850 · Last update on 20 Jul 2020

On-time payments · 95% · Good · 1 missed
Credit Utilization · 95% · Not bad · -15%
Age of credit · 8 years · Good

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #6347EB and DM Sans
• Media: service logos, icons
• Platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces, category and progress colors, rating colors (good / not bad), gauge, error / disabled
• Type scale, spacing, radii, elevation
• All states: current tab, current segment, pressed, disabled
• Headers, tab bar, segmented tabs, period picker, budget summary, category cards, progress rows, subscription rows, credit gauge, factor rows
• How progress and the score gauge are visualized

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, current segment, progress and gauge)

Deliverable: the link to your own Figma file containing the 3 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Budget

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces, category colors in budget bars, status colors (good, not bad, over budget), gauge colors, selected and disabled states, type scale, spacing, radii and elevation.

Brand color

Brand primary · violet

#6347EB

The app’s signature accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  $1,812

Use DM Sans for all UI text. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 375 × 812 (iPhone X / 11 Pro). Light mode. 01_Expenses may scroll vertically.
