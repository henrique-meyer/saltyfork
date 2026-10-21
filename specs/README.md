# SaltyFork: Project Specs

A platform for storing, sharing and forking recipes.

- Repo: https://github.com/henrique-meyer/saltyfork
- Owner: Henrique Meyer
- Source of truth: `PLAN.md` v2.6 (Oct 13, 2026). If these specs and PLAN.md disagree, PLAN.md wins until the conflict is resolved. Conflicts are listed in each file under "Conflicts / gaps".
- Status: draft. Items marked **Open** are not decided. Do not pick an answer for them without asking the owner.

## Files

| File | What it covers |
|---|---|
| [01-product.md](01-product.md) | Vision, users, features, phases (P1–P4), milestones, open questions |
| [02-architecture.md](02-architecture.md) | Azure hosting, ASP.NET Core API, Next.js web, Postgres + JSONB, AI, API design, i18n |
| [03-data-model.md](03-data-model.md) | Recipe format (schema.org + `saltyfork:`), tables, drafts/versions/forks, ingredient DB, nutrition/allergens, OFF mirror |
| [04-infrastructure.md](04-infrastructure.md) | What to build first: Azure resources, environments, Bicep, CI/CD, Key Vault, seed/import jobs |

## Start here (for Codex)

Start with infrastructure (`04-infrastructure.md`), then the data model (`03-data-model.md`). The API comes first; the web app is just the first client of that API.

## Domain note

The **domain is Open** (PLAN.md §11 Q1). Keep it in config (never hard-coded), because ingredient URIs and the `saltyfork:` namespace URI depend on it and must never change once live.
