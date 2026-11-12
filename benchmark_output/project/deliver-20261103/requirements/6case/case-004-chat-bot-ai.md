# Chat Bot AI（6case / case-004）

- 原始模板（只读）：https://www.figma.com/design/98KpwcDyXWGwrmTcr6QziU/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/98KpwcDyXWGwrmTcr6QziU/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Chat Bot AI — AI assistant app

Design the complete Chat Bot AI mobile app: Sam Rivera logs in, browses past chats, generated images and PDF exports, starts a new chat, continues a conversation that ends with a generated image, exports it as PDF, and manages profile, theme and cloud storage.
Canvas 428 × 928, light mode only. Home, the conversation and Cloud Space may scroll vertically. Today is Dec 30, 2023. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 12 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color and the typefaces in 01 · Foundations are fixed. Define every other color yourself (neutrals, text, surfaces, success / warning / error / disabled, storage-breakdown colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, sheets, dialogs, message bubbles and every business component as reusable components in your file.
5. Use the logo, generated images, PDF icon and icons from 04 · Media. People have no photos: use Avatar_Neutral or initials.
6. Copy and data must match “Fixed data” exactly. Long answers may be cut off where the frame ends; everything listed must still be visible. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Login

02_Home_Chats

Goal: Sign in to the account.

Goal: Find a past conversation or start a new one.

MUST INCLUDE

MUST INCLUDE

• Actions: Forgot Password? · Login · “Don’t have an account?” Sign Up
• Brand: logo
• Copy: “Login to your account”
• Form: Email “sam.rivera@example.com” · Password entered (masked, can be shown or hidden)
• Legal: Terms of use · Privacy policy
• Social sign-in: “Or login with” · Facebook · Google

• Account: avatar (profile entry) · back
• Actions: New Topic
• Chats: 7 chats, newest first, each with question, answer preview and time · the 3-days-ago chat shows its generated image (DATA)
• Copy: “Start a new chat with Chat Bot AI” · logo
• History: “History” · search “Search ...”
• View: Chats / Archived / Images / Exports · current: Chats

LINKS

LINKS

→ Login → 02_Home_Chats

→ New Topic → 05_Chat_New
→ chat “Tell me the story…” → 06_Chat_Conversation
→ Images → 03 · Exports → 04
→ avatar → 08_Profile_Settings

03_Home_Images

04_Home_Exports

Goal: Browse every image the assistant generated.

Goal: Find a PDF export.

MUST INCLUDE

MUST INCLUDE

• Account: same as 02
• Actions: New Topic
• Copy: same as 02
• History: same as 02
• Images: 8 generated images (DATA)
• View: same switch as 02 · current: Images

• Account: same as 02
• Actions: New Topic
• Copy: same as 02
• Exports: 7 PDF files, newest first, each with PDF icon, title, date and size (DATA)
• History: same as 02
• View: same switch as 02 · current: Exports

LINKS

LINKS

→ Chats → 02 · Exports → 04
→ New Topic → 05_Chat_New

→ Chats → 02 · Images → 03
→ New Topic → 05_Chat_New

05_Chat_New

06_Chat_Conversation

Goal: Start a conversation from a blank chat.

Goal: Read the conversation and act on messages.

MUST INCLUDE

MUST INCLUDE

• Actions: menu · export · send
• Assistant: logo · “Chat Bot AI 4.5” · “Premium account”
• Copy: “How can I help you my friend? 😊”
• Input: “Ask me anything...” (empty)
• Suggestions: 4 prompts, each with title and detail (DATA)

• Actions: menu · export · send
• Assistant: logo · “Chat Bot AI 4.5” · “Premium account”
• Input: “Ask me anything...” (empty)
• Messages: 4 messages in this order — You · Chat Bot AI · You · Chat Bot AI (DATA) · each sender identified
• Message actions: on your messages Edit · Copy; on the story Copy · Share · Regenerate; on the image Download · Share · Regenerate

LINKS

→ menu → 02_Home_Chats

LINKS

→ menu → 02_Home_Chats
→ export → 07_Export_PDF_Sheet

07_Export_PDF_Sheet

08_Profile_Settings

Goal: Name and export the conversation as PDF.

Goal: Check the account and reach settings.

MUST INCLUDE

MUST INCLUDE

• Actions: close · Export
• Copy: “Export as PDF” · “All your conversations with Chat Bot AI will be exported as PDF. Please choose a title for this file”
• Form: Title “The story of a student”
• Media: PDF_File_Icon
• Presentation: sheet over 06_Chat_Conversation; the conversation stays behind it

• Account: avatar · Sam Rivera · “premium account” · “278 days until the end of the premium account”
• Actions: back · more
• Copy: “Profile & Settings”
• Footer: “Chat Bot AI - Version 2.0.5” · Terms of use · Privacy policy
• Settings: Change password · Data & storage “83% Used” · Email sam.rivera@example.com · Send feedback (“Chat Bot AI can make mistakes. Consider checking important information and send us your feedback”) · Theme “System default”

LINKS

→ close → 06 · Export → 06

LINKS

→ back → 02_Home_Chats
→ more → 09_Account_Actions_Sheet
→ Theme → 10_Theme_Sheet
→ Data & storage → 11_Cloud_Space

09_Account_Actions_Sheet

10_Theme_Sheet

Goal: Leave or remove the account.

Goal: Choose the app theme.

MUST INCLUDE

MUST INCLUDE

• Actions: Delete Account · Sign out
• Presentation: sheet over 08_Profile_Settings; Profile stays behind it

• Options: Dark mode · Light mode · System default · only one can be chosen · current: System default
• Presentation: sheet over 08_Profile_Settings; Profile stays behind it

LINKS

LINKS

→ Sign out → 01_Login
→ tap outside → 08

→ tap outside → 08

11_Cloud_Space

12_Clear_Cache_Dialog

Goal: See what uses storage and free some up.

Goal: Confirm clearing the cache.

MUST INCLUDE

MUST INCLUDE

• Actions: back · more
• Clear cache: “Clear cache” · 238.05 MB
• Copy: “Cloud Space”
• Delete all chats: “Delete all chats” · 12.48 GB · “Warning! By deleting all chats, all photos, conversations and documents will be lost and cannot be recovered!”
• Exports: “Exports” · 37 items · 506 MB · note (DATA) · latest 3 exports, each with title, date, size and delete
• Footer: same as 08
• Images: “Images” · 169 items · 8,225 MB · note (DATA) · 7 thumbnails
• Usage: “12.48 GB of 15 GB used” · Chats 25% · Images 55% · Exports 3%

• Actions: Cancel · Delete
• Copy: “Clear cache” · “You are requesting to delete a cache with a size of 238.05 MB. Are you sure about your request?”
• Presentation: dialog over 11_Cloud_Space; Cloud Space stays behind it

LINKS

→ Cancel → 11 · Delete → 11

LINKS

→ back → 08_Profile_Settings
→ Clear cache → 12_Clear_Cache_Dialog

Navigation structure

• Entry: 01_Login → 02_Home_Chats.
• Home has four views of one screen, switched in place: Chats (02), Archived (entry only), Images (03), Exports (04). All share the same header (back, avatar, “Start a new chat with Chat Bot AI”, New Topic, History search).
• Chat: New Topic → 05_Chat_New; a chat → 06_Chat_Conversation; export → 07 (sheet over 06). Menu on 05 / 06 returns to 02.
• Account: avatar → 08_Profile_Settings; more → 09 (sheet); Theme → 10 (sheet); Data & storage → 11_Cloud_Space; Clear cache → 12 (dialog over 11).
• There is no tab bar.
• Entry only (no screen required): Archived, Search, Forgot Password?, Sign Up, social sign-in, suggestions, Edit, Copy, Share, Regenerate, Download, Change password, Send feedback, Delete Account, Delete all chats, export delete, Terms of use, Privacy policy.
• Do not add frames beyond the 12.

Fixed data & copy

Use these values verbatim. Message and preview texts below are complete; how much of a long answer is visible is your decision.

User

Chats (newest first)

Sam Rivera · sam.rivera@example.com · premium account · 278 days left · avatar = Avatar_Neutral · Theme: System default · Data & storage 83% Used

1. “How can I forget a bad memory?” — “Forgetting a bad memory entirely may be challenging, as memories are complex and deeply ingrained in the brain. However, there are strategies you can use to cope with and reduce the impact of negative memories.” — 28 mins ago
2. “Tell me the story of a student who was going to school and some interesting things happened to her on the way.” — “I’ll try to create that. Here is the image I generated based on your description. I hope you like it. 😊” + Gen_Student — 3 days ago
3. “What can I do to increase concentration while studying?” — “Improving concentration while studying involves adopting effective study habits, creating a conducive environment, and taking care of your overall well-being.” — 12 days ago
4. “What do you know about the French Revolution?” — “The French Revolution was a period of radical social and political change in France that lasted from 1789 to 1799.” — 16 days ago
5. “Who is Pope Francis?” — “As of my last knowledge update in January 2022, Pope Francis, born Jorge Mario Bergoglio, is the head of the Roman Catholic Church.” — 17 days ago
6. “How to get more followers on Instagram?” — “Increasing your followers on Instagram requires a combination of strategies to engage with your audience and attract new followers.” — 20 days ago
7. “Tell me about the latest trends in fashion design” — “As of my last knowledge update in January 2022, I can provide some general trends that were prevalent in fashion design.” — 2 months ago

Images (03)

Exports (newest first)

8 images in this order: Gen_Mug · Gen_Rat · Gen_Statue · Gen_Student · Gen_Statue · Gen_Mug · Gen_Rat · Gen_Student

How can I forget a bad memory? · DEC 30, 2023 · 2.16 MB
How to get more followers on Instagram? · DEC 16, 2023 · 158 KB
Pope Francis · DEC 05, 2023 · 4.62 MB
The effects of morning exercise on the body · NOV 04, 2023 · 75 KB
New methods of advertising in Instagram · SEP 24, 2023 · 492 KB
Saffron export business · SEP 08, 2023 · 169 KB
The best cologne brands · AUG 16, 2023 · 27 KB

New chat suggestions

Conversation (06)

Brainstorm names — for my fantasy football team with a frog theme
Suggest some codenames — for a project introducing flexible work arrangements
Write a SQL query — that adds a “status” column to an “orders” table
Explain why popcorn pops — to a kid who loves watching it in the microwave

You: “Tell me the story of a student who was going to school and some interesting things happened to her on the way.”
Chat Bot AI: the story “Once upon a time, in the quaint town of Meadowville, there lived a spirited high school student named Lily…” (full text: Story_Text in 04 · Media)
You: “What a beautiful story it was! Imagine a student going to school. She has purple hair and shoes. Also, her hat and clothes are yellow and she wears glasses. She has a phone in her left hand.”
Chat Bot AI: “I’ll try to create that. Here is the image I generated based on your description. I hope you like it. 😊” + Gen_Student

Cloud Space (11)

Login

12.48 GB of 15 GB used · Chats 25% · Images 55% · Exports 3%
Images · 169 Item · 8,225 MB · “These Images are in the cache and by deleting them, the original file will not be lost. You can download the image again by going to the relevant topic” · thumbnails Gen_Mug, Gen_Rat, Gen_Statue, Gen_Student, Gen_Mug, Gen_Rat, Gen_Statue
Exports · 37 Item · 506 MB · “The following PDFs cannot be recovered after deletion. But you can get the PDF output again by going to the relevant chat.” · latest 3: How can I forget a bad memory? DEC 30, 2023 2.16 MB · Pope Francis DEC 05, 2023 4.62 MB · The effects of morning exercise on the body NOV 04, 2023 75 KB
Clear cache 238.05 MB · Delete all chats 12.48 GB

Email sam.rivera@example.com · Password masked (8 characters) · “Login to your account” · “Don’t have an account? Sign Up” · “Or login with” Google / Facebook · Terms of use | Privacy policy

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand primary color + Bricolage Grotesque and Nunito
• Media: logo, generated images, PDF icon, icons, neutral avatar
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, semantic and storage-breakdown colors
• Type scale, spacing, radii, elevation
• All states: selected view and theme, pressed, disabled, focused, destructive
• Headers, message bubbles, chat list items, sheets, dialogs and all business components
• How storage usage is visualised

How it is evaluated

Your file is compared with the brief on coverage, data and flow — not on visual similarity to any reference.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current view and theme, sender of each message, sheets and dialogs over their parent, destructive actions)

Deliverable: the link to your own Figma file containing the 12 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Chat Bot AI

Fixed: the brand primary color and the two typefaces below — they carry the Chat Bot AI identity. Everything else is yours to define and apply consistently: neutrals and grays, text colors, surfaces and backgrounds, semantic colors (success, warning, error, disabled), storage-breakdown colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary

#612A74

The Chat Bot AI brand color. Where and how much to use it is your decision.

Typefaces

Bricolage Grotesque

Nunito  Aa Bb Cc 0123456789  12.48 GB

Bricolage Grotesque comes from the source kit. Nunito replaces SF Pro Rounded (Apple-only, not available on every machine). Which face, size, weight and line height goes where is yours to define as a consistent type scale.

Canvas: 428 × 928 (iPhone). Light mode only.
