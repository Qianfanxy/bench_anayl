# Fruit Hub（6case / case-006）

- 原始模板（只读）：https://www.figma.com/design/OaDbNxIW1tqgFPCmshxmg6/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/OaDbNxIW1tqgFPCmshxmg6/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Fruit Hub — fruit salad ordering app

Design the complete Fruit Hub mobile app: Tony tells the app their first name, browses fruit salad combos, adds one to the basket, checks out with delivery details or a card, and tracks the delivery.
Canvas 375 × 812, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 10 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, success / error / warning / disabled, supporting colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the sheets and every business component as reusable components in your file.
5. Use the logo, product photos, illustrations, map and icons from 04 · Media. Prices use the Naira glyph (Icon_Naira or “₦”).
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Splash

02_Welcome

Goal: Brand recognition while the app loads.

Goal: Explain the offer and start.

MUST INCLUDE

MUST INCLUDE

• Brand: Logo_Fruit_Hub

• Actions: Let’s Continue
• Copy: “Get The Freshest Fruit Salad Combo” · “We deliver the best and freshest fruit salad in town. Order for a combo today!!!”
• Media: Basket_Welcome · Fruit_Drops

LINKS

→ auto → 02_Welcome

LINKS

→ Let’s Continue → 03_Name

03_Name

04_Home

Goal: Tell the app your first name.

Goal: Find a fruit salad combo.

MUST INCLUDE

MUST INCLUDE

• Actions: Start Ordering
• Copy: “What is your firstname?”
• Form: first name, entered “Tony”
• Media: Basket_Name · Fruit_Drops

• Account: “Hello Tony, What fruit salad combo do you want today?” · menu entry · My basket entry
• Categories: Hottest / Popular / New combo / Top · current: Hottest
• Hottest: Quinoa fruit salad · Tropical fruit salad · Melon fruit salad, each with photo, name, price, favourite toggle and add to basket
• Recommended: “Recommended Combo” · Honey lime combo · Berry mango combo, each with photo, name, price, favourite toggle and add to basket
• Search & filter: search “Search for fruit salad combos” · filter entry

LINKS

→ Start Ordering → 04_Home

LINKS

→ Quinoa fruit salad → 05_Product_Quinoa
→ My basket → 06_Basket

05_Product_Quinoa

06_Basket

Goal: Choose a quantity and add the combo to the basket.

Goal: Review the basket and check out.

MUST INCLUDE

MUST INCLUDE

• Actions: Go back · favourite toggle · Add to basket
• Contents: “One Pack Contains:” · Red Quinoa, Lime, Honey, Blueberries, Strawberries, Mango, Fresh mint.
• Copy: “Quinoa Fruit Salad” · “If you are looking for a new fruit salad to eat today, quinoa is the perfect brunch for you.”
• Media: Salad_Quinoa
• Quantity: 1 pack, can be decreased / increased · price ₦10,000

• Actions: Go back · Checkout
• Copy: “My Basket”
• Items: Quinoa fruit salad · Melon fruit salad · Tropical fruit salad, each with photo, name, “2 packs” and ₦20,000
• Total: “Total” ₦60,000

LINKS

→ Go back → 04_Home
→ Checkout → 07_Checkout_Delivery

LINKS

→ Go back → 04_Home
→ Add to basket → 06_Basket

07_Checkout_Delivery

08_Checkout_Card

Goal: Give delivery details and choose how to pay.

Goal: Pay by card.

MUST INCLUDE

MUST INCLUDE

• Actions: close · Pay on delivery · Pay with card
• Delivery: “Delivery address” 10th avenue, Lekki, Lagos State · “Number we can call” 09090605708 · both filled in
• Presentation: opens over 06_Basket; the basket stays behind it

• Actions: close · Complete Order
• Card: “Card Holder’s Name” Tony Chris · “Card Number” 1234 5678 9012 1314 · “Date” 10/30 · “CVV” 123 · all filled in
• Presentation: opens over 06_Basket; the basket stays behind it

LINKS

LINKS

→ close → 06_Basket
→ Pay with card → 08_Checkout_Card
→ Pay on delivery → 09_Order_Complete

→ close → 06_Basket
→ Complete Order → 09_Order_Complete

09_Order_Complete

10_Track_Order

Goal: Confirm the order was placed.

Goal: Follow the delivery.

MUST INCLUDE

MUST INCLUDE

• Actions: Track order · Continue shopping
• Copy: “Congratulations!!!” · “Your order has been taken and is being attended to”
• Status: success mark (Icon_Success_Check)

• Actions: Go back · call the delivery agent
• Copy: “Delivery Status”
• Map: Map_Delivery
• Steps, in this order: Order Taken (done, Step_Order_Taken) · Order Is Being Prepared (done, Step_Order_Prepared) · Order Is Being Delivered (current, “Your delivery agent is coming”, Step_Order_Delivering) · Order Received (not yet)

LINKS

→ Track order → 10_Track_Order
→ Continue shopping → 04_Home

LINKS

→ Go back → 04_Home

Navigation structure

• One linear flow, no bottom navigation: 01_Splash → 02_Welcome → 03_Name → 04_Home → 05_Product_Quinoa → 06_Basket → 07_Checkout_Delivery → 08_Checkout_Card → 09_Order_Complete → 10_Track_Order.
• 07 and 08 are sheets over the basket (one frame each). 07 can skip the card step: Pay on delivery → 09.
• Pushed screens with Go back: 05, 06, 10.
• Entry only (no frame): menu, search, filter, categories other than Hottest, favourite toggles, add-to-basket on Home, combos other than Quinoa, call agent.

Fixed data & copy

Use these values verbatim. Currency Nigerian Naira (₦).

Customer

Combos (name · price · photo)

Home sections

First name Tony (entered on 03_Name; greeting on 04_Home)

Honey lime combo · ₦2,000 · Salad_Honey_Lime
Berry mango combo · ₦8,000 · Salad_Berry_Mango
Quinoa fruit salad · ₦10,000 · Salad_Quinoa
Tropical fruit salad · ₦10,000 · Salad_Tropical
Melon fruit salad · ₦10,000 · Salad_Melon

Recommended Combo: Honey lime, Berry mango
Categories: Hottest (current) / Popular / New combo / Top
Hottest: Quinoa, Tropical, Melon

Quinoa Fruit Salad

My Basket

Delivery

One Pack Contains: Red Quinoa, Lime, Honey, Blueberries, Strawberries, Mango, Fresh mint.
“If you are looking for a new fruit salad to eat today, quinoa is the perfect brunch for you.”
Quantity 1 · ₦10,000

Quinoa fruit salad · 2 packs · ₦20,000
Melon fruit salad · 2 packs · ₦20,000
Tropical fruit salad · 2 packs · ₦20,000
Total ₦60,000

Delivery address: 10th avenue, Lekki, Lagos State
Number we can call: 09090605708
Options: Pay on delivery · Pay with card

Card

Order complete

Delivery status

Card Holder’s Name: Tony Chris
Card Number: 1234 5678 9012 1314
Date: 10/30 · CVV: 123
Button: Complete Order

“Congratulations!!!”
“Your order has been taken and is being attended to”
Track order · Continue shopping

Order Taken ✓ · Order Is Being Prepared ✓ · Order Is Being Delivered (now) “Your delivery agent is coming” · Order Received (pending)

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color #FFA451 + Nunito
• Media: logo, product photos, illustrations, map, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, semantic and supporting colors
• Type scale, spacing, radii, elevation
• All states: selected, favourited, pressed, disabled, filled, done / current / pending
• Headers, sheets and all business components
• How the step progress and the map are presented

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current category, filled fields, sheet over basket, done / current / pending steps)

Deliverable: the link to your own Figma file containing the 10 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Fruit Hub

Fixed: the brand primary color and the typeface below — they carry the Fruit Hub identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (success, error, warning, disabled), supporting colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#FFA451

The Fruit Hub brand color. Where and how much to use it is your decision.

Typeface

Bad Script · wordmark only

Nunito

Fruit Hub

Aa Bb Cc 0123456789  ₦60,000

Use Nunito for all UI text (replaces the source’s Brandon Grotesque, which is not available). Bad Script appears only inside the supplied Logo_Fruit_Hub — do not use it elsewhere. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 375 × 812 (iPhone). Light mode only. Currency: Nigerian Naira (₦, glyph supplied as Icon_Naira).
