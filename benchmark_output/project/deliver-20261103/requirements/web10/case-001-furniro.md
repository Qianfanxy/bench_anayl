# Furniro（web10 / case-001）

- 原始模板（只读）：https://www.figma.com/design/2Q0GuFJHXWFV6nKJTChfBz/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/2Q0GuFJHXWFV6nKJTChfBz/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Furniro — furniture store website

Design a furniture e-commerce website: browse the range, open a product, add it to the cart, compare two sofas, check out, contact the store and read the blog. Desktop web, 1440 wide, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 9 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in page order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii, elevation and the page grid, and apply them consistently.
4. 02 · Components gives only a default Button and a default Text Field. Design all other states, the header, the footer, the navigation and every business component as reusable components in your file.
5. Use the logo, the photos, the social logos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Home

02_Shop

Goal: Get a feel for the store and find products.

Goal: Browse the full catalog.

MUST INCLUDE

MUST INCLUDE

• Browse The Range: “Browse The Range” · “Find the right pieces for every room in your home.” · Dining · Living · Bedroom, each with its photo (Photo_Range_Dining, Photo_Range_Living, Photo_Range_Bedroom)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · current: Home · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Hero: Photo_Hero · “New Arrival” · “Discover Our New Collection” · “Handcrafted sofas, chairs and tables for every room — explore our latest arrivals.” · “BUY NOW”
• Inspiration: “50+ Beautiful rooms inspiration” · “Our designers have already made many beautiful room prototypes to inspire you.” · “Explore More” · room slides Photo_Inspiration_Inner_Peace, Photo_Inspiration_2, Photo_Inspiration_3 · current slide: “01 — Bed Room” · “Inner Peace” · open (Icon_Arrow_Right) · next (Icon_Chevron_Right) · slide indicator: 4 slides, current 1
• Our Products: “Our Products” · 8 product cards, each with photo, name, description, price, old price and badge where given (see DATA) · “Show More”
• Product card hover: the Leviosa card is shown in its hover state with “Add to cart” · Share (Icon_Share) · Compare (Icon_Compare) · Like (Icon_Heart)
• Share your setup: “Share your setup with” · “#FurniroFurniture” · Photo_Setup_1 – Photo_Setup_9

• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · current: Shop · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Page title: Photo_Page_Banner · “Shop” · breadcrumb Home › Shop (Icon_Chevron_Right)
• Pagination: 1 · 2 · 3 · “Next” · current: 1
• Products: 16 product cards — the 8 products of DATA, then the same 8 again; the first Leviosa card is in its hover state (“Add to cart” · Share · Compare · Like)
• Toolbar: Filter (Icon_Filter) · grid view (Icon_Grid) · list view (Icon_View_List) · current view: grid · “Showing 1–16 of 32 results” · “Show” 16 · “Sort by” Default (Icon_Chevron_Down)

LINKS

→ any product card → 03_Product
→ Compare (hover card) → 05_Comparison
→ Home (nav or breadcrumb) → 01_Home
→ cart (header) → 06_Cart

LINKS

→ Shop (nav), BUY NOW, Show More → 02_Shop
→ any product card → 03_Product
→ Compare (hover card) → 05_Comparison
→ cart (header) → 06_Cart
→ Contact (nav) → 08_Contact

03_Product

04_Cart_Drawer

Goal: Decide on the Asgaard sofa and add it to the cart.

Goal: Confirm what was just added and move on.

MUST INCLUDE

MUST INCLUDE

• Breadcrumb: Home › Shop › Asgaard sofa (Icon_Chevron_Right)
• Description tabs: Description · Additional Information · Reviews [204] · current: Description · description text (see DATA) · Photo_Cloud_Sofa_1 · Photo_Cloud_Sofa_2
• Footer: see DATA (Footer)
• Gallery: Photo_Asgaard_Sofa (main) · thumbnails Photo_Outdoor_Sofa_Set, Photo_Outdoor_Sofa_Set_Alt, Photo_Stuart_Sofa, Photo_Maya_Sofa
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · current: Shop · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Meta: SKU SS001 · Category Sofas · Tags Sofa, Chair, Home, Shop · Share Logo_Facebook, Logo_LinkedIn, Logo_Twitter
• Options: Size L · XL · XS · selected: L · Color purple · black · gold (see DATA)
• Purchase: quantity − 1 + · “Add To Cart” · “+ Compare”
• Rating: 4.7 (Icon_Star, Icon_Star_Half) · “204 Customer Reviews”
• Related Products: “Related Products” · Syltherine · Leviosa · Lolito · Respira cards · “Show More”
• Summary: “Asgaard sofa” · Rs. 250,000.00 · short description (see DATA)

• Behind the drawer: the 03_Product page, inactive
• Cart drawer: “Shopping Cart” · close (Icon_Cart_Close) · item Photo_Asgaard_Sofa · “Asgaard sofa” · 1 × Rs. 250,000.00 · remove (Icon_Remove) · “Subtotal” Rs. 250,000.00
• Drawer actions: “Cart” · “Checkout” · “Comparison”

LINKS

→ Cart → 06_Cart
→ Checkout → 07_Checkout
→ Comparison → 05_Comparison
→ close → 03_Product

LINKS

→ Add To Cart → 04_Cart_Drawer
→ + Compare → 05_Comparison
→ Shop (breadcrumb) → 02_Shop
→ related product cards → 03_Product

05_Comparison

06_Cart

Goal: Compare two sofas side by side.

Goal: Review the cart before checking out.

MUST INCLUDE

MUST INCLUDE

• Add a product: “Add A Product” · “Choose a Product” (Icon_Chevron_Down)
• Compared products: Asgaard Sofa · Outdoor Sofa Set, each with photo, price, rating (Icon_Star) and review count (see DATA)
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · no item current · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Intro: “Go to Product page for more Products” · “View More”
• Page title: Photo_Page_Banner · “Product Comparison” · breadcrumb Home › Comparison (Icon_Chevron_Right)
• Specifications: groups General · Product · Dimensions · Warranty, one value per product on every row (see DATA) · “Add To Cart” under each product

• Cart table: columns Product · Price · Quantity · Subtotal · row Photo_Asgaard_Sofa · Asgaard sofa · Rs. 250,000.00 · 1 · Rs. 250,000.00 · remove (Icon_Delete)
• Cart Totals: “Cart Totals” · Subtotal Rs. 250,000.00 · Total Rs. 250,000.00 · “Check Out”
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · no item current · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Page title: Photo_Page_Banner · “Cart” · breadcrumb Home › Cart (Icon_Chevron_Right)

LINKS

→ Check Out → 07_Checkout
→ Asgaard sofa → 03_Product

LINKS

→ View More → 02_Shop
→ Add To Cart → 06_Cart

07_Checkout

08_Contact

Goal: Enter billing details and place the order.

Goal: Find the store’s details and send a message.

MUST INCLUDE

MUST INCLUDE

• Billing details: “Billing details” · First Name · Last Name · Company Name (Optional) · Country / Region: Sri Lanka (Icon_Chevron_Down) · Street address · Town / City · Province: Western Province (Icon_Chevron_Down) · ZIP code · Phone · Email address · Additional information
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · no item current · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Order summary: Product · Subtotal · Asgaard sofa × 1 · Rs. 250,000.00 · Subtotal Rs. 250,000.00 · Total Rs. 250,000.00
• Page title: Photo_Page_Banner · “Checkout” · breadcrumb Home › Checkout (Icon_Chevron_Right)
• Payment: Direct Bank Transfer · Cash On Delivery · selected: Direct Bank Transfer, with its note (see DATA)
• Place order: privacy note with link “privacy policy” (see DATA) · “Place order”

• Contact details: Address (Icon_Location) · Phone (Icon_Phone) · Working Time (Icon_Clock), each with its value (see DATA)
• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Form: Your name (placeholder “Abc”) · Email address (“Abc@def.com”) · Subject (“This is optional”) · Message (“Hi! I’d like to ask about”) · “Submit”
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · current: Contact · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Intro: “Get In Touch With Us” · intro copy (see DATA)
• Page title: Photo_Page_Banner · “Contact” · breadcrumb Home › Contact (Icon_Chevron_Right)

LINKS

→ Home (nav or breadcrumb) → 01_Home

LINKS

→ Place order → entry only (no frame)

09_Blog

Goal: Browse the store’s blog posts.

MUST INCLUDE

• Features: High Quality · Warranty Protection · Free Shipping · 24 / 7 Support, each with icon and line (see DATA)
• Footer: see DATA (Footer)
• Header: Logo_Furniro · “Furniro” · navigation Home / Shop / About / Contact · no item current · account (Icon_Account) · search (Icon_Search) · wishlist (Icon_Heart) · cart (Icon_Cart)
• Page title: Photo_Page_Banner · “Blog” · breadcrumb Home › Blog (Icon_Chevron_Right)
• Pagination: 1 · 2 · 3 · “Next” · current: 1
• Posts: 3 posts, each with photo, author Admin (Icon_User), date (Icon_Calendar), category (Icon_Tag), title, excerpt and “Read more” (see DATA)
• Sidebar: search (Icon_Search) · “Categories” with post counts · “Recent Posts” with thumbnail, title and date (see DATA)

LINKS

→ Home (nav or breadcrumb) → 01_Home

Navigation structure

• Site header on all 9 frames: Logo_Furniro + “Furniro”, then Home / Shop / About / Contact, then account, search, wishlist and cart. Current: Home on 01, Shop on 02–04, Contact on 08, none on 05, 06, 07 and 09. How the current item looks is yours.
• Footer on all 9 frames. Feature strip (High Quality, Warranty Protection, Free Shipping, 24 / 7 Support) on 02 and 05–09. Page title with breadcrumb on 02 and 05–09; 03 and 04 show the breadcrumb Home › Shop › Asgaard sofa.
• Main flow: 01_Home → 02_Shop → 03_Product → Add To Cart opens 04_Cart_Drawer over the product page → Cart → 06_Cart → Check Out → 07_Checkout. Compare (hover card, + Compare, drawer Comparison) → 05_Comparison. Header cart → 06_Cart. Contact → 08_Contact.
• 09_Blog: the source has no entry point to the blog — link it from wherever you see fit (e.g. the footer).
• Entry only (no frame): About, account, search, wishlist, Explore More, slide arrows, range tiles, Add to cart / Share / Like on cards, Filter, view toggles, Show, Sort by, pagination, size, color, quantity, social share, description tabs, Choose a Product, all form fields, Place order, Submit, Subscribe, Read more, categories, recent posts.

Fixed data & copy

Use these values verbatim.

Products (cards, in this order)

Asgaard sofa (03)

Asgaard copy (03)

Syltherine · Stylish cafe chair · Rs. 2,500,000.00 · old Rs. 3,500,000.00 · badge -30% (Photo_Product_Syltherine)
Leviosa · Stylish cafe chair · Rs. 2,500,000.00 (Photo_Product_Leviosa)
Lolito · Luxury big sofa · Rs. 7,000,000.00 · old Rs. 14,000,000.00 · badge -50% (Photo_Product_Lolito)
Respira · Outdoor bar table and stool · Rs. 500,000.00 · badge New (Photo_Product_Respira)
Grifo · Night lamp · Rs. 1,500,000.00 (Photo_Product_Grifo)
Muggo · Small mug · Rs. 150,000.00 · badge New (Photo_Product_Muggo)
Pingky · Cute bed set · Rs. 7,000,000.00 · old Rs. 14,000,000.00 · badge -50% (Photo_Product_Pingky)
Potty · Minimalist flower pot · Rs. 500,000.00 · badge New (Photo_Product_Potty)

Rs. 250,000.00 · rating 4.7 · 204 Customer Reviews · Reviews [204]
Size: L · XL · XS (selected L)
Color: purple #816DFA · black #000000 · gold #B88E2F
SKU SS001 · Category Sofas · Tags Sofa, Chair, Home, Shop

Short: Setting the bar as one of the most comfortable sofas in its class, the Asgaard is a compact, sturdy three-seater with a solid-wood frame and deep, soft cushions.
Description ¶1: Embodying the relaxed, honest spirit of Scandinavian design, the Asgaard pairs a solid-wood frame with soft, hard-wearing upholstery, built to be lived on every day.
Description ¶2: Weighing in at 45 kg, the Asgaard is sturdy without being bulky. Its high-density foam cushions keep their shape, the removable covers are easy to care for, and the low, clean silhouette fits a small apartment as comfortably as a large living room.

Cart (04, 06, 07)

Comparison (05) · products

Comparison (05) · General / Product

Asgaard sofa · 1 × Rs. 250,000.00 (Photo_Asgaard_Sofa)
Subtotal Rs. 250,000.00 · Total Rs. 250,000.00

Asgaard Sofa · Rs. 250,000.00 · 4.7 · 204 Review (Photo_Asgaard_Sofa)
Outdoor Sofa Set · Rs. 224,000.00 · 4.2 · 145 Review (Photo_Outdoor_Sofa_Set)

Values: Asgaard Sofa | Outdoor Sofa Set
General
Sales Package: 1 sectional sofa | 1 Three Seater, 2 Single Seater
Model Number: TFCBLIGRBL6SRHS | DTUBLIGRBL568
Secondary Material: Solid Wood | Solid Wood
Configuration: L-shaped | L-shaped
Upholstery Material: Fabric + Cotton | Fabric + Cotton
Upholstery Color: Bright Grey & Lion | Bright Grey & Lion
Product
Filling Material: Foam | Foam
Finish Type: Matte | Matte
Adjustable Headrest: No | Yes
Maximum Load Capacity: 280 KG | 300 KG
Origin of Manufacture: India | India

Comparison (05) · Dimensions / Warranty

Checkout (07)

Contact (08)

Dimensions
Width: 265.32 cm | 265.32 cm
Height: 76 cm | 76 cm
Depth: 167.76 cm | 167.76 cm
Weight: 45 KG | 65 KG
Seat Height: 41.52 cm | 41.52 cm
Leg Height: 5.46 cm | 5.46 cm
Warranty
Warranty Summary: 1 Year Manufacturing Warranty | 1.2 Year Manufacturing Warranty
Warranty Service Type: For Warranty Claims or Any Product Related Issues Please Email at operations@furniro.example | … at support@furniro.example
Covered in Warranty: Warranty Against Manufacturing Defect | Warranty of the product is limited to manufacturing defects only.
Not Covered in Warranty (both): The Warranty Does Not Cover Damages Due To Usage Of The Product Beyond Its Intended Use And Wear & Tear In The Natural Course Of Product Usage.
Domestic Warranty: 1 Year | 3 Months

Country / Region: Sri Lanka · Province: Western Province
Direct Bank Transfer note: Make your payment directly into our bank account. Please use your Order ID as the payment reference. Your order will not be shipped until the funds have cleared in our account.
Privacy note: Your personal data will be used to support your experience throughout this website, to manage access to your account, and for other purposes described in our privacy policy.

Intro: For more information about our products & services, please feel free to drop us an email. Our staff will always be there to help you out. Do not hesitate!
Address: 236 5th SE Avenue, New York NY10000, United States
Phone: Mobile: +(84) 546-6789 · Hotline: +(84) 456-6789
Working Time: Monday–Friday: 9:00 – 22:00 · Saturday–Sunday: 9:00 – 21:00

Blog posts (09, in this order)

Blog sidebar (09)

Features strip

All by Admin · 14 Oct 2022
1. Going all-in with millennial design · Wood (Photo_Blog_1) — Soft pastels, rounded silhouettes and natural wood: how millennial design took over the living room, and how to make it feel personal rather than borrowed from a feed.
2. Exploring new ways of decorating · Handmade (Photo_Blog_2) — Moving one lamp can change a whole room. Simple ways to refresh your space with what you already own, plus a few handmade pieces that add character.
3. Handmade pieces that took time to make · Wood (Photo_Blog_3) — From hand-turned legs to woven seats: meet the makers behind some of our favourite pieces and learn why slow craftsmanship lasts longer.

Categories: Crafts 2 · Design 8 · Handmade 7 · Interior 1 · Wood 6
Recent Posts (all 03 Aug 2022): Going all-in with millennial design (Photo_Recent_1) · Exploring new ways of decorating (Photo_Recent_2) · Handmade pieces that took time to make (Photo_Recent_3) · Modern home in Milan (Photo_Recent_4) · Colorful office redesign (Photo_Recent_5)

High Quality · crafted from top materials (Icon_Trophy)
Warranty Protection · Over 2 years (Icon_Guarantee)
Free Shipping · Order over Rs. 150,000 (Icon_Shipping)
24 / 7 Support · Dedicated support (Icon_Support)

Footer (all frames)

“Furniro.” · 400 University Drive Suite 200, Coral Gables, FL 33134 USA
Links: Home · Shop · About · Contact
Help: Payment Options · Returns · Privacy Policies
Newsletter: “Enter Your Email Address” · “SUBSCRIBE”
“2023 Furniro. All rights reserved”

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #B88E2F and Poppins
• Media: logo, photos, social logos, icons
• Default Button, default Text Field

• Layout, grid, grouping, order and emphasis on every page
• All other colors: neutrals, text, backgrounds / section tints, badges (sale, new), rating, links, error / disabled
• Type scale, spacing, radii, elevation
• All states: current nav item, card hover, selected size, current tab, current page, selected payment, current slide, focused field
• Header, footer, page title & breadcrumb, product card, toolbar, pagination, gallery, option pickers, stepper, tabs, comparison table, cart table, drawer, order summary, forms, blog card, sidebar widgets, feature strip
• How photos are cropped and placed

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current nav, card hover, selected options, current tab and page)

Deliverable: the link to your own Figma file containing the 9 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Furniro

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (including any tinted section backgrounds), sale / new badge colors, rating color, link and selected states, error / disabled, type scale, spacing, radii, elevation and the page grid.

Brand color

Brand primary · gold

#B88E2F

The store’s signature accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  Rs. 250,000.00

Use Poppins for all UI text. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: desktop web, 1440 wide. Light mode. Frame heights are free — every page scrolls vertically.
