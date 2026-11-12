# Payment Wallet（10case / case-006）

- 原始模板（只读）：https://www.figma.com/design/JxDq23kL46ZvP1olTycfUS/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/JxDq23kL46ZvP1olTycfUS/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Payment Wallet — pay, manage, grow

Design a mobile payment wallet: onboard, start with a phone number, see your bank balances and recent transactions, and reach the main areas from the side menu. Canvas 390 × 844, iPhone. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 4 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator, system numeric keypad). Design all other states, the headers, the navigation and every business component as reusable components in your file.
5. Use the illustration, avatars, bank and merchant marks and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Onboarding

02_Phone_Number

Goal: Understand the app and choose to start.

Goal: Enter a phone number to get started.

MUST INCLUDE

MUST INCLUDE

• Actions: “Get Started” · “Sign in”
• Copy: “Pay / Manage / Grow…” (one word per line) · “An easy app to manage all your payment and finance-related needs” · “Already have an account?”
• Media: Illustration_Onboarding

• Actions: “Cancel” · “Get Started”
• Form: “Phone Number” · country code +91 · empty (placeholder 9812345678) · focused
• Header: “Get Started” · “Please enter the mobile phone number”
• Keyboard: system numeric keypad open (Numeric Keypad)
• Presentation: sheet over 01_Onboarding

LINKS

LINKS

→ Get Started → 02_Phone_Number

→ Get Started → 03_Home
→ Cancel → 01_Onboarding

03_Home

04_Menu

Goal: Check my balances, move money and see recent transactions.

Goal: Reach the main areas of the app.

MUST INCLUDE

MUST INCLUDE

• Accounts: Axis Bank · HDFC Bank · Deutsche Bank · Union Bank, each with its mark and balance (see DATA)
• Actions: “Send” (Icon_Send) · “Receive” (Icon_Receive) · refresh balance (Icon_Refresh) · “Transaction History” · “Scan any QR” (Icon_Scan)
• Balance: Bank_HSBC · “Last Updated Balance” · ₹85,625 · “Primary” (Icon_Check_Badge)
• Header: Avatar_Hallie_Goebel (opens the menu) · search “Pay by name or phone” (Icon_Search) · history (Icon_History)
• Offer: “Invite friends and get ₹1,000 reward” (Icon_Offer)
• Transactions: “RECENT TRANSACTIONS” · 3 rows (see DATA)

• Account: Avatar_Hallie_Goebel · “Hallie Goebel” · hallie.goebel@example.com
• Actions: “Logout” (Icon_Logout)
• Menu: New Payment (Icon_New_Payment) · Bank Accounts (Icon_Bank) · All Transactions (Icon_History) · Rewards & Offers (Icon_Offer) · Settings (Icon_Settings) — source order
• Presentation: side menu over 03_Home, with 03_Home still partly visible

LINKS

→ tap the visible part of 03_Home → 03_Home

LINKS

→ avatar → 04_Menu

Navigation structure

• Onboarding: 01_Onboarding → Get Started → 02_Phone_Number (sheet over 01) → Get Started → 03_Home; Cancel → 01.
• 04_Menu is a side menu opened from the avatar on 03_Home. There is no tab bar in this task.
• Entry only (no frame): Sign in, search, history, refresh, account tiles, Send, Receive, reward banner, transaction rows, Transaction History, Scan any QR, menu rows, Logout.

Fixed data & copy

Use these values verbatim.

User

Primary account

Other accounts (source order)

Hallie Goebel · hallie.goebel@example.com · Avatar_Hallie_Goebel

HSBC (Bank_HSBC) · Last Updated Balance ₹85,625 · Primary

Axis Bank ₹3,500 (Bank_Axis)
HDFC Bank ₹63,520 (Bank_HDFC)
Deutsche Bank ₹36,258 (Bank_Deutsche)
Union Bank ₹67,820 (Bank_Union)

Recent transactions (newest first)

Reward

Phone sign-up

Paytm Auto Pay · 22 Jan · Weekly transaction · −₹3,500 (Merchant_Paytm)
Risa Midyett · 05 Jan · Gift for Christmas · +₹6,950 (Avatar_Risa_Midyett)
Amazon Pantry · 01 Jan · Subscription payment · −₹1,200 (Merchant_Amazon)

Invite friends and get ₹1,000 reward

Country code +91 · field empty, placeholder 9812345678

Menu (source order)

New Payment · Bank Accounts · All Transactions · Rewards & Offers · Settings · Logout

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #1E32FA and Inter
• Media: illustration, avatars, bank and merchant marks, icons
• Default Button, default Text Field, platform shell incl. numeric keypad

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces, Send / Receive, positive / negative amounts, reward banner, error / disabled
• Type scale, spacing, radii, elevation
• All states: focused field, primary account, pressed, disabled
• Headers, sheet, balance block, account tiles, actions, banner, transaction rows, scan button, side menu
• How the illustration and photos are cropped and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (focused phone field with keypad, primary account, sheet and side-menu presentation)

Deliverable: the link to your own Figma file containing the 4 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Payment Wallet

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (including any tint or gradient), positive / negative amounts, the action colors for Send and Receive, the reward banner, error and disabled, type scale, spacing, radii and elevation.

Brand color

Brand primary · ultramarine

#1E32FA

The app’s main brand color. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  ₹85,625

Use Inter for all UI text (it replaces the source’s SF Pro, which is not available). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 390 × 844 (iPhone 13 / 14). 03_Home may scroll vertically. Light or dark surfaces per screen are your decision.
