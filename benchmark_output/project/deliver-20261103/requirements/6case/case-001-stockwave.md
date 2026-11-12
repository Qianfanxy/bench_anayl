# StockWave（6case / case-001）

- 原始模板（只读）：https://www.figma.com/design/6dYmBM4krF7cY7597tycH1/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/6dYmBM4krF7cY7597tycH1/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

STOCKWAVE · LEVEL L2 · DESIGN TASK · v2

StockWave — stock trading app

Design the complete StockWave mobile app: Agatha Bella signs up, verifies her phone, lands on a home screen with her portfolio, indices, wishlist and stocks, reviews her portfolio, opens Netflix (NFLX), buys 3 shares and manages her profile.
Canvas 375 × 812 (iPhone), light mode only. Frozen demo data, not live quotes. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 12 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, gain / loss, error, disabled, chart colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the main navigation and every business component as reusable components in your file.
5. Use the StockWave logo, company logos, illustrations and icons from 04 · Media. People have no photos: use Avatar_Neutral.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Splash

02_Onboarding

Goal: Brand recognition while the app loads.

Goal: Introduce StockWave and start sign-up or sign-in.

MUST INCLUDE

MUST INCLUDE

• Brand: StockWave_Symbol · StockWave_Wordmark

• Actions: Skip · Sign in · Sign up
• Copy: “Stock trading suite” · “Streamline your investment decisions with expert guidance.”
• Media: the app shown on a phone (Blank_Phone_Frame)
• Pages: 2 onboarding pages · current: 1

LINKS

→ auto → 02_Onboarding

LINKS

→ Sign up → 03_Sign_Up_Empty
→ Skip → 03_Sign_Up_Empty

03_Sign_Up (Empty / Filled)

04_Verify_Phone

Goal: Create an account with minimum effort.

Goal: Enter a phone number to receive a code.

MUST INCLUDE

MUST INCLUDE

• Actions: Continue · Continue with Google · Continue with Apple · “Already have an account?” Sign In
• Copy: “Join StockWave” · “Embark on your investment journey with a single dollar.” · “Or continue with”
• Form: Email · Password · Username

• Actions: back · Send code
• Copy: “Enter your phone number” · “You’ll receive a 4 digit code for the phone number verification”
• Number pad: 1–9, *, 0, delete
• Phone: +1 202 555 0147 entered

STATES (ONE FRAME EACH)

LINKS

• 03_Sign_Up_Empty — nothing entered
• 03_Sign_Up_Filled — Agatha Bella · agbella@email.com · password entered (masked)

→ back → 03_Sign_Up_Filled
→ Send code → 05_Verify_Code

LINKS

→ Continue (Filled) → 04_Verify_Phone

05_Verify_Code

06_Welcome

Goal: Confirm the phone with a 4-digit code.

Goal: Greet the new investor.

MUST INCLUDE

MUST INCLUDE

• Actions: back · Resend code · Verify account
• Code: 4 digits · first digit entered: 2
• Copy: “Enter verification code” · “We have sent a verification code to your mobile number”
• Number pad: 1–9, *, 0, delete

• Actions: “I’m ready to start!”
• Copy: “Hello Agatha Bella!” · “Welcome to StockWave” · “It’s great to have you here”
• Media: Welcome_Hand

LINKS

→ I’m ready to start! → 07_Home

LINKS

→ back → 04_Verify_Phone
→ Verify account → 06_Welcome

07_Home

08_Portfolio

Goal: See portfolio value, markets and watched stocks at a glance.

Goal: Understand portfolio value and today’s gain and loss.

MUST INCLUDE

MUST INCLUDE

• Account: notifications entry
• Brand: StockWave_Wordmark
• Indices: S&P 500 (S&P · Standard & Poor’s) +49.50% · Dow Jones (DOW) +1.43%
• Main navigation: current tab Home
• Portfolio: “Portfolio value” $13,240.11 · show / hide value · 7-day trend line
• Stocks: “Stocks” · 5 — NFLX · AAPL · FB · BAC · F — each with logo, ticker, company, price, daily change and trend line
• Wishlist: “Wishlist” · add · 3 — AMZN · ADBE · FB — each with logo, ticker, company, daily change and trend line

• Actions: back
• Chart: portfolio value per day Mon–Sun (values in Fixed data) · highlighted: Sun $13,240.11
• Copy: “Portfolio”
• Main navigation: current tab Portfolio
• Portfolio: “Portfolio value” $13,240.11 · +1.53% today
• Stocks: “Stocks” · NFLX · AAPL — each with logo, ticker, company, price, daily change and trend line
• Today: Gain $234.11 · Loss $34.11

LINKS

LINKS

→ Portfolio value → 08_Portfolio
→ NFLX → 09_Stock_Detail
→ tabs → 07 / 08 / 10 / 11

→ back → 07_Home
→ NFLX → 09_Stock_Detail
→ tabs

09_Stock_Detail

10_Confirm_Order

Goal: Check one stock and start buying.

Goal: Review a buy order and choose how to pay.

MUST INCLUDE

MUST INCLUDE

• Actions: back · price alert entry · Buy stocks
• Chart: NFLX price over the current range · highlighted point Sep 27 · $88.04
• Copy: “Stock Detail”
• Financials: “Financials” · Revenue / Earnings / Performance · years 2018–2021
• Price: $88.91 · +$1.13 (+1.29%) today
• Range: 1D / 1W / 1M / 1Y / 5Y / ALL · current: 1M
• Stock: Logo_Netflix · NFLX · Netflix, Inc
• View: Summary / Details · current: Details

• Actions: back · Confirm order
• Copy: “Confirm Order”
• Order: NFLX · Netflix, Inc · $88.91 · Funding source “Stockup” · Approx share price $88.91 · Approx shares 3 · Fee $2.10 · Total $268.83
• Payment method: “Payment method” · Debit Card “Deposit & Invest right from your debit card” (Icon_Card) · Apple Pay “Connect your Apple Pay account” (Icon_Apple_Pay) · only one can be chosen · none chosen yet

LINKS

LINKS

→ back → 09_Stock_Detail
→ Confirm order → 07_Home

→ back → 07_Home
→ Buy stocks → 10_Confirm_Order

11_Profile

Goal: Identify the account and reach settings.

MUST INCLUDE

• Account: Avatar_Neutral · Agatha Bella · agbella@email.com
• Copy: “Profile”
• Entries: Account · Billing / Payments · FAQ · Language (English) · Security · Settings
• Invite: “Invite friends” · “Invite your friends and get $15”
• Main navigation: current tab Profile

LINKS

→ tabs

Navigation structure

• Onboarding: 01_Splash → 02_Onboarding → 03_Sign_Up_Empty → 03_Sign_Up_Filled → 04_Verify_Phone → 05_Verify_Code → 06_Welcome → 07_Home.
• Main navigation on 07, 08, 11 — five tabs in this order: Home (Icon_Home) → 07 · Portfolio (Icon_Portfolio) → 08 · Trade (Icon_Trade) → 10 · Market (Icon_Market, entry only) · Profile (Icon_Profile) → 11. The current tab must match the frame. How it looks is yours.
• Pushed screens with back: 04, 05, 08, 09, 10. 09 and 10 have no main navigation.
• Entry only (no screen required): Sign in, social sign-up, Resend code, notifications, show / hide value, Wishlist add, price alert, Summary / Financials tabs, ranges, Stockup, Market tab, profile entries, Invite friends.
• There is no sign-in, biometrics, PIN, password-reset or order-result screen — do not add frames beyond the 12.

Fixed data & copy

Use these values verbatim. “+” = up / gain, “−” = down / loss.

User

Stocks (ticker · company · price · daily change · logo)

Agatha Bella · agbella@email.com · +1 202 555 0147 · avatar = Avatar_Neutral
Language English · currency USD · amounts with two decimals

NFLX · Netflix, Inc · $88.91 · +1.29% · Logo_Netflix
AAPL · Apple, Inc · $142.65 · +0.81% · Logo_Apple
FB · Facebook, Inc · $343.01 · +1.07% · Logo_Facebook
BAC · Bank of America · $43.08 · +0.30% · Logo_Bank_of_America
F · Ford Motor · $14.06 · −0.32% · no logo supplied

Wishlist & indices

Portfolio

Wishlist: AMZN · Amazon, Inc · −0.05% · Logo_Amazon / ADBE · Adobe, Inc · +0.32% · Logo_Adobe / FB · Facebook, Inc · +1.07%
Indices: S&P 500 (S&P, Standard & Poor’s) +49.50% · Dow Jones (DOW) +1.43%

Portfolio value $13,240.11 · +1.53% today
Today: Gain $234.11 · Loss $34.11
Per day: Mon $12,240.11 · Tue $12,880.00 · Wed $12,460.00 · Thu $12,930.00 · Fri $13,160.00 · Sat $13,040.11 · Sun $13,240.11
Holdings shown: NFLX, AAPL

Stock detail (NFLX)

Order

$88.91 · +$1.13 (+1.29%) today · previous close $87.78
Range 1D 1W 1M 1Y 5Y ALL · current 1M · highlighted Sep 27 · $88.04
View Summary / Details · current Details
Financials: Revenue / Earnings / Performance · 2018 2019 2020 2021

Buy NFLX · Netflix, Inc · $88.91
Funding source “Stockup”
Approx share price $88.91 · Approx shares 3 · Fee $2.10
Total $268.83 (= 3 × $88.91 + $2.10)
Payment method: Debit Card · Apple Pay — none chosen yet

Sign up & verification

Onboarding, welcome & profile

“Join StockWave” · “Embark on your investment journey with a single dollar.”
Username · Email · Password · Continue · “Or continue with” · Continue with Google · Continue with Apple · “Already have an account? Sign In”
Phone: “Enter your phone number” · “You’ll receive a 4 digit code for the phone number verification” · Send code
Code: “Enter verification code” · “We have sent a verification code to your mobile number” · Resend code · Verify account

Onboarding: “Stock trading suite” · “Streamline your investment decisions with expert guidance.” · Skip · Sign in · Sign up
Welcome: “Hello Agatha Bella!” · “Welcome to StockWave” · “It’s great to have you here” · “I’m ready to start!”
Profile: Account · Security · Billing / Payments · Language: English · Settings · FAQ · Invite friends “Invite your friends and get $15”

Source corrections

The source mixes the brand names Stockline / StockWave and the emails agbella@email.com / agbella@gmail.com, shows Bank of America prices on the Netflix detail, an order total that ignores share count and fee ($141.65, “$3.00” shares), a chart point ($29,140) and a daily return (+1.74%) that contradict the portfolio value and today’s $200.00 net gain, decimal commas and typos (“suit”, “Sent code”). Follow this brief, not the source.

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color + Inter
• Media: StockWave logo, company logos, illustrations, icons, neutral avatar
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, gain / loss, semantic and chart colors
• Type scale, spacing, radii, elevation
• All states: selected, pressed, disabled, filled, hidden value, chosen / not chosen
• Headers, main navigation, number pad and all business components
• Chart styling (trend lines, portfolio chart, price chart, financial bars)

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tabs and ranges, empty vs filled form, partial code, gain vs loss, unchosen payment method)

Deliverable: the link to your own Figma file containing the 12 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

STOCKWAVE · 01 FOUNDATIONS

Foundations · StockWave

Fixed: the brand primary color and the typeface below — they carry the StockWave identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, gain / loss and other semantic colors (error, warning, disabled), chart colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#3E52C1

The StockWave brand color. Where and how much to use it is your decision.

Typeface

Inter

Aa Bb Cc 0123456789  $13,240.11  +1.29%

Use Inter for all UI text (Regular / Medium / Semi Bold / Bold available; it also replaces the unavailable SF Pro). The StockWave wordmark is supplied as an asset in 04 · Media — do not retype it.

Canvas: 375 × 812 (iPhone). Light mode only. Long screens (Home, Portfolio, Stock Detail) may scroll vertically.
