# Stylish（6case / case-003）

- 原始模板（只读）：https://www.figma.com/design/0J1ZWGCk2siHZb2mp0feAr/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/0J1ZWGCk2siHZb2mp0feAr/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Stylish — fashion & lifestyle shopping app

Design the complete Stylish mobile shopping app: a first-time shopper goes through onboarding, signs in, browses featured deals and trending products, opens a product, reviews the shopping bag, pays and manages the profile.
Canvas 375 × 812, light mode only. Home, Product list, Product detail and Profile may scroll vertically. Currency: Indian rupee (₹). Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 15 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, success / error / disabled, sale and rating colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the main navigation and every business component as reusable components in your file.
5. Use the logo, product photos, banners, payment logos and icons from 04 · Media. A product marked “no photo supplied” needs a consistent fallback of your choice.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Splash

02_Onboarding_Choose_Products

Goal: Recognise the brand while the app loads.

Goal: Learn what the app offers (step 1).

MUST INCLUDE

MUST INCLUDE

• Brand: Stylish logo

• Actions: Next · Skip
• Copy: “Choose Products” · “Browse thousands of products across fashion, beauty, electronics and more.”
• Media: Onboarding_Choose_Products
• Progress: step 1 of 3

LINKS

→ auto-advance → 02_Onboarding_Choose_Products

LINKS

→ Next → 03_Onboarding_Make_Payment
→ Skip → 05_Sign_In

03_Onboarding_Make_Payment

04_Onboarding_Get_Your_Order

Goal: Learn how paying works (step 2).

Goal: Learn how delivery works (step 3).

MUST INCLUDE

MUST INCLUDE

• Actions: Next · Prev · Skip
• Copy: “Make Payment” · “Pay securely with your saved cards, PayPal or Apple Pay.”
• Media: Onboarding_Make_Payment
• Progress: step 2 of 3

• Actions: Get Started · Prev · Skip
• Copy: “Get Your Order” · “Track your order until it arrives at your door.”
• Media: Onboarding_Get_Your_Order
• Progress: step 3 of 3

LINKS

LINKS

→ Prev → 02 · Next → 04 · Skip → 05_Sign_In

→ Prev → 03 · Get Started → 05_Sign_In · Skip → 05_Sign_In

05_Sign_In

06_Sign_Up

Goal: Sign in to an existing account.

Goal: Create an account.

MUST INCLUDE

MUST INCLUDE

• Actions: Forgot Password? · Login · “Create An Account” Sign Up
• Copy: “Welcome Back!”
• Form: Password (can be shown or hidden) · Username or Email · nothing entered yet
• Social sign-in: “- OR Continue with -” · Apple · Facebook · Google

• Actions: Create Account · “I Already Have an Account” Login
• Copy: “Create an account”
• Form: Confirm Password · Password · Username or Email · both passwords can be shown or hidden · nothing entered yet
• Legal: “By clicking the Create Account button, you agree to the public offer”
• Social sign-in: “- OR Continue with -” · Apple · Facebook · Google

LINKS

→ Login → 08_Get_Started
→ Forgot Password? → 07_Forgot_Password
→ Sign Up → 06_Sign_Up

LINKS

→ Create Account → 08_Get_Started
→ Login → 05_Sign_In

07_Forgot_Password

08_Get_Started

Goal: Request a password reset.

Goal: Enter the store.

MUST INCLUDE

MUST INCLUDE

• Actions: Submit
• Copy: “Forgot password?” · “* We will send you a message to set or reset your new password”
• Form: email address (“Enter your email address”), nothing entered yet

• Actions: Get Started
• Copy: “You want Authentic, here you go!” · “Find it here, buy it now!”
• Media: Get_Started_Photo

LINKS

LINKS

→ Get Started → 09_Home

→ Submit → 05_Sign_In

09_Home

10_Product_List

Goal: Discover deals, categories and trending products.

Goal: Browse every item in the store.

MUST INCLUDE

MUST INCLUDE

• Account: avatar · menu entry
• Banner: “40–50% OFF” · “Now in all products” · “All colours” · Shop Now · 3 slides · current: slide 2
• Brand: Stylish logo
• Categories: Beauty · Fashion · Kids · Mens · Womens · Gifts, each with its image
• Deal of the Day: “Deal of the Day” · “22h 55m 20s remaining” · View all · 4 products (DATA)
• Featured: “All Featured” · Sort · Filter
• Main navigation: current tab Home
• Promotions: Special Offers · Flat and Heels · Hot Summer Sale · New Arrivals · Sponsored (DATA)
• Search: “Search any Product..” · voice input
• Trending Products: “Trending Products” · “Last Date 28/02/22” · View all · 5 products (DATA)

• Account: avatar · menu entry
• Brand: Stylish logo
• Main navigation: current tab Home
• Products: 14 products, each with image, name, description, price and rating count (DATA)
• Results: “52,082+ Items” · Sort · Filter
• Search: “Search any Product..” · voice input

LINKS

→ tabs

LINKS

→ Trending Products View all → 10_Product_List
→ Sponsored → 11_Product_Detail
→ tabs

11_Product_Detail

12_Shopping_Bag

Goal: Judge a product and add it to the bag.

Goal: Review the bag before paying.

MUST INCLUDE

MUST INCLUDE

• Actions: back · cart entry · Go to cart · Buy Now · View Similar · Add to Compare
• Delivery: “Delivery within 1 hour”
• Gallery: 5 photos (Nike_Sneakers_1–5) · current: photo 1
• Main navigation: current tab Home
• Policies: Nearest Store · VIP · Return policy
• Price: ₹1,500 · was ₹2,999 · 50% Off
• Product: “Nike Sneakers” · “Vision Alta Men’s Shoes Size (All Colours)” · rating count 56,890 · “Product Details” with its text and “More”
• Similar: “Similar To” · “282+ Items” · Sort · Filter · 4 products (DATA)
• Size: 6 UK / 7 UK / 8 UK / 9 UK / 10 UK · current: 7 UK (“Size: 7 UK”)

• Actions: back · wishlist entry · Apply Coupons “Select” · Proceed to Payment · View Details
• Copy: “Shopping Bag”
• Item: Women’s Casual Wear · photo · Size 42 (changeable) · Qty 1 (changeable) · “Delivery by 10 May”
• Order Payment Details: Order Amounts ₹7,000.00 · Convenience: Know More · Apply Coupon · Delivery Fee ₹30.00 · Order Total ₹7,030.00 · EMI Available · Details
• Total: ₹7,030.00

LINKS

→ back → 11_Product_Detail
→ Proceed to Payment → 13_Payment

LINKS

→ back → 09_Home
→ Go to cart → 12_Shopping_Bag
→ tabs

13_Payment

14_Payment_Success_Overlay

Goal: Choose how to pay and confirm.

Goal: Know the payment went through.

MUST INCLUDE

MUST INCLUDE

• Actions: back · Continue
• Copy: “Checkout” · “Payment”
• Main navigation: current tab Cart
• Payment methods: VISA · PayPal · Maestro · Apple Pay, each “*********2109” · only one can be chosen · current: VISA
• Summary: Order ₹7,000 · Shipping ₹30 · Total ₹7,030

• Copy: “Payment done successfully.”
• Presentation: dialog over 13_Payment; Payment stays behind it
• Status: success mark

LINKS

→ tap dialog → 09_Home

LINKS

→ back → 12_Shopping_Bag
→ Continue → 14_Payment_Success_Overlay
→ tabs

15_Profile

Goal: Review and edit account details.

MUST INCLUDE

• Account: avatar · edit avatar
• Actions: back · Change Password · Save
• Bank Account Details: Bank Account Number · Account Holder’s Name · IFSC Code (DATA)
• Business Address Details: Postcode · Address · City · State · Country (DATA)
• Copy: “Profile”
• Personal Details: Email Address aashifa@gmail.com · Password (masked)

LINKS

→ back → 09_Home

Navigation structure

• Onboarding: 01 → 02 → 03 → 04 → 05_Sign_In; Skip on 02–04 goes straight to 05.
• Account: 05_Sign_In ↔ 06_Sign_Up; 05 → 07_Forgot_Password → 05. Login / Create Account → 08_Get_Started → 09_Home.
• Main navigation on 09, 10, 11, 13 — five tabs in this order: Home (Icon_Home) → 09 · Wishlist (Icon_Wishlist, entry only) · Cart (Icon_Cart) → 12_Shopping_Bag · Search (Icon_Search, entry only) · Setting (Icon_Settings) → 15_Profile. The current tab must match the frame. How it looks is yours.
• Purchase: 09 → 11_Product_Detail → 12_Shopping_Bag → 13_Payment → 14 (dialog over 13) → 09.
• Entry only (no screen required): menu, Sort, Filter, voice input, Shop Now, View all on Deal of the Day / New Arrivals, Visit now, Buy Now, View Similar, Add to Compare, Apply Coupons, Know More, EMI Details, Change Password, Save, social sign-in.
• Do not add frames beyond the 15.

Fixed data & copy

Use these values verbatim. Counts use Indian digit grouping (1,52,344). “was” = original price shown struck through or otherwise marked as former price — how is yours.

User & account

Categories (Home)

Aashifa · aashifa@gmail.com · password masked · avatar = Avatar_Illustrated
Sign in / Sign up fields: “Username or Email”, “Password”, “Confirm Password” (placeholders, nothing entered)

Beauty (Category_Beauty) · Fashion (Category_Fashion) · Kids (Category_Kids) · Mens (Category_Mens) · Womens (Category_Womens) · Gifts (Category_Gifts)

Deal of the Day

Trending Products

Women Printed Kurta · ₹1,500 · was ₹2,499 · 40% Off · 56,890 ratings (Deal_Women_Printed_Kurta)
HRX by Hrithik Roshan · ₹2,499 · was ₹4,999 · 50% Off · 3,44,567 ratings (Deal_HRX_Sneakers)
Philips BHH880/10 · “Hair Straightening Brush With Keratin Infused Bristles (Black).” · ₹999 · was ₹1,999 · 50% Off · 6,46,776 ratings · no photo supplied
TITAN Men Watch- 1806N · “This Titan watch in Black color is I wanted to buy for a long time” · ₹1,500 · was ₹3,500 · 57% Off · 15,007 ratings (Deal_Titan_Watch)

IWC Schaffhausen 2021 Pilot’s Watch “SIHH 2019” 44mm · ₹650 · was ₹1,599 · 59% off (Trending_IWC_Watch)
Labbin White Sneakers For Men and Female · ₹650 · was ₹1,250 · 48% off (Trending_Labbin_Sneakers)
Mammon Women’s Handbag (Set of 3, Beige) · ₹750 · was ₹1,999 · 62% off · no photo supplied
Do Bhai Women Wedges Sandal (Butterfly) · ₹750 · was ₹1,499 · 50% off (Trending_Wedges_Sandal)
Lakme Enrich Matte Lipstick - Shade RM1 (4.7gm) · ₹950 · was ₹1,990 · 52% off (Trending_Lakme_Lipstick)

Promotions (Home)

Product list (52,082+ Items)

Special Offers 😱 · “We make sure you get the offer you need at best prices” (Promo_Special_Offer)
Flat and Heels · “Stand a chance to get rewarded” · Visit now (Promo_Flat_And_Heels)
Hot Summer Sale banner (Promo_Hot_Summer_Sale)
New Arrivals · “Summer’ 25 Collections” · View all
Sponsored · “up to 50% Off” (Promo_Sponsored_Shoes)
Banner slide: Promo_Banner_Sale

Black Winter Jacket · Autumn And Winter Casual cotton-padded jacket · ₹499 · 6,890
Mens Starry · Mens Starry Sky Printed Shirt, 100% Cotton Fabric · ₹399 · 1,52,344
Black Dress · Solid Black Dress for Women, Sexy Chain Shorts Ladies · ₹2,000 · 5,23,456
Pink Embroidered Dress · EARTHEN Rose Pink Embroidered Tiered Maxi Dress · ₹1,900 · 45,678
Flare Dress · Antheaa Black & Rust Orange Floral Print Tiered Midi Flared Dress · ₹1,990 · 3,35,566
Denim Dress · Blue cotton denim dress, Look 2 printed cotton dress · ₹999 · 27,344
Jordan Stay · The classic Air Jordan 12 to create a shoe that’s fresh · ₹4,999 · 10,23,456
Realme 7 · 6 GB RAM | 64 GB ROM | Expandable Upto 256 GB · ₹3,499 · 3,44,567
Sony PS4 · Sony PS4 Console, 1TB Slim with 3 Games · ₹1,999 · 8,35,566
Black Jacket · Warm and comfortable everyday jacket · ₹2,999 · 2,23,569
D7200 Digital Camera · D7200 Digital Camera (Nikon) · ₹26,999 · 67,456 · no photo supplied
Men’s Formal Shoes · George Walker Derby Brown Formal Shoes · ₹999 · 13,45,678
MuscleBlaze Muesli · Nutritional powerhouse: MuscleBlaze High Protein Muesli · ₹3,900 · 1,35,566
Hot Chocolate · Hot chocolate with ashwagandha · ₹200 · 6,23,569
Photos: List_<Name> in 04 · Media, same order

Product detail

Similar To (282+ Items)

Nike Sneakers · “Vision Alta Men’s Shoes Size (All Colours)” · 56,890 ratings · ₹1,500 · was ₹2,999 · 50% Off
Product Details: “Perhaps the most iconic sneaker of all-time, this original “Chicago” colorway is the cornerstone to any sneaker collection. Made famous in 1985 by Michael Jordan, the shoe has stood the test of time, becoming the most famous colorway of the Air Jordan 1. This 2015 release saw the…” + More
Sizes 6 UK · 7 UK (selected) · 8 UK · 9 UK · 10 UK · “Delivery within 1 hour”

Nike Sneakers · Nike Air Jordan Retro 1 Low Mystic Black · ₹1,900 · 46,890 (Similar_1)
Nike Sneakers · Mid Peach Mocha Shoes For Man White Black Pink Sneakers · ₹1,900 · 2,56,890 (Similar_2)
Nike Sneakers · Nike Air Jordan 1 Low Shoes For Man Basketball Shoes · ₹1,900 · 1,56,890 (Similar_3)
Nike Sneakers · Jordan 1 Hyper Royal Heavy Quality · ₹1,500 · 96,890 (Similar_4)

Bag & payment

Profile

Item: Women’s Casual Wear (Bag_Womens_Casual_Wear) · Size 42 · Qty 1 · Delivery by 10 May · ₹7,000.00
Order Amounts ₹7,000.00 + Delivery Fee ₹30.00 = Order Total ₹7,030.00
Payment summary: Order ₹7,000 · Shipping ₹30 · Total ₹7,030
Methods: VISA (Logo_Visa) · PayPal (Logo_PayPal) · Maestro (Logo_Maestro) · Apple Pay (Logo_Apple) — each “*********2109”; VISA selected

Email Address aashifa@gmail.com · Password masked
Business Address: Postcode N1 2LL · Address 216 St Paul’s Rd · City London · State England · Country United Kingdom
Bank: Account Number 204356XXXXXXX · Account Holder’s Name Abhiraj Sisodiya · IFSC Code SBIN00428

Onboarding & sign-in copy

02 “Choose Products” · 03 “Make Payment” · 04 “Get Your Order” (bodies as in the frame list)
Sign in “Welcome Back!” · Sign up “Create an account” · Forgot “Forgot password?”
Get Started “You want Authentic, here you go!” · “Find it here, buy it now!”

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color + Montserrat
• Media: logo, product photos, banners, payment logos, icons, illustrated avatar
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, semantic, sale and rating colors
• Type scale, spacing, radii, elevation
• All states: selected, pressed, disabled, focused, current slide / step
• Headers, main navigation, product cards, dialogs and all business components
• How prices, discounts and ratings are shown

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, size, slide, step and payment method; empty forms)

Deliverable: the link to your own Figma file containing the 15 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Stylish

Fixed: the brand primary color and the typeface below — they carry the Stylish identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (success, error, warning, disabled), sale / discount and rating colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#F83758

The Stylish brand color. Where and how much to use it is your decision.

Typeface

Montserrat

Aa Bb Cc 0123456789  ₹1,500  50% Off

Use Montserrat for all UI text (Regular / Medium / SemiBold / Bold available). The Stylish logo is supplied as artwork in 04 · Media — do not retype it.

Canvas: 375 × 812 (iPhone). Light mode only.
