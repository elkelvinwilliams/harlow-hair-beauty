# Harlow Hair & Beauty — Salon Website

A premium, multi-page marketing website for a hair & beauty studio in Tottenham, London
(formerly Harlow, England),
built around taking bookings. This repo is the starting point so the project can be
worked on **remotely** (cloned/checked out on any device or a cloud Claude session).

## Decisions locked in

| Decision        | Choice                                                        |
|-----------------|---------------------------------------------------------------|
| Business        | Hair & beauty studio, Tottenham, London (moved from Harlow)    |
| Primary goal    | Take bookings / appointments                                  |
| Style direction | Elegant & premium                                             |
| Tech stack      | HTML + Tailwind CSS                                           |
| Scope           | Multi-page (4–6 pages)                                        |
| Branding        | Client-supplied (real name, brand, copy, photos) — TBC        |

## Status

🟢 **Live.** All five pages are built, animated, accessible (WCAG AA) and published:
**https://elkelvinwilliams.github.io/harlow-hair-beauty/**. Business operating docs live
in [`business/`](business/). Remaining placeholders to replace with real content: prices
(#6), photos (#8), testimonials (#9), contact details (#10), booking method (#12).
*(Was: "🟡 Scaffold stage — no site pages built yet.")*

## Content checklist (to be filled in, one by one)

**Brand**
1. [x] Salon name + tagline — **Hagiazo Hair**, strapline **"Be set apart"**
       (*Hagiazo*, verb: to sanctify, to make holy, to set apart for a special purpose)
2. [x] Logo — supplied: interlocking double-H monogram (`assets/hagiazo-logo.jpeg`)
3. [x] Brand colours — **canonical spec: [`business/02_Brand_Truth.md`](business/02_Brand_Truth.md).**
       Monochrome near-black `#2A2420` on stone `#ECEBE7` / cream `#FAFAF8`, warm
       near-black bands `#0D0A07`. *(Superseded the original bronze `#A98A66` on
       `#ECE4D8`/`#F7F3EC` direction — old values preserved in BIZ-02.)*
4. [x] Fonts — **Fraunces** (serif headings) + Inter (sans body).
       *(Superseded Playfair Display — see BIZ-02.)*

**Positioning:** premium **braids & locs** studio for the Afro-Caribbean community in
Tottenham, London. The venue works two ways: clients book a chair with Ruvimbo, and
independent stylists can **hire a chair** (see `contact.html#chair-hire`). Craft: box/knotless
braids, cornrows, twists, starter locs & loc maintenance. *(Previously Harlow, Essex.)*
Design inspiration: ever.co.id (editorial, minimal, lots of whitespace & motion).
Logo: standalone HH monogram (background removed) woven through nav, hero, footer & about.

**Content**
5. [x] About / story — founder **Ruvimbo** (~15 yrs); therapist-turned-stylist,
       "loving people through their transformation"; faith-subtle "set apart / renewing
       of the mind" thread. Craft: box braids & knotless, cornrows, locs & retwists,
       wig-making & revamps.
6. [ ] Services + prices
7. [x] Team / stylists — solo founder for now: **Ruvimbo** (founder feature on About;
       monogram placeholder until a real photo is supplied)
8. [ ] Photos (hero, gallery, team)
9. [ ] Testimonials / reviews

**Practical**
10. [~] Address, phone, email, opening hours — **address supplied:** Studio 40, Unit 7
        Creative Works, Fountayne Road, Tottenham, London N15 4QL. Phone, email
        and hours still placeholders.
11. [x] Social links — Instagram (@hagiazohair) + TikTok live; Facebook placeholder (coming soon)
12. [ ] Booking method (external link vs built-in form vs both)

## Local preview

Plain static HTML — no build step. Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Stack (edition 2 — November 2026)

- `css/site.css` — the whole design system (dark-first editorial on the house tokens:
  Fraunces + Inter, hairlines not boxes, underline buttons, sharp corners, reduced-motion safe).
- `js/site.js` — behaviour: header, mobile nav, reveals, counters, marquee, gallery filter +
  lightbox, testimonial carousel, FAQ accordion, booking estimator, chat launcher.
  **Two settings live at the top of this file:** `BOOKING_URL` (the external booking system —
  empty until it exists; every Book button then goes to `booking.html`) and `WHATSAPP`.
- No Tailwind, no npm — the previous Tailwind build was retired with this edition.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Home — hero, stats, marquee, story, six styles, work teaser, prices, values, client stories, CTA |
| `services.html` | Full price list — six styles with length × parting-size breakdowns; prep & aftercare |
| `our-work.html` | Gallery with filters + lightbox (`gallery.html` redirects here) |
| `testimonials.html` | Client stories — carousel + grid (placeholder slots until real reviews exist) |
| `about.html` | Story, values, founder (real photo), the six differences, studio strip |
| `faqs.html` | Ten questions, accordion |
| `contact.html` | Studio info, map, enquiry form, chair hire |
| `booking.html` | Choose style → length → parting size, live estimate, hand-off to WhatsApp / booking link |

## Placeholder slots (fill these as content arrives)

Every image frame is a `.media` element with a `data-slot` name and a "Photo coming soon" tag.
To drop in a real photo, replace the inner `<div class="ph …"></div>` with
`<img src="assets/your-photo.jpg" alt="…">` — the frame, overlay and hover zoom stay the same.

| Slot(s) | Where | Suggested shot |
|---|---|---|
| `hero-photo` | Home hero | Client in the chair, dark backdrop, landscape |
| `intro-portrait`, `about-studio-portrait` | Home story, About | Portrait, 4:5 / 3:4 |
| `service-<id>`, `service-<id>-detail` | Home cards, Services | One finished look per style |
| `work-teaser-1/2`, `gallery-01…12` | Home, Our Work | Portrait 3:4 results — set `data-title`, `data-desc`, `data-cat` on the tile |
| `prices-photo`, `cta-backdrop`, `social-backdrop`, `services-backdrop` | Bands | Atmosphere / studio |
| `studio-1…4` | About | Inside the studio |
| Testimonial `.t-card.slot` and the carousel JSON on `testimonials.html` | Home, Testimonials | Real reviews only, with consent |
| `+44 (0) 000 000 0000`, postcode, `BOOKING_URL`, `WHATSAPP` | Footer, Contact, `js/site.js` | Real contact details |
