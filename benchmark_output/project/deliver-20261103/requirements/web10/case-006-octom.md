# Octom（web10 / case-006）

- 原始模板（只读）：https://www.figma.com/design/ZTk0l7k9c4VHhZoZHocGuw/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/ZTk0l7k9c4VHhZoZHocGuw/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

OCTOM — team task management web app

Design a team task-management web app: see today’s overview, plan the project timeline, move tasks on a board, manage files, edit your profile and chat with the team. Desktop web app, 1440 × 1024, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 6 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in page order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand color and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii, elevation and the page grid, and apply them consistently.
4. 02 · Components gives only a default Button and a default Text Field. Design all other states, the header, the footer, the navigation and every business component as reusable components in your file.
5. Use the logo, the avatars, the photos and the icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Dashboard

02_Timeline

Goal: See today’s workload, schedule and messages at a glance.

Goal: Plan the project phases on a day-by-day timeline.

MUST INCLUDE

MUST INCLUDE

• Messages: “Messages” · 4 conversations, each with avatar, name and last message (see DATA)
• New Task: “New Task” · more (Icon_More) · “Task Title” · field “Create new” · emoji row 🎉 😍 😁 🔥 😘 😉 😎 👩 🙄 · “Add Collaborators” · chips Angela · Chris (each with an avatar) · add (Icon_Plus) · send (Icon_Send)
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Dashboard
• Stats: Task Completed 08 · New Task 10 · Project Done 10, each with icon, trend line and change “10+ more / 10+ more / 08+ more from last week”
• Task Done: “Task Done” · Daily · Weekly · Monthly · current: Monthly · line chart with two series, y axis 0 – 400, months May – Apr (values illustrative)
• Tasks: “Task” · 2 task rows, each with play (Icon_Play), “Start from” and time (Icon_Clock), title, link (Icon_Link), comments (Icon_Comment), progress and “Reminder” (Icon_Bell) (see DATA)
• Today’s Schedule: “Today’s Schedule” · “30 minute call with Client” · “+ Invite” · “Project Discovery Call” · 3 participant avatars + initials “R” · timer 28:35 · call (Icon_Phone)
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

• Bars: 11 task bars on the timeline, each with label and percent (see DATA)
• Complete Task: “Complete Task” · line chart of 7 points 67 · 73 · 53 · 47 · 39 · 27 · 27 · highlighted point: the last
• Day scale: S 04 … S 21 (18 consecutive days)
• Header: “Timeline” · “Today” · previous (Icon_Chevron_Left) · “June 20, 2022” · next (Icon_Chevron_Right) · “+ Invite” · team avatars with +5
• Phases: UX Research · Information Architecture · Design Phase (Build Wireframe, User Interface Design) · Prototyping · Development (Back-End Development, Front-End Development), each phase with member avatars and more (Icon_More)
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Timeline
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

LINKS

→ sidebar icons → other frames

LINKS

→ sidebar icons → 02_Timeline, 03_Task_Board, 05_Settings, 06_Messages, 04_Files
→ a message → 06_Messages

03_Task_Board

04_Files

Goal: Track tasks across the four board columns and chat with the group.

Goal: Find a folder or a recent file and check storage.

MUST INCLUDE

MUST INCLUDE

• Board: columns Backlog · To Do · In Progress · Review, each with more (Icon_More) and add (Icon_Plus) · 12 task cards (see DATA)
• Group chat: “Group Chat” · messages from members (avatar) and from you (see DATA) · voice message 1:25 (Icon_Play) · input “write here...” (Icon_Mic, Icon_Send)
• Header: “🔥 Task” · team avatars with +6 · add (Icon_Plus)
• Members: “Member (25)” · “View All” · member avatars
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Task
• Task card: tag · title · “Create content for peceland App” · date (Icon_Calendar) · 3 member avatars · checklist 0/8 (Icon_Checklist) or “4 Comment” (Icon_Comment) · “11 file” (Icon_Attachment) · cover photo where given
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

• Activity Chart: “Activity Chart” · bar chart with legend Media · Photos · Docs (values illustrative)
• All Files: “All Files” · “Show All” (Icon_Chevron_Down) · 6 folders (Icon_Folder), each with name, file count and member chips (see DATA)
• Available Storage: “Available Storage” · 27% · “140GB / 512GB” · Media 86 GB · Documents 26 GB · Music 10 GB · Other File 18 GB, each with icon and usage bar
• Header: “Files” · “+ Create New Folder” · “Upload” (Icon_Upload)
• Recent Files: “Recent Files” · “View All” · table Name · Size · Last Modified · Members, sortable (Icon_Arrow_Up) · 4 rows with file icon (Icon_File), member avatars and more (Icon_More_Vertical) (see DATA)
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Files
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

LINKS

LINKS

→ sidebar icons → other frames

→ sidebar icons → other frames

05_Settings

06_Messages

Goal: Update your personal details.

Goal: Read and reply in the Design Team conversation.

MUST INCLUDE

MUST INCLUDE

• Form: First name “Dristin” · Last name “Watson” · Email “dristin.watson@example.com” (Icon_Mail) · photo upload “Click to upload or drag and drop” · “SVG, PNG, JPG or GIF (max. 800x400px)” (Icon_Upload_Cloud) · Role “Product Designer”
• Profile header: Photo_Gradient_Blue (cover) · Avatar_Current_User · “Settings” · “Cancel” · “Save”
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Settings
• Tabs: My details · Profile · Password · Team · Plan · Billing · Email · Notifications · current: My details
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

• Contact panel: Avatar_Killan_James · “Killan James” · “@killanjames” · “Attachments” 4 files (Icon_File) with size and date · “View all” · “Members” · “+ Add Member” · Novita · Milie Nose · Ikhsan SD · Aditya with avatars (see DATA)
• Conversation list: “Messages” · search “Search...” (Icon_Search) · 3 pinned conversations · “All Messages” · 5 conversations, each with avatar, name, time, last message and unread count where given · current: Design Team (see DATA)
• Conversation: header Avatar_Design_Team · “Design Team” · “60 members, 10 online” · member avatars · add (Icon_Plus) · messages and day divider (see DATA) · composer “Add a comment...” (Icon_Mic, Icon_Emoji, Icon_Image, Icon_Attachment, Icon_Send)
• Sidebar: Logo_Octom · “OCTOM.” · icon navigation Dashboard (Icon_Nav_Dashboard) · Timeline (Icon_Nav_Timeline) · Task (Icon_Nav_Task) · Settings (Icon_Nav_Settings) · Messages (Icon_Nav_Messages) · Files (Icon_Nav_Files) · current: Messages
• Top bar: search field “Search anything...” (Icon_Search) · notifications (Icon_Bell) with count 2 · Avatar_Current_User · account menu (Icon_Chevron_Down)

LINKS

→ sidebar icons → other frames

LINKS

→ sidebar icons → other frames

Navigation structure

• Sidebar and top bar on all 6 frames. The sidebar is icon-only in this order: Dashboard → 01, Timeline → 02, Task → 03, Settings → 05, Messages → 06, Files → 04. Current item as listed on each frame; how it looks is yours.
• From 01_Dashboard, a message row opens 06_Messages.
• Entry only (no frame): search, notifications, account menu, chart period tabs, play / reminder, invite, call, emoji, collaborators, date navigation, phases, bars, column actions, cards, group chat, create folder, upload, folders, file rows, storage, tabs other than My details, Cancel / Save, conversations other than Design Team, attachments, add member, composer actions.

Fixed data & copy

Use these values verbatim.

Dashboard (01)

Timeline bars (02, by phase)

Task board · Backlog / To Do (03)

Messages: Cris Morich — Hi Dristin! How are you? (Avatar_Cris_Morich) · Charmie — Do you need that design? (Avatar_Charmie) · Jason Mandala — What is the price of hourly... (Avatar_Jason_Mandala) · Charlie Chu — Awesome design!! (Avatar_Charlie_Chu)
Task 1: Search Inspiration for project · Start from 9.00 am · inspiration.example.com · 8 comments · 24% complete
Task 2: Search Inspiration for project · Start from 3.00 am · moodboard.example.org · 5 comments · 60% complete

UX Research: Profile 48% · Menu 54% · Settings 39%
Information Architecture: Login 48% · Services 54%
Build Wireframe: Testimonials 69%
User Interface Design: Menu 61% · Homepage 48%
Prototyping: Our Portfolio 63%
Development: Profile 48%
Front-End Development: Services 54%

Backlog: Design · Create styleguide foundation · Aug 20, 2021 · 0/8 · cover Photo_Gradient_Blue | Research · Copywriting Content · Aug 20, 2021 · 0/8 | Planning · Update requirement list · Sep 20, 2021 · 4 Comment · 11 file
To Do: Research · Auditing information architecture · Aug 20, 2021 · 0/8 | Content · Update support documentation · Aug 16, 2021 · 0/8 · cover Photo_Gradient_Glass | Research · Qualitative research planning · Aug 20, 2021 · 0/8

Task board · In Progress / Review (03)

Group chat (03, in order)

Files (04)

In Progress: Planning · Listing deliverables checklist · Sep 20, 2021 · 4 Comment · 11 file | Research · Usability test plan · Aug 20, 2021 · 0/8 | Design · Onboarding copy · Aug 20, 2021 · 0/8 · cover Photo_Gradient_Orange
Review: Content · Design System · Aug 16, 2021 · 0/8 · cover Photo_Gradient_Red | Design · High Fidelity UI Desktop · Aug 20, 2021 · 0/8 | Content · Handoff deliverables checklist · Sep 20, 2021 · 4 Comment · 11 file

Member: Hello! 👋 · 08.00 am
You: Hi, Everyone 🔥 · 08.01 am
Member: How are you? What did you do, everyone? · 08.03 am
Member: Good ✌ · 08.05 am
Member: voice message · 1:25

Folders: Documents · 24 files | Music · 102 files | Work Project · 84 files | Personal Media · 2450 files | Reddingo Backup · 22 files | Root · 105 files
Recent Files: Proposal.docx · 2.9 MB · Feb 25, 2022 | Background.jpg · 3.5 MB · Feb 24, 2022 | Apex website.fig · 23.5 MB · Feb 22, 2022 | Illustration.ai · 7.2 MB · Feb 20, 2022

Conversation list (06)

Design Team conversation (06, in order)

Attachments (06)

Pinned: Killan James · 4:30 PM · Typing... · 2 (Avatar_Killan_James) | Design Team · 9:36 AM · Hello! Everyone (Avatar_Design_Team) | Ahmed Medi · 1:15 AM · Wow really Cool 🔥 (Avatar_Ahmed_Medi)
All Messages: Claudia Maudi · 4:30 PM · Typing... (Avatar_Claudia_Maudi) | Novita · 4:30 PM · yah, nice design · 2 (Avatar_Novita) | Milie Nose · 8:20 PM · Awesome 🔥 · 1 (Avatar_Milie_Nose) | Ikhsan SD · yesterday · Voice message (Avatar_Ikhsan_SD) | Aditya · yesterday · publish now (Avatar_Aditya)

Killan James · 10:12 AM: Hi, are you still a web designer? / Would love to see some designs 😁
— Today, March 24 —
Claudia Maudi · 10:30 AM: Hey, happy to hear from you. Yes, I will be back in a couple of days. / Here are some designs I took earlier today. [Photo_Chat_Design_1, Photo_Chat_Design_2]
Dristin Watson (you) · 10:30 AM: Great 🔥 That’s a nice design idea. 😍👏
Milie Nose · 8:20 PM: Awesome 🔥

Very important file.figma · Some file.scratch · List of something.xd · Very important file.svg — each 7.5 MB · 3.22.22, 11:15 AM

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy
• Brand color #5051F9 and DM Sans
• Media: logo, avatars, photos, icons
• Default Button, default Text Field

• Layout, grid, grouping, order and emphasis on every screen
• All other colors: neutrals, text, surfaces, chart and bar colors, tag colors, status / progress colors, online status, error / disabled
• Type scale, spacing, radii, elevation
• All states: current nav item, current period tab, current settings tab, current conversation, unread, typing, hover, focused field
• Sidebar, top bar, stat cards, charts, task rows, schedule card, message rows, gantt rows and bars, kanban columns and cards, chat bubbles, folders, file table, storage panel, profile header, tabs, form, contact panel
• How avatars, covers and photos are cropped

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current nav, tabs, conversation, unread / typing)

Deliverable: the link to your own Figma file containing the 6 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · OCTOM

Fixed: the brand color and the typeface below. Everything else is yours to define and apply consistently: neutrals and grays, text colors, app background and surfaces, chart and timeline bar colors, task tag colors, progress and status colors, online status, unread badge, selected states, error / disabled, type scale, spacing, radii, elevation and the layout grid.

Brand color

Brand primary · indigo

#5051F9

The app’s signature accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  24% complete

Use DM Sans for all UI text. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: desktop web app, 1440 × 1024 per screen. Light mode. Screens do not scroll as a page; panels may scroll inside.
