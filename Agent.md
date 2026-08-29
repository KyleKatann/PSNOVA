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
8. During a multi-item implementation run, do not trigger or inspect GitHub Actions after every item. Complete the planned implementation items first, then run/check the full GitHub Actions test suite once at the end.

## Recovery point

The pre-modernization site is preserved in:

- Branch: `backup/pre-modernization-20260830`
- Source commit at backup creation: `cb3ac9bdc6b6551a18f2ced40e57d152f9e6b2a6`

Do not modify or repurpose that branch.

## Design direction

Use a SteamCozy-style information-first design rather than an SF/HUD theme.

Principles:

- Clean and lightweight.
- Data-first rather than decorative.
- Light neutral surfaces with restrained accent colors.
- High information density without visual clutter.
- Search and filters should be prominent.
- One-column mobile layout.
- Tables prioritize readability and comparison.
- Avoid neon, scanlines, heavy animation, large decorative effects, or intrusive ads.
- Dark mode may be added later, but it must remain visually restrained.

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
18. Give every important page a unique descriptive `<title>`.
19. Give every important page a unique meta description.
20. Remove obsolete `meta keywords` tags.
21. Add canonical URLs.
22. Add `sitemap.xml`.
23. Add or review `robots.txt`.
24. Add Open Graph metadata where useful.
25. Add explicit image width/height to reduce layout shift.

### Priority B

26. Lazy-load below-the-fold images where appropriate.
27. Remove duplicate image assets.
28. Optimize large images while preserving acceptable quality.
29. Move generation notebooks/tools out of the public `docs/` tree.
30. Remove `.ipynb_checkpoints` from version control and ignore them.
31. Separate `data/`, `tools/`, and `docs/` concerns.
32. Move authoritative game data toward CSV/JSON rather than generated HTML.
33. Generate data-heavy HTML from authoritative structured data.
34. Add restrained hover/transition behavior.
35. Add sticky filter/table headers where useful.
36. Improve compact rarity/status presentation without decorative excess.

### Monetization backlog

Google display ads are deferred for now.
Prefer unobtrusive link-based affiliate placements.

37. Replace the current Rakuten banner with contextual text/product links where practical.
38. Evaluate Surugaya affiliate text links for used PS Vita software, hardware, and guidebooks.
39. Evaluate Amazon Associates text links for related products.
40. Evaluate ValueCommerce LinkSwitch for supported merchant links.
41. Add consistent and clearly visible PR/affiliate disclosure styling.

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

Tests belong under `tests/` and should use the Python standard library where possible so the repository has no unnecessary test dependency.
Add tests alongside each implementation item, but run/check the complete GitHub Actions suite once after the planned implementation batch is finished.

## Definition of done for each item

An implementation item is ready for final validation when:

- The change is implemented.
- Relevant automated tests are added or updated when feasible.
- The public-site behavior is not knowingly regressed on desktop or mobile.
- The item has its own clear commit.

The implementation batch is complete only after the final GitHub Actions run passes.

## Data safety

Do not silently alter gameplay values, names, materials, rarity, shop levels, or other source data while changing layout or code structure.
When a data correction is needed, make it a separate change with its own evidence and test/sentinel update.
