# BIZ-02 — Brand & Theme Guideline (Single Source of Truth)

> **Document control**
> | Field | Value |
> |---|---|
> | **Reference** | BIZ-02 |
> | **Title** | Brand & Theme Guideline — Single Source of Truth |
> | **Status** | 🟢 **Confirmed canonical (2026-09-06)** |
> | **Owner** | Ruvimbo (Founder) |
> | **Prepared by** | Claude (Technical Architect) |
> | **Approved by** | Elkelvin / Ruvimbo — confirmed the shipped brand, 2026-09-06 |
> | **Reference build** | https://elkelvinwilliams.github.io/harlow-hair-beauty/ |
> | **Review cycle** | When the brand changes |

**This is the one place the brand is defined.** Everything — new pages, print, social,
future work — follows this. It is derived directly from the **live site**, which the
founder confirmed on 2026-09-06 as the theme and guideline of record.

---

## Decision (confirmed) — resolves contradiction C1

Two documents once described two different brands. **The shipped, live brand wins.**

| Attribute | ~~`README.md` (superseded)~~ | **Canonical (live site)** |
|---|---|---|
| Heading font | ~~Playfair Display~~ | **Fraunces** |
| Accent | ~~Bronze `#A98A66`~~ | **Near-black `#2A2420`** (monochrome) |
| Ink | ~~`#14110C`~~ | **`#131110`** |
| Stone | ~~`#ECE4D8`~~ | **`#ECEBE7`** |
| Cream | ~~`#F7F3EC`~~ | **`#FAFAF8`** |
| Scheme | ~~Warm bronze-accented~~ | **Monochrome black & white** |

*Old values are struck through, not deleted — preserved here as the record. Reasoning:
the live site is the real, approved product; reverting would be a rebrand, not a fix.
`README.md` has been reconciled to cite this document.*

---

## 1. Name, meaning & voice

- **Name:** Hagiazo Hair · **Strapline:** *Be set apart*
- **Meaning:** *hagiazo* (v.) — to sanctify, to make holy, **to set apart for a special
  purpose**. The "set apart / renewing of the mind" thread is the soul of the brand.
  **Niche-critical — protected.**
- **Voice:** plain, warm, confident. Short sentences. Understated luxury — never hype.
  Faith-subtle, never preachy. The About founder story is the tone reference.

## 2. Typography

- **Headings:** **Fraunces** (serif) → fallback Georgia, serif. Weights 400–600.
- **Body:** **Inter** (sans) → fallback system-ui, sans-serif. Weights 300–600.
- **Type scale (as built):**
  | Use | Size |
  |---|---|
  | Hero display | `clamp(3.5rem, 10vw, 8rem)`, serif, tight leading |
  | Section heading | `text-4xl → text-6xl` serif, weight 600, often with an italic accent word |
  | Sub-heading | `text-2xl` |
  | Body | `text-sm` / `text-base`, Inter, relaxed leading |
  | **Section label** | `0.68rem`, weight 600, **letter-spacing 0.24em**, UPPERCASE, colour `--label` |

## 3. Colour tokens *(canonical — `css/style.css :root` + `tailwind.config.js`)*

| Token | Hex | Role |
|---|---|---|
| `--accent` | `#2A2420` | Lines, prices, icons on light *(flips to `rgba(250,250,248,0.82)` on dark)* |
| `--ink` | `#131110` | Buttons, primary text |
| `--dark` | `#0D0A07` | Dramatic bands & footer (warm near-black) |
| `--graphite` | `#45413C` | Charcoal |
| `--stone` | `#ECEBE7` | Light section backgrounds |
| `--cream` | `#FAFAF8` | Soft near-white page background |
| `--text` | `#1A1714` | Body text |
| `--muted` | `#6E6A64` | Secondary body text |
| `--label` | `#8A847C` | Small labels |
| `--border` | `#E3E1DC` | Hairlines |

**Accessibility rule (from our WCAG pass):** faint text sits at **`white/55` or darker**
on dark, **`gray-500` or darker** on light — never lighter (they fail AA contrast).

## 4. Layout & spacing

- **Container:** `max-w-7xl`, padding `px-6 lg:px-12`, centred.
- **Vertical rhythm:** sections breathe — **`py-24` / `py-28`** desktop. Generous whitespace
  is the luxury; don't crowd.
- **Corners: SHARP.** Structural elements have **no border-radius** — the editorial,
  gallery-like feel depends on it. (Only tiny UI dots/pills are round.)
- Alternate **light (`--cream`/`--stone`) and dark (`--dark`) bands** for drama.

## 5. Buttons & components

- **Buttons:** UPPERCASE, `font-size 0.8rem`, weight 500, **letter-spacing 0.12em**,
  padding `0.9rem 2.1rem`, **2px border**, sharp corners, subtle light-sweep on hover.
  - `.btn-cream` — cream fill, for **dark** backgrounds (inverts to outline on hover)
  - `.btn-outline` — outline, for **dark** backgrounds
  - `.btn-outline-dark` — outline, for **light** backgrounds
  - Primary CTAs carry a **4px magnetic pull** (fine-pointer only).
- **Section label + accent line:** a `0.24em`-tracked uppercase label, often above a
  **44×2px accent line** that animates in with `scaleX`.
- **Nav:** sticky, `aria-current` active state with an underline indicator.

## 6. Motion *(tasteful, transform/opacity only)*

- **Signature easing:** `cubic-bezier(0.16, 1, 0.3, 1)` for reveals & transitions.
- **Buttons:** `cubic-bezier(0.22, 1, 0.36, 1)`. **Count-ups / pops:** springy
  `cubic-bezier(0.34, 1.56, 0.64, 1)`.
- **Entrances:** `.reveal` / `.reveal-delay-1..5` / `.clip-reveal` / `.fade-up`.
- **Depth:** subtle hero **parallax** on decorative layers only (factor 0.06–0.16).
- **Non-negotiable:** everything respects **`prefers-reduced-motion`** (all motion off,
  content force-revealed).

## 7. Imagery

- **Logo:** interlocking **double-H monogram** (`assets/hh-light.png` / `hh-dark.png`);
  full lockup `assets/hagiazo-lockup-light.png` / `-dark.png`.
- **Founder:** `assets/ruvimbo.jpg` · **Meaning artwork:** `assets/hagiazo-meaning.jpeg`.
- **Photography direction (for the real photos you'll send):** warm, natural light,
  clean/dark backdrops, focus on texture and craft; editorial not clinical. Keep the
  monochrome-with-warmth palette in mind so photos sit with the theme.
- **Do not delete or alter brand assets** — they are the identity of record.

## 8. Do / Don't

| ✅ Do | ❌ Don't |
|---|---|
| Keep sharp corners & generous whitespace | Round everything or crowd sections |
| Use Fraunces headings + Inter body | Reintroduce Playfair or any gold/bronze accent |
| Keep motion subtle, transform-only, reduced-motion safe | Add bouncy/heavy animation or animate on scroll heavily |
| Keep faint text at AA-safe opacity | Drop text below `white/55` or `gray-500` |
| Let the "set apart" voice stay understated | Make it hype-y or heavily religious |

---

## Change log
| Date | Version | Change | By |
|---|---|---|---|
| 2026-09-06 | 0.1 | Initial draft; recorded C1, recommended shipped brand | Claude |
| 2026-09-06 | 1.0 | **Founder confirmed shipped brand as canonical.** Expanded into full Brand & Theme Guideline (type scale, layout, components, motion, imagery, do/don't) from the live build. | Claude |
