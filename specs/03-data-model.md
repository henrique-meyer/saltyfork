# 03 · Data Model

## Recipe format
- Base: **schema.org `Recipe` JSON-LD**, extended with a namespaced vocabulary with the `saltyfork:` prefix (namespace URI is **Open** pending the domain). Published as a versioned spec with JSON Schema, examples and validators. Henrique maintains it.
- Every published version must be valid schema.org JSON-LD.
- Extension fields:
  - `saltyfork:ingredients[]`: `{text, amount, amountMax, unit, ingredient: {"@id": "https://<domain>/ingredients/{id}", sameAs: [FDC/Wikidata/FoodOn URIs]}, preparation, optional, group}`. The plain `recipeIngredient` strings are always kept too.
  - `saltyfork:steps[]`: ids, sections, timers, temperatures, ingredient refs per step.
  - `saltyfork:id`, `saltyfork:version`, `saltyfork:versionId`, `saltyfork:parent {recipeId, versionId}`, `saltyfork:origin {type: original|fork|import, sourceUrl, credit}`.
  - `saltyfork:credit`, `saltyfork:allergens`, `saltyfork:nutrition` (**always calculated**), `saltyfork:specVersion`.

## Core tables (PostgreSQL)
```
users        (id, entra_oid, handle UNIQUE, display_name, avatar_photo_id, plan, locale, created_at, deleted_at)
recipes      (id, owner_id, slug, status [draft_only|published|hidden|removed],
              visibility [private|unlisted|public], origin_type [original|fork|import],
              forked_from_version_id NULL, source_url NULL, current_version_id NULL,
              draft_doc JSONB NULL, draft_updated_at, created_at, deleted_at)
recipe_versions (id, recipe_id, version_no, doc JSONB, doc_hash, author_id, change_note, published_at)
              UNIQUE(recipe_id, version_no)  -- IMMUTABLE, append-only
credits      (recipe_id, upstream_recipe_id, upstream_version_id, upstream_author_id, text)
recipe_books (id, owner_id, name, is_default)
book_entries (book_id, recipe_id, pinned_version_id NULL, added_at)
photos       (id, owner_id, blob_key, width, height, alt, moderation_state, rights [own|permitted|unknown], created_at, deleted_at)
recipe_photos(recipe_version_id OR draft recipe_id, photo_id, position)
recipe_ingredients (id, recipe_version_id OR draft, position, group_label, original_text, amount, amount_max,
              unit_id, ingredient_id NULL, preparation, optional, alternatives[] ingredient_ids,
              unquantified, match_confidence, match_status [auto|confirmed|unmatched])
imports      (id, user_id, source_url, raw JSONB, parser, status, created_recipe_id)
reports, takedowns, ui_strings, moderation_audit
P2+: posts, post_photos, comments, follows, reactions, notifications
P3+: sites, site_pages, site_collections, api_clients
```
**Open:** how `recipe_photos` / `recipe_ingredients` reference a draft (PLAN.md says "version OR draft" without a concrete design). **Open:** `comments` keyed by version, recipe, or both (proposed: stored per version, shown across versions).

## Drafts, versions, forks
- **Draft:** one mutable `draft_doc` per recipe, overwritten on autosave. No history rows.
- **Publish:** validate → insert `recipe_versions` (`version_no+1`, `doc_hash`, photos by reference) → move `current_version_id`.
- **Published versions are never updated or deleted by the app.** Enforce with DB privileges and/or triggers (app role has INSERT/SELECT only on `recipe_versions`).
- **Fork:** new `recipes` row owned by the forking user, `forked_from_version_id` = exact parent version. Parent is untouched. Fork starts as a draft with the **fork content filter applied**: ingredients kept, steps rewritten neutrally (optional AI help + similarity check), **photos and story dropped**. Author credit and parent link kept forever.
- **Forks can never be blocked** by the author. No exceptions.
- **Save:** `book_entries` reference, no copy.
- **Delete:** soft delete by default ("removed by author"; forks keep author credit). Audited hard delete for takedown and privacy erasure requests: purges content and blobs, leaves a tombstone (id + reason). This is the only exception to immutability.

## Master ingredient database
Every recipe line keeps its original text and links to one canonical ingredient (`ingredient_id`).
```
ingredients (id, slug, canonical_name, parent_id NULL, entry_kind [generic|branded|recipe],
             status [provisional|verified|merged|retired], merged_into_id NULL,
             brand_name NULL, gtin NULL (indexed), recipe_id NULL, recipe_version_id NULL (pinned),
             nutrition_estimated, estimate_source_id NULL, confidence, usage_count,
             fdc_id NULL, off_code NULL, wikidata_qid NULL, foodon_iri NULL,
             density_g_per_ml NULL, created_by [ai|user|seed], created_at, updated_at)
ingredient_regions, ingredient_names (locale, name, type), ingredient_allergens (generic only),
ingredient_label_allergens (branded, reference only), ingredient_diet_flags, ingredient_units,
units, ingredient_nutrition (source, per_100g JSONB, ...), ingredient_evidence,
ingredient_suggestions, match_review_queue, moderation_audit
```
- Hierarchy via `parent_id` (Roma tomato → tomato; Oreo → chocolate sandwich cookie).
- Merges keep `merged_into_id` redirects so ids are stable.
- Unknown ingredients get a **provisional** entry immediately (never blocks import), filed under the closest generic parent, with the parent's nutrition copied as an **estimate** (`nutrition_estimated=true`, shown as "estimated").
- Recipe-as-ingredient: `entry_kind=recipe` pins a version. DAG check (recursive CTE) rejects cycles; depth cap (e.g. 5).
- Record the data source per row.

## Nutrition and allergens (core rule)
- **Always calculated** from linked ingredients and amounts. **Never trust stated values**: nutrition/allergens in source JSON-LD, text or creator claims are stripped on import and never shown.
- **Calculated allergens come from generic ingredients only.** Each generic entry lists only the US Big 9 allergens it inherently contains. Never inherited from parent, child or brand.
- Branded line: calculated allergens come from its generic parent.
- **Branded label info** (`ingredient_label_allergens`, label nutrition from FDC Branded or OCR) may be shown as **reference only**, labelled "Label data — may change over time" with source and date. Never used in calculations or filters.
- Alternatives ("butter or margarine"): allergens = union; nutrition uses the first option.
- Unquantified lines ("salt to taste"): counted for allergens, excluded from nutrition, marked "not counted".
- Recipe pages show: "Allergens and nutrition are calculated from generic ingredients. Always check product packaging. Formulas change."

## Open Food Facts (OFF)
- Kept in a **separate mirrored DB** (or separate Postgres schema `off_mirror` with its own role), refreshed from OFF's daily full export plus deltas. **Phase P2, after owner sign-off.**
- Used internally only: barcode → product name/brand, categories as hints for a generic parent.
- The app DB stores **only OFF product codes (`off_code`)** plus USDA, Wikidata, AI and user data. OFF facts (allergens, nutrition, images, ingredient text) are never copied in.

## Conflicts / gaps
- PLAN.md §4a phasing contradicts itself: the "Later (P2+)" list includes branded products and multi-locale names, but the "v2.4 phasing" puts them in P1. This spec follows v2.4.
- Wikidata is listed as a seed source for the generic tree, but Wikidata enrichment is scheduled for P2. Treat P1 seed as USDA only unless decided otherwise. **Open.**
