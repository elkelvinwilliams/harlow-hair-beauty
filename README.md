# Harlow Hair & Beauty — Salon Website

A premium, multi-page marketing website for a hair & beauty salon in Harlow, England,
built around taking bookings. This repo is the starting point so the project can be
worked on **remotely** (cloned/checked out on any device or a cloud Claude session).

## Decisions locked in

| Decision        | Choice                                                        |
|-----------------|---------------------------------------------------------------|
| Business        | Hair & beauty salon, Harlow, England                          |
| Primary goal    | Take bookings / appointments                                  |
| Style direction | Elegant & premium                                             |
| Tech stack      | HTML + Tailwind CSS                                           |
| Scope           | Multi-page (4–6 pages)                                        |
| Branding        | Client-supplied (real name, brand, copy, photos) — TBC        |

## Status

🟡 **Scaffold stage.** This is an elegant placeholder skeleton so there's something
real to preview and iterate on remotely. All copy/images marked `TODO` are placeholders
to be replaced with the salon's real content.

## Content checklist (to be filled in, one by one)

**Brand**
1. [x] Salon name + tagline — **Hagiazo Hair**, strapline **"Be set apart"**
       (*Hagiazo*, verb: to sanctify, to make holy, to set apart for a special purpose)
2. [x] Logo — supplied: interlocking double-H monogram (`assets/hagiazo-logo.jpeg`)
3. [x] Brand colours — black ink `#14110C` on warm stone `#ECE4D8` / cream `#F7F3EC`,
       space-gray neutrals, muted bronze accent `#A98A66` (premium B&W direction)
4. [x] Fonts — Playfair Display (serif headings) + Inter (sans body)

**Positioning:** premium **braids & locs** studio for the Afro-Caribbean community in
Harlow (box/knotless braids, cornrows, twists, starter locs & loc maintenance).
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
10. [ ] Address, phone, email, opening hours
11. [x] Social links — Instagram (@hagiazohair) + TikTok live; Facebook placeholder (coming soon)
12. [ ] Booking method (external link vs built-in form vs both)

## Local preview

Tailwind is compiled to a static stylesheet (`css/tailwind.css`) — no CDN, no
runtime build. Just open `index.html` in a browser, or run a static server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

If you change the markup (add/remove Tailwind classes), rebuild the CSS:

```bash
npm install        # first time only
npm run build:css  # or `npm run watch:css` while editing
```

## Planned pages

- `index.html` — Home (hero, services preview, about preview, testimonials, CTA)
- `services.html` — Full services + price list
- `about.html` — Story + team
- `gallery.html` — Work / salon photos
- `contact.html` — Contact details, hours, map, booking
