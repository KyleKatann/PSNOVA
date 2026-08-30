# PSNOVA Agent Guide

## Purpose

This repository is the source for the PSNOVA攻略サイト published with GitHub Pages.
Modernization work must preserve existing data and URLs while improving usability, maintainability, SEO, accessibility, and monetization readiness.

## Non-negotiable workflow

1. Change one implementation item at a time.
2. Before changing data-heavy pages, treat existing game data as the source of truth unless the task explicitly changes the data.
3. Add or extend a test whenever the change can be checked automatically.
4. Commit each completed implementation item separately with a descriptive commit message.
5. Do not combine unrelated refactors with a functional change.
6. Keep existing public URLs under `/PSNOVA/` stable unless a separate migration decision is made.
7. If a change causes a regression found during final validation, fix or revert only that item rather than continuing on top of a broken state.
8. GitHub Actions tests are manual-only. Do not run them after each commit. Complete the planned implementation batch first, then trigger the `tests` workflow once with `workflow_dispatch` for final validation.
9. Never use image-generation tools for this project. All visual changes must be implemented with repository HTML/CSS/JavaScript and existing approved assets only.
10. Keep the repository-root `reference/` archive. It contains historical PSNOVA/wiki source material used for design and data verification and must not be deleted during legacy-code cleanup.

## Recovery point

The pre-modernization site is preserved in Git history and in:

- Branch: `backup/pre-modernization-20260830`
- Source commit at backup creation: `cb3ac9bdc6b6551a18f2ced40e57d152f9e6b2a6`
- Historical source/reference material: repository-root `reference/`

Do not modify or repurpose the backup branch. `reference/` may be read for comparison, but keep the archive intact.

## Design direction

Use an information-first Japanese game-guide design with strong readability. Game8 may be used only as a reference for **color-placement pattern, hierarchy, contrast, spacing, navigation, and state treatment**. Do not copy its actual color palette, branding, proprietary graphics, or exact composition.

Principles:

- Clean and lightweight.
- Data-first rather than decorative.
- Strong visual hierarchy and contrast.
- Use the pattern `dark navigation / light content surface / one clear accent / separate link color`, but use PSNOVA-specific colors.
- Current PSNOVA palette: cool navy navigation, white surfaces, cool indigo accent, muted blue links, and pale blue-gray page background.
- Do not use Game8-style yellow as the site accent color.
- Search and filters should be prominent.
- Current/selected navigation states must be immediately visible.
- One-column mobile layout.
- Tables prioritize readability and comparison.
- For data tables, the original PSNOVA wiki/HTML is an approved internal reference: use compact cells, clear 1px-style grid separation, pale blue data surfaces, and existing native category icons where available.
- Do not restore old wiki editor/action icons such as add/edit/paragraph-edit controls; only gameplay/category identification icons should return.
- Avoid neon, scanlines, heavy animation, large decorative effects, or intrusive ads.
- Dark mode may be added later, but it must remain visually restrained.
- Keep the homepage hero/illustrative image, but do not use large screenshots or illustrative JPEGs on internal data pages.
- Prefer the game's existing compact native PNG icons for weapon/class/category identification. If no suitable native icon exists, use a restrained CSS marker rather than adding decorative imagery.

## Implementation backlog

Work through this list sequentially unless a dependency requires otherwise.

### Priority S

1. Fix mobile hamburger menu rendering without a missing image dependency. **Implemented**
2. Prevent the mobile sidebar from blocking access to the main content. **Implemented**
3. Remove `document.write()` from shared navigation/sidebar rendering. **Implemented**
4. Remove latent shared-JS errors such as invalid `appendChild("span")` usage. **Implemented**
5. Establish the modern information-first visual foundation. **Implemented**
6. Simplify and modernize the header/navigation. **Implemented**
7. Simplify and modernize the sidebar/navigation. **Implemented**
8. Modernize tables as data-oriented UI. **Implemented**
9. Add weapon-name search. **Implemented**
10. Add weapon filters such as type, rarity, and shop level. **Implemented**
11. Add numeric sorting for useful weapon columns. **Implemented**
12. Add persistent search entry points to data pages and later the site home. **Implemented**

### Priority A

13. Add in-page category navigation for large data pages. **Implemented**
14. Normalize table semantics using `thead`, `tbody`, `th`, and `td` correctly. **Implemented**
15. Move deprecated presentational HTML such as `bgcolor` and inline table styling into CSS. **Implemented**
16. Remove duplicate/conflicting CSS rules while preserving behavior. **Implemented**
17. Reduce hard-coded absolute internal URLs where safe. **Implemented**
18. Give every important page a unique descriptive `<title>`. **Implemented via shared page metadata.**
19. Give every important page a unique meta description. **Implemented via shared page metadata.**
20. Remove obsolete `meta keywords` tags. **Implemented at runtime.**
21. Add canonical URLs. **Implemented via shared page metadata.**
22. Add `sitemap.xml`. **Implemented**
23. Add or review `robots.txt`. **Implemented as a project-site policy file; note that host-root robots policy requires control of `kylekatann.github.io/`.**
24. Add Open Graph metadata where useful. **Implemented for JS-aware clients; static head metadata remains preferable for non-JS social crawlers.**
25. Add explicit image width/height to reduce layout shift. **Implemented for verified key assets.**

### Priority B

26. Lazy-load below-the-fold images where appropriate. **Implemented**
27. Remove duplicate image assets. **Implemented**
28. Optimize large images while preserving acceptable quality. **Deferred: requires a binary image-processing pass that can verify output quality and size.**
29. Move generation notebooks/tools out of the public `docs/` tree. **Implemented**
30. Remove `.ipynb_checkpoints` from version control and ignore them. **Implemented**
31. Separate `data/`, `tools/`, and `docs/` concerns. **Implemented**
32. Move authoritative game data toward CSV/JSON rather than generated HTML. **Deferred: migrate one verified dataset at a time without changing gameplay values.**
33. Generate data-heavy HTML from authoritative structured data. **Deferred until item 32 has a verified source dataset.**
34. Add restrained hover/transition behavior. **Implemented**
35. Add sticky filter/table headers where useful. **Implemented**
36. Improve compact rarity/status presentation without decorative excess. **Implemented**
37. Remove internal-page illustrative screenshots and use compact native icons/markers instead. **Implemented**
38. Rework the visual system toward a high-contrast Japanese guide-site layout while preserving PSNOVA identity and using a distinct PSNOVA palette. **Implemented**
39. Restore the original wiki-style compact table density and native weapon-category icons in data rows without restoring editor/action icons. **Implemented**

### Monetization backlog

Google display ads are deferred for now.
Prefer unobtrusive link-based affiliate placements.

40. Replace the current Rakuten banner with contextual text/product links where practical. **Implemented**
41. Evaluate Surugaya affiliate text links for used PS Vita software, hardware, and guidebooks. **Pending account/affiliate link registration.**
42. Evaluate Amazon Associates text links for related products. **Pending account/affiliate link registration.**
43. Evaluate ValueCommerce LinkSwitch for supported merchant links. **Pending account/affiliate link registration.**
44. Add consistent and clearly visible PR/affiliate disclosure styling. **Implemented**

## Testing policy

Automated tests should focus on regressions that are cheap to detect statically.
Examples:

- Referenced local assets exist.
- Shared navigation contains expected core links.
- No `document.write()` remains after that migration item is completed.
- No invalid `appendChild` string calls remain.
- Required pages keep valid titles and metadata.
- Internal links use expected paths and do not unintentionally change established public URLs.
- Data tables retain expected row counts or known sentinel records when refactored.
- Internal data pages do not display large illustrative JPEG screenshots; compact native PNG icons remain allowed.
- Data-table styling keeps the compact wiki-derived grid and native weapon icon mapping while preserving semantic `thead/tbody/th/td` structure.
- The modern visual layer retains defined contrast tokens for cool navy navigation, white surfaces, PSNOVA indigo accents, and muted blue links.
- The palette must not regress to copied Game8 yellow accent values.
- Repository-root `reference/` remains present after cleanup work.

Tests belong under `tests/` and should use the Python standard library where possible so the repository has no unnecessary test dependency.
Add tests alongside each implementation item. The GitHub Actions `tests` workflow must not run on `push` or `pull_request`; trigger it manually once with `workflow_dispatch` after the planned implementation batch is complete.

## Definition of done for each item

An implementation item is ready for final validation when:

- The change is implemented.
- Relevant automated tests are added or updated when feasible.
- The public-site behavior is not knowingly regressed on desktop or mobile.
- The item has its own clear commit.

The implementation batch is complete only after the manually triggered final GitHub Actions run passes.

## Data safety

Do not silently alter gameplay values, names, materials, rarity, shop levels, or other source data while changing layout or code structure.
When a data correction is needed, make it a separate change with its own evidence and test/sentinel update.
