# Stock Trading（10case / case-003）

- 原始模板（只读）：https://www.figma.com/design/nISgchmziUh7mWv20c4JGx/
- 模型收到的提示词：

```
请在以下Figma文件中完成完整设计:
Figma 文件:https://www.figma.com/design/nISgchmziUh7mWv20c4JGx/
请先阅读「00·Start Here」中的设计任务，参考「01· Foundations」中的视觉规范，复用「02·Components」中的组件，使用「04·Media」中的素材，最终将完整设计交付至「03·Workspace」。
```

## 00 · Start Here 设计任务

LEVEL L2 · DESIGN TASK · v2

Stock Trading — Indonesian stock investing app

Design an Indonesian stock investing app (Bahasa Indonesia, dark mode): see your main balance, today’s trending tickers and your watchlist, browse global trending stocks, open the GOTO stock detail, and top up your balance at Alfamart up to the payment code. Canvas 375 × 812, dark mode. Work in your own new Figma file — this file is read-only reference.

How to work

1. Build exactly the 6 frames below, named exactly as listed (one state per frame), and wire them as a clickable prototype with the listed links.
2. Everything in “Must include” must appear on that frame. The lists are grouped by subject and sorted alphabetically — they are not in screen order and say nothing about layout, grouping, emphasis or styling. Those are your decisions.
3. The brand primary color, the typeface and dark mode in 01 · Foundations are fixed. Define every other color yourself (dark background and surface levels, neutrals, text, gain / loss, selected, warning, error / disabled, chart colors), plus type scale, spacing, radii and elevation, and apply them consistently.
4. 02 · Components gives only a default Button, a default Text Field and the platform shell (status bar, home indicator). Design all other states, the headers, the tab bar, tabs and chips, and every business component as reusable components in your file.
5. Use the company logos, ticker marks and icons from 04 · Media.
6. Copy and data must match “Fixed data” exactly (Indonesian number format: Rp2.125.000 · 0,58%). This brief wins over anything you may know of the original kit.

Frames · goals · must include · links

Frame names are fixed. Must-include lists are grouped by subject and sorted A–Z: they state what is on the screen, never where it goes or how it looks.

01_Aktivitas

02_Trending

Goal: See my balance, today’s trending tickers and my watchlist.

Goal: Browse what is trending in global and regional markets.

MUST INCLUDE

MUST INCLUDE

• Actions: Deposit (Icon_Deposit) · Tarik (Icon_Withdraw)
• Balance: “Dana Utama” · Rp2.125.000 · rising Rp206.920 (10,79%)
• Header: “Aktivitas” · menu (Icon_Menu) · settings (Icon_Settings)
• Main navigation: tab bar Aktivitas / Trending / Top Up / Pasar / Profil · current: Aktivitas
• Trending today: “Trending Hari ini” · BRRI · ARB · FSX, each with mark, ticker, price and change (see DATA)
• Watchlist: “Watchlist Saya” · add (Icon_Plus) · DHDI · AMRI · ODD · PYQ · DAN, each with mark, ticker, company, price and change (see DATA)

• Header: “Trending” · menu (Icon_Menu) · settings (Icon_Settings)
• Indices: IHSG · NIKKEI · SENSEX, each with value and direction (see DATA)
• Main navigation: tab bar · current: Trending
• Market tabs: Global · Crypto · Reksadana · CFD · current: Global
• Recommendations: “Rekomendasi” · NFLX · META · AMZN, each with ticker, company, price and change (see DATA)
• Regions: Asia · Eropa · Amerika · Mata Uang · current: Asia
• Trending list: “Trending” · period “24 jam” (Icon_Chevron_Down) · ROTI · GOTO · ABNB · UNVR · BBRI · ADRO, each with logo, ticker, company, price and change (see DATA) · “Lihat Semua” (Icon_Chevron_Right)

LINKS

→ Deposit → 04_Top_Up_Metode
→ Trending tab → 02_Trending
→ Top Up tab → 04_Top_Up_Metode

LINKS

→ GOTO → 03_Detail_Saham
→ Aktivitas tab → 01_Aktivitas
→ Top Up tab → 04_Top_Up_Metode

03_Detail_Saham

04_Top_Up_Metode

Goal: Understand how GOTO is doing before buying or selling.

Goal: Choose how to top up my balance.

MUST INCLUDE

MUST INCLUDE

• Actions: Beli · Jual
• Chart: 1D price line with a highlighted point and tooltip, time axis 6:00 – 2:00 (see DATA)
• Compare: “Dibandingkan dengan” · BUKA · BBRI · SIDO, each with company, ticker, price and change (see DATA)
• Header: back (Icon_Back) · add (Icon_Plus) · share (Icon_Share) · favorite (Icon_Star)
• Key stats: “Keystats” · 8 rows (see DATA)
• Range tabs: 1D · 5D · 1M · 6M · YTD · 1Y · 5Y · MAX · current: 1D
• Stock: Logo_GOTO · GOTO · GoTo Gojek Tokopedia · Rp189 · falling −Rp9 (−4,55%) · “Hari ini”

• Balance: “Dana Saya” · Rp2.125.000
• Header: “Top Up” · back (Icon_Back) · help (Icon_Help)
• Main navigation: tab bar · current: Top Up
• Methods: “Pilih Metode” · ATM (Icon_ATM) · Kartu Debit (Icon_Debit_Card) · Mobile Banking (Icon_Mobile_Banking) · Indomaret (Icon_Store) · Alfamart (Icon_Store), each opens its next step (Icon_Chevron_Right)

LINKS

→ Alfamart → 05_Top_Up_Nominal
→ back → 01_Aktivitas

LINKS

→ back → 02_Trending

05_Top_Up_Nominal

06_Top_Up_Pembayaran

Goal: Pick the top-up amount for Alfamart.

Goal: Know exactly how and by when to pay at the store.

MUST INCLUDE

MUST INCLUDE

• Action: Bayar
• Amount options: “Pilih Nominal Top Up” · Rp50.000 · Rp100.000 · Rp200.000 · Rp300.000 · Rp500.000 · Rp1.000.000 · selected: Rp500.000
• Custom amount: “Atau masukkan nominal di sini” · field “Minimal Rp10.000” — empty
• Header: “Top Up” · back (Icon_Back) · help (Icon_Help)
• Main navigation: tab bar · current: Top Up
• Method: “Top Up ke” · Alfamart (Icon_Store) · “Ganti”
• Steps: 1 Masukkan Nominal · 2 Pembayaran · current: step 1

• Action: Oke
• Deadline: “Bayar Sebelum” · Minggu, 30 Oktober 2022, 13:32 WIB · countdown 00 : 08 : 46
• Guide: “Panduan Pembayaran” · 6 steps (see DATA)
• Payment: No Transaksi · Nominal · Kode Pembayaran with copy (Icon_Copy) (see DATA)
• Title: “Selesaikan Pembayaran” · “Silakan selesaikan proses pembayaran”

LINKS

→ Oke → 01_Aktivitas

LINKS

→ Bayar → 06_Top_Up_Pembayaran
→ back / Ganti → 04_Top_Up_Metode

Navigation structure

• Bottom tab bar with 5 tabs in this order: Aktivitas (Icon_Tab_Aktivitas), Trending (Icon_Tab_Trending), Top Up (Icon_Plus), Pasar (Icon_Tab_Pasar), Profil (Icon_Tab_Profil). Current tab: Aktivitas on 01, Trending on 02, Top Up on 04 and 05. 03 and 06 have no tab bar. How the current tab looks is yours.
• Browse flow: 01_Aktivitas → 02_Trending → 03_Detail_Saham (GOTO).
• Top-up flow: 01_Aktivitas (Deposit or Top Up tab) → 04_Top_Up_Metode → 05_Top_Up_Nominal (Alfamart) → 06_Top_Up_Pembayaran → Oke → 01_Aktivitas.
• Entry only (no frame): menu, settings, Tarik, watchlist add, other tickers, Crypto / Reksadana / CFD, Eropa / Amerika / Mata Uang, 24 jam, Lihat Semua, Rekomendasi cards, range tabs other than 1D, add / share / favorite, Jual, Beli, compare items, ATM / Kartu Debit / Mobile Banking / Indomaret, help, copy code, Pasar, Profil.

Fixed data & copy

Use these values verbatim. Bahasa Indonesia; prices in rupiah; Indonesian number format (“.” thousands, “,” decimals).

Balance

Trending Hari ini (price · change)

Watchlist Saya (company · price · change)

Dana Utama: Rp2.125.000 · ▲ Rp206.920 (10,79%)
Dana Saya (top up): Rp2.125.000

BRRI · 8.600 · +50 (+0,58%) (Logo_BRRI)
ARB · 8.600 · +50 (+0,58%) (Logo_ARB)
FSX · 8.600 · +50 (+0,58%) (Logo_FSX)

DHDI · PT Duatiga Pertama · 8.600 · +50 (+0,58%) (Logo_DHDI)
AMRI · PT Atma Merapi · 2.421 · −121 (−4,76%) (Logo_AMRI)
ODD · PT Okufo Dokuri · 5.300 · +31 (+0,59%) (Logo_ODD)
PYQ · PT Pimnas Yosque · 3.867 · −71 (−1,80%) (Logo_PYQ)
DAN · PT Danang Amin · 6.600 · −201 (−2,96%) (Logo_DAN)

Indices (Asia)

Trending · 24 jam (company · price · change)

Rekomendasi (company · price · change)

IHSG · 7.206,92 · rising
NIKKEI · 27.105,20 · falling
SENSEX · 59.959,85 · rising

ROTI · Nippon Indosari Tbk · 8.600 · +50 (+0,58%) (Logo_ROTI)
GOTO · GoTo Gojek Tokopedia · 189 · −9 (−4,55%) (Logo_GOTO)
ABNB · Airbnb Inc · 5.300 · +31 (+0,59%) (Logo_ABNB)
UNVR · Unilever Indonesia · 3.867 · −71 (−1,80%) (Logo_UNVR)
BBRI · Bank Rakyat Indonesia · 4.630 · +38 (+0,83%) (Logo_BBRI)
ADRO · Adaro Energy Indonesia · 3.600 · +21 (+0,59%) (Logo_ADRO)

NFLX · Netflix, Inc · 2.122.340 · −0,20%
META · Meta Platforms · 987.890 · +1,29%
AMZN · Amazon.com, Inc · 1.001.333 · −6,20%
(ticker badges are text — no logos)

GOTO · 1D chart

Dibandingkan dengan (price · change)

Keystats (GOTO)

Price at 6:00 197 · 10:00 199 · 14:00 194 · 18:00 196 · 22:00 192 · 2:00 189
Tooltip on the 22:00 point: Rp192 · 28 Okt 2022 - 22:00 · Volume: 102K

Bukalapak Tbk · BUKA · Rp276 · +2,82%
Bank Rakyat Indonesia · BBRI · Rp4.630 · +0,83%
PT Industri Jamu · SIDO · Rp740 · +2,82%

Previous Close · Rp198
Day Range · Rp188 - Rp199
Year Range · Rp180 - Rp396
Market Cap · 694,70T IDR
AVG Volume · 167,58M
P/E Ratio · 15,50
Dividend Yield · 3,76%
Primary Exchange · IDX

Pembayaran

Panduan Pembayaran (6 steps)

No Transaksi · FD8U4J38J004093J8U80TJ039
Nominal · Rp500.000
Kode Pembayaran · 1111000065665144

1. Catat kode pembayaran di atas dan datang ke gerai Alfamart, Alfa Midi, Lawson atau DAN+DAN terdekat.
2. Beritahukan ke kasir bahwa Anda ingin melakukan pembayaran.
3. Kasir akan menanyakan kode pembayaran. Berikan kode pembayaran Anda 1111000065665144.
4. Kasir akan melakukan konfirmasi data konsumen berupa Nama Merchant, Nama Konsumen, dan Nominal. Lakukan pembayaran ke kasir sejumlah nominal yang disebutkan.
5. Terima struk sebagai bukti pembayaran sudah sukses dilakukan. Notifikasi pembayaran akan langsung diterima oleh Merchant.
6. Selesai.

What is fixed · what is yours

Fixed (given)

Yours (designer decides)

• Frame list and exact names
• Must-include content per frame (what, not how)
• Navigation structure and links
• All data and copy (Bahasa Indonesia)
• Brand primary #279646, Roboto, dark mode
• Media: company logos, ticker marks, icons
• Default Button, default Text Field, platform shell

• Layout, grouping, order and emphasis on every screen
• All other colors: background / surface levels, neutrals, text, gain / loss, selected, warning, error / disabled, chart
• Type scale, spacing, radii, elevation
• All states: current tab, selected tab / chip / range / amount, rising / falling, current step, pressed, disabled
• Headers, tab bar, tabs, chips, cards, rows, chart, key-stats table, stepper, payment details
• Chart styling and tooltip

How it is evaluated

Your file is compared with this brief on coverage, data and flow — not on visual similarity to any original.

1. Checklist coverage per frame
2. Data & copy accuracy
3. Flow & prototype completeness
4. Information hierarchy
5. Visual quality & consistency of your own system
6. Component reuse
7. State design (current tab, selected tab / chip / range / amount, current step, rising / falling, empty field)

Deliverable: the link to your own Figma file containing the 6 named frames, your components and the prototype.

## 01 · Foundations 视觉规范

Foundations · Stock Trading

Fixed: the brand primary color, the typeface and dark mode — they carry the app’s identity. Everything else is yours to define and apply consistently: dark background and surface levels, neutrals and grays, text colors, semantic colors (gain / loss, selected, success, warning, error, disabled), chart colors, type scale, weights per role, spacing, radii and elevation.

Brand color

Brand primary · green

#279646

The app’s brand color. Where and how much to use it is your decision.

Typeface

Aa Bb Cc 0123456789  Rp2.125.000  +0,58%

Use Roboto for all UI text (Regular / Medium / SemiBold / Bold available). Sizes, weights and line heights are yours to define as a consistent type scale.

Canvas: 375 × 812 (Android / iPhone size). Dark mode only. Language: Bahasa Indonesia (copy is fixed in the brief). Number format: Indonesian — “.” for thousands, “,” for decimals (Rp2.125.000 · 0,58%). 01_Aktivitas, 02_Trending, 03_Detail_Saham and 06_Top_Up_Pembayaran may scroll vertically.
