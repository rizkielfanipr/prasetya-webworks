---
version: alpha
name: Disewain
description: >-
  A warm, approachable design system with a vibrant orange identity, cream-toned
  backgrounds, soft bordered surfaces, clear typography and restrained elevation.
source:
  url: https://disewain.biz.id/
  extractedAt: 2026-10-24
  tokensMeasured: true
---

# Prasetya Webworks Design System

This document is the source of truth for the website's visual language. It adapts the supplied Disewain design reference to Prasetya Webworks while preserving the existing content, routes and bilingual experience.

## Visual direction

- Warm, optimistic and professional.
- Orange is reserved for primary actions, emphasis and active states.
- Cream backgrounds create separation without heavy shadows.
- Cards use thin borders, subtle transparency and generous whitespace.
- Headings are geometric and confident; body text stays clean and highly legible.
- Static surfaces remain flat. Only primary calls to action receive elevation.

## Logo

- Mark "Ubin": four tiles on a 2×2 grid (orange rounded square, navy half disc, soft-orange quarter disc, orange dot) that loosely form a **P**. It stands for a website assembled from blocks and templates; the dot is the finishing touch of a promise kept (*prasetya* means a pledge). The half disc is navy on light backgrounds and white on dark ones.
- Wordmark: "prasetya" in Raleway Bold and "webworks" in Raleway Medium Italic orange, outlined to paths so the logo does not depend on loaded fonts.
- Files (all SVG, no raster source needed):
  - `public/images/prasetya-webworks-logo.svg` — navy text, for light backgrounds (`site.logo`).
  - `public/images/prasetya-webworks-logo-white.svg` — white text, for dark backgrounds such as the footer (`site.logoOnDark`).
  - `public/favicon.svg` — the mark on a navy rounded tile, so it reads on light and dark browser tabs. `favicon.png`, `favicon.ico` and `apple-touch-icon.png` (square, full-bleed for iOS masking) are rendered from it.
- Do not recolour the logo with CSS filters; use the matching file.

## Semantic color tokens

| Token | Value | Role |
|---|---|---|
| `--background` | `#FFFAF4` | Page background |
| `--foreground` | `#0F172A` | Primary text |
| `--card` | `#FFFFFF` | Cards and panels |
| `--primary` | `#FF5100` | Primary CTA and emphasis |
| `--primary-foreground` | `#FFFFFF` | Text and icons on orange |
| `--secondary` | `#FFF1E8` | Soft orange surface |
| `--accent` | `#FFE2CF` | Highlight surface |
| `--muted-surface` | `#F6F3F0` | Neutral raised surface |
| `--muted-foreground` | `#646464` | Supporting text |
| `--border` | `#EADED5` | Default border |
| `--ring` | `#FF5100` | Keyboard focus ring |

Do not introduce a new visual color for ordinary components when a semantic token already covers its role. Status colors may be added only when the product has an actual error, warning, success or information state.

## Typography

### Families

- Display and headings: **Raleway**, fallback `sans-serif`.
- Body, captions and interface labels: **Plus Jakarta Sans**, fallback `sans-serif`.

### Scale

| Role | Size | Weight | Line height | Tracking |
|---|---:|---:|---:|---:|
| Display desktop | `60px` | 500 | 1 | `-1.5px` |
| Display tablet | `48px` | 500 | 1 | `-1px` |
| Display mobile | `36px` | 500 | 1.05 | `-0.7px` |
| Heading small | `14px` | 600 | 1.43 | `-0.35px` |
| Body large | `16px` | 400 | 1.5 | 0 |
| Body medium | `15px` | 400 | 1.87 | 0 |
| Body small | `14px` | 500 | 1.43 | 0 |
| Body small strong | `14px` | 600 | 1.43 | 0 |
| Caption | `12px` | 500–700 | 1.33 | 0 |
| Eyebrow | `12px` | 700 | 1.33 | `1.44px` |

Eyebrows use uppercase orange text. Avoid mixing Raleway and Plus Jakarta Sans within a single heading.

## Spacing

The base unit is `4px`.

| Name | Value |
|---|---:|
| `xxs` | `4px` |
| `xs` | `8px` |
| `sm` | `12px` |
| `md` | `16px` |
| `lg` | `20px` |
| `xl` | `24px` |
| `xxl` | `32px` |
| `xxxl` | `36px` |
| `section` | `40px` |
| `band` | `64px` |

Section padding-inline is `24px` on mobile, `32px` on tablet and `40px` from desktop upward.

## Radius and elevation

- Standard cards, buttons and form containers: `16px` (`--radius`).
- Compact controls: `12px`.
- Small inline controls: minimum `8px`.
- Avoid pill shapes unless the control semantically benefits from it.
- Cards use a border and no shadow by default.
- Primary CTA shadow:

```css
box-shadow:
  0 10px 15px -3px rgb(255 81 0 / 25%),
  0 4px 6px -4px rgb(255 81 0 / 25%);
```

Do not invent additional elevation levels.

## Components

### Primary button

- Height: `48px`.
- Padding: `14px 24px`.
- Background: `--primary`.
- Text and icons: white (`--primary-foreground`), Plus Jakarta Sans 14/600.
- Keep primary-button foreground white in default and hover states for clear contrast against orange.
- Radius: `16px`.
- Uses the primary CTA shadow.

### Outline button

- Height: `38–48px` depending on context.
- White background, foreground text and `--border` stroke.
- No shadow.
- Hover uses `--secondary` and a stronger orange border.

### Card

- White or translucent-white background.
- `1px` border using `--border` or a low-opacity orange.
- Radius: `16px`.
- Padding: `20–24px`.
- No shadow at rest.
- Hover may strengthen the border and move at most `3px` vertically.

### Form controls

- White background, `1px` input border and `12px` radius.
- Keyboard focus uses the orange ring and must not rely on color alone when an error exists.
- Labels remain visible; placeholders do not replace labels.

### Navigation

- Warm translucent background with a subtle bottom border.
- Desktop horizontal links; mobile uses a menu trigger and a bordered white panel.
- Minimum touch target is `36px`; primary actions target `48px`.

## Responsive layout

| Viewport | Grid | Heading | Section padding |
|---:|---:|---:|---:|
| `375px` | 1 column | `36px` | `24px` |
| `768px` | 2 columns | `48px` | `32px` |
| `1024px` | 4 columns | `60px` | `40px` |
| `1280–1440px` | up to 5 columns | `60px` | `40px` |

- Never force desktop grids onto mobile.
- Text columns use `minmax(0, 1fr)` to prevent overflow.
- Long Indonesian and English strings must wrap without changing page width.
- Respect `prefers-reduced-motion` for every transition and animation.

## shadcn implementation rules

- Follow shadcn's source-owned model: generic primitives live in `src/components/ui/`.
- Use semantic tokens rather than hard-coded page colors.
- Static primitives remain Astro components and ship no client JavaScript.
- Add framework hydration only when state cannot be handled accessibly with native HTML.
- Compose existing primitives before adding duplicate markup.

Current primitives:

- `src/components/ui/Button.astro`
- `src/components/ui/Card.astro`
- `src/components/ui/SectionIntro.astro` (`layout="center"` default, or `layout="split"`: lined eyebrow, left heading, right description, used by Cara Kerja, Paket and FAQ)
- `src/components/ui/FilterChips.astro`
- `src/components/ui/Pagination.astro`

## Do

- Use orange for primary calls to action and short visual emphasis.
- Use Raleway for headings and Plus Jakarta Sans for body/interface copy.
- Use bordered cards with clear spacing and restrained hover movement.
- Keep content readable and layouts responsive from 320px upward.
- Preserve visible focus, semantic HTML and sufficient touch targets.

## Do not

- Add arbitrary shadow tiers.
- Return to blue as the primary brand color.
- Use full-pill radii everywhere.
- hide labels in favor of placeholders.
- Add a dark theme without a measured and approved design.
- hard-code visible UI text outside `src/i18n/content.ts`.

## Known gaps

- A complete semantic status-color ramp is not defined.
- A first-class dark theme is not defined.
- Complex form error and readonly states need a future design pass.
- Motion uses the project's existing restrained transitions; the original source did not provide exact easing tokens.
