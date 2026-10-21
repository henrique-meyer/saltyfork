# 02 · Architecture

## Decided
- **Hosting:** Microsoft Azure.
- **Core API:** ASP.NET Core (C#). Runs as its own Container App or App Service.
- **Web and creator sites:** Next.js (TypeScript) for server rendering, SEO and (later) multi-tenant sites by hostname.
- **Database:** Azure Database for PostgreSQL Flexible Server. Relational tables plus JSONB for recipe documents.
- **Auth:** Entra External ID (OIDC).
- **API first:** the web app uses the public API surface (plus a few internal endpoints).
- **All AI is free for every user.** AI cost is an operating expense, tracked per active user in App Insights.
- **No ads or affiliate links** on free pages, profiles or the feed.
- **US launch, en-US only,** but every UI string is in language files from day one.

## Open (to finalize with the coding agent)
- ORM (EF Core suggested in PLAN.md), libraries, repo layout (monorepo assumed but not decided).
- Container Apps vs App Service for web and API.
- Azure Functions vs Container Apps jobs for workers.
- Service Bus vs Storage Queue.
- Azure region.
- Search: start with Postgres full-text search and add Azure AI Search when needed (cost lever), or AI Search from day one.

## Components
```
Clients: Web (Next.js) · later extension, PWA, native apps, 3rd-party apps
      │  same versioned API
Azure Front Door (CDN, WAF, TLS; later custom domains)
      │
 Web/SSR app (Next.js)      Core API (ASP.NET Core) ── Entra External ID
                              ├─ PostgreSQL Flexible Server (app DB)
                              ├─ Blob Storage (photo originals, resized variants)
                              ├─ Search (Postgres FTS first, or Azure AI Search)
                              ├─ Queue ─► workers: import, image resize+moderation,
                              │           search indexing, nutrition calc, notifications, sitemap
                              ├─ OFF mirror (separate DB or schema, internal only; P2)
                              └─ Key Vault, App Insights / Log Analytics
```

## Key flows
- **Import:** URL → queue → worker fetches (respects robots.txt, timeouts, size caps) → parse JSON-LD (`Recipe`, `@graph`) → fallback to microdata/heuristics/LLM → normalize to the format → strip stated nutrition/allergens → parse and match ingredients → save as private import.
- **Publish:** validate draft (every ingredient line resolved) → write immutable version → compute nutrition/allergens → emit event → indexer updates search.
- **Recipe pages:** server-rendered, cached at Front Door. Cache keys use immutable version ids. Each page has JSON-LD, Open Graph/Twitter cards and a generated share image.

## AI
Used for: ingredient matching (embedding similarity + LLM choice among DB candidates), import extraction fallback, fork rewrite assist (user reviews; similarity check), moderation, and later translation.
- Matching accuracy is a hard requirement: tracked against a labeled evaluation set, **gated in CI**.
- Low-confidence matches go to the author to confirm. A recipe cannot be published until every line is resolved.
- AI moderation has no human team at launch. Every decision goes to `moderation_audit` (model, version, confidence, rationale) and can be reverted. Henrique does periodic sample reviews.
- Cost control: cache results, smaller models for routine matching, batching, per-user rate limits.
- **Open:** model provider/deployment (e.g. Azure OpenAI is not named in PLAN.md).

## API
- REST + JSON. OpenAPI 3.1 generated from code; that spec is the contract.
- Responses in the format's JSON-LD: `application/ld+json; profile=saltyfork/v1`.
- URL versioning: `/v1`.
- Resources: `/recipes`, `/recipes/{id}/versions/{n}`, `/recipes/{id}/draft`, `/recipes/{id}/fork`, `/books`, `/imports`, `/users/{handle}`, `/search`, `/posts`, `/comments`, `/sites`.
- Version endpoints are immutable and cacheable (ETag = `doc_hash`).
- Auth: Entra OIDC for users; scoped OAuth for third-party apps (P3); API keys for read-only public data. Quotas/rate limits per client (API Management later).
- Bulk export of a user's book (JSON-LD zip) always available. Webhooks in P3.
- Public responses must never contain Open Food Facts fields (enforced by a test; see 05).

## Internationalization
- No hard-coded UI strings. Keys like `recipe.publish.confirm`, in ICU MessageFormat.
- Source of truth: DB table `ui_strings (key, locale, message, status [source|machine|reviewed], updated_at)`, exported to locale files at build time (no runtime DB lookups). Fallback to `en-US`.
- CI runs a pseudo-locale to catch missing keys and truncation.
- Dates/numbers/currency via `Intl`/CLDR. Units stored canonically (metric base + original unit), shown in US customary or metric per user. °F/°C.
- Recipes carry a `language` tag. Recipe translation is later.
- AI-assisted UI translation with human approval is planned (not needed at launch).
