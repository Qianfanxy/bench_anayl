# Fasco（web10 / case-003）

- 原始模板（只读）：https://www.figma.com/design/MJqW2pGKpfgozMkzULp1Ne/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/MJqW2pGKpfgozMkzULp1Ne/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

FASCO — fashion store website

Design a fashion e-commerce website: land on the home page, browse the shop, open a product, add it to the cart, review the cart, check out, and sign up, sign in or recover an account. Desktop web, 1920 wide, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 11 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in page order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the two typefaces in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii, elevation and the page grid, and apply them consistently.
4. 02 · Components gives only a default Button and a default Text Field. Design all other states, the header, the footer, the navigation and every business component as reusable components in your file.
5. Use the photos, the avatars, the sign-in logos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Home

02_Shop

Goal: Discover deals, new arrivals and the brand.

Goal: Filter the catalog and pick a product.

MUST INCLUDE

MUST INCLUDE

• Brands: Minimog · Retrolie · Brook · Learts · Vagabond (as wordmarks)
• Collection banner: Photo_Collection with item labels “Flat Cap” · “Cotton Shirt” · “Suspender” · “Leather Shoes” · “Men Collection” · “Classic Gentleman” · “DESCRIPTION” · copy (see DATA) · “Size:” M · $100.00 · “Buy Now”
• Deals Of The Month: “Deals Of The Month” · copy (see DATA) · “Buy Now” · “Hurry, Before It’s Too Late!” · countdown 02 Days · 06 Hr · 05 Mins · 30 Sec · deal slides Photo_Deal_1, Photo_Deal_2, Photo_Deal_3 · current slide card “01 — Spring Sale” · “30% OFF” · previous / next (Icon_Chevron_Left, Icon_Chevron_Right) · slide indicator: 4 slides, current 1
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: “FASCO” · Support Center · Invoicing · Contract · Careers · Blog · FAQs · “Copyright © 2022 FASCO. All Rights Reserved.”
• Header: “FASCO” wordmark · navigation Home / Deals / New Arrivals / Packages · current: Home · “Sign in” · “Sign Up”
• Hero: Photo_Hero_Left · Photo_Hero_Top · Photo_Hero_Bottom · Photo_Hero_Right · “ULTIMATE” · “SALE” · “NEW COLLECTION” · “SHOP NOW”
• Instagram: “Follow Us On Instagram” · copy (see DATA) · Photo_Instagram_1 – Photo_Instagram_7
• New Arrivals: “New Arrivals” · copy (see DATA) · tabs Men’s Fashion · Women’s Fashion · Women Accessories · Men Accessories · Discount Deals · current: Women’s Fashion · 6 product cards (see DATA) · “View More”
• Newsletter: “Subscribe To Our Newsletter” · copy (see DATA) · email field “michael@example.com” · “Subscribe Now” · Photo_Subscribe_Left · Photo_Subscribe_Right
• Testimonials: “This Is What Our Customers Say” · copy (see DATA) · 3 testimonial cards with avatar, quote, rating (Icon_Star), name and role (see DATA) · current: James K. · previous / next (Icon_Chevron_Left, Icon_Chevron_Right)

• Collection banner: Photo_Collection with item labels “Flat Cap” · “Cotton Shirt” · “Suspender” · “Leather Shoes” · “Men Collection” · “Classic Gentleman” · “DESCRIPTION” · copy (see DATA) · “Size:” M · $100.00 · “Buy Now”
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Filters: “Filters” · Size S · M · L · XL · Colors (swatches) · Prices $0-$50 · $50-$100 · $100-$150 · $150-$200 · $300-$400 · Brands Minimog · Retrolie · Brook · Learts · Vagabond · Abby · Collections All products · Best sellers · New arrivals · Accessories · Tags Fashion · Hats · Sandal · Belt · Bags · Sneaker · Denim · Sunglasses · Beachwear
• Footer: “FASCO” · Home · Shop · Products · Pages · “Copyright © 2022 FASCO. All Rights Reserved.”
• Header: “FASCO” wordmark · navigation Home / Shop / Products / Pages · current: Shop · search (Icon_Search) · account (Icon_Account) · wishlist (Icon_Star) · cart (Icon_Cart)
• Instagram: “Follow Us On Instagram” · copy (see DATA) · Photo_Instagram_1 – Photo_Instagram_7
• Newsletter: “Subscribe To Our Newsletter” · copy (see DATA) · email field “michael@example.com” · “Subscribe Now” · Photo_Subscribe_Left · Photo_Subscribe_Right
• Page title: “Fashion” · breadcrumb Home › Fashion (Icon_Chevron_Right)
• Pagination: 1 · 2 · 3 · next (Icon_Chevron_Right) · current: 1
• Products: 9 product cards with photo, name, price and old price where given; “Sold Out” on Linen-blend Shirt (see DATA)
• Toolbar: sort “Best selling” (Icon_Chevron_Down) · view options grid / list (Icon_View_Grid, Icon_View_List) · current: grid

LINKS

→ any product card → 03_Product
→ cart (header) → 05_Cart
→ account (header) → 08_Sign_In

LINKS

→ SHOP NOW, View More → 02_Shop
→ Sign in → 08_Sign_In
→ Sign Up → 07_Sign_Up

03_Product

04_Mini_Cart

Goal: Choose size and color for the Denim Jacket and add it to the cart.

Goal: Confirm the jacket is in the cart and move on.

MUST INCLUDE

MUST INCLUDE

• Actions: Compare (Icon_Compare) · Ask a question (Icon_Question) · Share (Icon_Share)
• Collection banner: Photo_Collection with item labels “Flat Cap” · “Cotton Shirt” · “Suspender” · “Leather Shoes” · “Men Collection” · “Classic Gentleman” · “DESCRIPTION” · copy (see DATA) · “Size:” M · $100.00 · “Buy Now”
• Delivery: “Estimated Delivery:” Jul 30 - Aug 03 (Icon_Delivery) · “Free Shipping & Returns:” On all orders over $75 (Icon_Returns) · “Guarantee safe & secure checkout”
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: “FASCO” · Home · Shop · Products · Pages · “Copyright © 2022 FASCO. All Rights Reserved.”
• Gallery: Photo_Denim_Jacket_Blue_2 (main) · thumbnails Photo_Denim_Jacket_Lilac, Photo_Denim_Jacket_Blue_1, Photo_Denim_Jacket_Blue_2, Photo_Denim_Jacket_Blue_3, Photo_Denim_Jacket_Black_1, Photo_Denim_Jacket_Black_2
• Header: “FASCO” wordmark · navigation Home / Shop / Products / Pages · current: Products · search (Icon_Search) · account (Icon_Account) · wishlist (Icon_Star) · cart (Icon_Cart)
• Newsletter: “Subscribe To Our Newsletter” · copy (see DATA) · email field “michael@example.com” · “Subscribe Now” · Photo_Subscribe_Left · Photo_Subscribe_Right
• Options: “Size: M” · M · L · XL · XXL · selected: M · “Color: Blue” · Blue · Black · Lilac · selected: Blue
• People Also Loved: “People Also Loved” · copy (see DATA) · “Buy Now” · “Hurry, Before It’s Too Late!” · countdown 02 Days · 06 Hr · 05 Mins · 30 Sec · deal slides Photo_Deal_1, Photo_Deal_2, Photo_Deal_3 · current slide card “01 — Spring Sale” · “30% OFF” · previous / next (Icon_Chevron_Left, Icon_Chevron_Right) · slide indicator: 4 slides, current 1
• Purchase: “Quantity” − 1 + · “Add to cart”
• Summary: “FASCO” · “Denim Jacket” · rating (Icon_Star) · (3) · $39.00 · old $59.00 · “Save 33%”
• Urgency: “24 people are viewing this right now” (Icon_Eye) · “Hurry up! Sale ends in:” 00 : 05 : 59 : 47 · “Only 9 item(s) left in stock!” with stock level

• Behind the drawer: the 03_Product page, inactive; header cart shows count 1
• Mini cart: “Shopping Cart” · close (Icon_Close) · “Buy $36.00 more and get Free Shipping” with progress toward free shipping · item Photo_Denim_Jacket_Blue_2 · “Denim Jacket” · “Color : Blue” · $39.00 · quantity − 01 + · checkbox “For $10.00 please wrap the product” (unchecked) · “Subtotal” $39.00 · “Checkout” · “View Cart”

LINKS

→ View Cart → 05_Cart
→ Checkout → 06_Checkout
→ close → 03_Product

LINKS

→ Add to cart → 04_Mini_Cart
→ Shop (nav) → 02_Shop
→ cart (header) → 05_Cart

05_Cart

06_Checkout

Goal: Review the cart before checking out.

Goal: Enter contact, delivery and payment details and pay.

MUST INCLUDE

MUST INCLUDE

• Cart table: columns Product · Price · Quantity · Total · row Photo_Denim_Jacket_Blue_2 · “Denim Jacket” · “Color : Blue” · “Remove” · $39.00 · − 01 + · $39.00
• Cart total: checkbox “For $10.00 please wrap the product” (unchecked) · “Subtotal” $39.00 · “Checkout”
• Footer: “FASCO” · Home · Shop · Products · Pages · “Copyright © 2022 FASCO. All Rights Reserved.”
• Header: “FASCO” wordmark · navigation Home / Shop / Products / Pages · no item current · search (Icon_Search) · account (Icon_Account) · wishlist (Icon_Star) · cart (Icon_Cart) with count 1
• Newsletter: “Subscribe To Our Newsletter” · copy (see DATA) · email field “michael@example.com” · “Subscribe Now” · Photo_Subscribe_Left · Photo_Subscribe_Right
• Page title: “Shopping Cart” · breadcrumb Home › Your Shopping Cart (Icon_Chevron_Right)

• Contact: “Contact” · “Don’t have an account? Create Account” · Email Address
• Delivery: “Delivery” · Country / Region (Icon_Chevron_Down) · First Name · Last Name · Address · City · Postal Code · checkbox “Save This Info for future”
• Footer: “FASCO” · Home · Shop · Products · Pages · “Copyright © 2022 FASCO. All Rights Reserved.”
• Header: “FASCO” wordmark · navigation Home / Shop / Products / Pages · no item current · search (Icon_Search) · account (Icon_Account) · wishlist (Icon_Star) · cart (Icon_Cart) with count 1
• Newsletter: “Subscribe To Our Newsletter” · copy (see DATA) · email field “michael@example.com” · “Subscribe Now” · Photo_Subscribe_Left · Photo_Subscribe_Right
• Order summary: Photo_Denim_Jacket_Blue_2 with quantity 1 · “Denim Jacket” · Blue · $39.00 · “Discount code” · “Apply” · Subtotal $39.00 · Shipping $40.00 · Total $79.00
• Page title: “FASCO Checkout”
• Payment: “Payment” · “Credit Card” · Card Number (Icon_Lock) · Expiration Date · Security Code · Card Holder Name · checkbox “Save This Info for future” · “Pay Now”

LINKS

→ Checkout → 06_Checkout
→ Denim Jacket → 03_Product

LINKS

→ Create Account → 07_Sign_Up
→ Pay Now → entry only (no frame)

07_Sign_Up

08_Sign_In

Goal: Create a FASCO account.

Goal: Sign in to FASCO.

MUST INCLUDE

MUST INCLUDE

• Card: “FASCO” wordmark · “FASCO Terms & Conditions”
• Form: “Create Account” · First Name · Last Name · Email Address · Phone Number · Password · Confirm Password · “Create Account” · “Already have an account? Login”
• Media: Photo_Sign_Up
• Social sign-up: “Sign up with Google” (Logo_Google) · “Sign up with Email” (Logo_Gmail) · “OR”

• Card: “FASCO” wordmark · “FASCO Terms & Conditions”
• Form: “Sign In To FASCO” · Email · Password · “Sign In” · “Register Now” · “Forgot Password?”
• Media: Photo_Sign_In
• Social sign-in: “Sign in with Google” (Logo_Google) · “Sign in with Email” (Logo_Gmail) · “OR”

LINKS

LINKS

→ Create Account → 01_Home
→ Login → 08_Sign_In

→ Sign In → 01_Home
→ Register Now → 07_Sign_Up
→ Forgot Password? → 09_Forgot_Password

09_Forgot_Password

10_Confirmation_Code

Goal: Request a confirmation code to recover the account.

Goal: Enter the code that was e-mailed.

MUST INCLUDE

MUST INCLUDE

• Card: “FASCO” wordmark · “FASCO Terms & Conditions”
• Form: “Forgot Password” · First Name · Last Name · Email Address · Phone Number · “Send Confirmation Code” · “Already have an account? Login”
• Media: Photo_Sign_In

• Card: “FASCO” wordmark · “FASCO Terms & Conditions”
• Form: “Enter The Confirmation Code” · Confirmation Code · “Recover Account” · “Didn’t receive Confirmation Code? Resend Now”
• Media: Photo_Sign_In

LINKS

LINKS

→ Send Confirmation Code → 10_Confirmation_Code
→ Login → 08_Sign_In

→ Recover Account → 11_New_Password

11_New_Password

Goal: Set a new password.

MUST INCLUDE

• Card: “FASCO” wordmark · “FASCO Terms & Conditions”
• Form: “Enter Your New Password” · New Password · Confirm Password · “Submit”
• Media: Photo_Sign_In

LINKS

→ Submit → 01_Home

Navigation structure

• Two headers, as in the source: the home header on 01 (Home / Deals / New Arrivals / Packages, Sign in, Sign Up; current: Home) and the store header on 02–06 (Home / Shop / Products / Pages, then search, account, wishlist, cart; current: Shop on 02, Products on 03–04, none on 05–06; the cart shows count 1 on 04–06). How the current item looks is yours.
• Footer variants: the home footer on 01, the store footer on 02–06. 07–11 are full-screen sign-in pages without header and footer.
• Shopping flow: 01 SHOP NOW → 02_Shop → product card → 03_Product → Add to cart opens 04_Mini_Cart over the product page → View Cart → 05_Cart → Checkout → 06_Checkout (Checkout in the mini cart also goes straight to 06).
• Account flow: Sign Up → 07 → Create Account → 01 · Sign in → 08 → Sign In → 01 · Forgot Password? → 09 → Send Confirmation Code → 10 → Recover Account → 11 → Submit → 01. Store header account → 08, cart → 05.
• Entry only (no frame): Deals, New Arrivals, Packages, Products, Pages, search, wishlist, Buy Now, slide arrows, category tabs, filters, sort, view options, pagination, size / color / quantity, Compare, Ask a question, Share, gift wrap, Remove, Discount code, Pay Now, social sign-in buttons, Resend Now, Subscribe Now, footer links.

Fixed data & copy

Use these values verbatim.

Home copy

Collection banner (01, 02, 03)

New Arrivals cards (01, in order)

Deals Of The Month: Hand-picked styles at their best prices this month — once the timer runs out, the deals are gone.
New Arrivals: Fresh pieces just landed: easy dresses, cosy knits and everyday shirts for the new season.
Instagram: Tag @fasco to be featured — real outfits from our community, styled your way.
Testimonials: Real reviews from people who shop with FASCO.
Newsletter: Be the first to hear about new arrivals, exclusive deals and styling tips. No spam — unsubscribe anytime.

Men Collection · Classic Gentleman
Item labels: Flat Cap · Cotton Shirt · Suspender · Leather Shoes
DESCRIPTION: A sharp, vintage-inspired look built around a wool flat cap, a crisp cotton shirt and classic suspenders. Easy to dress up or down, and made to last for years.
Size: M · $100.00 · Buy Now

Shiny Dress (Photo_Shiny_Dress) · Long Dress (Photo_Long_Dress) · Full Sweater (Photo_Full_Sweater) · White Dress (Photo_White_Dress) · Colorful Dress (Photo_Colorful_Dress) · White Shirt (Photo_White_Shirt)
Each: brand FASCO · 5-star rating · (4.1k) Customer Reviews · $95.50 · Almost Sold Out

Testimonials (01, in order)

People Also Loved (03)

Shop products (02, in order)

Suzan B. · UI Designer (Avatar_Suzan_B) — “The items I ordered were the best investment I ever made. I can’t say enough about your quality service.”
James K. · Traveler (Avatar_James_K) — “You won’t regret it. I would like to personally thank you for your outstanding product. Absolutely wonderful!”
Megen W. · UI Designer (Avatar_Megen_W) — “Just what I was looking for. Thank you for making it painless, pleasant and, most of all, hassle-free! All products are great.”
All: 5-star rating

Copy: Shoppers who looked at this jacket also loved these deals — grab them before the timer runs out.
Slides, countdown and card as in Deals Of The Month.

Rounded Red Hat · $8.00 (Photo_Rounded_Red_Hat)
Linen-blend Shirt · $17.00 · Sold Out (Photo_Linen_Blend_Shirt)
Long-sleeve Coat · $106.00 (Photo_Long_Sleeve_Coat)
Boxy Denim Hat · $25.00 (Photo_Boxy_Denim_Hat)
Linen Plain Top · $25.00 (Photo_Linen_Plain_Top)
Oversized T-shirt · $11.00 · old $14.00 (Photo_Oversized_TShirt)
Polarised Sunglasses · $18.00 · old $21.00 (Photo_Polarised_Sunglasses)
Rockstar Jacket · $22.00 (Photo_Rockstar_Jacket)
Dotted Black Dress · $20.00 (Photo_Dotted_Black_Dress)

Denim Jacket (03–06)

Cart & checkout totals

Features strip

Brand FASCO · rating with (3) reviews · $39.00 · old $59.00 · Save 33%
Sizes M · L · XL · XXL (selected M) · Colors Blue · Black · Lilac (selected Blue)
Quantity 1 · 24 people are viewing this right now · Sale ends in 00 : 05 : 59 : 47 · Only 9 item(s) left in stock!
Estimated Delivery: Jul 30 - Aug 03 · Free Shipping & Returns: On all orders over $75

Cart (04, 05): Denim Jacket · Color : Blue · 1 × $39.00 · Subtotal $39.00 · Buy $36.00 more and get Free Shipping · gift wrap “For $10.00 please wrap the product” unchecked
Checkout (06): Subtotal $39.00 · Shipping $40.00 · Total $79.00

High Quality · crafted from top materials (Icon_Trophy)
Warranty Protection · Over 2 years (Icon_Guarantee)
Free Shipping · Order over $75 (Icon_Shipping)
24 / 7 Support · Dedicated support (Icon_Support)

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #000000, Volkhov and Poppins
• Media: photos, avatars, sign-in logos, icons
• Default Button, default Text Field

• Layout, grid, grouping, order and emphasis on every page
• All other colors: neutrals, text, backgrounds / surfaces, sale and discount, rating, stock / urgency, links, error / disabled
• Type scale (which levels use Volkhov), spacing, radii, elevation
• All states: current nav item, current tab, current slide, selected size / color / view, sold out, checked, focused field, current page, cart count
• Headers, footers, hero collage, brand strip, countdown, deal slider, tabs, product cards, collection banner, feature strip, Instagram strip, testimonial cards, newsletter, filters, gallery, pickers, stepper, mini cart, cart table, checkout form, order summary, auth cards
• How photos are cropped and placed

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current nav, tabs, selected options, sold out, cart count)

Deliverable: the link to your own Figma file containing the 11 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · FASCO

Fixed: the brand color and the two typefaces below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces, sale / discount color, rating color, stock and urgency colors, link and selected states, error / disabled, type scale, spacing, radii, elevation and the page grid.

Brand color

Brand primary · black

#000000

The store’s main ink and action color. Where and how much to use it is your decision.

Typefaces

Volkhov — Aa Bb Cc  New Arrivals

Poppins — Aa Bb Cc 0123456789  $39.00

Use Volkhov for the FASCO wordmark and headings, Poppins for all other UI text. Which levels use which typeface, sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: desktop web, 1920 wide. Light mode. Frame heights are free — store pages scroll vertically; the sign-in pages are one screen (1920 × 1080).
