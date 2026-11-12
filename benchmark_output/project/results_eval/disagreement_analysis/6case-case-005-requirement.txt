# FinX（6case / case-005）

- 原始模板（只读）：https://www.figma.com/design/B2Sbh1dTGQFUT6PZkSTqHy/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/B2Sbh1dTGQFUT6PZkSTqHy/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

FinX — mobile banking and trading app

Design the complete FinX mobile app for Alex Morgan: a banking area (sign up, verify identity, see cards, exchange rates, transactions, budget and profile) and an XTrade trading area (portfolio, crypto market, stock and crypto exchange).
Canvas 390 × 844, iPhone. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 10 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typefaces in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, light / dark mode, gain / loss, success / error / warning / disabled, chart colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, both bottom navigations and every business component as reusable components in your file.
5. Use logos, coin icons, banners, the avatar, the ID card placeholder and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Welcome

02_Photo_ID

Goal: Start using FinX or log in.

Goal: Verify identity by scanning an ID card.

MUST INCLUDE

MUST INCLUDE

• Actions: GET STARTED · Log In (“Already have an account?”)
• Copy: “Manage your finances simply”
• Media: Illustration_Welcome

• Actions: back · TRY AGAIN · CONTINUE
• Camera: the ID card being scanned (ID_Card_Placeholder)
• Copy: “Photo ID Card” · “Please point the camera at the ID card”

LINKS

LINKS

→ GET STARTED → 02_Photo_ID

→ back → 01_Welcome
→ CONTINUE → 03_Bank_Home

03_Bank_Home

04_Bank_Transactions

Goal: See payment cards, exchange rates and recent transactions.

Goal: Understand this week’s spending against the monthly budget.

MUST INCLUDE

MUST INCLUDE

• Actions: menu · contacts · notifications (unread)
• Cards: “Payment card” · 2 cards
• Exchange rates: “Exchange rates” · AUD / EUR / GBP, each with rate and change · entry to all rates
• Main navigation: current tab Home
• Transactions: “Transactions” · 3 transactions, newest first · entry to all transactions

• Actions: history · currency exchange · notifications (unread)
• Balance: “Total balance” $41,900.10
• Budget: “Monthly budget” · $1,080.24 spent of $2,500 · Food & restaurants $890.12 · Tickets & Journey $190.12
• Copy: “Transactions”
• Main navigation: current tab Trans.
• Weekly spending: “Transactions” $1,041.90 · period Week (changeable) · spend per day Mon 01 – Sat 06 · selected day: Thu 04, $134.90

LINKS

→ Transactions entry → 04_Bank_Transactions
→ tabs → 04 / 03 / 05

LINKS

→ tabs → 04 / 03 / 05

05_Profile

06_XTrade_Welcome

Goal: Review the account and reach settings.

Goal: Introduce XTrade, the FinX trading area.

MUST INCLUDE

MUST INCLUDE

• Account: Avatar_User · Alex Morgan · alex.morgan@finx.app · +1 234 567 8901 · edit avatar
• Actions: notifications · history · more menu
• Main navigation: current tab Profile
• Settings: Contact us · Edit profile information · Help & Support · Language: English · Notifications: ON · Privacy policy · Security · Theme: Light mode

• Actions: GET STARTED
• Brand: “FinX”
• Copy: “Zero fee payment on XTrade” · “No 1 design for E-bank, e-wallet, personal financial mobile application.”

LINKS

→ GET STARTED → 07_Trade_Home

LINKS

→ tabs → 04 / 03 / 05

07_Trade_Home

08_Market

Goal: See portfolio value and jump into trading.

Goal: Scan coin prices and pick one to trade.

MUST INCLUDE

MUST INCLUDE

• Account: Avatar_User · search “Search” · scan · notifications (unread)
• Banners: Banner_ETH_2_0 · Banner_Upcoming_Events
• Exchange rates: same as 03 · See all
• Main navigation: current tab Home
• Portfolio: “My Portfolios” · See all · BTC / ETH / XRP / BNB, each with logo, name, holding, value, 24h change and 7-day trend
• Shortcuts: Deposit · Earn · Gift card · More · Orders · Referral · Save coins · Shop

• Actions: filter
• Coins: 9 coins, each with ticker, name, 24h volume, price and 24h change
• Copy: “Market”
• Main navigation: current tab Markets
• Search: “Search coin”
• Tabs: Favorites / Spot / Futures / Zones / Others · current: Favorites

LINKS

LINKS

→ BTC → 10_Exchange_Crypto
→ tabs → 07 / 08 / 09

→ BTC → 10_Exchange_Crypto
→ tabs → 07 / 08 / 09

09_Exchange_Stock

10_Exchange_Crypto

Goal: Swap one stock for another.

Goal: Place a limit order for BTC.

MUST INCLUDE

MUST INCLUDE

• Actions: filter · swap direction · calculator
• Copy: “Exchange”
• From: AAPL (Apple Inc.) · Logo_Apple · amount $156.50 being entered · stock changeable
• Keypad: 1 · 2 ABC · 3 DEF · 4 GHI · 5 JKL · 6 MNO · 7 PQRS · 8 TUV · 9 WXYZ · 0 · backspace
• Main navigation: current tab Exchange
• Side: Buy / Sell · current: Buy
• To: SPOT (Spotify) · Logo_Spotify · ≈ 0.69 shares at $226.90 · stock changeable

• Copy: “Exchange”
• Main navigation: current tab Exchange
• Order book: 5 asks and 5 bids, each with price and amount (BTC)
• Order form: side Buy / Sell · current Buy · type Limit (changeable) · price 29,198.00 USDT (− / +) · amount 0.0500 BTC (− / +) · 25% / 50% / 75% / 100% · Total 1,459.90 USDT · Available 2,500.00 USDT · Buy BTC
• Pair: BTC / USDT · Logo_BTC · Vol 2.8B · last price 29,198.24 · +3.73% · pair changeable
• View: Orderbook / Chart · current: Orderbook

LINKS

LINKS

→ tabs → 07 / 08 / 09

→ tabs → 07 / 08 / 09

Navigation structure

• Banking: 01_Welcome → 02_Photo_ID → 03_Bank_Home. Trading: 06_XTrade_Welcome → 07_Trade_Home. Two entry points, two areas.
• Banking navigation on 03, 04, 05 — five tabs in this order: Trans. (Icon_Tab_Transactions) → 04 · Feeds (Icon_Tab_Feeds, entry only) · Home (Icon_Tab_Home, centre) → 03 · Wallet (Icon_Tab_Wallet, entry only) · Profile (Icon_Tab_Profile) → 05.
• Trading navigation on 07, 08, 09, 10 — five tabs in this order: Home (Icon_Tab_Home) → 07 · Markets (Icon_Tab_Markets) → 08 · Exchange (Icon_Tab_Exchange, centre) → 09 · Futures (Icon_Tab_Futures, entry only) · Wallets (Icon_Tab_Wallet, entry only).
• The current tab must match the frame. How the navigations look is yours.
• Entry only (no frame): Log In, TRY AGAIN, menu, contacts, notifications, history, currency exchange, more menu, settings rows, edit avatar, search, scan, shortcuts, banners, See all, filter, calculator, Chart view, Sell.

Fixed data & copy

Use these values verbatim. Today is Apr 13, 2022. Currency USD unless stated.

User

Payment cards

Exchange rates (vs USD, all rising)

Alex Morgan · alex.morgan@finx.app · +1 234 567 8901 · avatar = Avatar_User

Mastercard (Logo_Mastercard) · 3141 5926 5358 9793 · ALEX MORGAN · Exp 06/24
Mastercard (Logo_Mastercard) · 5412 7534 0192 4467 · ALEX MORGAN · Exp 11/25

AUD $0.80 · +0.03 (+3.9%)
EUR $1.10 · +0.03 (+2.8%)
GBP $1.30 · +0.03 (+2.4%)

Bank transactions (newest first)

Weekly spending

Monthly budget

Car loans (Icon_Car_Loan) · $13.10 · −4.5% · today 9:01 AM
Mortgage real estate (Icon_Mortgage) · $15.10 · −1.5% · Apr 12, 2022 5:01 AM
Personal loans (Icon_Personal_Loan) · $41.10 · −6.5% · Mar 13, 2022 7:02 PM

Total balance $41,900.10 · this week $1,041.90 · period Week
Mon 01 $96.40 · Tue 02 $210.25 · Wed 03 $305.80 · Thu 04 $134.90 (selected) · Fri 05 $58.20 · Sat 06 $236.35

$1,080.24 spent of $2,500
Food & restaurants (Icon_Food) $890.12 · Tickets & Journey (Icon_Ticket) $190.12

Profile settings

Trade shortcuts

My Portfolios (holding · value · 24h)

Edit profile information · Notifications ON · Language English
Security · Theme Light mode
Help & Support · Contact us · Privacy policy

Deposit · Referral · Earn · Save coins · Orders · Shop · Gift card · More (icons Icon_Deposit … Icon_More_Horizontal)

BTC Bitcoin · 0.5000 BTC · $14,599.12 · +3.73%
ETH Ethereum · 2.0000 ETH · $3,700.24 · −1.07%
XRP Ripple · 5,000 XRP · $2,465.00 · +1.76%
BNB BNB · 1.2000 BNB · $289.56 · +0.62%
Logos: Coin_BTC, Coin_ETH, Coin_XRP, Coin_BNB

Market · Favorites (price · 24h · volume)

Stock exchange

Order book BTC / USDT (price · amount BTC)

BTC Bitcoin $29,198.24 · +3.73% · 2.8B
ETH Ethereum $1,850.12 · −1.07% · 1.1B
USDT TetherUS $1.00 · +0.01% · 41.2B
BNB BNB $241.30 · +0.62% · 412.5M
ADA Cardano $0.2874 · −0.62% · 186.0M
XRP Ripple $0.4930 · +1.76% · 990.0M
SOL Solana $20.58 · +2.15% · 305.4M
DOT Polkadot $4.92 · +0.84% · 98.7M
AVAX Avalanche $11.36 · −0.45% · 120.3M

Buy · from AAPL (Apple Inc.) $156.50 → to SPOT (Spotify) at $226.90 per share ≈ 0.69 shares

Asks: 29,203.00 · 0.0446 / 29,201.80 · 0.1185 / 29,200.65 · 0.0797 / 29,199.40 · 0.0032 / 29,198.50 · 0.1852
Bids: 29,198.00 · 0.2104 / 29,196.75 · 0.0446 / 29,195.20 · 0.1185 / 29,194.10 · 0.0797 / 29,193.50 · 0.0560
Form: Limit · 29,198.00 USDT × 0.0500 BTC = 1,459.90 USDT · Available 2,500.00 USDT

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color #1573FE + Poppins and Roboto
• Media: logos, coin icons, banners, avatar, ID card placeholder, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, light / dark mode, gain / loss, semantic and chart colors
• Type scale, spacing, radii, elevation
• All states: selected, pressed, disabled, unread, rising / falling
• Headers, both bottom navigations and all business components
• Chart styling (weekly spending, budget, trends, order book depth)

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tabs and switches, selected day, unread notifications, gains vs losses, amount being entered)

Deliverable: the link to your own Figma file containing the 10 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · FinX

Fixed: the brand primary color and the two typefaces below — they carry the FinX identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, light / dark mode, semantic colors (gain / loss, success, error, warning, disabled), chart and supporting colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#1573FE

The FinX brand color. Where and how much to use it is your decision.

Typefaces

Poppins

Roboto

Aa  $41,900.10

Aa Bb Cc 0123456789  +3.73%

Poppins and Roboto are the FinX typefaces (Regular / Medium / SemiBold / Bold available). Which face, size and weight goes where is yours to define as a consistent type scale.

Canvas: 390 × 844 (iPhone). Light or dark mode — per area or for the whole app — is your decision.
