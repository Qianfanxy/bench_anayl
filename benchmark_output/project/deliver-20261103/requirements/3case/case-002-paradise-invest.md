# Paradise Invest（3case / case-002）

- 原始模板（只读）：https://www.figma.com/design/AuqY1P2MVRVdEbLBKDwPWn/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/AuqY1P2MVRVdEbLBKDwPWn/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

DESIGNER STARTER / PARADISE INVEST · LEVEL L2 · v2

Complete mobile product design

Content, structure, brand primary and typefaces are fixed. Layout, hierarchy, all other colors, states, components and visual system are yours.

THE ASSIGNMENT

Design the complete Paradise Invest mobile investment app (brand: Paradise Group) for a first-time investor: sign up, understand their portfolio, follow plans and news, and manage their profile and bank accounts.

English interface / Nigerian Naira (₦) / one signed-in user: Jonas Macroni. Base viewport 414 × 932 for every frame; Home may scroll vertically.

FIXED by this brief: frame list & names, the content each frame must contain (what, not how), navigation structure, all data and copy, brand primary color, typefaces (DM Sans + Inter), media, a default Button, a default Text Field and the platform shell.

YOURS to decide: layout, grouping, order and emphasis on every screen; all other colors (neutrals, text, surfaces, semantic); type scale, spacing, radii, elevation; all states (selected, pressed, disabled, focused, error); headers, bottom navigation and every business component.

FRAMES TO DELIVER (11) — USE THESE EXACT NAMES

01_Splash · 02_Welcome · 03_Create_Account_Empty · 03_Create_Account_Filled · 03_Create_Account_Error · 04_Home ·

05_My_Asset_Overlay · 06_Notification · 07_Profile · 08_Contact_Info · 09_Bank_Account_Info. One frame per state.

FRAME-BY-FRAME CHECKLIST

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks. Layout, grouping, emphasis and styling are your decisions.

01_Splash

Goal: brand recognition while the app loads.

Must include:
• Brand: Paradise Group logo

Links: auto-advances to 02_Welcome.

02_Welcome

Goal: explain the value and start sign-up.

Must include:
• Actions: Create account · Login
• Copy: “Stay on top of your finance with us.” · “We are your new financial advisors to recommend the best investments for you.”
• Media: Welcome_Illustration

Links: Create account → 03_Create_Account_Empty.

03_Create_Account (Empty / Filled / Error)

Goal: create an account with minimum effort and clear validation.

Must include:
• Actions: back · Create account · “Already have an account?” Login
• Copy: “Create an account” · “Invest and double your income now”
• Form: Email address · Full name · Password (can be shown or hidden)

States (one frame each):
• Empty — nothing entered; Create account cannot be submitted yet
• Error — email “jonas.macroni@invest” · message “Enter a valid email address”
• Filled — Jonas Macroni · jonas.macroni@invest.ai · password entered (masked); Create account can be submitted

Links: back → 02_Welcome; Create account (Filled) → 04_Home.

04_Home

Goal: see total wealth and today’s change at a glance, then explore plans and learning content.

Must include:
• Account: “Welcome, Jonas.” · menu entry · notification entry
• Actions: Invest now
• Articles: “Investment Guide” · 3 articles, each with title, summary and thumbnail
• Main navigation: current tab Home
• Plans: “Best Plans” · See All · Gold 30% / Silver 60% / Platinum 90% return, each with its coin image
• Portfolio: “Your total asset portfolio” · ₦203,935 · +2%

Links: portfolio → 05_My_Asset_Overlay; notification entry → 06_Notification; Account tab → 07_Profile.

05_My_Asset_Overlay

Goal: inspect holdings and recent activity without leaving Home.

Must include:
• Actions: close · See All Plans
• Copy: “My Asset”
• Current plan: “Current Plans” · Gold · 30% return
• History: “History” · 4 transactions, each with type (Buy / Sell), stock, amount and date
• Portfolio: “Your total asset portfolio” · ₦203,935 · +2%
• Presentation: opens over Home; Home stays behind it

Links: close → 04_Home.

06_Notification

Goal: scan recent updates quickly.

Must include:
• Actions: back
• Copy: “Notification”
• Notifications: 3, newest first, each with thumbnail, message and time

Links: back → 04_Home.

07_Profile

Goal: identify the account and reach account settings.

Must include:
• Account: avatar · Jonas Macroni · level “Expert”
• Copy: “Profile”
• Entries: Bank Account Info · Contact Info · Document Info · Settings · Source of Funding Info
• Main navigation: current tab Account

Links: Contact Info → 08_Contact_Info; Bank Account Info → 09_Bank_Account_Info; Home tab → 04_Home.

08_Contact_Info

Goal: review personal details and see what is missing.

Must include:
• Account: avatar · edit avatar
• Actions: back
• Copy: “Contact info”
• Details: Birthdate · Email · Gender · Name — each with its value and Change
• Not added yet: Address · Phone Number — each with Add

Links: back → 07_Profile.

09_Bank_Account_Info

Goal: review linked bank accounts and add a new one.

Must include:
• Accounts: 2, each with bank logo, bank name, masked number, holder and more options
• Actions: Add account · back
• Copy: “Bank account info”

Links: back → 07_Profile.

STRUCTURE (FIXED)

Main navigation on 04_Home and 07_Profile — four tabs in this order: Home (Icon_Tab_Home) → 04 · Product (Icon_Tab_Product_Search, entry only) · Transaction (Icon_Tab_Transaction, entry only) · Account (Icon_Tab_Account) → 07. The current tab must match the frame. How it looks is yours.

My Asset opens as an overlay above Home (not a separate pushed screen). Notifications open from Home. Profile is the Account tab; Contact info and Bank account info are pushed from it with back navigation.

Entry-only (no screen required): menu, Invest now, See All, See All Plans, Login, Source of Funding Info, Document Info, Settings, Change / Add, edit avatar, more-options, Add account.

DATA & COPY (FIXED)

User: Jonas Macroni · Expert · 05 November 1993 · Male · jonas.macroni@invest.ai · phone and address not added. Same name and avatar everywhere.

Portfolio: ₦203,935, +2% — identical on Home and My Asset. Plans: Gold 30% return · Silver 60% return · Platinum 90% return. Current plan: Gold.

History (all Mon 22 Jun 2020): Buy “AAPL” Stock ₦200,000 · Sell “TLKM” Stock ₦150,000 · Buy “FB” Stock ₦1,000,240 · Sell “AAPL” Stock ₦1,000,240. Sell = money in, Buy = money out.

Articles: “Basic type of investments” — This is how you set your foot for the 2020 stock market recession. What’s next…

“How much can you start with?” — What do you like to see? It’s a very different market from 2018. The way…

“Welcome to New NASDAQ” — When we talk about Wall Street, what looks good might be different… (no photo supplied: choose a consistent fallback).

Notifications (newest first): “Where do you see yourself in the next ages?” 30 secs ago · “Check out today’s best investor. You’ll learn from him.” 3 min ago · “Apple stocks just increased. Check it out now.” 15 min ago.

Banks: Bank of America — 0182128xxx · Zenith Bank — 0182128xxx; holder Jonas Macroni.

The source file mixes user names, currencies (N / Rp) and has typos. Follow this brief, not the source.

HANDOFF & EVALUATION

Copy Components and Media into your own new Figma file; do not edit, rename or delete anything in this starter file.

Deliver all 11 frames with the exact names above, prototype links as listed, and your own reusable components. Submit your file link.

Evaluated: (1) checklist coverage per frame · (2) data & copy accuracy · (3) flow & prototype completeness · (4) information hierarchy · (5) visual quality & consistency of your own system · (6) component reuse · (7) state design.

The completed reference screens are withheld. There is no single correct layout.

## 01 · Foundations 视觉规范

PARADISE INVEST / DESIGN FOUNDATIONS

Fixed: brand primary + typefaces. You build everything else.

01  BRAND COLOR (FIXED)

Only the brand primary is given. Define every other color yourself — neutrals and grays, text, backgrounds and surfaces, semantic colors (gain / loss, error, disabled) and any supporting colors — once, and use them consistently.

Brand primary

#31A062

The Paradise Invest brand color. Where and how much to use it is your decision.

02  TYPEFACES (FIXED)

DM Sans and Inter are the brand typefaces (Inter replaces the unavailable SF Pro). Which face, size, weight and line height goes where is yours to define as a consistent type scale.

DM Sans  Aa ₦203,935

Inter  Aa Bb Cc 0123456789

03  YOUR SYSTEM (TO DESIGN)

• Base viewport 414 × 932 (fixed). Home may scroll vertically.

• Define your own type scale, spacing rhythm, corner radii, elevation, dividers and icon sizing — and apply them consistently on every screen.

• Build reusable components for repeated patterns. Component reuse and consistency are evaluated.

• Icons from 04 · Media may be recolored to your palette; do not redraw brand assets.
