# Expenio（10case / case-005）

- 原始模板（只读）：https://www.figma.com/design/Due9oPeFd4oHqHjMvF2ehH/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/Due9oPeFd4oHqHjMvF2ehH/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Expenio — personal expense manager

Design Expenio, a personal expense manager: get started, check your balance and spending, open your wallet, add a new card, pay a friend and keep the receipt. Canvas 375 × 812, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 6 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the logo, illustrations, card artwork, avatars, merchant and card-network marks and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Get_Started

02_Home

Goal: Understand what Expenio is and start.

Goal: See my balance, spending trend and latest transactions.

MUST INCLUDE

MUST INCLUDE

• Actions: “Get Started”
• App: Logo_Expenio
• Copy: “Going cashless has never been easier with the world’s leading expense manager.”
• Media: Illustration_Get_Started

• Actions: open balance (Icon_Chevron_Right) · “See all” · new payment (Icon_Plus)
• Balance: “My Balance” · $25,520.00
• Expenses: “Expenses” chart, MAR – AUG, JUN highlighted at $80.40
• Greeting: “Hello, Maria” · “Home” · Avatar_Maria_Lopez
• Transactions: “Wallet” · 3 rows (see DATA)

LINKS

LINKS

→ Get Started → 02_Home

→ open balance / See all → 03_Wallet
→ new payment → 05_Payment

03_Wallet

04_Add_Card

Goal: Review my card, an offer and my transactions.

Goal: Add a new payment card.

MUST INCLUDE

MUST INCLUDE

• Actions: “Back” (Icon_Back) · add card (Icon_Add_Card)
• Card: Maria’s Visa card (see DATA) · card 1 of 3 in the wallet
• Header: “Wallet”
• Promo: “POPULAR” · “Get up to 15% cashback on clothing and apparel” (Promo_Cashback)
• Transactions: “Transactions” · 3 rows (see DATA)

• Actions: close (Icon_Close) · “Add new card”
• Card preview: shows the number typed so far (see DATA, Logo_Mastercard); name and expiry not yet entered
• Form: “Card holder’s name” (empty, placeholder “Name on card”) · “Card number” 5412 7534 0089 2216, focused, Mastercard detected (Logo_Mastercard) · “Expiry Date” (empty, placeholder “MM / YY”) · “CVV” (empty, placeholder “123”, help Icon_Help)
• Header: “Add new card”
• Presentation: sheet over 03_Wallet

LINKS

→ Back → 02_Home
→ add card → 04_Add_Card

LINKS

→ Add new card / close → 03_Wallet

05_Payment

06_Receipt

Goal: Pay Robert $50.00 with my card.

Goal: Confirm what I paid.

MUST INCLUDE

MUST INCLUDE

• Actions: “Cancel” · “Pay now”
• Amount: $50.00
• Card: Maria’s Visa card (as on 03_Wallet) · card 1 of 3
• Header: “Payment”
• Note: “Add a note” (empty)
• Payee: “PAYING” · “Robert Dawson” (Avatar_Robert_Dawson)

• Actions: share (Icon_Share) · “Home”
• Header: “Receipt”
• Receipt: “CASH RECEIPT” · 20.08.2020 · Amount · Service Fee · Internet Charge · Total · barcode (Barcode_Receipt) (see DATA)

LINKS

→ Home → 02_Home

LINKS

→ Pay now → 06_Receipt
→ Cancel → 02_Home

Navigation structure

• Flow: 01_Get_Started → Get Started → 02_Home. From 02: open balance or See all → 03_Wallet; new payment → 05_Payment → Pay now → 06_Receipt → Home → 02_Home.
• 04_Add_Card is a sheet over 03_Wallet. There is no tab bar in this task.
• Entry only (no frame): transaction rows, chart points, the promo, other cards in the wallet, share, typing a note.

Fixed data & copy

Use these values verbatim.

User

Balance

Expenses chart

Maria Lopez · Avatar_Maria_Lopez

My Balance $25,520.00 (the same balance printed on Maria’s card)

Months MAR · APR · MAY · JUN · JUL · AUG
Highlighted point: JUN · $80.40 (the curve shape of other months is illustrative)

Transactions (newest first)

Maria’s card

New card (04)

Nike Air Max 2090 · 15 Aug 2020 · −$243.00 (Merchant_Nike)
iPad Pro 2020 · 10 Aug 2020 · −$799.00 (Merchant_Apple)
Uber · 5 Mar 2020 · +$50.00 (Merchant_Uber)

Visa (Logo_Visa) · BALANCE $25,520.00
4225 9765 0008 6141 · MARIA LOPEZ · EXPIRY 09/24
Artwork: Card_Texture_Coral

Mastercard (Logo_Mastercard) · 5412 7534 0089 2216
Holder name, expiry and CVV not yet entered

Promo

Payment

Receipt

POPULAR · Get up to 15% cashback on clothing and apparel · Promo_Cashback

Paying Robert Dawson (Avatar_Robert_Dawson) · $50.00 · from Maria’s Visa card

CASH RECEIPT · 20.08.2020
Amount $40.00 · Service Fee $2.82 · Internet Charge $7.18
Total $50.00

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #007AFF and Inter
• Media: logo, illustrations, card artwork, avatars, merchant and card-network marks, barcode, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces, chart, positive / negative amounts, error / disabled
• Type scale, spacing, radii, elevation
• All states: focused field, current card in the wallet, highlighted chart point, pressed, disabled
• Headers, balance card, payment card, chart, transaction rows, promo card, sheet, receipt
• How images are cropped and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (focused card-number field, current card, highlighted chart point, sheet presentation)

Deliverable: the link to your own Figma file containing the 6 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Expenio

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (including any tint or gradient), the payment-card artwork, chart colors, positive / negative amounts, error and disabled, type scale, spacing, radii and elevation.

Brand color

Brand primary · blue

#007AFF

Expenio’s main brand color. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  $25,520.00

Use Inter for all UI text (it replaces the source’s SF Pro and Helvetica Neue, which are not available). Numbers printed on the payment card may use a monospaced face of your choice. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 375 × 812 (iPhone X / 11 Pro). Light mode only. 02_Home and 03_Wallet may scroll vertically.
