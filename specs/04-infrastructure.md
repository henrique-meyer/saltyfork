# 04 · Infrastructure (build first)

This is a **proposal**. Items marked **Decided** come from PLAN.md. Everything else is a suggestion for Codex to confirm with the owner.

## Decided by PLAN.md
- Azure. PostgreSQL Flexible Server. Blob Storage. Front Door. Entra External ID. Key Vault. App Insights / Log Analytics. Queue + workers.
- ASP.NET Core API and Next.js web as separate deployable apps.
- IaC: Bicep (PLAN.md says "Bicep/Terraform"; this spec uses Bicep per owner instruction).
- Budgets/alerts and capped log ingestion (cost control).

## Proposed environments
| Env | Purpose | Notes |
|---|---|---|
| `dev` | shared development | smallest SKUs, scale to zero, AI Search Free or none |
| `prod` | live | Postgres Burstable B1ms–B2s to start |
A `staging` environment is **Open** (cost vs safety). Local dev: Postgres in Docker, Azurite for storage.

## Proposed Azure resources (per environment)
- Resource group `rg-saltyfork-<env>`. Region: **Open**.
- Log Analytics workspace + App Insights (sampling on, daily cap).
- Key Vault (RBAC mode). All secrets here; apps read via managed identity. No secrets in repo or pipeline variables.
- User-assigned managed identities for API, web, jobs.
- PostgreSQL Flexible Server: app DB `saltyfork`; Entra auth enabled; separate roles for app (no UPDATE/DELETE on `recipe_versions`), migrations, and (P2) `off_mirror`.
- Storage account: containers `photos-original`, `photos-variants`; queues if Storage Queue is chosen.
- Container Registry (if Container Apps chosen).
- Container Apps environment (or App Service plan): `api`, `web`, and jobs. **Open:** Container Apps vs App Service.
- Front Door Standard + WAF in front of `web` and `api` (may be deferred in `dev` to save cost).
- Entra External ID tenant: one-time manual setup; document steps (Bicep support is limited).
- Budget + cost alerts per resource group.
- Search: start with Postgres full-text search; add AI Search later (cost lever). **Open.**

## Suggested repo layout (Open)
```
/infra        Bicep modules + per-env parameter files
/api          ASP.NET Core solution (+ tests)
/web          Next.js app
/jobs         seed/import jobs
/spec         format spec, JSON Schema, examples
/specs        these docs
/scripts      download scripts (e.g. OFF export download), never the data itself
```

## CI/CD (GitHub Actions, proposed)
- On PR: build + test API and web, lint, `bicep build` + what-if, OpenAPI generation check, pseudo-locale check (missing i18n keys), ingredient matcher eval gate (once it exists), test that no OFF fields reach public API responses.
- On merge to main: build images, push, deploy to `dev`. Promote to `prod` manually with approval.
- Auth to Azure via OIDC federated credentials (no stored secrets).
- DB migrations run as a separate pipeline step/job with the migrations role. Tool: **Open** (EF Core migrations likely).
- Guard: `.gitignore` and a CI check that block large data dumps (OFF exports) from the repo.

## Data jobs
### USDA FDC seed job (P1)
- Downloads FDC exports (Foundation / SR Legacy for generics; Branded Foods for branded entries).
- Loads the top ~2–3k common generic ingredients plus branded products into `ingredients`, `ingredient_nutrition`, `ingredient_units`, with `fdc_id` and data source per row.
- Idempotent (upsert by `fdc_id`), re-runnable when FDC updates. Selection rule for "top 2–3k": **Open**.
- Curated USDA seed files may live in the repo.

### Open Food Facts mirror import job (P2, after owner sign-off)
- Scheduled job (Function or Container Apps job): load daily full export, apply delta files between.
- Writes only to the separate OFF mirror DB/schema, using its own role. The app role can read for matching; public API code paths must not access it.
- Idempotent loads with validation; alert on failed refresh.
- The download script may be in the repo; the data never is.
- Can be built early in `dev` but must not run against `prod` until owner sign-off. **Open:** separate server vs separate schema.

## First tasks for Codex (suggested order)
1. Repo skeleton, `.gitignore`, CI that builds empty API and web.
2. Bicep for `dev`: RG, Log Analytics, App Insights, Key Vault, identities, Postgres, Storage, Container Apps env/ACR.
3. Deploy pipeline with OIDC to Azure.
4. DB migrations baseline: core tables + immutability privileges/triggers on `recipe_versions`.
5. Entra External ID sign-in on API.
6. `ui_strings` table + build-time export + pseudo-locale CI check.
7. USDA seed job.
8. Budgets/alerts, then `prod` parameters.

## Open
Region; staging env; Container Apps vs App Service; Functions vs Container Apps jobs; Service Bus vs Storage Queue; migration tool; AI provider; OFF mirror topology; domain (needed before Front Door custom domain and stable ingredient URIs).
