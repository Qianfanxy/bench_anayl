# Nectar（6case / case-002）

- 原始模板（只读）：https://www.figma.com/design/weYFSS5IcozT265TIIh0H2/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/weYFSS5IcozT265TIIh0H2/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

NECTAR · LEVEL L2 · DESIGN TASK · v2

Nectar — online groceries app

Design the complete Nectar mobile grocery app: a shopper in Dhaka signs in with a phone number, browses the store, opens a product, explores a category, fills the cart, checks out, gets an order confirmation and manages the account.
Canvas 414 × 896 (iPhone), light mode only. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 12 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, success / error / warning / disabled, rating), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the main navigation and every business component as reusable components in your file.
5. Use product photos, category images, the logo, flag, illustrations and icons from 04 · Media. People have no photos: use Avatar_Neutral.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Splash

02_Onboarding

Goal: Brand recognition while the app loads.

Goal: Welcome a new shopper and get started.

MUST INCLUDE

MUST INCLUDE

• Brand: Nectar logo

• Actions: Get Started
• Brand: Nectar_Carrot
• Copy: “Welcome to our store” · “Get your groceries in as fast as one hour”
• Media: Photo_Welcome_Delivery

LINKS

→ auto → 02_Onboarding

LINKS

→ Get Started → 03_Sign_In

03_Sign_In

04_Verification

Goal: Start sign-in with a phone number or a social account.

Goal: Verify the phone number with a 4-digit code.

MUST INCLUDE

MUST INCLUDE

• Actions: Continue with Google · Continue with Facebook
• Copy: “Get your groceries with nectar” · “Or connect with social media”
• Media: Photo_Sign_In_Groceries
• Phone: country code +880 (Flag_Bangladesh) · number not entered yet

• Actions: back · Resend Code · next
• Code: “Code” · 4 digits, none entered yet
• Copy: “Enter your 4-digit code”

LINKS

LINKS

→ back → 03_Sign_In
→ next → 05_Home

→ phone number → 04_Verification

05_Home

06_Product_Detail

Goal: Find groceries fast — by search, offer or category.

Goal: Judge a product and add it to the basket.

MUST INCLUDE

MUST INCLUDE

• Best Selling: “Best Selling” · See all · Bell Pepper Red, Ginger
• Brand: Nectar_Carrot
• Exclusive Offer: “Exclusive Offer” · See all · Organic Bananas, Red Apple
• Groceries: “Groceries” · See all · categories Pulses, Rice · products Beef Bone, Broiler Chicken
• Location: Dhaka, Banasree
• Main navigation: current tab Shop
• Products (all sections): each with image, name, unit, price and add to cart
• Promotion: “Fresh Vegetables” · “Get Up To 40% OFF” (Banner_Fresh_Vegetables)
• Search: “Search Store”

• Actions: back · share · favourite (not favourited yet) · Add To Basket
• Details: “Product Detail” with its description (open) · “Nutritions” 100gr · “Review” 5 of 5 stars
• Product: Product_Red_Apple · “Natural Red Apple” · “1kg, Price” · $4.99
• Quantity: 1, can be decreased / increased

LINKS

→ back → 05_Home
→ Add To Basket → 09_My_Cart

LINKS

→ Red Apple → 06_Product_Detail
→ tabs → 05 / 07 / 09 / 12

07_Explore

08_Beverages

Goal: Browse the store by category.

Goal: Pick drinks from one category.

MUST INCLUDE

MUST INCLUDE

• Categories: 6, each with its image — Fresh Fruits & Vegetable · Cooking Oil & Ghee · Meat & Fish · Bakery & Snacks · Dairy & Eggs · Beverages
• Copy: “Find Products”
• Main navigation: current tab Explore
• Search: “Search Store”

• Actions: back · filter entry
• Copy: “Beverages”
• Products: 6 — Diet Coke · Sprite Can · Apple & Grape Juice · Orange Juice · Coca Cola Can · Pepsi Can — each with image, name, size, price and add to cart

LINKS

LINKS

→ back → 07_Explore

→ Beverages → 08_Beverages
→ tabs

09_My_Cart

10_Checkout_Overlay

Goal: Review the basket and go to checkout.

Goal: Confirm delivery, payment and cost, then place the order.

MUST INCLUDE

MUST INCLUDE

• Actions: Go to Checkout, showing the cart total $14.96
• Cart: 4 items — Bell Pepper Red · Egg Chicken Red · Organic Bananas · Ginger — each with image, name, unit, price, quantity 1 (can be decreased / increased) and remove
• Copy: “My Cart”
• Main navigation: current tab Cart

• Actions: close · Place Order
• Copy: “Checkout”
• Legal: “By placing an order you agree to our Terms And Conditions” (Terms And Conditions is a link)
• Order rows: Delivery “Select Method” · Payment (card, Icon_Payment) · Promo Code “Pick discount” · Total Cost $14.96 — each row opens its own choice
• Presentation: opens over 09_My_Cart; the cart stays behind it

LINKS

LINKS

→ Go to Checkout → 10_Checkout_Overlay
→ tabs

→ close → 09_My_Cart
→ Place Order → 11_Order_Accepted

11_Order_Accepted

12_Account

Goal: Confirm the order unambiguously.

Goal: Identify the account and reach account settings.

MUST INCLUDE

MUST INCLUDE

• Actions: Track Order · Back to home
• Copy: “Your Order has been accepted” · “Your items have been placed and are on their way to being processed”
• Media: Illustration_Order_Accepted

• Account: Avatar_Neutral · “Afsar Hossen” · edit name entry · imshuvo97@gmail.com
• Actions: Log Out
• Entries: About · Delivery Address · Help · My Details · Notifications · Orders · Payment Methods · Promo Code
• Main navigation: current tab Account

LINKS

LINKS

→ Back to home → 05_Home

→ tabs

Navigation structure

• Onboarding: 01_Splash → 02_Onboarding → 03_Sign_In → 04_Verification → 05_Home.
• Main navigation on 05, 07, 09, 12 — five tabs in this order: Shop (Icon_Shop) → 05 · Explore (Icon_Explore) → 07 · Cart (Icon_Cart) → 09 · Favourite (Icon_Favourite, entry only) · Account (Icon_Account) → 12. The current tab must match the frame. How it looks is yours.
• Pushed screens with back: 04, 06, 08. 06 and 08 have no main navigation.
• 10_Checkout_Overlay opens over 09_My_Cart; 11_Order_Accepted replaces it.
• Entry only (no screen required): See all, add to cart on product cards, share, favourite, filter, Resend Code, social sign-in, Track Order, Favourite tab, Delivery / Payment / Promo Code rows, account entries, edit name, Log Out.
• There is no search-results, filter, favourites, location or order-failed screen — do not add frames beyond the 12.

Fixed data & copy

Use these values verbatim.

Shopper

Catalog (name · unit · price · image)

Afsar Hossen · imshuvo97@gmail.com · avatar = Avatar_Neutral
Location: Dhaka, Banasree · phone country code +880 (Bangladesh)
Currency USD · unit line format “1kg, Price”

Organic Bananas · 7pcs · $4.99 · Product_Organic_Bananas
Red Apple · 1kg · $4.99 · Product_Red_Apple (detail title “Natural Red Apple”)
Bell Pepper Red · 1kg · $4.99 · Product_Bell_Pepper_Red
Ginger · 250gm · $2.99 · Product_Ginger
Beef Bone · 1kg · $4.99 · Product_Beef_Bone
Broiler Chicken · 1kg · $4.99 · Product_Broiler_Chicken
Egg Chicken Red · 4pcs · $1.99 · Product_Egg_Chicken_Red

Beverages (name · size · price)

Home

Diet Coke · 355ml · $1.99
Sprite Can · 325ml · $1.50
Apple & Grape Juice · 2L · $15.99
Orange Juice · 2L · $15.99
Coca Cola Can · 325ml · $4.99
Pepsi Can · 330ml · $4.99

Location “Dhaka, Banasree” · search “Search Store”
Promotion “Fresh Vegetables” · “Get Up To 40% OFF”
Exclusive Offer: Organic Bananas, Red Apple
Best Selling: Bell Pepper Red, Ginger
Groceries: categories Pulses (Category_Pulses), Rice (Category_Rice); Beef Bone, Broiler Chicken

Product detail

Cart & checkout

“Natural Red Apple” · “1kg, Price” · quantity 1 · $4.99
Product Detail: “Apples are nutritious. Apples may be good for weight loss. Apples may be good for your heart. As part of a healthful and varied diet.”
Nutritions: 100gr · Review: 5 of 5 stars

Bell Pepper Red $4.99 · Egg Chicken Red $1.99 · Organic Bananas $4.99 · Ginger $2.99 — quantity 1 each
Total $14.96 — the same on Go to Checkout and Total Cost
Delivery “Select Method” · Promo Code “Pick discount”

Explore

Sign in, verification & order

“Find Products” · search “Search Store”
Fresh Fruits & Vegetable · Cooking Oil & Ghee · Meat & Fish · Bakery & Snacks · Dairy & Eggs · Beverages (images: Category_*)

Sign in: “Get your groceries with nectar” · +880 · “Or connect with social media” · Continue with Google · Continue with Facebook
Verification: “Enter your 4-digit code” · “Code” · Resend Code
Onboarding: “Welcome to our store” · “Get your groceries in as fast as one hour” · Get Started
Accepted: “Your Order has been accepted” · “Your items have been placed and are on their way to being processed” · Track Order · Back to home

Account

Source corrections

Afsar Hossen · imshuvo97@gmail.com
Orders · My Details · Delivery Address · Payment Methods · Promo Code · Notifications · Help · About · Log Out

The source has typos (Naturel, Frash, Orenge, “Priceg”, “placcd”, Promo Cord, Notifecations), product prices that differ between screens and cart totals that do not add up ($12.96 / $13.97). Follow this brief, not the source.

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color + Poppins
• Media: product photos, category images, logo, flag, illustrations, icons, neutral avatar
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, semantic and rating colors
• Type scale, spacing, radii, elevation
• All states: selected, pressed, disabled, favourite, quantity, open / closed
• Headers, main navigation, overlay and all business components

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tabs, quantities, favourite, empty code input, checkout over cart)

Deliverable: the link to your own Figma file containing the 12 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

NECTAR · 01 FOUNDATIONS

Foundations · Nectar

Fixed: the brand primary color and the typeface below — they carry the Nectar identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (success, error, warning, disabled), rating and supporting colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#53B175

The Nectar brand color. Where and how much to use it is your decision.

Typeface

Poppins

Aa Bb Cc 0123456789  $14.96  1kg, Price

Use Poppins for all UI text (Regular / Medium / SemiBold / Bold available). It replaces the source font Gilroy, which is not available. The Nectar logo is supplied as an asset in 04 · Media — do not retype it.

Canvas: 414 × 896 (iPhone). Light mode only. Long screens (Home) may scroll vertically.
