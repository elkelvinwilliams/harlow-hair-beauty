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
3. [ ] Brand colours (hex)
4. [ ] Fonts

**Content**
5. [ ] About / story
6. [ ] Services + prices
7. [ ] Team / stylists
8. [ ] Photos (hero, gallery, team)
9. [ ] Testimonials / reviews

**Practical**
10. [ ] Address, phone, email, opening hours
11. [ ] Social links
12. [ ] Booking method (external link vs built-in form vs both)

## Local preview

No build step required — Tailwind is loaded via CDN for now.
Just open `index.html` in a browser, or run a static server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Planned pages

- `index.html` — Home (hero, services preview, about preview, testimonials, CTA)
- `services.html` — Full services + price list
- `about.html` — Story + team
- `gallery.html` — Work / salon photos
- `contact.html` — Contact details, hours, map, booking
