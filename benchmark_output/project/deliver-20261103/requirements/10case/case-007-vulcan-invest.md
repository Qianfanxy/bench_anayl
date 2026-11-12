# Vulcan Invest（10case / case-007）

- 原始模板（只读）：https://www.figma.com/design/xwz3EN8BuC5TToLY27zcHm/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/xwz3EN8BuC5TToLY27zcHm/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Vulcan Invest — banking and stock investing

Design the investing area of Vulcan Bank’s app: from the home screen, open Invest for the first time, set a PIN, review the portfolio, study a stock and buy one share with a confirmation. Canvas 414 × 896, iPhone. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 7 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the illustration, company logos and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Home

02_About_Investment

Goal: See my balance, act on my money and review today’s history.

Goal: Learn what investing offers and start.

MUST INCLUDE

MUST INCLUDE

• Actions: “My card” (Icon_Card) · “Transfer” (Icon_Transfer) · “Mobile” (Icon_Mobile) · search history (Icon_Search)
• Balance: $3,821 (Icon_Safe) · Vulcan Bank payment card (no number shown) · 2 pages, current: 1
• History: “History” · “TODAY” · 3 rows (see DATA)
• Main navigation: tab bar Main / Payments / Cashback / Invest / More · current: Main

• Actions: back (Icon_Back) · start (Icon_Arrow_Right)
• Copy: “Investment” · two paragraphs (see DATA)
• Media: Illustration_Investment

LINKS

→ start → 03_Create_PIN
→ back → 01_Home

LINKS

→ Invest tab → 02_About_Investment

03_Create_PIN

04_Portfolio

Goal: Create a 4-digit PIN for the brokerage account.

Goal: See how my investments perform.

MUST INCLUDE

MUST INCLUDE

• Actions: back (Icon_Back) · “Ready”
• Header: “Create PIN code”
• Keypad: 1–9 and 0 with letters (2 ABC … 9 WXYZ) · delete (Icon_Backspace)
• PIN: 4 positions · 3 entered (9 · 7 · 7) · 4th empty

• Cases: “Cases” · AAPL · TSLA · NFLX · MSFT, each with logo, price and change (see DATA)
• Chart: monthly earnings, Mar – Sep, axis 0 / 50k / 100k
• Header: back (Icon_Back) · “Investment Portfolio” · menu (Icon_Menu) · chart (Icon_Chart, with an unread dot) · insights (Icon_Insights)
• Main navigation: tab bar · current: Invest
• Summary: “Total earning” $87,875 · +10% · “Profit” $28,160 · +32%

LINKS

→ Ready → 04_Portfolio
→ back → 02_About_Investment

LINKS

→ AAPL case → 05_Trading
→ back / Main tab → 01_Home

05_Trading

06_Stock_Transaction

Goal: Study Apple’s price before deciding.

Goal: Set up the purchase of one Apple share.

MUST INCLUDE

MUST INCLUDE

• Actions: “Buy” (Icon_Arrow_Up) · “Sell” (Icon_Arrow_Down)
• Chart: AAPL intraday candlesticks, 10 am – 3 pm, axis $100.00 – $150.00
• Header: back (Icon_Back) · “Trading” · menu (Icon_Menu) · chart (Icon_Chart) · insights (Icon_Insights)
• Main navigation: tab bar · current: Invest
• Period: Day · Week · Month · Year · All · current: Day
• Position: “Market Value” $97.83 · “Buying Power” $18,943.43
• Stock: AAPL · Apple Inc. · $143.43 · +31.62 (28.28%) (Logo_Apple)

• Account: “ACCOUNT” · USD $18,943.43 (selected) · EUR €16,473.11
• Actions: “Buy”
• Form: “Quantity” 1 (“1 lot = 1 stock”) · “Price” $143.43 (“1 unit = $143.43” · “commission $14.34”)
• Header: back (Icon_Back) · “Stock transaction” · menu (Icon_Menu)
• Main navigation: tab bar · current: Invest
• Stock: Apple Inc. · AAPL · $143.43 · +31.62 (28.28%) (Logo_Apple)

LINKS

LINKS

→ Buy → 07_Confirm_Purchase
→ back → 05_Trading

→ Buy → 06_Stock_Transaction
→ back → 04_Portfolio

07_Confirm_Purchase

Goal: Confirm or cancel the purchase.

MUST INCLUDE

• Actions: “Cancel” · “Buy”
• Copy: “Are you sure?”
• Presentation: dialog over 06_Stock_Transaction

LINKS

→ Cancel → 06_Stock_Transaction
→ Buy (entry only — the purchase result is not part of this task)

Navigation structure

• Bottom tab bar on 01 and 04–06 with 5 tabs in this order: Main (Icon_Main), Payments (Icon_Payments), Cashback (Icon_Cashback), Invest (Icon_Invest), More (Icon_More). Current: Main on 01; Invest on 04–06. How the current tab looks is yours. 02, 03 and 07 have no tab bar.
• First-time Invest flow: 01_Home → Invest tab → 02_About_Investment → start → 03_Create_PIN → Ready → 04_Portfolio.
• Buying: 04 → AAPL → 05_Trading → Buy → 06_Stock_Transaction → Buy → 07_Confirm_Purchase (dialog over 06).
• Entry only (no frame): My card, Transfer, Mobile, history search and rows, card pager, Payments / Cashback / More tabs, other cases, Sell, periods, menu, chart, insights, EUR account, Buy on 07.

Fixed data & copy

Use these values verbatim.

Bank and balance

History · TODAY (top to bottom)

About Investment (02)

Vulcan Bank · balance $3,821 · payment card (no number shown)

Airbnb · Payments · −$560 (Icon_Location)
to Anna Nelsen · Transfer · −$380 (Icon_Transfer)
from Anna Nelsen · Transfer · +$470 (Icon_Transfer_In)

Investment
“I will help you create an investment portfolio in less than five minutes!”
“Have you wanted to invest in the shares of global giants for a long time? Now it is possible by opening a brokerage account. Let’s start!”

PIN

Portfolio summary

Cases

4 digits · entered so far: 9 7 7

Total earning $87,875 · +10%
Profit $28,160 · +32%
Chart: monthly, Mar – Sep, axis 0 / 50k / 100k

AAPL · $143.43 · +31.62 (28.28%) · Logo_Apple
TSLA · $739.38 · +9.21 (1.26%) · Logo_Tesla
NFLX · $573.14 · −2.29 (0.40%) · Logo_Netflix
MSFT · $294.80 · +0.50 (0.17%) · Logo_Microsoft

Apple trading

Order (06)

AAPL · Apple Inc. · $143.43 · +31.62 (28.28%)
Intraday axis $100.00 – $150.00 (step $10), 10 am – 3 pm
Market Value $97.83 · Buying Power $18,943.43

Account: USD $18,943.43 (selected) · EUR €16,473.11
Quantity 1 · 1 lot = 1 stock
Price $143.43 · 1 unit = $143.43 · commission $14.34

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #FA5555 and Inter
• Media: illustration, company logos, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• Light or dark per screen, and all other colors: neutrals, text, surfaces, gains / losses, chart, buy / sell, error / disabled
• Type scale, spacing, radii, elevation
• All states: current tab, current period, selected account, PIN progress, focused field, pressed, disabled
• Headers, tab bar, balance card, quick actions, history rows, PIN keypad, stock cards, charts, account selector, dialog
• Chart rendering (the candle values between the axis limits are illustrative)

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, current period, selected account, PIN progress, dialog presentation)

Deliverable: the link to your own Figma file containing the 7 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Vulcan Invest

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (light or dark, including any gradient), gains / losses, chart colors, the buy / sell actions, error and disabled, type scale, spacing, radii and elevation.

Brand color

Brand primary · persian red

#FA5555

Vulcan Bank’s main brand color. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  $143.43  +28.28%

Use Inter for all UI text (the source mixes Inter, Roboto, Open Sans and SF Pro; Inter replaces all of them). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 414 × 896 (iPhone 11 Pro Max). The source mixes light and dark screens — light or dark per screen is your decision, as long as it is one coherent system. 04_Portfolio may scroll vertically.
