## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Project conventions

These rules keep the codebase consistent. Follow them for every change; details and reasons are in `docs/development.md` and `docs/architecture.md`.

### Before you finish a change

1. `npm run format` then `npm run validate` (Prettier check, ESLint, Stylelint, `astro check`). It must pass with 0 errors; CI runs the same command and will not deploy otherwise.
2. `npm run build` succeeds.
3. For UI changes, check the built site (`npm run preview`) at 360px, 768px and desktop: no horizontal scroll, ID and EN pages, header/footer on home and catalog.
4. For refactors that should not change the UI, compare full-page screenshots before and after (with `prefers-reduced-motion: reduce`) and expect zero pixel difference.
5. Update the docs in `docs/` in the same change when behaviour, structure, routes or setup change. Record new technical decisions as an ADR in `docs/decisions/`.

### Structure

- `src/pages/` only routes: import a page component and pass `locale` and params. No markup or styles there.
- `src/components/layout/` site-wide pieces (SiteHeader, SiteFooter, WhatsAppFloat); `components/ui/` generic, text via props (SectionIntro, FilterChips, Pagination); `components/home/` one component per home section, composed in `HomePage.astro`; `components/templates/` template catalog.
- Reuse existing components before writing new markup. Do not copy a component to change it slightly; add a prop.
- Shared browser logic goes in `src/scripts/` as exported functions; component `<script>` blocks import them.
- Site constants (email, logo, preview URL) come from `src/config/site.ts`.
- Components talk through `data-*` attributes and ids they own, not globals.

### Text and URLs

- All UI text lives in `src/i18n/content.ts`, with the same keys in `id` and `en`. Never hard-code visible text in components.
- URLs and anchors are English, lowercase, hyphenated, plural for collections (`/templates/<category>/page/<n>/`, `#packages`). Indonesian is the default locale at `/`, English at `/en/`.

### CSS

- Component styles go in the component's scoped `<style>`. `src/styles/global.css` holds only design tokens, base element styles and cross-component utilities (`.section-pad`, `.field-row`, `.scroll-reveal`).
- Use tokens (`var(--blue)`, `var(--font-serif)`, `var(--header-height)`, …) instead of raw values that already have a token.
- One rule per selector (Stylelint enforces `no-duplicate-selectors`). Order: base rules, `@keyframes`, `@media` 1000px → 800px → 560px, then `prefers-reduced-motion`.
- Never use `filter: blur()` for decoration (Stylelint blocks it): Safari iOS clips it to a square inside rounded, overflow-hidden containers. Use `radial-gradient`.
- Constrain grid columns that hold text with `minmax(0, 1fr)`; Android falls back to a wider serif font.
- Respect `prefers-reduced-motion` for animations and transitions.

### Templates catalog

- Template data: `src/data/templates.json` (codes are permanent, never renumber). Live demos: add the code to `src/data/live-previews.json` only after the WordPress demo is ready. See `docs/template-catalog.md`.

### Git

- Conventional Commits (`feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `ci:`, `chore:`).
- Pushing to `main` deploys to production.

## Documentation

Project documentation: `docs/README.md`.

Astro documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
