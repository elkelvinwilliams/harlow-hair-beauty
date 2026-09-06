# UPGRADE_00 — Repository Inventory & Classification

> **Document control**
> | Field | Value |
> |---|---|
> | **Reference** | UPG-00 |
> | **Title** | Repository Inventory & Classification (Phase 1) |
> | **Status** | 🟢 Complete — awaiting client review before Phase 2 |
> | **Owner** | Elkelvin Williams (Founder) |
> | **Prepared by** | Claude (acting CSO / COO / Technical Architect) |
> | **Approved by** | — *(not yet reviewed)* |
> | **Date** | 2026-09-06 |
> | **Review cycle** | Once, at engagement start |
> | **Governing rule** | Nothing deleted. Nothing flattened. Nothing niche-specific lost. |

---

## 0. Executive summary (read this first)

This engagement was scoped for a repository of **business operating documents**
(strategy, financial model, SOPs, compliance registers) to inventory and enrich.

**What actually exists here is a website codebase.** It is a well-built one — five
live, animated, accessible pages for *Hagiazo Hair* — but it contains **almost none
of the business operating system** the six-system architecture describes. There is
nothing to *delete* or *restructure*; the work of Phases 2–6 is overwhelmingly
**net-new document creation**, not enrichment of existing operating docs.

Three findings dominate:

1. **The operating system does not exist yet.** No business plan, financial model,
   pricing strategy, SOPs, compliance register, insurance record, GDPR/ICO
   documentation, or governance. This is the real gap — and the real opportunity.
2. **The one brand document contradicts the shipped product.** `README.md` specifies
   a brand (Playfair Display, bronze `#A98A66`, stone `#ECE4D8`) that appears
   **nowhere in the code**. The live site runs a different, monochrome brand
   (Fraunces, near-black `#2A2420`). One of these is canonical; the docs must be
   reconciled to the truth. *(See §5, contradiction C1.)*
3. **Both status documents are stale.** `README.md` and `HANDOFF.md` both say
   "scaffold stage — no site pages built." All five pages are built and live. The
   record of the business does not match the state of the business.

**No files were changed in Phase 1 other than the creation of this inventory.**

---

## 1. Confirmed engagement parameters (please verify)

The FILL-THIS-IN block arrived with placeholders. Below are the values I have
inferred from the repository and our prior work. **Please confirm or correct each —
I have not acted on them beyond this inventory.**

| Field | Inferred value | Confidence |
|---|---|---|
| **Repository** | `elkelvinwilliams/harlow-hair-beauty` (local: `/home/user/harlow-hair-beauty`) | Certain |
| **Business** | A premium braids & locs studio in Harlow, Essex, serving the Afro-Caribbean community, built around taking bookings | High |
| **Niche / sector** | Hair & beauty — specialist Afro-textured protective styling (braids, cornrows, locs, wigs) | High |
| **UK regulator / licence** | **Largely unregulated for braiding** — no special-treatments licence is normally required for braids/locs. But these regimes apply: **HMRC** self-employment/Self Assessment; **UK GDPR + ICO** registration (client data); **Consumer Rights Act 2015**; **Health & Safety at Work etc. Act 1974**; **Harlow District Council** local requirements. *Colour/chemical, scalp treatment or any skin-piercing work would pull in additional rules — to confirm which services are offered.* | Medium — **needs your confirmation with Harlow Council** |
| **Protected content** | Founder story & brand voice (`about.html`); the *Hagiazo* meaning/etymology; all brand assets (logos, monogram, `ruvimbo.jpg`, `hagiazo-meaning.jpeg`); the shipped brand token system | High |
| **Restructure?** | **Assumed NO** — keep the existing website structure; add the operating system as a new parallel tree. *You left this blank; I have defaulted to no restructuring.* | Needs confirmation |

---

## 2. Full file inventory

Every tracked file, what it covers, and its apparent status.

### Website — pages (client-facing shopfront)
| File | Covers | Status |
|---|---|---|
| `index.html` | Home: hero, services preview, about teaser, "what we stand for", testimonials, gallery preview, CTA | 🟢 Live. Copy corrected (honest stats, no "walk in"). Testimonials still placeholder. |
| `services.html` | Full service menu across braids, locs, cornrows/protective, kids/packages | 🟢 Live. **Prices are placeholder** (checklist #6 open). |
| `about.html` | Founder story (Ruvimbo), "Our Story" cascade, values, "set apart" pull-quote | 🟢 Live. **Copy is final & niche-critical — protect.** |
| `gallery.html` | Filterable work grid, Instagram CTA | 🟢 Live. **Images are placeholder gradients** (checklist #8 open). |
| `contact.html` | Connect hub, enquiry form, info, map, booking form, FAQs | 🟢 Live. **Address / phone / hours placeholder; forms not wired to a backend** (checklist #10, #12 open). |

### Website — implementation & brand system
| File | Covers | Status |
|---|---|---|
| `css/style.css` | Custom CSS + **the de-facto brand token system** (`:root` colours, type, motion) | 🟢 Canonical brand tokens live here. |
| `css/tailwind.css` | Compiled Tailwind utilities (generated) | 🟢 Generated artefact — rebuilt via `npm run build:css`. |
| `src/tailwind.input.css` | Tailwind entry (`@tailwind` directives) | 🟢 Source. |
| `tailwind.config.js` | Tailwind theme: brand colours + font families | 🟢 **Second half of the canonical brand spec.** |
| `js/main.js` | Shared animation system (scroll pipeline, reveals, parallax, count-ups, nav, menu) | 🟢 Live, hardened in Phase 1 of prior work. |

### Brand assets (all niche-critical — never delete)
| File | Covers | Status |
|---|---|---|
| `assets/hh-light.png` / `hh-dark.png` | HH monogram (light/dark) | 🟢 In use across nav/hero/footer. |
| `assets/hagiazo-lockup-dark.png` / `-light.png` | Full logo lockup + strapline | 🟢 In use (About). |
| `assets/hagiazo-logo.jpeg` | Original supplied logo | 🟡 Source/reference. |
| `assets/hagiazo-meaning.jpeg` | The *Hagiazo* etymology / brand-meaning artwork | 🟡 Brand soul — not currently surfaced on site. |
| `assets/ruvimbo.jpg` | Founder photo | 🟡 Supplied; About currently uses monogram placeholder — candidate to swap in. |

### Documentation & project meta
| File | Covers | Status |
|---|---|---|
| `README.md` | Project overview, "decisions locked in", 12-item content checklist | 🟠 **Stale + contradicts code** (brand spec, build status). Closest thing to a brand/strategy doc. Enrich + reconcile — do not delete. |
| `HANDOFF.md` | Desktop→remote session handoff instructions | 🟠 **Superseded** (site is built). Candidate for `_archive/` with a note — flagged, not moved. |

### Tooling & configuration
| File | Covers | Status |
|---|---|---|
| `package.json` / `package-lock.json` | npm scripts (CSS build), dev deps (tailwind, jimp) | 🟢 Fine. |
| `.gitignore` | Ignore rules (node_modules, env, shots) | 🟢 Fine. |
| `.claude/settings.json` | Enables design plugins (frontend-design, impeccable, ui-ux-pro-max) | 🟢 Your work (PR #2). Auto-installs in fresh sessions. |
| `.claude/launch.json` | Local static-server launch config (port 8743) | 🟢 Fine. |

---

## 3. Map onto the six-system architecture

Which parts of the current repo already serve each target system. **Keeping your
existing names** — this is a map, not a re-organisation.

| # | System | Served today by | Coverage |
|---|---|---|---|
| 1 | **Strategy** — direction, capital, roadmap | Fragments in `README.md` ("decisions locked in", checklist) | 🔴 ~5% — no plan, model, pricing strategy or roadmap |
| 2 | **Operations** — the engine room | `package.json` / `launch.json` (site build only) | 🔴 0% — no service delivery, booking, supplier or capacity processes |
| 3 | **Core Delivery** — the main service, incl. regulated | `services.html` (menu, placeholder prices), craft narrative in `about.html` | 🟠 ~20% — shopfront exists; no back-of-house spec, timings, consultation/patch-test or aftercare docs |
| 4 | **Differentiator** — the second engine | The "therapist-turned-stylist / set apart / renewing of the mind" story in `about.html` & `README` item 5 | 🟠 ~25% — exists as *brand narrative*; not operationalised into an experience protocol |
| 5 | **Growth & Partnerships** — demand, referrals | The website itself; social links (IG/TikTok); Instagram CTAs | 🟠 ~20% — strong demand *asset*; no marketing plan, referral/loyalty scheme, Google Business or review engine behind it |
| 6 | **Governance & Compliance** — licence to operate | — | 🔴 0% — no registration, insurance, GDPR/ICO, privacy policy, H&S, consent or retention records |

---

## 4. Document classification

Per the governing rule, every item classified as **Niche-critical (protected)**,
**Universal**, or **Orphaned**.

**Niche-critical — PROTECTED (enrich only; never restructure or reword the substance):**
- `about.html` founder story & brand voice — the soul of the business.
- The brand token system (`css/style.css` `:root` + `tailwind.config.js` theme) — the
  de-facto identity of record.
- All `assets/*` — logos, monogram, `ruvimbo.jpg`, `hagiazo-meaning.jpeg`.
- `README.md` items 1–5, 7, 11 (brand name, strapline, meaning, story, positioning,
  founder, live social handles) — domain facts supplied by you.

**Universal — bring to standard:**
- The five HTML pages as *implementation* (structure/markup), `js/main.js`,
  `css/tailwind.css`, `src/`, `package.json`, `.gitignore`, `.claude/*`.
- `README.md` as a *project document* (frame it to the standard; preserve the domain facts inside).

**Orphaned — flagged, not moved:**
- `HANDOFF.md` — a superseded session artefact. Recommend archiving to `_archive/`
  with a note in a later phase; **left in place for now** pending your say-so.
- `assets/hagiazo-meaning.jpeg` — brand-critical but not surfaced anywhere; not
  orphaned in value, only in use. Flag for a home (e.g. an About "meaning" section).

---

## 5. Contradictions found (to reconcile in Phase 4 — nothing overwritten yet)

| ID | Contradiction | Value A | Value B | Note |
|---|---|---|---|---|
| **C1** | **Brand specification** | `README.md`: **Playfair Display** + Inter; accent **bronze `#A98A66`**; ink `#14110C`; stone `#ECE4D8`; cream `#F7F3EC` | Shipped code: **Fraunces** + Inter; accent **`#2A2420`** (mono, flips near-white on dark); ink `#131110`; dark `#0D0A07`; stone `#ECEBE7`; cream `#FAFAF8` | The README brand hexes/fonts appear **nowhere** in code. **The shipped code is live and canonical.** Recommend: README updated to cite the code; old values recorded. *Needs your confirmation that mono-Fraunces is the intended brand.* |
| **C2** | **Build status** | `README.md` & `HANDOFF.md`: "🟡 scaffold — no site pages built" | Reality: all 5 pages built, animated, accessible, live on GitHub Pages | Status docs lag reality. Update to current state. |
| **C3** | **Business name** | `README.md` H1: "Harlow Hair & Beauty"; repo slug `harlow-hair-beauty` | Brand of record: **Hagiazo Hair** (`package.json` name `hagiazo-hair`) | Cosmetic; the repo slug predates the brand. No rename proposed unless you want it. |
| **C4** | **Business descriptor** | `README`/`HANDOFF`: generic "hair & beauty salon" | Positioning: specialist **braids & locs** for the Afro-Caribbean community | The generic framing undersells the niche; align language in Phase 3. |
| **C5** | **Location** | "Harlow, **England**" (docs) | "Harlow, **Essex**" (site + this doc) | Trivial; standardise to "Harlow, Essex". |

*No financial contradictions can exist yet — there is no financial model. Pricing on
`services.html` is unvalidated placeholder (see Assumptions, to be built in Phase 2).*

---

## 6. What the repository does NOT yet have

The operating system, in full. None of the following exists:

**System 1 — Strategy:** business plan; vision/mission/values doc; **financial model**
(revenue, costs, contribution, breakeven, cash flow); **pricing strategy** &
rationale; capacity/utilisation model; roadmap; capital/funding plan.

**System 2 — Operations:** SOPs (booking, consultation, service delivery, sanitation,
opening/closing, no-show handling); client-records process; supplier & stock list;
calendar/capacity plan; payment handling process.

**System 3 — Core Delivery:** service specification (each style: description, timing,
skill, materials); **patch-test & consultation protocol** (required for any colour);
aftercare documentation; quality standard.

**System 4 — Differentiator:** the "calm chair / therapeutic experience / set apart"
promise turned into a **documented, repeatable experience protocol** with its own KPIs.

**System 5 — Growth & Partnerships:** marketing plan; content calendar; **Google
Business Profile** plan; review-generation engine; referral/loyalty scheme; partnership map.

**System 6 — Governance & Compliance:** HMRC self-employment registration record;
**insurance** (public/treatment/product liability) record; **UK GDPR + ICO**
documentation; **privacy policy** & **terms of service**; H&S policy & **risk
assessment**; **client consent** (incl. photo consent) forms; **data-retention
schedule**; complaints procedure.

**Operating-system scaffolding (this framework's own deliverables):**
`DOCUMENT_STANDARDS.md`; Writing Style Guide; the six-system architecture document;
per-folder `00_Index.md`; master document register; assumptions register;
canonical-sources declaration; phase gates; PDF generation script + CI workflow.

---

## 7. Decisions I need before Phase 2 (I will not proceed without these)

1. **Where the operating system lives.** This is a website repo. My recommendation:
   build the business OS **additively, inside this repo**, as a new top-level
   `/operating-system/` tree (six numbered system folders) sitting alongside the
   website — one versioned source of truth, nothing to the site touched. Alternative:
   a separate repo. **Confirm the location.**
2. **Restructure?** You left it blank. I will **not** restructure your website. Confirm.
3. **Canonical brand (C1).** Confirm the shipped **mono-Fraunces** brand is correct
   and README should be reconciled to it — or tell me Playfair/bronze was the real
   intent and the code drifted.
4. **Regulatory confirmation.** Confirm the service list so I can scope compliance
   precisely — specifically whether any **colour/chemical, scalp-treatment, or
   skin-piercing** services are offered (these change the licensing picture with
   Harlow Council).
5. **Engagement parameters (§1).** Confirm the inferred business/sector/protected-content values.

---

## 8. Confirmation

**Nothing was deleted, flattened, moved, or reworded in Phase 1.** The only change to
the repository is the creation of this file. Awaiting your review and the five
decisions above before beginning Phase 2 (additive scaffolding).
