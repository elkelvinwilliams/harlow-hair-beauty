# BIZ-02 — Brand Truth (Single Source of Truth)

> **Document control**
> | Field | Value |
> |---|---|
> | **Reference** | BIZ-02 |
> | **Title** | Brand Truth — Single Source of Truth |
> | **Status** | 🟢 Drafted — **one decision pending** (which brand is canonical) |
> | **Owner** | Ruvimbo (Founder) |
> | **Prepared by** | Claude (Technical Architect) |
> | **Approved by** | — *(not yet reviewed)* |
> | **Date** | 2026-09-06 |
> | **Review cycle** | When the brand changes |

**Purpose:** end the split-brain. Right now two documents describe two *different*
brands. This document is the one place the brand is defined; everything else should
cite it.

---

## The conflict (contradiction C1 from the inventory)

| Attribute | `README.md` says | The **shipped, live site** uses |
|---|---|---|
| Heading font | **Playfair Display** | **Fraunces** (fallback Georgia) |
| Body font | Inter | Inter *(agree)* |
| Accent | **Bronze `#A98A66`** | **Near-black `#2A2420`** (flips to near-white `rgba(250,250,248,0.82)` on dark) |
| Ink | `#14110C` | `#131110` |
| Dark band | — | `#0D0A07` (warm near-black) |
| Stone (section bg) | `#ECE4D8` | `#ECEBE7` |
| Cream (page bg) | `#F7F3EC` | `#FAFAF8` |
| Overall scheme | Warm bronze-accented | **Monochrome black & white**, warm near-blacks, **no gold/bronze** |

The README's fonts and hexes appear **nowhere in the code.** The live site has been
running the monochrome/Fraunces brand throughout.

## My recommendation

**Adopt the shipped brand (monochrome + Fraunces) as canonical**, because:
- It is the **real, live product** — already built, previewed, and approved through our work.
- It reads as more premium and editorial than a bronze-accented scheme, matching the
  "quiet luxury / set apart" positioning.
- Reverting to Playfair/bronze would be a **rebrand of a working site**, not a fix.

**→ Decision needed from you:** reply **"confirm shipped brand"** and I'll (a) mark this
doc canonical and (b) update `README.md` to cite it — recording, not deleting, the old
values. Or tell me Playfair/bronze was the real intention and the code drifted, and
we'll plan the change deliberately.

*(Nothing is overwritten until you decide. Both values are preserved above.)*

---

## Canonical brand specification *(pending your confirmation)*

### Name & meaning
- **Name:** Hagiazo Hair
- **Strapline:** *Be set apart*
- **Meaning:** *hagiazo* (verb) — to sanctify, to make holy, **to set apart for a special
  purpose**. This is the soul of the brand; the "set apart / renewing of the mind" thread
  runs through the About story. **Niche-critical — protected.**

### Typography
- **Headings:** Fraunces (serif) → fallback Georgia, serif
- **Body:** Inter (sans) → fallback system-ui, sans-serif
- *Source of record: `tailwind.config.js` + `css/style.css`.*

### Colour tokens *(as implemented, `css/style.css :root`)*
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

### Logo & assets
- Primary mark: interlocking **double-H monogram** (`assets/hh-light.png` / `hh-dark.png`)
- Full lockup with strapline: `assets/hagiazo-lockup-light.png` / `-dark.png`
- Founder photo: `assets/ruvimbo.jpg` · Meaning artwork: `assets/hagiazo-meaning.jpeg`
- **Do not delete or alter these; they are the brand identity of record.**

### Voice
Plain, warm, confident. Short sentences. Understated luxury — never hype. Faith-subtle,
never preachy. The About page founder story is the reference for tone.

---

## Change log
| Date | Version | Change | By |
|---|---|---|---|
| 2026-09-06 | 0.1 | Initial draft; records C1, recommends shipped brand as canonical | Claude |
