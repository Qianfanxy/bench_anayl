# Meet（10case / case-004）

- 原始模板（只读）：https://www.figma.com/design/gpHSfBEIfxme0n5JVF5ENT/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/gpHSfBEIfxme0n5JVF5ENT/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Meet — dating and social app

Design Meet, a dating and social app: sign in, browse stories and posts on Explore, decide on suggested partners, visit a friend’s profile and watch a short, and manage your own profile from its menu. Canvas 393 × 852, iPhone, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 8 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The two brand colors and the typeface in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, backgrounds and surfaces including any tint or gradient, overlays on photos, online / active, like, error / disabled), plus type scale, spacing, radii, blur and elevation, and apply them consistently.
4. 02 · Components gives only a default Button and the platform shell (status bar, home indicator). Design all other states, the headers, the tab bar, the tabs, the sheet, the drawer and every business component as reusable components in your file.
5. Use the photos, logo and icons from 04 · Media. Each person always uses their own portrait.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Welcome

02_Apple_ID_Sheet

Goal: Choose how to get started.

Goal: Confirm signing in with an Apple ID.

MUST INCLUDE

MUST INCLUDE

• Actions: “Continue with Facebook” (Icon_Facebook) · “Continue with Google” (Icon_Google) · “Use mobile number” · “Sign Up”
• Copy: “Don’t have an account?” · headline “Let’s meet new people around you”
• Media: Portrait_Sarah_Payne with a heart (Icon_Heart) · Portrait_Henry · Portrait_Lucie · Portrait_Marry · Portrait_Pierre

• Actions: close (Icon_Close) · Face ID (Icon_Face_ID)
• App: Logo_Meet
• Copy: “Apple ID” · “Do you want to sign in to Meet Dating App: Meet People with your Apple ID “sarahp@example.com”?” · “Face ID”
• Presentation: sheet over 01_Welcome

LINKS

LINKS

→ Sign Up → 02_Apple_ID_Sheet

→ Face ID → 03_Explore
→ close → 01_Welcome

03_Explore

04_Find_Partner

Goal: Catch up on stories and posts from people.

Goal: Decide on the next suggested partner.

MUST INCLUDE

MUST INCLUDE

• Actions: “Make Friends” · “Search Partners”
• Feed: Noemi Slater · Yu Jian · Maddison Burke posts, each with portrait, name, photo and like (Icon_Like) / comment (Icon_Chat) / more (Icon_More) (see DATA)
• Header: “Explore” · notifications (Icon_Bell)
• Main navigation: tab bar Home / Dating / Add / Chat / Profile · current: Home
• Stories: “Your Story” with add (Icon_Plus) · Ben · Lucie · Marry · Claire · Lina · Jo · Henry · Pierre, each with portrait and first name

• Actions: like (Icon_Heart) · pass (Icon_Close) · super like (Icon_Star)
• Card stack: top card John, 27 · San Francisco (Icon_Location) · 20 km away · Active Now (Portrait_John); 5 more cards behind it (see DATA)
• Header: back (Icon_Back) · “Find your partner”
• Main navigation: tab bar · current: Dating

LINKS

→ back / Home tab → 03_Explore
→ Profile tab → 07_Profile

LINKS

→ Claire (story) → 05_Friend_Profile
→ Dating tab → 04_Find_Partner
→ Profile tab → 07_Profile

05_Friend_Profile

06_Short_Video

Goal: See who Claire is and connect.

Goal: Watch a short and react to it.

MUST INCLUDE

MUST INCLUDE

• Actions: “Follow” · “Message”
• Header: back (Icon_Back) · “Claire Smith” · more (Icon_More)
• Main navigation: tab bar · current: Home
• Media grid: Claire_01 – Claire_09 (01 and 09 are videos, Icon_Play)
• Profile: Portrait_Claire_Smith · “63K Followers”
• Tabs: Top · Recent · Short · current: Top

• Actions: like 123 (Icon_Heart) · comment 89 (Icon_Chat) · share (Icon_Send) · more (Icon_More)
• Author: Portrait_Yu_Jian · “Yu Jian” · “Follow”
• Caption: “I think I’m in love with you” · “Liked by Harrison Pearce and others” · music “Nothing Can Stop Me! · Jperriel” (Icon_Music) · “4 people” (Icon_Person)
• Header: back (Icon_Back) · “Short” · camera (Icon_Camera)
• Main navigation: tab bar · current: Home
• Media: Short_Yu_Jian_Shore, full-screen video

LINKS

→ back → 03_Explore
→ Short (tab) → 06_Short_Video

LINKS

→ back → 05_Friend_Profile

07_Profile

08_Menu

Goal: See and manage my own profile.

Goal: Reach account areas from the profile.

MUST INCLUDE

MUST INCLUDE

• Actions: “Edit Profile” · “Share Profile”
• Header: menu (Icon_Menu) · “Sarah Payne”
• Main navigation: tab bar · current: Profile
• Media grid: Sarah_01 – Sarah_09 (01 is a video, Icon_Play)
• Profile: Portrait_Sarah_Payne · “103K Followers”
• Tabs: Top · Recent · Short · current: Top

• Account: Portrait_Sarah_Payne · “Sarah Payne” · “Show Profile” · close (Icon_Close)
• App: Logo_Meet
• Menu: Archive · Close Friends · Discover people · Favorites · Group profiles · Saved · Setting · Your Activity, each with its icon and Icon_Chevron_Right (source order in DATA)
• Presentation: drawer over 07_Profile

LINKS

LINKS

→ close / Show Profile → 07_Profile

→ menu → 08_Menu
→ Home tab → 03_Explore

Navigation structure

• Sign-in flow: 01_Welcome → Sign Up → 02_Apple_ID_Sheet (sheet over 01) → Face ID → 03_Explore.
• Bottom tab bar on 03–07 with 5 tabs in this order: Home (Icon_Home), Dating (Icon_Heart), Add (Icon_Plus), Chat (Icon_Chat), Profile (Portrait_Sarah_Payne). Current: Home on 03, 05 and 06; Dating on 04; Profile on 07. How the current tab looks is yours.
• 05 and 06 are pushed from Explore (Claire’s story → her profile → its Short tab → the short). 08_Menu is a drawer over 07_Profile.
• Entry only (no frame): Continue with Facebook / Google, Use mobile number, notifications, Make Friends, Search Partners, other stories, feed actions, Your Story, like / pass / super like, Follow, Message, more, Top / Recent tabs, grid items, short actions, camera, Edit Profile, Share Profile, menu rows, Add, Chat.

Fixed data & copy

Use these values verbatim.

Me

Stories (in this order)

Feed posts (portrait · photo)

Sarah Payne · 103K Followers · Portrait_Sarah_Payne
Apple ID: sarahp@example.com

Your Story (Portrait_Sarah_Payne) · Ben · Lucie · Marry · Claire · Lina · Jo · Henry · Pierre (Portrait_<name>; Claire = Portrait_Claire_Smith)

Noemi Slater (Portrait_Noemi_Slater · Post_Noemi_Slater)
Yu Jian (Portrait_Yu_Jian · Post_Yu_Jian)
Maddison Burke (Portrait_Maddison_Burke · Post_Maddison_Burke)

Partner cards (top to bottom of the stack)

Friend profile

Short video

John, 27 · San Francisco · 20 km away · Active Now (Portrait_John)
Dan, 28 · Fremont · 12 km away · Active Now (Portrait_Dan)
Aidan, 25 · San Ramon · 20 km away · Active Now (Portrait_Aidan)
William, 24 · Stockton · 40 km away · Active Now (Portrait_William)
Keven, 24 · Los Angeles · 560 km away · Active Now (Portrait_Keven)
Kalvin, 23 · Los Angeles · 560 km away · Active Now (Portrait_Kalvin)

Claire Smith · 63K Followers · Portrait_Claire_Smith
Grid: Claire_01_Video_Ocean, Claire_02 – Claire_08, Claire_09_Video_Reef

Yu Jian · “I think I’m in love with you”
Liked by Harrison Pearce and others
Nothing Can Stop Me! · Jperriel · 4 people
Likes 123 · Comments 89

My profile grid

Menu (source order)

Sarah_01_Video_Wave, Sarah_02 – Sarah_09

Setting (Icon_Settings) · Your Activity (Icon_Activity) · Archive (Icon_Archive) · Saved (Icon_Saved) · Close Friends (Icon_Close_Friends) · Favorites (Icon_Star) · Group profiles (Icon_Group) · Discover people (Icon_Discover)

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand colors #4B164C + #DD88CF and Inter
• Media: portraits, posts, profile grids, logo, icons
• Default Button, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, backgrounds / surfaces (tints, gradients), overlays on photos, online / active, like, error / disabled
• Type scale, spacing, radii, blur, elevation
• All states: current tab, current profile tab, pressed, followed / liked, disabled
• Headers, tab bar, tabs, story avatars, feed post, swipe card stack, action buttons, profile header, media grid, short-video overlay, sign-in sheet, drawer and menu rows
• How photos are cropped and treated

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, current profile tab, top card of the stack, sheet / drawer presentation)

Deliverable: the link to your own Figma file containing the 8 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Meet

Fixed: the two brand colors and the typeface below — they carry Meet’s identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, backgrounds and surfaces (including any tint or gradient), overlays on photos, semantic colors (online / active, like, error, disabled), type scale, weights per role, spacing, radii, blur and elevation.

Brand colors

Brand primary · plum

Brand secondary · orchid pink

#4B164C

#DD88CF

Meet’s main brand color (the “M” of the logo). Where and how much to use it is your decision.

The second brand color, Meet’s accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  John, 27  103K Followers

Use Inter for all UI text (Regular / Medium / Semi Bold / Bold / Extra Bold available; it replaces the source’s SF Pro, which is not available). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 393 × 852 (iPhone 15). Light mode only. 03_Explore, 05_Friend_Profile and 07_Profile may scroll vertically.
