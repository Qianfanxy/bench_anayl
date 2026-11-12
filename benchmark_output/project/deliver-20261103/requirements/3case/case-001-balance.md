# Balance（3case / case-001）

- 原始模板（只读）：https://www.figma.com/design/fnULASWChHEL3I3D7Sc3I7/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/fnULASWChHEL3I3D7Sc3I7/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Balance — personal finance app

Design the complete Balance mobile app: a personal finance app where Esaaa Warden signs up with a phone number, checks the balance, upcoming bills and transactions, manages cards and crypto assets, reads income analytics, follows a coin price, sends money to a contact and browses a community forum.
Canvas 375 × 812, light mode only. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 11 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, success / error / warning / disabled, chart colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the main navigation and every business component as reusable components in your file.
5. Use logos, card artwork, flags and icons from 04 · Media. People have no photos: use Avatar_Neutral or initials.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Sign_Up

02_OTP

03_Home_My_Balance

Goal: Start registration with a phone number.

Goal: Verify the phone number with a 4-digit code.

Goal: See the total balance at a glance and start money actions.

MUST INCLUDE

MUST INCLUDE

MUST INCLUDE

• Actions: Continue
• Copy: “Sign up” · “Sign up with phone number” · “A code will be sent to your number”
• Legal: “By signing up, you agree to the Terms of Service and Privacy Policy, including Cookie Use.” (Terms of Service and Privacy Policy are links)
• Phone: country code +62 (Flag_Indonesia, changeable) · number 858 2409 3560

• Actions: back · Resend code · Continue
• Code: 4 digits, none entered yet
• Copy: “OTP” · “Enter code”
• Legal: same text as 01_Sign_Up

• Account: avatar · “Hi, Esaaa!” · messages entry · notifications entry
• Actions: Send · Receive · Add
• Balance: “Your Balance” $190,008.03 · +8% · currency USD (Flag_USA, changeable)
• Main navigation: current tab Home
• Spending: “Financial health” · “Latest 7 days” · daily spend Mon–Sun with values on a 10K–50K scale · entry to details
• Transfer list: “Transfer list” · add contact · 5 contacts
• View: switch between My Balance / Upcoming Bills / Transactions · current: My Balance

LINKS

→ back → 01_Sign_Up
→ Continue → 03_Home_My_Balance

LINKS

→ Continue → 02_OTP

LINKS

→ Upcoming Bills → 04_Home_Upcoming_Bills
→ Transactions → 05_Home_Transactions
→ Send → 11_Send
→ contact Bessie Cooper → 11_Send
→ Financial health details → 09_Analytics
→ messages entry → 06_Discussion_Forum
→ tabs → 03 / 09 / 07 / 08

04_Home_Upcoming_Bills

05_Home_Transactions

06_Discussion_Forum

Goal: Review upcoming subscription bills and pay one.

Goal: Scan recent money movement.

Goal: Browse community finance discussions.

MUST INCLUDE

MUST INCLUDE

MUST INCLUDE

• Account: same as 03
• Bill actions: Add · Edit · Delete
• Bills: “Upcoming Bills” · 3 bills, soonest due first, each with logo, name, amount, due date, cycle, category and Pay now
• Main navigation: current tab Home
• View: same switch as 03 · current: Upcoming Bills

• Account: same as 03
• Main navigation: current tab Home
• Transactions: “Transactions” · 6 transactions, newest first, each with logo, type, date and signed amount (+ money in, − money out)
• View: same switch as 03 · current: Transactions

• Actions: back · messages entry · notifications entry
• Copy: “Discussion Forum”
• Posts: 2 posts, each with avatar, name, verified badge, topic, date and time, body, comment / like / dislike counts and a more menu · the user has liked Devon Lane’s post
• Search & filter: search “Search...” · Filter
• Topics: Personal Finance / Investments / Cryptocurrencies · current: Personal Finance

LINKS

LINKS

→ My Balance → 03
→ Upcoming Bills → 04
→ tabs

LINKS

→ My Balance → 03
→ Transactions → 05
→ tabs

→ back → 03_Home_My_Balance

07_Cards

08_Profile

09_Analytics

Goal: See the primary card and crypto assets.

Goal: See account identity, all cards and recent activity.

Goal: Understand income vs expenses and where income comes from.

MUST INCLUDE

MUST INCLUDE

MUST INCLUDE

• Actions: back · avatar · more menu · Add Card
• Assets: “Assets” · Solana / Bitcoin / Ethereum with ticker and value
• Card: primary card (Card_Art_Green, Esaaa Warden, **** **** **** 3447, Exp 09/24)
• Copy: “Cards”
• Main navigation: current tab Cards
• Transactions: latest 3

• Account: Esaaa Warden · avatar · primary card number · edit profile entry
• Actions: back · messages entry · notifications entry · more menu
• Cards: “Your Cards” · all 3 cards
• Copy: “Profile”
• Main navigation: current tab Profile
• Transactions: “Transactions” · See all · latest 3

• Actions: back · avatar · more menu
• Copy: “Analytics”
• Income breakdown chart: Sales $15,190.00 · 52% / Investment $11,451.03 · 39% / Other $2,590.00 · 9% · headline share “52%”
• Main navigation: current tab Analytics
• Period: “Monthly” (changeable)
• Totals: Total income $29,231.03 · Total expenses $1,999.00
• View: Income / Expenses · current: Income

LINKS

LINKS

→ back → 03
→ Bitcoin → 10_Markets
→ tabs

→ See all → 05_Home_Transactions
→ tabs

LINKS

→ back → 03
→ tabs

10_Markets

11_Send

Goal: Check a coin's price and trade it.

Goal: Send money to a contact.

MUST INCLUDE

MUST INCLUDE

• Actions: back · avatar · Sell · Buy
• Coin: “Bitcoin” with logo (changeable)
• Copy: “Markets”
• History: “History” · See all · Solana / Bitcoin / Ethereum
• Price: “Current price” $1,954.00 (+3.85%)
• Price chart: candlesticks · price scale $1,000–$5,000 · times 08:00–24:00
• Range: 1H 2H 8H 1D 1W 1M 1Y · current: 1D

• Actions: back · avatar · Send
• Amount: $500.00
• Copy: “Send”
• Number pad: 1–9, “.”, 0, backspace
• Recipient: Bessie Cooper · avatar · card **** **** **** 8820 · option to change recipient

LINKS

→ back → 03
→ Send → 03_Home_My_Balance

LINKS

→ back → 07_Cards

Navigation structure

• Onboarding: 01_Sign_Up → 02_OTP → 03_Home_My_Balance.
• Home has three views of one screen, switched in place: My Balance (03), Upcoming Bills (04), Transactions (05). All three share the same account area (avatar, greeting, messages, notifications).
• Main navigation on 03, 04, 05, 07, 08, 09 — four tabs in this order: Home (Icon_Home) → 03 · Analytics (Icon_Analytics) → 09 · Cards (Icon_Cards) → 07 · Profile (Icon_Profile) → 08. The current tab must match the frame. How it looks is yours.
• Pushed screens with back: 02, 06, 07, 08, 09, 10, 11. 06, 10 and 11 have no main navigation.
• There is no Receive, notifications or payment-success screen — do not add frames beyond the 11.

Fixed data & copy

Use these values verbatim. Amounts: “+” = money in, “-” = money out.

User & balance

Transfer list

Esaaa Warden · greeting “Hi, Esaaa!” · avatar = Avatar_Neutral
Phone: +62 (Indonesia) 858 2409 3560
Today: Aug 20, 2023 · currency USD
“Your Balance” $190,008.03 · +8% · currency selector USD (Flag_USA)

Add contact, then: Bessie Cooper, Devon Lane, Eleanor Pena, Jenny Wilson, Cody Fisher

Financial health

Upcoming bills (soonest first)

“Latest 7 days” · spend per day · axis 10K–50K
Mon 24K · Tue 35K · Wed 45K · Thu 22K · Fri 34K · Sat 18K · Sun 30K

Line Messenger (Logo_Line) · $21.00 · due Sep 05, 2023 · 1 month · Subscriptions · Pay now
Adobe XD (Logo_Adobe_XD) · $126.02 · due Sep 19, 2023 · 1 month · Subscriptions · Pay now
Netflix (Logo_Netflix) · $932.53 · due Jul 08, 2024 · 1 year · Subscriptions · Pay now
Bill actions: Add · Edit · Delete

Transactions (newest first)

Cards

Aug 19, 2023 · PayPal (Logo_PayPal) · Transferred · -$123.00
Jul 20, 2023 · DANA (Logo_DANA) · Transferred · -$12.00
May 08, 2023 · Google Play (Logo_Google_Play) · Refund · +$234.00
Feb 28, 2023 · Shopee (Logo_Shopee) · Refund · +$15.00
Jan 25, 2023 · Apple (Logo_Apple) · Payment · -$92.00
Jan 16, 2023 · Spotify (Logo_Spotify) · Payment · -$20.00
Show latest 3 where a screen asks for “latest 3”.

Card_Art_Green · Esaaa Warden · **** **** **** 3447 · Exp 09/24 · primary
Card_Art_Pink · Esaaa Warden · **** **** **** 8821 · Exp 03/26
Card_Art_Purple · Esaaa Warden · **** **** **** 5104 · Exp 11/25

Assets

Analytics

Solana · SOL · $12,094.08 (Crypto_Solana)
Bitcoin · BTC · $17,238.11 (Crypto_Bitcoin)
Ethereum · ETH · $8,200.00 (Crypto_Ethereum)

Total income $29,231.03 · Total expenses $1,999.00
Switch: Income (selected) / Expenses · Period: Monthly
Sales $15,190.00 · 52%
Investment $11,451.03 · 39%
Other $2,590.00 · 9%
Headline share: 52% (Sales)

Markets

Send

Bitcoin · “Current price” $1,954.00 (+3.85%)
Ranges 1H 2H 8H 1D 1W 1M 1Y · selected 1D
Candlestick · y $1,000–$5,000 · x 08:00 10:00 12:00 15:00 18:00 21:00 24:00
“History” + See all: Solana, Bitcoin, Ethereum · actions Sell / Buy

Recipient Bessie Cooper · **** **** **** 8820 · amount $500.00
Keypad 1–9, “.”, 0, backspace · button “Send”

Discussion forum

Sign up & OTP

Search placeholder “Search...” · Filter
Topics: Personal Finance (selected) / Investments / Cryptocurrencies

Devon Lane (verified) · Personal finance · Jan 18, 2023 · 11:00 AM · liked
“FindBuddy is a comprehensive personal finance app that allows you to track and manage your spending, create budgets, and set financial goals. It also provides a visual representation of your financial health.”
12 Comments · 160 Likes · 0 Dislikes

Eleanor Pena (verified) · Personal finance · Jan 18, 2023 · 11:00 AM
“Personal Capital is not only a budgeting tool but also an investment tracker. It provides a holistic view of your financial situation by combining budgeting and investment tracking features.”
12 Comments · 160 Likes · 0 Dislikes

Sign up: “Sign up with phone number” · helper “A code will be sent to your number” · Continue
Legal: “By signing up, you agree to the Terms of Service and Privacy Policy, including Cookie Use.” (Terms of Service, Privacy Policy as links)
OTP: “Enter code” · 4 digits · “Resend code” · Continue

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color + Plus Jakarta Sans
• Media: logos, card artwork, flags, icons, neutral avatar
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, semantic and chart colors
• Type scale, spacing, radii, elevation
• All states: selected, pressed, disabled, error, liked, destructive
• Headers, main navigation and all business components
• Chart styling (bars, breakdown, candlesticks)

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (selected tabs and switches, liked post, empty code inputs, signed amounts)

Deliverable: the link to your own Figma file containing the 11 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Balance

Fixed: the brand primary color and the typeface below — they carry the Balance identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (success, error, warning, disabled), supporting and chart colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#BFB7FD

The Balance brand color. Where and how much to use it is your decision.

Typeface

Plus Jakarta Sans

Aa Bb Cc 0123456789  $190,008.03  +8%

Use Plus Jakarta Sans for all UI text (Regular / Medium / SemiBold available).

Canvas: 375 × 812 (iPhone). Light mode only.
