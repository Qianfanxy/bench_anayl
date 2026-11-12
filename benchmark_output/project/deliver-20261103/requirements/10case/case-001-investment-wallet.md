# Investment Wallet（10case / case-001）

- 原始模板（只读）：https://www.figma.com/design/efeLy7ogjybd9HZN6rfLbp/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/efeLy7ogjybd9HZN6rfLbp/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Investment Wallet — crypto wallet for beginners

Design the Investment Wallet mobile app for a beginner investor: see the wallet balance, assets and savings pockets, discover investing strategies and coins, read about the “Aggressive Growth” strategy, invest 3,021 DAI in it and confirm the result.
Canvas 375 × 812, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 5 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, gain / loss, risk levels, success / disabled, accents and chart colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the page indicator, the sheets and every business component as reusable components in your file.
5. Use the coin logos, neutral avatar and icons from 04 · Media. Emoji in the copy are plain text characters.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Wallet

02_Discovery

Goal: See total balance, assets and savings pockets.

Goal: Discover strategies and coins worth investing in.

MUST INCLUDE

MUST INCLUDE

• Account: Avatar_Neutral · “My Wallet” · address 0xc8...320f · scan entry
• Actions: Send · Receive
• Assets: “Assets” · Ethereum / Dai / Avalanche / PancakeSwap, each with logo, name, holding, value and 24h change
• Balance: $54,292.79 · +5.21%
• Main navigation: page 2 of 3 (My Wallet)
• Pockets: “Pockets” · My New House 🏡 · Tesla Model S Plaid 🚙, each with value, name and change · Add Pocket

• Account: Avatar_Neutral · search entry
• Coin list: “Coin Lists” · 10 coins, each with logo, name, ticker, price and 24h change
• Coin list tabs: 🔥 Trending / 📺 Watchlist / ❤️ Favorites / 💵 Stablecoins / 🔗 BNB Chain Ecosystem · current: Trending
• For you: “December 05” · “For You Today” · Stable Income · Binance Index Strategy, each with risk, participants, yearly return and View
• Main navigation: page 3 of 3 (Discovery)
• Strategies: “Investing Strategies” · The Big Long · Aggressive Growth · Best Projects · Strategy 2022, each with yearly return, 3 asset logos and “+N” more

LINKS

LINKS

→ swipe / page indicator → 02_Discovery

→ Aggressive Growth → 03_Strategy
→ swipe / page indicator → 01_Wallet

03_Strategy

04_Invest_Amount

Goal: Understand the Aggressive Growth strategy before investing.

Goal: Enter how much DAI to invest.

MUST INCLUDE

MUST INCLUDE

• About: “About Strategy” · description (see DATA)
• Actions: Invest · dismiss
• Facts: 159% per Year · Interest Income / High Risk · Level of risk / $1,000 · Minimum investment amount / 2 Years · Recommended investment period / 1,982 · Participants
• Presentation: sheet over 02_Discovery
• Projection: $1,590.00 · “This is how much you can earn in a year if you invest $1,000 to “Aggressive Growth”” · growth chart Dec ’21 – Dec · risk “🔥 High Risk”
• Share of assets: “Share of Assets” · 5 assets, each with logo, name, ticker and share (see DATA)

• Actions: back · Max · swap input currency · Hold to Invest (Icon_Face_ID)
• Amount: DAI (Coin_DAI) · 3,021 being entered
• Copy: “Invest to Strategy” · “⛽️ No gas, free investments”
• Keypad: 1 · 2 ABC · 3 DEF · 4 GHI · 5 JKL · 6 MNO · 7 PQRS · 8 TUV · 9 WXYZ · “,” · 0 · backspace
• Presentation: sheet over 02_Discovery

LINKS

→ back → 03_Strategy
→ Hold to Invest → 05_Invest_Success

LINKS

→ Invest → 04_Invest_Amount
→ dismiss → 02_Discovery

05_Invest_Success

Goal: Confirm the investment.

MUST INCLUDE

• Actions: close · View Pocket
• Celebration: 🎉 and confetti
• Copy: “You’ve invested!” · “3,021.00 DAI in the “Aggressive Growth” strategy. You will find the purchased coins in a new pocket.”
• Presentation: sheet over 02_Discovery

LINKS

→ close → 02_Discovery
→ View Pocket → 01_Wallet

Navigation structure

• Top level is a horizontal pager with 3 pages and a page indicator: page 1 (not part of this task), page 2 My Wallet (01_Wallet), page 3 Discovery (02_Discovery). The indicator must show the current page. How it looks is yours.
• 03, 04 and 05 are sheets stacked over 02_Discovery (one frame each).
• Invest flow: 02_Discovery → 03_Strategy → 04_Invest_Amount → 05_Invest_Success.
• Entry only (no frame): Send, Receive, scan, search, assets, pockets, Add Pocket, View on For You cards, other strategies, coins, coin-list tabs other than Trending, Max, swap currency.

Fixed data & copy

Use these values verbatim. Today is December 05. Prices in USD.

Wallet

Assets (holding · value · 24h)

Pockets

“My Wallet” · 0xc8...320f · $54,292.79 · +5.21%
= assets $10,261.18 + pockets $44,031.61

Ethereum · 2.569032 ETH · $3,226.31 · +3.48% (Coin_ETH)
Dai · 3,045.86 DAI · $3,021.15 · −0.02% (Coin_DAI)
Avalanche · 180.02 AVAX · $2,440.09 · +1.54% (Coin_AVAX)
PancakeSwap · 397.33 CAKE · $1,573.63 · −0.02% (Coin_CAKE)

My New House 🏡 · $15,642.40 · +7.86%
Tesla Model S Plaid 🚙 · $28,389.21 · −2.13%
Add Pocket

For You Today

Investing Strategies (per year · logos · more)

Coin Lists · 🔥 Trending (price · 24h)

Stable Income · Low risk · 10,982 participants · 6.24% per year · View
Binance Index Strategy · Medium risk · 264 participants · 12.56% per year · View

The Big Long · 15.16% · BTC, ETH, USDT · +3
Aggressive Growth · 159% · MATIC, MANA, CAKE · +2
Best Projects · 46.22% · NEAR, DASH, AVAX · +12
Strategy 2022 · 26.08% · ETC, DAI, BNB · +2

Bitcoin BTC $16,963.58 · −0.12%
Ethereum ETH $1,259.10 · +1.15%
Tether USDT $1.01 · +0.01%
Binance Coin BNB $288.01 · +0.76%
USD Coin USDC $0.9999 · −0.02%
Binance USD BUSD $1.00 · −0.01%
XRP XRP $0.3891 · +2.54%
Dogecoin DOGE $0.1012 · −0.17%
Cardano ADA $0.3196 · +0.09%
Polygon MATIC $0.9082 · +2.18%

Aggressive Growth

Share of Assets

Invest & success

Projection: $1,590.00 earned in a year on $1,000
Chart labels: Dec ’21 · Mar · Jun · Sep · Dec
“The aggressive growth strategy allows you to earn 159% per annum, but with a high risk. Our analysts have balanced the strategy with different assets so that the strategy pays off within the recommended time frame.”
Facts (with emoji): 🌱 159% per Year · 🔥 High Risk · 💵 $1,000 minimum · 🗓️ 2 Years · 🧑 1,982 participants

Polygon (MATIC) 50.00%
Decentraland (MANA) 25.00%
PancakeSwap (CAKE) 12.50%
Dogecoin (DOGE) 6.25%
Maker (MKR) 6.25%

Amount 3,021 DAI (balance 3,045.86 DAI; minimum $1,000 met)
Button “Hold to Invest”
Success: “You’ve invested!” · 3,021.00 DAI · button “View Pocket”

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color #2B2D33 + Nunito
• Media: coin logos, neutral avatar, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, gain / loss, risk levels, accents, chart colors
• Type scale, spacing, radii, elevation
• All states: current page, selected tab, pressed, disabled, amount being entered, rising / falling
• Headers, page indicator, sheets and all business components
• Chart and share-of-assets styling, confetti

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current page, current coin-list tab, gains vs losses, risk levels, amount being entered)

Deliverable: the link to your own Figma file containing the 5 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Investment Wallet

Fixed: the brand primary color and the typeface below — they carry the wallet’s identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (gain / loss, risk levels, success, disabled), accent and chart colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary · graphite

#2B2D33

The wallet’s brand color. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  $54,292.79  +5.21%

Use Nunito for all UI text (Regular / Medium / SemiBold / Bold / ExtraBold available; it replaces the source’s SF Pro Rounded, which is not available). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 375 × 812 (iPhone). Light mode only. 01_Wallet, 02_Discovery and 03_Strategy may scroll vertically.
