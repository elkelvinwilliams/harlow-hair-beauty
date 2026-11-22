# Design reference: hagiazohair.netlify.app

A design brief written from observing the public site on 22 Nov 2026. It describes structure, styling and motion in our own words so a new build can match the structure and feel. Nothing from the site (markup, CSS, JS, images, fonts or copy) is included; only our notes and our own screenshots under `screens/`.

Tech observed (names only): a single-page React app built with Vite, React Router for routing, Tailwind CSS v4 (utility classes, oklch neutral palette), `tailwindcss-animate` style utilities (`animate-in fade-in`), Lucide icons. No animation library (no Framer Motion, GSAP, Lenis, AOS). Reveal and counter effects are hand-rolled with IntersectionObserver and requestAnimationFrame. Fonts from Google Fonts.

---

## 1. Page list and global structure

| Route | Page | Desktop height | Mobile height |
|---|---|---|---|
| `/` | Home | 7424px | 12553px |
| `/services` | Services and pricing | 6208px | 9923px |
| `/our-work` | Gallery | 3695px | 8055px |
| `/testimonials` | Client stories | 2325px | 4272px |
| `/about` | About and founder | 3976px | 6045px |
| `/faqs` | FAQ accordion | 2285px | 3452px |
| `/contact` | Contact form, map | 1633px | 3307px |
| `/booking` | Four-step booking wizard | 1362px | 3624px |

Deep links to any route other than `/` return the Netlify 404 page. The app only works via client-side navigation (no SPA redirect rule is deployed). Our build should ship a proper fallback.

### Header (all pages)
- Fixed to top, full width, z-index above everything. Three-part layout: wordmark left, centred nav, booking link right. Inner max width about 1280px with 32px side gutters.
- Wordmark is two words: a bold condensed uppercase word (Oswald, 30px desktop, wide tracking) followed by an italic serif word (Playfair Display italic, light grey) that turns white on hover.
- Nav: 7 text links, Montserrat 12px, uppercase, letter-spacing 0.1em, grey (#a1a1a1). Active link is white with a 1px white underline sitting a few pixels under the text. Hover turns a link white (colour transition 300ms). No underline-slide animation on nav links; only the colour change.
- Right: a "book now" call-to-action with a small calendar icon, Oswald 12px uppercase, 0.2em tracking, white, with a 2px white underline (see button styles).
- At the top of the page the header is a vertical gradient from 90% black to transparent with 20px vertical padding. Once `scrollY` passes about 20px it switches to solid black and 12px vertical padding. The switch is a 300ms transition on all properties. Height ~68px either way.
- Mobile (under ~1024px): wordmark, a short "BOOK" underline link, and a hamburger (icon button labelled "Toggle navigation menu"). Opening it slides down a full-width black panel below the header. Each nav item is a 56px-tall row, Montserrat 14px uppercase, grey, with a thin bottom border and a right-pointing chevron; the active item is white. Below the list: a full-width centred Oswald "book an appointment" link with a 2px white underline, then a one-line grey location and hours string. The hamburger swaps to an X.

### Footer (all pages)
- Black, 1px top border in #171717, 64px top padding, 48px bottom (96px on mobile to clear the WhatsApp pill).
- Four equal columns (268px each on desktop, stacked on mobile, 2 columns on tablet):
  1. Wordmark, a two-line grey description, a small uppercase "tagline" label and an italic serif tagline, then three icon links (Instagram, TikTok, WhatsApp) as plain line icons.
  2. "Navigation": Oswald 14px uppercase heading with a 1px #262626 underline rule, then 8 links in Montserrat 12px uppercase grey; the last link (book) is white and bold.
  3. "Studio hours": same heading style; two rows each with a clock icon, a bold day range, and a time line; a small grey note underneath.
  4. "Studio contact": pin, phone and mail icon rows; a 1px rule; then a centred "reserve your chair" underline button.
- Bottom bar: 1px top rule, copyright line left (grey 12px), a tagline right, and a small "back to top" arrow icon button at far right.

### Persistent elements
- A WhatsApp pill fixed bottom-right (24px inset), a 44px round-ish icon button with a white outline chat icon; it fades to light grey on hover. Links to a `wa.me` number.
- Smooth scrolling is enabled at the document level.
- Custom dark scrollbar: 8px wide, track #0a0a0a, thumb #2a2a2a, hover #444444.
- Text selection is inverted (white background, black text).

---

## 2. Page-by-page sections

Spacing convention used everywhere: sections are padded 80px top/bottom on tablet and 112px on desktop (`py-20 lg:py-28`), content constrained to 1280px with 16/24/32px gutters at phone/tablet/desktop. Section headings are centred, Oswald bold uppercase 48–60px with the last word (or two) swapped into Playfair Display italic in a lighter grey, followed by a 1px, 48px-wide centred rule and a 1–2 line grey Montserrat lead. Alternating sections use pure black (#000) and a near-black (#0a0a0a) to separate bands without borders.

### 2.1 Home (`/`)

1. **Hero** (min-height 92vh, flex-centred, 96px top padding). Full-bleed photo of a client in a salon chair, slightly darkened and contrast-boosted, with a top-to-bottom black overlay (70% → 50% → 80%). Centre-aligned stack: an all-caps H1 at 96px desktop / 30px phone, with the two-word second half in italic serif in #e5e5e5 and a heavy text shadow; a 48px rule; a three-line grey lead (18px); two underline buttons side by side (primary "book", secondary "explore"); a tiny uppercase "scroll" label with a 40px vertical gradient line beneath it. Content fades up on load (see motion).
2. **Stats strip** (#0a0a0a, 40px padding). Four centred stats in a 4-col grid (2-col on phone), 32px gap: a big Oswald number (48px, with a "+" or "%") over a 12px uppercase grey label. Numbers count up when scrolled into view.
3. **Marquee ribbon** (black, 16px padding, overflow hidden). A single row of 20 uppercase service names in Oswald 12px, separated by a small star/asterisk icon, duplicated so it scrolls continuously leftward (28s linear loop).
4. **Intro / "service beyond expectation"** (black, 96px padding). Two-column grid: left column has a left-aligned heading (italic serif middle word), two grey paragraphs (16px then 14px); right column is a tall portrait image (aspect ~4:5) with a slow Ken Burns zoom and an inner gradient. 48px gap.
5. **Service cards / "what we offer"** (black, 112px padding). Centred heading + lead, then a 3-col grid (1 on phone, 2 on tablet), 32px gap, six cards. Each card: a 16:10 image with a numbered "01" label top-left (Oswald, white, 12px), a "from £…" price bottom-right (Oswald 12px), and a bottom-up black gradient overlay at 80% opacity; image zooms to 105% on hover over 700ms. Below the image: Oswald 20px uppercase title, a two-line grey description (14px), a 1px rule, a one-line grey note about what's included, another rule, then a row with the primary underline "book this style" link left and a plain grey "view sizes" link right. Beneath the grid a centred secondary underline link to the full price list.
6. **Portfolio teaser / "discover our works"** (#0a0a0a, 112px padding). 12-col grid: two tall portrait images on the left (two columns, 24px gap, the second one offset downward by ~64px), each with an uppercase eyebrow + bold caption overlaid at the bottom-left; the right column (about 5/12) holds a left-aligned heading, grey lead, and a row with a primary underline link plus a grey handle link to Instagram.
7. **Price list / "our prices"** (black, 112px padding). 12-col grid. Left 6 cols: left-aligned heading, grey lead, then a price table of six rows, each a flex row with a bold Oswald 12px uppercase service name on the left, a dotted/1px rule filling the middle and an Oswald bold price on the right, separated by 1px #262626 rules; then an underline link to all prices. Right 6 cols: a landscape photo (aspect ~4:3) with a quote card overlaid bottom-left (italic serif quote, 18px, with a tiny uppercase attribution).
8. **Values / "what we stand for"** (#0a0a0a, 112px padding). Centred heading; 3-col grid, 48px gap; each column has a 1px top rule, a tiny grey "pillar 01" eyebrow, an Oswald 20px title, a one-line italic serif subtitle, and a grey paragraph. All left-aligned.
9. **Testimonials preview / "what clients say"** (black, 112px padding). Centred heading; 3-col grid; each card: 1px top rule, five small star icons (white, filled), an italic serif quote (16px, #d4d4d4), a 1px rule, then name (Oswald bold 12px uppercase) with the style under it (grey 11px) and the town right-aligned in 12px uppercase grey. Centred underline link below.
10. **Closing CTA / "ready for your transformation?"** (128px padding, text centred, overflow hidden). Full-bleed darkened photo background with a black gradient, centred two-line heading (second line italic serif), grey lead, two underline buttons (book + WhatsApp).

Heading hierarchy on Home: one H1 (hero) → H2 per section → H3 for card titles and value pillars.

### 2.2 Services (`/services`)

- The whole page sits on a fixed, full-viewport background photo (a salon interior) with `background-attachment: fixed` and a 75% black overlay with a very slight blur; a mobile fallback uses an `<img>` in the same fixed layer. Content scrolls over it, so it reads as a subtle parallax backdrop. Page has no H1; it opens with a centred H2 "artisanal services" page title (same title treatment as every inner page: Oswald + italic serif, rule, grey lead) with 112px top padding.
- **Six service blocks**, one per style, each a 12-col grid (`lg:grid-cols-12`, 48px gap), stacked with ~96px between them, separated by a 1px #262626 rule:
  - Left 5 cols: tiny grey "style 01" eyebrow, an Oswald 36px uppercase H3, a one-line italic serif tagline, a 4:3 photo (with Ken Burns on hover), an "estimated duration" line and "starting from £…" line in small grey/white, then a primary underline "book …" link.
  - Right 7 cols: a header row with two 10px uppercase grey labels ("length and sizing breakdown" left, "GBP (£)" right) over a 1px rule; then one or more length groups, each introduced by a small white diamond bullet + Oswald 14px H4 (e.g. a length name), followed by three rows (small / smedium / medium) laid out as flex rows: Oswald bold 12px name, a 1px #262626 leader line filling the gap, Oswald bold 18px price. Below the groups a "service note" line with an info icon in 12px grey.
- **Preparation and aftercare** block: centred heading; 2-col grid (48px gap); each column has an icon + Oswald 14px uppercase H3, then a bulleted list (three items) where each bullet starts with a bold Montserrat lead-in and continues in grey 14px.
- Closing centred secondary underline link to booking.

### 2.3 Our work (`/our-work`)

1. **Title band** (min-height 45–60vh, centred, 112px top padding). H1 "our works" (second word italic serif), grey lead, then a three-stat row (500+, 6, 5.0 with a star) separated by 1px vertical rules, same stat style as Home but smaller (30px numbers).
2. **Filter bar**: a horizontal, scroll-snapping row of 6 text buttons (Oswald 12–14px uppercase, wide tracking, 44px min height), each with a small superscript count in grey. Active filter is white with a 1px underline; others are grey. Filtering swaps the grid immediately (no transition observed).
3. **Gallery grid** (48px vertical padding): 3-col grid (1/2 on smaller), 24px gap, twelve cards. Each card is a 3:4 portrait tile, cursor pointer, overflow hidden, image zooms to 105% on hover over 700ms; a bottom-up black gradient overlay is always present and strengthens on hover; the caption block sits bottom-left over the image: a 10px uppercase grey category eyebrow, Oswald 18px uppercase title, a one-line grey description.
4. **Lightbox**: clicking a card opens a fixed full-screen layer at 95% black with a backdrop blur, fading in over 200ms. Centred: the image (max ~80vh), a close X button top-right (outside the image), then under a 1px rule a two-column footer: eyebrow + Oswald 28px title + description on the left, a primary underline "book this look" link on the right. Escape does not close it; only the X.
5. **Social banner / "follow the chair"** (full-bleed, min-height 380px, 80px vertical margins). Darkened salon photo background with a left-to-right black gradient; left-aligned Oswald heading with italic serif second half, grey lead, and a primary underline link with an Instagram icon to the account.

### 2.4 Testimonials (`/testimonials`)

1. **Title** (H2) + lead + rule, 64px bottom margin.
2. **Featured quote carousel** (max width 896px, centred). 1px top rule; a row with five stars + "5.0 verified client" label in 12px uppercase; a large italic serif quote (28–30px, white) with a faint oversized quotation-mark glyph top-right; 1px rule; then a footer row: name (Oswald 16px bold uppercase), style and town (grey 12px), date (grey 11px) on the left and prev/next chevron buttons with a "1 / 5" counter on the right. Buttons swap the quote instantly.
3. **All testimonials**: a header row ("all client testimonials (5)" in Oswald 14px left, "100% 5-star reputation" grey right) over a 1px rule; then a 3-col grid of the same cards used on Home (stars, italic quote, rule, name/style, town).
4. **Three promise tiles** (96px top margin): 1px top rule across; 3-col grid; each centred: a circled check icon, Oswald 14px uppercase H4, grey two-line note.
5. **Closing CTA**: centred H3 (italic serif second word), lead, primary underline link with calendar icon.

### 2.5 About (`/about`)

1. **Title** (H2 "to set apart") + lead explaining the name + rule.
2. **Philosophy** (12-col grid, 48px gap, 96px bottom margin). Left 6 cols: Oswald 36px H3 with italic serif ending, two grey paragraphs, a 1px rule, then a three-stat row (year, "1-on-1", "100%") with vertical rule separators and 10px grey labels. Right 6 cols: a tall portrait photo (aspect ~3:4) with a quote card overlaid at the bottom (italic serif 16px + tiny attribution).
3. **Values band** (#0a0a0a, 80px padding): same three-pillar component as Home with H3 heading and H4 pillars, eyebrow text "stand for · 01".
4. **Founder** (12-col grid, 96px bottom margin). Left 5 cols: 4:5 portrait with a tiny uppercase caption under it; right 7 cols, vertically centred: Oswald 36px H3 ("meet …" + italic serif name), a grey paragraph, a left-bordered (2px white/30) italic serif pull quote, then three inline "✦ specialism" tags in Oswald 10px uppercase.
5. **Studio strip** (#0a0a0a, 48px padding, overflow hidden): centred Oswald 16px H4 "inside the studio"; 4-col grid of 3:4 photos (2-col on phone), 16px gap, each with a slow Ken Burns alternate zoom.
6. **Closing CTA**: centred two-line H3, lead, primary underline link.

### 2.6 FAQs (`/faqs`)

- Title (H2) + lead + rule. Then a single column (max width 896px) of ten accordion items.
- Each item: a full-width button row (24–28px padding) with a tiny grey "01." index, an Oswald 18–20px uppercase H3 question, and a Lucide chevron-down icon at the right; 1px #171717 bottom border between items; hover changes the border/colour over 200ms. Open state rotates the chevron and reveals a grey 14px answer paragraph plus a small "category: …" label; one item open at a time.
- The grey lead at top mentions four themes (preparation, inclusions, deposit, aftercare).

### 2.7 Contact (`/contact`)

- Title (H2) + lead + rule. Then a 2-col grid (5/7 split, 48px gap):
  - Left "studio information" (Oswald 24px H3 with 1px rule): four icon rows (pin, phone, mail, clock), each a white 14px label over a grey 12px detail; a rule; a "connect directly" 10px label; two underline links (WhatsApp, Instagram) with icons; a rule; a "map: …" label row; then a 320px-tall embedded Google Map (`maps.google.com/maps?…&output=embed`) styled with CSS filters (invert, contrast 125%, grayscale) so it matches the dark theme.
  - Right "send a message" form (Oswald 24px H3 + grey lead): fields are borderless, transparent inputs with only a 1px bottom border in white/30 that turns white on focus (colour transition); labels are Oswald 10px uppercase with a "*" for required. Fields: full name (text), email, phone (tel) in a 2-col row, inquiry type (native select, 5 options: availability, style consultation, wig construction, colour matching, general), message (textarea, 6 rows). Submit is a full-width primary underline button "send inquiry" with a send icon; disabled state is 50% opacity.
  - The form has no `action`, no Netlify form attributes and the bundle contains no fetch, mail or third-party form endpoint near the form, so submissions are handled client-side only (state/UI feedback). Treat it as a visual pattern; our build needs a real backend or Netlify Forms.

### 2.8 Booking (`/booking`)

- Title (H2 "online booking") + lead + rule.
- **Stepper**: four equal columns (`grid-cols-4`), each with an Oswald 12px number and label ("style and size", "date and time", "details and add-ons", "review and confirm"); the active step is white, completed steps show a check icon, upcoming steps are grey; a 1px rule beneath.
- **Body**: 12-col grid, 40px gap. Left 8 cols hold the active step; right 4 cols hold a sticky "booking summary" card: Oswald 14px heading, a 1px rule, label/value rows (style, length, size, date, time slot; add-ons when chosen) separated by #262626 rules, then an "estimated total" row in Oswald bold 24px, deposit and balance lines, a rule, and three "✦" reassurance bullets in 12px grey. Totals update live.
- Step 1 "select your service": a 2-col grid of six service options, each a left-aligned tile with a tiny "01" index, "from £…" at right, Oswald 18px title (selected title gets a white underline), grey description; then "length variant" and "braid size and density" rows of text-button chips (Oswald 12px uppercase; selected = white with underline, others grey; price shown under each size); a service-note line with an icon; a right-aligned "continue →" underline button.
- Step 2 "pick appointment date and time": a native date input with the underline style (past dates disabled), four time-slot chips with clock icons, an info note about slot length, back/continue links.
- Step 3 "your information and enhancements": name, email, phone inputs (underline style, 1-col then 2-col), four optional add-on checkboxes rendered as rows (Oswald title, grey description, "+£…" price), a hair-notes textarea. Inline red validation messages appear under empty required fields.
- Step 4 "review and confirm": a summary list (style, length/size, slot, client, add-ons, total), a "deposit and cancellation policy" note box, back link and a primary "confirm and reserve chair" underline button. Confirmation screen (not triggered by us) shows a reference and a "notify on WhatsApp" link that opens `wa.me/<number>?text=…` with a prefilled message containing the style, date, time and reference, plus a "return to home" link. No payment provider or server call is present; the booking is client-side only.
- Service deep links are supported: `/booking?service=<slug>` preselects a style (used by the Home cards).

---

## 3. Visual system

### Colour palette (computed, converted to hex)

| Role | Value |
|---|---|
| Page background (body) | `#070707` |
| Section black | `#000000` |
| Alternate band / stats / studio strip | `#0a0a0a` |
| Footer top border, FAQ dividers | `#171717` |
| Standard rule / border (most common) | `#262626` |
| Hover border | `#404040` |
| Placeholder text | `#525252` |
| Body copy, nav links, labels (most common text colour) | `#a1a1a1` |
| Secondary button text, quote text | `#d4d4d4` |
| Italic serif accent in headings | `#e5e5e5` |
| Lightest grey | `#f5f5f5` |
| Headings, primary buttons, prices | `#ffffff` |
| Scrollbar thumb / hover | `#2a2a2a` / `#444444` |
| Translucent whites (borders, underlines) | white at 20%, 30%, 40%, 60% |
| Validation red (Tailwind red-400/500) | `#f87171` / `#ef4444` |

Overlays are always black gradients: bottom-up `black 80% → transparent`, top-down `black 70% → 50% → 80%` on the hero, left-to-right `black → 60% → transparent` on banners. One decorative text gradient exists: `#f5f5f5 → #d4d4d4 → #a1a1a1` left to right. There is no accent colour anywhere; the palette is strictly monochrome.

### Typography

| Use | Family | Weight | Size (desktop) | Tracking / case |
|---|---|---|---|---|
| Hero H1 | Oswald | 700 | 96px (30px phone, 60px tablet) | tight, uppercase |
| Section H2 | Oswald | 700 | 48–60px | 0.05em, uppercase |
| Italic accent inside headings | Playfair Display | 400 italic | matches heading | normal, mixed case, #e5e5e5 |
| Card / block H3 | Oswald | 700 | 18–36px | 0.05em, uppercase |
| Sub-labels H4 | Oswald | 400–700 | 14–16px | 0.05em, uppercase |
| Eyebrows, labels, table names | Oswald | 400 | 10–12px | 0.05em, uppercase |
| Prices, stats | Oswald | 700 | 18px (table), 24px (total), 48px (stats) | uppercase |
| Buttons | Oswald | 400 | 12px (14px sm) | 0.2em, uppercase |
| Nav links | Montserrat | 400/500 | 12px | 0.1em, uppercase |
| Body copy | Montserrat | 400 | 14–16px, line-height 1.6 | normal |
| Small print | Montserrat | 400 | 11–12px | normal |
| Quotes, taglines, subtitles | Playfair Display | 400 italic | 14–30px | normal |

Fonts loaded: Montserrat (300, 400, 500, 600, 700, plus 400/600 italic), Oswald (400–700), Playfair Display (500, plus 400/600 italic). Body is antialiased.

### Buttons and links
There is one button component with two variants; neither has a background, border or radius.
- Shape: inline-flex, 44px min height, 4px vertical padding, 8px gap for an icon, Oswald uppercase with 0.2em tracking.
- Underline: a pseudo-element 2px tall in `currentColor`, positioned 8px above the bottom edge, spanning the full text width. On hover it extends 0.4rem beyond both ends (left/right transition 300ms) and the icon nudges 4px to the right (transform 300ms).
- Primary: white text, white 2px underline.
- Secondary: #d4d4d4 text, 1px underline at white/40; on hover text and underline go white.
- Nav variant is 12px. Plain text links (e.g. "view sizes") are Montserrat 12px uppercase grey turning white.
- Filter and option "chips" reuse the same idea: text only, selected = white + 1px underline.

### Radii, shadows, borders
- Border radius: none anywhere. Every image, card, input, button and the lightbox are square-cornered.
- Box shadows: none. Depth comes only from gradients and the hero text shadow (`0 4px 24px` black 95% + `0 2px 8px` black 80%).
- Borders: 1px hairlines in #262626 / #171717 / white at 20–30%; 2px only for the pull-quote left border.
- Images: `object-cover`, often with `brightness(0.9) contrast(1.05–1.1)` filters to sink them into the black.

---

## 4. Motion

- **Hero load**: the hero copy stack uses a `fadeUp` keyframe (opacity 0 → 1, translateY 16px → 0) over 0.8s with easing `cubic-bezier(0.16, 1, 0.3, 1)`, staggered 0.3s / 0.4s / 0.5s / 0.6s / 0.7s per child (heading, rule, lead, buttons, scroll cue). The hero image runs a one-shot Ken Burns (scale 1 → 1.12 over 14s, ease-out, holds).
- **Ken Burns elsewhere**: `scale 1 → 1.05 → 1` over 20s ease-in-out, infinite alternate, on intro/side images; a side variant to 1.06 on about-page studio tiles.
- **Marquee**: `translateX(0 → -50%)` over 28s linear, infinite, on a duplicated row.
- **Counters**: stat numbers count up from 0 using requestAnimationFrame once 50% visible (IntersectionObserver threshold 0.5).
- **Scroll reveal**: minimal. Beyond the counters there is no per-section reveal; sections render immediately. The feel of motion comes from the slow image zooms, not from scroll-triggered animation.
- **Hover**: image scale to 105% over 700ms inside `.group` cards; button underline extension and icon nudge (300ms); colour transitions on links, borders and icons (150–300ms, Tailwind default ease). Card borders brighten from #262626 to #404040.
- **Header**: transparent-gradient to solid black and padding reduction, 300ms, at 20px scroll.
- **Lightbox**: fade-in 200ms with backdrop blur.
- **Mobile nav**: panel appears beneath the header (no measurable slide; treat as a quick fade/height change).
- **Parallax**: only the Services page backdrop via `background-attachment: fixed`. No smooth-scroll library, no cursor effects.
- Document `scroll-behavior: smooth` for in-page jumps (back-to-top button).

---

## 5. Components inventory

- **Section title**: centred H2 (bold condensed + italic serif accent), 48px rule, grey lead. Used on every page.
- **Stat**: big number + tiny label; 4-up strip (Home) or 3-up inline with vertical rules (Our work, About).
- **Marquee ribbon** (Home only).
- **Service card** (Home): image with index + price overlay, title, description, included-note, two links.
- **Service block** (Services): two-column spec sheet with leader-line price rows grouped by length.
- **Price table** (Home): name / leader / price rows.
- **Portfolio teaser**: two offset portraits with overlaid captions + copy column.
- **Gallery tile + filter bar + lightbox** (Our work).
- **Testimonial card** (stars, italic quote, name/style/town) and **featured quote carousel** with prev/next and counter.
- **Value pillar** (eyebrow, title, italic subtitle, paragraph; 3-up).
- **Promise tile** (icon, title, note; 3-up).
- **Founder block** (portrait + bio + left-bordered pull quote + tags).
- **Studio strip** (4 portrait photos).
- **Accordion** (FAQ).
- **Form controls**: underline inputs, native select, textarea, checkbox rows, date input, chip buttons.
- **Stepper + sticky summary** (Booking).
- **CTA banner** (photo background + centred heading + two buttons).
- **WhatsApp pill**, **back-to-top** arrow.

### Forms and where they submit
- Contact form: name, email, phone, inquiry type (select), message. No action/endpoint; client-side only.
- Booking wizard: style, length, size, date, time slot, name, email, phone, up to four add-ons, notes. No endpoint; final screen offers a WhatsApp hand-off with a prefilled message.

### External destinations
- Instagram: `https://www.instagram.com/hagiazohair`
- TikTok: `https://vm.tiktok.com/ZNRwuLbhB/`
- WhatsApp: `https://wa.me/447000000000` (placeholder number; the booking hand-off appends `?text=` with a prefilled message)
- Phone: `tel:` with a placeholder `+44 (0) 000 000 0000`
- Email: `mailto:hello@hagiazohair.co.uk`
- Map: Google Maps embed for Harlow, Essex

### Imagery
- Hero photo and the Services backdrop are local assets. All other photography is Unsplash stock (12 distinct photos reused across pages) plus two Cloudinary-hosted images. Treat all of it as placeholder; our build needs real studio photography.

---

## 6. What makes it feel the way it does

1. **Strict monochrome with no accent colour.** Everything is black, white and six greys. Hierarchy is carried entirely by type weight, size and opacity, which reads as editorial and expensive.
2. **Two contrasting typefaces in every heading.** A heavy condensed sans for the bulk of the headline with the last word in a light italic serif. This single device appears in the wordmark, every section title, the hero and most CTAs, and it is the most recognisable trait of the site.
3. **No boxes.** No rounded corners, no shadows, no filled buttons, no card backgrounds. Structure comes from 1px hairlines, leader lines in price tables, and tight grids. Buttons are text with a 2px underline that stretches on hover.
4. **Slow, quiet motion.** Twenty-second image zooms, a 28s marquee, and a soft 0.8s fade-up on the hero. Nothing bounces or slides; hover effects are a slow 700ms zoom and a 300ms underline stretch. This restraint supports the "calm, unhurried chair" message.
5. **Generous vertical rhythm and alternating bands.** 112px section padding, 96px between service blocks, and alternating #000 / #0a0a0a bands instead of dividers, so long pages still feel airy.

---

## 7. What could not be captured

- The embedded Google Map tile did not render in our environment (the embed redirects to a host outside the allowed network), so the contact screenshots show an empty map area. The map itself is a standard Google embed with invert/grayscale filters.
- The booking confirmation screen and the contact form's post-submit state were not triggered, to avoid sending anything to a third party's site. Their behaviour is described from the bundle's strings only.
- Full-page screenshots cannot show the Services page's fixed-background parallax; the backdrop appears only in the first viewport of `services-desktop.png`. View the page live for the effect.
- Mobile nav open/close transition timing and the header's exact scroll breakpoint were measured from CSS and script strings, not from frame captures.
- The hero mid-animation captures (`*-hero-300ms.png`) were taken 300ms after the route rendered; on inner pages there is little or no load animation, so those frames look like the settled state.

## Screenshot index (`screens/`)

- Per page, 1440px: `<page>-desktop.png` (full page), `<page>-hero-300ms.png` (first viewport, 300ms after render).
- Per page, 390px: `<page>-mobile.png` (full page).
- Extras: `home-mobile-hero.png`, `home-mobile-nav-open.png`, `home-header-scrolled.png`, `home-service-card-hover.png`, `our-work-card-hover.png`, `our-work-lightbox.png`, `our-work-filter-french-curls.png`, `faqs-accordion-open.png`, `testimonials-carousel-next.png`, `booking-step2-desktop.png`, `booking-step3-desktop.png`, `booking-step4-desktop.png`.
- Pages: home, services, our-work, testimonials, about, faqs, contact, booking.
