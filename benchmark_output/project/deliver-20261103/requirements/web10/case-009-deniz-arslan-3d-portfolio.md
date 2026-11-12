# Deniz Arslan 3D Portfolio（web10 / case-009）

- 原始模板（只读）：https://www.figma.com/design/c3zaMtiBbbSxN3JfJtE2Hu/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/c3zaMtiBbbSxN3JfJtE2Hu/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Deniz Arslan — 3D artist portfolio

Design a two-page personal portfolio for a 3D artist and sculptor: a work page with three projects and an about page with skills and contact. Desktop web, 1440 wide, light mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 2 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in page order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The two brand colors and the typeface in 01 · Foundations are fixed. Define every other color yourself, plus type scale, spacing, radii, elevation and the page grid, and apply them consistently.
4. 02 · Components gives no Button or Text Field: the source has neither (every action is a text link). Design the header, footer, link style, current-page state and every content block as reusable components in your file.
5. Use the portrait photo and the icons from 04 · Media. The three project images are not supplied in the source — use image placeholders. The logo “da.” is plain text.
6. Copy and data must match “Fixed data” exactly. This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Work

02_About

Goal: See who the artist is and browse three projects.

Goal: Learn about the artist’s background and skills, and get in touch.

MUST INCLUDE

MUST INCLUDE

• Footer: “Deniz Arslan ⏤ 2020” · Artstation · LinkedIn · Twitter
• Header: logo “da.” · navigation Work / About / Playground / Contact · current: Work
• Intro: “Hello, I’m Deniz.” · “A senior-year design student who is trying to specialize in 3D modeling & texturing.” · scroll cue (Icon_Arrow_Down)
• Projects: 3 project blocks, each with number and name, description, tools line where given, link or status, and an image placeholder (see DATA)

• Contact: “I’d be thrilled to hear about your next project” (Icon_Arrow_Right) · “deniz.arslan@example.com” · “View Resume”
• Footer: “Deniz Arslan ⏤ 2020” · Artstation · LinkedIn · Twitter
• Header: logo “da.” · navigation Work / About / Playground / Contact · current: About
• Intro: “Hi, I’m Deniz Arslan, 3D artist & sculptor.” · biography (2 paragraphs, see DATA) · Photo_Profile
• Skills: “Main Software” and “Main Skills”, each with its list (see DATA)

LINKS

LINKS

→ About (nav) → 02_About
→ logo “da.”, Work (nav) → 01_Work (self)

→ logo “da.”, Work (nav) → 01_Work

Navigation structure

• Two pages share the header and footer. The current page is shown in the navigation.
• Work → 01_Work · About → 02_About · logo “da.” → 01_Work.
• Entry only (no frame): Playground, Contact, project links, Artstation / LinkedIn / Twitter, the email address, View Resume.

Fixed data & copy

Use these values verbatim.

Projects (in order)

Biography (02_About)

Skills (02_About)

01 / Goblin Bust — “Goblin concept digital sculpture with human-like skin. Learned a lot of quick tips and look development.” · tools: “Sculpted in ZBrush, retopologized and UV-mapped in Maya, textured in Mari, rendered with Arnold.” · link “More shots from this project ↗”
02 / Skin Shader Study — “Subsurface weight, specular roughness and diffuse maps generated with procedural and manual techniques.” · link “See case study →”
03 / Creature Concept — “Experimental creature modeling for a school project.” · status “Project WIP” (not a link)

“My work is mainly focused on 3D modeling, texturing and rendering. I like exploring creatures with a touch of dark surrealism for characters and production.”
“Now I’m an interactive media design student in Istanbul ⏤ currently freelancing and seeking internship opportunities.”

Main Software: Pixologic ZBrush, Autodesk Maya, The Foundry Mari, Arnold Renderer, Blender, Forger · Adobe CC, Figma, Ableton
Main Skills: Organic and Polygonal Modeling, UV Layout, Texturing, Retopology, Illustration, Sound Design

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame names and links
• Must-include content (what, not how)
• All data and copy
• Brand colors #181717 and #2429AF, and DM Sans
• Media: portrait photo, icons

• Layout, grid, grouping, order and emphasis on both pages
• All other colors: page background, secondary text, dividers, image placeholders
• Type scale, spacing
• All states: current page, link hover
• Header, footer, link style, project block, skill list, contact block
• How the portrait is cropped and placed

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse (shared header / footer)

Deliverable: the link to your own Figma file containing the 2 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Deniz Arslan

Fixed: the two brand colors and the typeface below. Everything else is yours to define and apply consistently: page background, grays for secondary text, dividers, image placeholders, link and current-page states, type scale, spacing, and the page grid.

Brand colors

Brand ink

Brand accent · blue

#181717

#2429AF

The portfolio’s main text and line color. Where and how much to use it is your decision.

The portfolio’s only accent. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  da.

Use DM Sans for all UI text. Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: desktop web, 1440 wide. Light mode. Frame heights are free — both pages scroll vertically.
