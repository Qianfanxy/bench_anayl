# Travelin（10case / case-002）

- 原始模板（只读）：https://www.figma.com/design/9SYZ6WViis3SYesGQnnFuw/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/9SYZ6WViis3SYesGQnnFuw/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Travelin — travel booking app

Design the Travelin mobile app: open the app, start the journey, sign in, and land on a home screen with the upcoming flight, travel categories, recommended journeys and a recommended hotel. Canvas 430 × 932, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 4 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The two brand colors and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, overlays on photos, status badge, rating, error / disabled), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the language selector, the tab bar and every business component as reusable components in your file.
5. Use the logo, photos and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Splash

02_Get_Started

Goal: Brand moment while the app opens.

Goal: Invite the traveller to start.

MUST INCLUDE

MUST INCLUDE

• Brand: Logo_Travelin · tagline “Your Passport to Seamless Adventures!”

• Action: “Your Journey Starts Here” (Icon_Plane)
• Brand: Logo_Travelin
• Headline: “Ready to explore beyond boundaries?”
• Language: “English” (Icon_Chevron_Down)
• Media: Photo_Aerial_Island

LINKS

→ after delay → 02_Get_Started

LINKS

→ Your Journey Starts Here → 03_Sign_In

03_Sign_In

04_Home

Goal: Sign in with email / phone or a social account.

Goal: See the upcoming trip and find the next journey.

MUST INCLUDE

MUST INCLUDE

• Actions: “Forgot password?” · “Sign In” · “Sign Up”
• Copy: “Don’t have an account?” · “Discover the World with Every Sign In” · “Let’s Travel you in.” · “or sign in with”
• Fields: “Email or Phone Number” · “Password” — both empty
• Language: “English” (Icon_Chevron_Down)
• Media: Photo_Hot_Air_Balloons
• Social sign-in: Apple (Icon_Apple) · Facebook (Icon_Facebook) · Google (Icon_Google)

• Account: “Hi, Paul” · 2,000 points (Icon_Coin) · avatar (Photo_Avatar_Cat)
• Categories: Bus · Ferry · Flights · Hotels · Trains, each with its icon
• Hotels: “Hotel recommendations for you” · See all · Swiss-Belhotel Rainforest Kuta (see DATA)
• Journeys: “Journey together” · See all · Labengki Sombori · Mount Bromo · Sailing Komodo (see DATA)
• Main navigation: tab bar Home / Orders / Deals / Account · current: Home
• Search: “Where to go?” (Icon_Search)
• Upcoming flight: ticket with status, date, route, times, duration, airline, class, stops and booking ID (see DATA)

LINKS

→ Sign In → 04_Home

LINKS

→ Home tab: current (no link)

Navigation structure

• Launch flow: 01_Splash → (after delay) 02_Get_Started → 03_Sign_In → 04_Home.
• 04_Home has a bottom tab bar with 4 tabs in this order: Home (Icon_Home), Orders (Icon_Ticket), Deals (Icon_Deals), Account (Icon_Account); current: Home. Only Home is part of this task — how the current tab looks is yours.
• Entry only (no frame): language selector, Forgot password?, social sign-in, Sign Up, search, categories, See all, journey and hotel cards, the flight ticket, Orders, Deals, Account.

Fixed data & copy

Use these values verbatim. Prices in USD.

Account

Upcoming flight

Journey together (rating · price · duration)

“Hi, Paul” · 2,000 points · Photo_Avatar_Cat

Status: Upcoming · 24 March 2024
CGK 05:30 → DPS 08:00 · 1h 30m
Sentosa Air · Economy · Direct
Booking ID: ZEEBAW
(local times — Bali is 1 hour ahead of Jakarta)

Mount Bromo · Volcano in East Java · ★ 4.9 · Start from $150/pax · 3D2N (Photo_Mount_Bromo)
Labengki Sombori · Islands in Sulawesi · ★ 4.8 · Start from $250/pax · 3D2N (Photo_Labengki_Sombori)
Sailing Komodo · Labuan Bajo · ★ 4.8 · Start from $200/pax · 3D2N (Photo_Sailing_Komodo)

Hotel recommendations for you

Categories · tabs

Sign-in copy

Swiss-Belhotel Rainforest Kuta · 4-star hotel
Jl. Sunset Road No. 101, Kuta, Bali, Indonesia
$50/night (Photo_Hotel_Room)

Categories: Flights (Icon_Flight) · Hotels (Icon_Hotel) · Trains (Icon_Train) · Ferry (Icon_Ferry) · Bus (Icon_Bus)
Tabs: Home · Orders · Deals · Account

“Let’s Travel you in.” · “Discover the World with Every Sign In”
Fields: Email or Phone Number · Password
“Forgot password?” · Sign In · “or sign in with”
“Don’t have an account?” · Sign Up

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand colors #007A8C + #336749 and Inter
• Media: logo, photos, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, overlays on photos, status badge, rating, error / disabled
• Type scale, spacing, radii, elevation
• All states: current tab, pressed, focused / filled fields, disabled
• Headers, language selector, tab bar, flight ticket, category items, journey and hotel cards, social sign-in buttons
• How photos are cropped and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, empty fields, pressed / disabled where shown)

Deliverable: the link to your own Figma file containing the 4 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Travelin

Fixed: the two brand colors and the typeface below — they carry Travelin’s identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, overlays on photos, semantic colors (status badges, rating, success, error, disabled), type scale, weights per role, spacing, radii and elevation.

Brand colors

Brand primary · teal

Brand secondary · forest green

#007A8C

#336749

Travelin’s main brand color. Where and how much to use it is your decision.

The second brand color (the “in” of the logo). Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  $150/pax  CGK → DPS

Use Inter for all UI text (Regular / Medium / Semi Bold / Bold available). Sizes, weights and line heights are yours to define as a consistent type scale. The logo is an image in 04 · Media — do not retype it.

Canvas: 430 × 932 (iPhone). Light mode only. 04_Home may scroll vertically.
