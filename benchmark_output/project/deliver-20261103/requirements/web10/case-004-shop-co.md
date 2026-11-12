# Shop.co（web10 / case-004）

- 原始模板（只读）：https://www.figma.com/design/O3xqX7yz6SWQNetHEC6PTm/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/O3xqX7yz6SWQNetHEC6PTm/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

SHOP.CO — fashion store website

Design a fashion e-commerce website: discover new arrivals and best sellers, filter a category, review a product and its customer reviews, and check the cart. Desktop web, 1440 wide, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 4 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in page order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the two typefaces in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii, elevation and the page grid, and apply them consistently.
4. 02 · Components gives only a default Button and a default Text Field. Design all other states, the header, the footer, the navigation and every business component as reusable components in your file.
5. Use the photos, the social and payment logos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Home

02_Category

Goal: Get inspired and find something to buy.

Goal: Filter the Casual category and pick a product.

MUST INCLUDE

MUST INCLUDE

• Announcement bar: “Sign up and get 20% off to your first order.” · “Sign Up Now” · close (Icon_Close)
• Brands: NORDE · ATELIER K · MONVALE · RIVA · CASSEL (as wordmarks)
• Browse by dress style: “BROWSE BY DRESS STYLE” · Casual · Formal · Party · Gym, each with its photo (Photo_Style_Casual, Photo_Style_Formal, Photo_Style_Party, Photo_Style_Gym)
• Customer reviews: “OUR HAPPY CUSTOMERS” · previous / next (Icon_Arrow_Left, Icon_Arrow_Right) · 3 review cards with 5-star rating, name, verified mark (Icon_Verified) and quote (see DATA)
• Footer: see DATA (Footer)
• Header: “SHOP.CO” wordmark · navigation Shop (Icon_Chevron_Down) / On Sale / New Arrivals / Brands · no item current · search field “Search for products...” (Icon_Search) · cart (Icon_Cart) · account (Icon_Account)
• Hero: “FIND CLOTHES THAT MATCH YOUR STYLE” · copy (see DATA) · “Shop Now” · stats 200+ International Brands · 2,000+ High-Quality Products · 30,000+ Happy Customers · Photo_Hero · two Icon_Sparkle
• New Arrivals: “NEW ARRIVALS” · 4 product cards, each with photo, name, rating (Icon_Star, Icon_Star_Half) with score, price, and old price + discount where given (see DATA) · “View All”
• Newsletter: “STAY UP TO DATE ABOUT OUR LATEST OFFERS” · email field “Enter your email address” · “Subscribe to Newsletter”
• Top Selling: “TOP SELLING” · 4 product cards, each with photo, name, rating (Icon_Star, Icon_Star_Half) with score, price, and old price + discount where given (see DATA) · “View All”

• Announcement bar: “Sign up and get 20% off to your first order.” · “Sign Up Now” · close (Icon_Close)
• Breadcrumb: Home › Casual (Icon_Chevron_Right)
• Filters: “Filters” (Icon_Filter) · T-shirts · Shorts · Shirts · Hoodie · Jeans (Icon_Chevron_Right) · “Price” range $50 – $200 · “Colors” 10 swatches (see DATA) · selected: blue (Icon_Check) · “Size” XX-Small · X-Small · Small · Medium · Large · X-Large · XX-Large · 3X-Large · 4X-Large · selected: Large · “Dress Style” Casual · Formal · Party · Gym (Icon_Chevron_Right) · “Apply Filter”
• Footer: see DATA (Footer)
• Header: “SHOP.CO” wordmark · navigation Shop (Icon_Chevron_Down) / On Sale / New Arrivals / Brands · current: Shop · search field “Search for products...” (Icon_Search) · cart (Icon_Cart) · account (Icon_Account)
• Newsletter: “STAY UP TO DATE ABOUT OUR LATEST OFFERS” · email field “Enter your email address” · “Subscribe to Newsletter”
• Pagination: “Previous” (Icon_Arrow_Left) · 1 · 2 · 3 · … · 8 · 9 · 10 · “Next” (Icon_Arrow_Right) · current: 1
• Products: 9 product cards, each with photo, name, rating (Icon_Star, Icon_Star_Half) with score, price, and old price + discount where given (see DATA)
• Results header: “Casual” · “Showing 1-9 of 100 Products” · “Sort by: Most Popular” (Icon_Chevron_Down)

LINKS

→ any product card → 03_Product
→ Home (breadcrumb) → 01_Home
→ cart (header) → 04_Cart

LINKS

→ Shop Now, View All, Casual tile → 02_Category
→ any product card → 03_Product
→ cart (header) → 04_Cart

03_Product

04_Cart

Goal: Choose color and size, read reviews and add the T-shirt to the cart.

Goal: Review the cart and its order summary.

MUST INCLUDE

MUST INCLUDE

• Announcement bar: “Sign up and get 20% off to your first order.” · “Sign Up Now” · close (Icon_Close)
• Breadcrumb: Home › Shop › Men › T-shirts (Icon_Chevron_Right)
• Footer: see DATA (Footer)
• Gallery: Photo_One_Life_TShirt_1 (main) · thumbnails Photo_One_Life_TShirt_1, Photo_One_Life_TShirt_2, Photo_One_Life_TShirt_3 · selected: the first
• Header: “SHOP.CO” wordmark · navigation Shop (Icon_Chevron_Down) / On Sale / New Arrivals / Brands · current: Shop · search field “Search for products...” (Icon_Search) · cart (Icon_Cart) · account (Icon_Account)
• Newsletter: “STAY UP TO DATE ABOUT OUR LATEST OFFERS” · email field “Enter your email address” · “Subscribe to Newsletter”
• Options: “Select Colors” olive · teal · navy (see DATA) · selected: olive (Icon_Check) · “Choose Size” Small · Medium · Large · X-Large · selected: Large
• Purchase: quantity − 1 + (Icon_Minus, Icon_Plus) · “Add to Cart”
• Reviews: “All Reviews” (451) · filter (Icon_Filter) · sort “Latest” (Icon_Chevron_Down) · “Write a Review” · 6 review cards with rating, name, verified mark (Icon_Verified), more (Icon_More), quote and post date (see DATA) · “Load More Reviews”
• Summary: “ONE LIFE GRAPHIC T-SHIRT” · rating 4.5/5 (Icon_Star, Icon_Star_Half) · $260 · old $300 · -13% · description (see DATA)
• Tabs: Product Details · Rating & Reviews · FAQs · current: Rating & Reviews
• You might also like: “YOU MIGHT ALSO LIKE” · 4 product cards, each with photo, name, rating (Icon_Star, Icon_Star_Half) with score, price, and old price + discount where given (see DATA)

• Announcement bar: “Sign up and get 20% off to your first order.” · “Sign Up Now” · close (Icon_Close)
• Breadcrumb: Home › Cart (Icon_Chevron_Right)
• Cart items: 3 line items, each with photo, name, size, color, price, quantity − 1 + (Icon_Minus, Icon_Plus) and remove (Icon_Trash) (see DATA)
• Footer: see DATA (Footer)
• Header: “SHOP.CO” wordmark · navigation Shop (Icon_Chevron_Down) / On Sale / New Arrivals / Brands · no item current · search field “Search for products...” (Icon_Search) · cart (Icon_Cart) · account (Icon_Account)
• Newsletter: “STAY UP TO DATE ABOUT OUR LATEST OFFERS” · email field “Enter your email address” · “Subscribe to Newsletter”
• Order Summary: “Order Summary” · Subtotal $565 · Discount (-20%) -$113 · Delivery Fee $15 · Total $467 · promo field “Add promo code” (Icon_Tag) · “Apply” · “Go to Checkout” (Icon_Arrow_Right)
• Title: “YOUR CART”

LINKS

→ Go to Checkout → entry only (no frame)
→ Home (breadcrumb) → 01_Home
→ item → 03_Product

LINKS

→ Add to Cart → 04_Cart
→ Shop (breadcrumb) → 02_Category
→ product cards → 03_Product

Navigation structure

• Announcement bar, header, newsletter block and footer on all 4 frames. Header current: Shop on 02 and 03, none on 01 and 04. How the current item looks is yours.
• Flow: 01_Home → Shop Now / View All / Casual tile → 02_Category → product card → 03_Product → Add to Cart → 04_Cart. Header cart → 04_Cart from any frame. Product cards on any frame open 03_Product (the product page template, shown for One Life Graphic T-shirt).
• Entry only (no frame): Sign Up Now, close bar, On Sale, New Arrivals, Brands, search, account, review arrows, Formal / Party / Gym tiles, filter options, Apply Filter, sort, pagination, gallery thumbnails, color / size / quantity, tabs, Write a Review, Load More Reviews, remove, promo code, Go to Checkout, Subscribe, footer links.

Fixed data & copy

Use these values verbatim.

Hero (01)

New Arrivals (01, in order)

Top Selling (01, in order)

FIND CLOTHES THAT MATCH YOUR STYLE
Browse through our diverse range of meticulously crafted garments, designed to bring out your individuality and cater to your sense of style.
Shop Now · 200+ International Brands · 2,000+ High-Quality Products · 30,000+ Happy Customers

T-shirt with Tape Details · 4.5/5 · $120 (Photo_TShirt_Tape_Details)
Skinny Fit Jeans · 3.5/5 · $240 · old $260 · -20% (Photo_Skinny_Fit_Jeans)
Checkered Shirt · 4.5/5 · $180 (Photo_Checkered_Shirt)
Sleeve Striped T-shirt · 4.5/5 · $130 · old $160 · -30% (Photo_Sleeve_Striped_TShirt)

Vertical Striped Shirt · 5.0/5 · $212 · old $232 · -20% (Photo_Vertical_Striped_Shirt)
Courage Graphic T-shirt · 4.0/5 · $145 (Photo_Courage_Graphic_TShirt)
Loose Fit Bermuda Shorts · 3.0/5 · $80 (Photo_Loose_Fit_Bermuda_Shorts)
Faded Skinny Jeans · 4.5/5 · $210 (Photo_Faded_Skinny_Jeans)

Happy customers (01, in order; all 5 stars, verified)

Casual products (02, in order)

One Life Graphic T-shirt (03)

Sarah M. — “I’m blown away by the quality and style of the clothes I received from Shop.co. From casual wear to elegant dresses, every piece I’ve bought has exceeded my expectations.”
Alex K. — “Finding clothes that align with my personal style used to be a challenge until I discovered Shop.co. The range of options they offer is truly remarkable, catering to a variety of tastes and occasions.”
James L. — “As someone who’s always on the lookout for unique fashion pieces, I’m thrilled to have stumbled upon Shop.co. The selection of clothes is not only diverse but also on-point with the latest trends.”

Gradient Graphic T-shirt · 3.5/5 · $145 (Photo_Gradient_Graphic_TShirt)
Polo with Tipping Details · 4.5/5 · $180 (Photo_Polo_Tipping_Details)
Black Striped T-shirt · 5.0/5 · $120 · old $150 · -30% (Photo_Black_Striped_TShirt)
Skinny Fit Jeans · 3.5/5 · $240 · old $260 · -20%
Checkered Shirt · 4.5/5 · $180
Sleeve Striped T-shirt · 4.5/5 · $130 · old $160 · -30%
Vertical Striped Shirt · 5.0/5 · $212 · old $232 · -20%
Courage Graphic T-shirt · 4.0/5 · $145
Loose Fit Bermuda Shorts · 3.0/5 · $80
Color swatches: green #00C12B · red #F50606 · yellow #F5DD06 · orange #F57906 · cyan #06CAF5 · blue #063AF5 (selected) · purple #7D06F5 · pink #F506A4 · white #FFFFFF · black #000000

Rating 4.5/5 · $260 · old $300 · -13%
Description: This graphic t-shirt is perfect for any occasion. Crafted from a soft and breathable fabric, it offers superior comfort and style.
Colors: olive #4F4631 (selected) · teal #314F4A · navy #31344F
Sizes: Small · Medium · Large (selected) · X-Large · Quantity 1

Reviews (03, in order; all verified)

You might also like (03, in order)

Cart (04, in order)

Samantha D. · 4.5 — “I absolutely love this t-shirt! The design is unique and the fabric feels so comfortable. As a fellow designer, I appreciate the attention to detail. It’s become my favorite go-to shirt.” · Posted on August 14, 2023
Alex M. · 4 — “The t-shirt exceeded my expectations! The colors are vibrant and the print quality is top-notch. Being a UI/UX designer myself, I’m quite picky about aesthetics, and this t-shirt definitely gets a thumbs up from me.” · Posted on August 15, 2023
Ethan R. · 3.5 — “This t-shirt is a must-have for anyone who appreciates good design. The minimalistic yet stylish pattern caught my eye, and the fit is perfect. I can see the designer’s touch in every aspect of this shirt.” · Posted on August 16, 2023
Olivia P. · 4 — “As a UI/UX enthusiast, I value simplicity and functionality. This t-shirt not only represents those principles but also feels great to wear. It’s evident that the designer poured their creativity into making this t-shirt stand out.” · Posted on August 17, 2023
Liam K. · 4 — “This t-shirt is a fusion of comfort and creativity. The fabric is soft, and the design speaks volumes about the designer’s skill. It’s like wearing a piece of art that reflects my passion for both design and fashion.” · Posted on August 18, 2023
Ava H. · 4.5 — “I’m not just wearing a t-shirt; I’m wearing a piece of design philosophy. The intricate details and thoughtful layout of the design make this shirt a conversation starter.” · Posted on August 19, 2023

Polo with Contrast Trims · 4.0/5 · $212 · old $242 · -20% (Photo_Polo_Contrast_Trims)
Gradient Graphic T-shirt · 3.5/5 · $145
Polo with Tipping Details · 4.5/5 · $180
Black Striped T-shirt · 5.0/5 · $120 · old $150 · -30%

Gradient Graphic T-shirt · Size: Large · Color: White · $145 · qty 1 (Photo_Gradient_Graphic_TShirt)
Checkered Shirt · Size: Medium · Color: Red · $180 · qty 1 (Photo_Checkered_Shirt)
Skinny Fit Jeans · Size: Large · Color: Blue · $240 · qty 1 (Photo_Skinny_Fit_Jeans)
Subtotal $565 · Discount (-20%) -$113 · Delivery Fee $15 · Total $467

Footer (all frames)

SHOP.CO · We have clothes that suit your style and which you’re proud to wear. From women to men.
Logo_Twitter · Logo_Facebook · Logo_Instagram · Logo_GitHub
COMPANY: About · Features · Works · Career
HELP: Customer Support · Delivery Details · Terms & Conditions · Privacy Policy
FAQ: Account · Manage Deliveries · Orders · Payments
RESOURCES: Free eBooks · Development Tutorial · How to - Blog · Youtube Playlist
Shop.co © 2000-2023, All Rights Reserved · Logo_Visa · Logo_Mastercard · Logo_PayPal · Logo_Apple_Pay · Logo_Google_Pay

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #000000, Archivo Black and Plus Jakarta Sans
• Media: photos, social and payment logos, icons
• Default Button, default Text Field

• Layout, grid, grouping, order and emphasis on every page
• All other colors: neutrals, text, backgrounds / surfaces (hero, cards, newsletter), discount, rating, verified mark, error / disabled
• Type scale (letter case, which levels use Archivo Black), spacing, radii, elevation
• All states: current nav item, selected color / size / thumbnail, current tab, current page, checked filter, focused field, hover
• Announcement bar, header, footer, hero, stats, brand strip, product card, style tiles, review card, newsletter, filter panel, price range, chips, pagination, gallery, pickers, stepper, tabs, review list, cart line item, order summary
• How photos are cropped and placed

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current nav, selected options, current tab and page)

Deliverable: the link to your own Figma file containing the 4 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · SHOP.CO

Fixed: the brand color and the two typefaces below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (including the hero and card backgrounds), discount color, rating color, verified mark, link and selected states, error / disabled, type scale, spacing, radii, elevation and the page grid.

Brand color

Brand primary · black

#000000

The store’s main ink and action color. Where and how much to use it is your decision.

Typefaces

ARCHIVO BLACK — NEW ARRIVALS

Plus Jakarta Sans — Aa Bb Cc 0123456789  $260

Use Archivo Black for the SHOP.CO wordmark and display headings, Plus Jakarta Sans for all other UI text. Which levels use which typeface, sizes, weights, letter case and line heights are yours to define as a consistent type scale.

Canvas: desktop web, 1440 wide. Light mode. Frame heights are free — every page scrolls vertically.
