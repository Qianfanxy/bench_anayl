# Foodgo（3case / case-003）

- 原始模板（只读）：https://www.figma.com/design/6hoGDBVDBZzsRgxZ16ZMry/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/6hoGDBVDBZzsRgxZ16ZMry/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

DESIGNER STARTER / FOODGO · LEVEL L2 · v2

Complete mobile product design

Content, structure, the two brand colors and typefaces are fixed. Layout, hierarchy, all other colors, states, components and visual system are yours.

THE ASSIGNMENT

Design the complete Foodgo burger-ordering app: browse the menu, inspect a burger, customize it, pay, and get support or manage the profile.

English interface / US dollars ($) / one signed-in customer: Sophia Patel. Base viewport 430 × 932 for every frame; Home and Customize may scroll vertically.

FIXED by this brief: frame list & names, the content each frame must contain (what, not how), navigation structure, all data and copy, the two brand colors (red #EF2A39, dark brown #3C2F2F), typefaces (Lobster logotype + Roboto), media, a default Button, a default Text Field and the platform shell.

YOURS to decide: layout, grouping, order and emphasis on every screen; all other colors (neutrals, text, surfaces, rating, semantic); type scale, spacing, radii, elevation; all states (selected, favourited, added, checked, pressed, disabled, focused, destructive); headers, bottom navigation, dialogs and every business component.

FRAMES TO DELIVER (11) — USE THESE EXACT NAMES

01_Splash · 02_Home · 03_Product_Cheeseburger · 04_Product_Veggie · 05_Product_Chicken · 06_Product_Fried_Chicken ·

07_Customize · 08_Payment · 09_Payment_Success_Overlay · 10_Profile · 11_Support_Chat. One frame per state.

FRAME-BY-FRAME CHECKLIST

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks. Layout, grouping, emphasis and styling are your decisions.

01_Splash

Goal: brand recognition while the app loads.

Must include:
• Brand: Foodgo wordmark
• Media: Splash_Burger_Stack

Links: auto-advances to 02_Home.

02_Home

Goal: find a burger fast — by search, category or browsing.

Must include:
• Account: avatar
• Brand: Foodgo wordmark · “Order your favourite food!”
• Categories: All / Combos / Sliders / Classic · current: All
• Main navigation: current tab Home · Add entry
• Menu: 4 items, each with image, category, name, rating and favourite toggle · Cheeseburger Wendy’s Burger is a favourite
• Search & filter: search “Search” · filter entry

Links: each menu item → its product frame (03–06); Profile tab → 10_Profile; Support tab → 11_Support_Chat.

03–06_Product_* (4 frames, same structure)

Goal: judge a burger and choose spice level and portions before ordering.

Must include:
• Actions: back · search · Order Now
• Burger: image · full name · rating · preparation time · description
• Portion: current portion, can be decreased / increased
• Price: price for the current portion
• Spicy: level from Mild to Hot · current level
Data per burger: see DATA.

Links: back → 02_Home; Order Now on 03_Product_Cheeseburger → 07_Customize (Order Now on 04–06 is entry only).

07_Customize

Goal: personalize the Cheeseburger Wendy’s Burger and see the total before paying.

Must include:
• Actions: back · search · Order Now
• Add-ons: “Toppings” Tomato, Onions, Pickles, Bacon, Cheese, Mushroom, Avocado · “Side options” Fries, Coleslaw, Salad, Onion Rings, Mozzarella Sticks · each can be added or removed · added: Tomato, Cheese, Fries
• Copy: “Customize Your Burger to Your Tastes. Ultimate Experience”
• Media: Burger_Exploded_Custom
• Portion: 2, can be decreased / increased
• Spicy: level from Mild to Hot · current level
• Total: $16.48

Links: back → 03_Product_Cheeseburger; Order Now → 08_Payment.

08_Payment

Goal: verify the order cost and pay with a saved card.

Must include:
• Actions: back · search · Pay Now
• Order summary: “Order summary” · Order $16.48 · Taxes $0.30 · Delivery fees $1.50 · Total $18.28 · Estimated delivery time 15–30 mins
• Payment methods: “Payment methods” · Credit card (Mastercard, 5105 **** **** 0505) · Debit card (Visa, 3566 **** **** 0505) · only one can be chosen · current: Credit card
• Save card: “Save card details for future payments” · on
• Total price: $18.28

Links: back → 07_Customize; Pay Now → 09_Payment_Success_Overlay.

09_Payment_Success_Overlay

Goal: confirm the payment unambiguously.

Must include:
• Actions: Go Back
• Copy: “Success!” · “Your payment was successful. A receipt for this purchase has been sent to your email.”
• Presentation: dialog over 08_Payment; Payment stays behind it
• Status: success mark

Links: Go Back → 02_Home.

10_Profile

Goal: review account details and reach account actions.

Must include:
• Account: avatar · Delivery address 123 Main St, Apartment 4A, New York, NY · Email sophiapatel@gmail.com · Name Sophia Patel · Password (masked, locked)
• Actions: back · settings · Edit Profile · Log out
• Entries: Order history · Payment Details

Links: back → 02_Home.

11_Support_Chat

Goal: get a delivery update from support.

Must include:
• Actions: back · menu · send
• Conversation: 7 items in the order given in DATA — each message from the agent or the customer · timestamp “26 minutes ago” after the agent’s third message
• Input: “Type here...”

Links: back → 02_Home.

STRUCTURE (FIXED)

Main navigation on 02_Home — in this order: Home → 02 · Profile → 10 · Support → 11 · Favourites (entry only), plus a central Add (entry only). The current tab must match the frame. How it looks is yours.

Order flow: Home → Product → Customize → Payment → Success dialog (over Payment) → Home. Product, Customize, Payment, Profile and Support use back navigation.

Entry-only (no screen required): search, filter, Combos / Sliders / Classic results, settings, menu, Payment Details, Order history, Edit Profile, Log out, Order Now on 04–06.

DATA & COPY (FIXED)

Customer: Sophia Patel · sophiapatel@gmail.com · 123 Main St, Apartment 4A, New York, NY. Use Avatar_Neutral wherever the customer appears.

Menu (category · name · rating · time · price per portion → portion shown on its product frame = price shown):

Cheeseburger · Wendy’s Burger · 4.9 · 26 mins · $8.24 → portion 1 = $8.24 · Hamburger · Veggie Burger · 4.8 · 14 mins · $9.99 → portion 1 = $9.99

Hamburger · Chicken Burger · 4.6 · 42 mins · $6.24 → portion 2 = $12.48 · Hamburger · Fried Chicken Burger · 4.5 · 14 mins · $6.75 → portion 4 = $27.00

Descriptions — Cheeseburger Wendy’s Burger: “A classic fast food burger that packs a punch of flavor in every bite: a juicy beef patty cooked to perfection, topped with melted American cheese, crispy lettuce, ripe tomato and crunchy pickles.”

Veggie: “A savory blend of fresh vegetables and herbs, topped with crisp lettuce, juicy tomatoes and tangy pickles, served on a soft, toasted bun.”

Chicken: “A delicious and healthier alternative to traditional beef burgers, perfect for a lighter meal.”

Fried Chicken: “A juicy chicken patty, hand-breaded and deep-fried to perfection, served on a warm bun with lettuce, tomato and a creamy sauce.”

Customize: add-ons are included at no extra cost; Total = 2 × $8.24 = $16.48. Payment: $16.48 + $0.30 + $1.50 = $18.28 (same total in summary and at Pay Now).

Chat (A = agent, C = customer): A “Hi, how can I help you?” · C “Hello, I ordered two Cheeseburger Wendy’s Burgers. Can I know how long it will take to arrive?” · A “Ok, please let me check!” · C “Sure...” ·

A “It’ll take 25 minutes to arrive at your address.” · [26 minutes ago] · C “Ok, thank you for your support.”

The source file has inconsistent totals ($16.49 / $18.19), a mismatched order in chat and typos (“Bacons”, “thanks you”). Follow this brief, not the source.

HANDOFF & EVALUATION

Copy Components and Media into your own new Figma file; do not edit, rename or delete anything in this starter file.

Deliver all 11 frames with the exact names above, prototype links as listed, and your own reusable components. Submit your file link.

Evaluated: (1) checklist coverage per frame · (2) data & copy accuracy · (3) flow & prototype completeness · (4) information hierarchy · (5) visual quality & consistency of your own system · (6) component reuse · (7) state design.

The completed reference screens are withheld. There is no single correct layout.

## 01 · Foundations 视觉规范

FOODGO / DESIGN FOUNDATIONS

Fixed: two brand colors + typefaces. You build everything else.

01  BRAND COLORS (FIXED)

Foodgo’s identity relies on two colors: the red and the dark brown below. Define every other color yourself — neutrals and grays, text, backgrounds and surfaces, rating, semantic colors (success, mild / hot, disabled) and any supporting colors — once, and use them consistently.

Brand red

Brand dark brown

#EF2A39

#3C2F2F

Foodgo brand color. Where and how much to use it is your decision.

Foodgo brand color. Where and how much to use it is your decision.

02  TYPEFACES (FIXED)

Lobster is reserved for the Foodgo logotype (use the supplied outlined wordmark). Roboto for all UI text. Sizes, weights and line heights are yours to define as a consistent type scale.

Foodgo

Roboto  Aa Bb Cc 0123456789  $18.28

03  YOUR SYSTEM (TO DESIGN)

• Base viewport 430 × 932 (fixed). Home and Customize may scroll vertically; horizontal carousels are allowed.

• Define your own type scale, spacing rhythm, corner radii, elevation, dividers and icon sizing — and apply them consistently on every screen.

• Build reusable components for repeated patterns. Component reuse and consistency are evaluated.

• Icons from 04 · Media may be recolored to your palette; do not redraw brand assets.
