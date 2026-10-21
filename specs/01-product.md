# 01 · Product

## Summary
SaltyFork is a public platform for storing, sharing and forking recipes, a kind of "GitHub for recipes" with a social layer. Recipes use an open, versioned format based on schema.org `Recipe` JSON-LD, so any app can read and write them.

**Principles:** open format with no lock-in (users can export everything); publishing is permanent and credited to authors; pages are fast and ad-free.

## Users
- **Home cooks (launch focus, free):** private recipe book, import from anywhere, save and fork others' recipes, "cooked it" photos (P2).
- **Creators (seeded early):** a small invited group publishes good public content from launch. A waitlist for creator sites (P3) opens at launch.
- **Brands/businesses (later):** branded collections and sites.
- **Developers/partners (later):** use the API and format.

## Market and pricing
- US only at launch, English UI. All UI strings live in language files from day one (see 02). EU and Brazil come later.
- **Free for everyone at launch.** All AI features are free on every tier. Free pages have no ads and no affiliate links.
- PLAN.md §2 also drafts paid tiers (Creator ~$8–12/mo, Pro/Brand, API usage) starting in P3. Prices are indicative only. **Open:** final pricing.

## Features by phase

### P1: MVP (US launch)
- Private recipe book; save = reference to a recipe (follows latest or pinned version).
- Import from URL, paste or file. Imports stay private until reworked (see 05).
- Drafts (editable), publishing (immutable versions), forking with author credit. Forks cannot be blocked.
- Master ingredient DB core: USDA FDC seed (~top 2–3k generic ingredients) plus FDC Branded, line parser + AI matcher, review queue, Big 9 allergens, diet flags, unit conversion, basic nutrition, recipe-as-ingredient lines, provisional auto-created entries, en-US names.
- Public SEO-friendly recipe pages with JSON-LD and Open Graph share cards.
- Search, with allergen/diet filters and basic nutrition.
- Export (whole book as JSON-LD zip).
- Open format spec v0.1.
- i18n foundation (ICU messages, locale-aware formatting).
- Creator invite program and creator-site waitlist.
- Soft delete and audited hard delete.

### P2: Social and safety
Follows, feed, comments, "cooked it" posts, likes/saves, notifications. Moderation (reporting, review queue, automated image/text screening), anti-spam (rate limits, new-account limits, CAPTCHA), takedown tooling. Ingredient DB enrichment: internal Open Food Facts mirror (after owner sign-off), barcode and label-photo OCR, AI duplicate merging, Wikidata/FoodOn links, user suggestions UI, pantry search.

### P3: Creators and developers
Grocery lists and meal planning, public ingredient API, paid creator sites (themes, custom domains, TLS), Stripe billing, WordPress/WPRM migration, public developer API (keys, OAuth, quotas, docs), browser extension, PWA share-sheet import.

### P4: Mobile and distribution
Native iOS/Android apps, automatic posting to social accounts.

## Milestones (indicative, from PLAN.md §9)
| Weeks | Milestone |
|---|---|
| 1–2 | Format spec v0.1, data model, Azure landing zone (IaC), CI/CD, Entra sign-in, i18n store + ICU, unit/locale formatting |
| 3–5 | Core API: recipes, drafts, publish→versions, books, photos, OpenAPI |
| 6–7 | Import pipeline; ingredient DB schema + USDA seed, parser + matcher, review queue |
| 8–9 | Forking, author credit, fork content filter/rewrite assist; soft/hard delete |
| 10–11 | Web app: book, editor, public pages, search and allergen filters |
| 12 | Hardening, ToS/privacy/takedown process, beta + creator seeding → **P1 US launch** |
| 13–20 | P2 |
| 21–32 | P3 |
| 33+ | P4 |

## Open questions
1. **Comments per version or per recipe?** PLAN.md proposes: stored per version, shown across all versions. **Open** until confirmed. Affects the `comments` table and P2 UX.
2. **Minimum user age?** 13+ (US, COPPA) is the candidate. **Open.**
3. **Creator cohort:** size, selection criteria, and what invited creators get. **Open.**
4. **Domain** (and trademark check for "SaltyFork"). **Open.** Ingredient URIs and the spec namespace depend on it.
5. Final pricing for paid tiers. **Open.**
