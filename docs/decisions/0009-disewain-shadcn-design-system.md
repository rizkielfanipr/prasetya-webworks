# ADR 0009 — Disewain-inspired, shadcn-style design system

## Status

Accepted — 24 October 2026

## Context

The website used a bespoke dark-blue visual language with repeated component styling. The new direction is based on the supplied Disewain design specification: warm orange accents, cream surfaces, Raleway headings, Plus Jakarta Sans body text, 16px radii and restrained elevation.

The site is statically rendered with Astro. Introducing React hydration for static buttons and cards would increase client JavaScript without improving behaviour.

## Decision

- Use shadcn's source-owned component model and semantic token vocabulary (`background`, `foreground`, `card`, `primary`, `border`, `ring`, and radius).
- Keep static primitives Astro-native. `Button.astro` and `Card.astro` live in `src/components/ui/` and are editable project source, following shadcn composition and variant conventions.
- Hydrate framework components only when interaction genuinely requires client state. Existing native `dialog` and `details` implementations remain because they are accessible and require no framework runtime.
- Map the previous token aliases to the new semantic tokens while the component migration is completed, avoiding duplicated color sources.
- Use Raleway for display/heading roles and Plus Jakarta Sans for body and interface roles.
- Support the measured light theme only. A dark theme is not inferred from the supplied design specification.

## Consequences

- Indonesian and English routes share one token source and one visual system.
- Existing routing, content, forms, scripts and static deployment remain unchanged.
- The site gains shadcn-style primitives without adding unnecessary browser JavaScript.
- Future generic controls should be added under `src/components/ui/` and consume semantic tokens rather than page-specific raw colors.
