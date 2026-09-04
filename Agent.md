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
11. Migrate historical reference pages one page at a time. Preserve gameplay facts and useful guide content, remove archived Wiki/Wayback chrome, analytics, ads, edit controls, and dead archive-only links, then register the new public page in sidebar, page metadata, site search, and sitemap in the same implementation item.
12. **Runtime JavaScript must never repair, normalize, sanitize, or reinterpret source HTML or source game data.** Do not use JavaScript to create, move, replace, or convert semantic table structure (`thead`, `tbody`, `tr`, `th`, `td`), remove deprecated presentation attributes/styles, repair malformed markup, or clean source text/data. Fix the raw HTML or its generator instead. JavaScript may only enhance already-valid markup, for example search, filtering, sorting, navigation, state classes, visual category classes, and scroll wrappers.
13. **Data-table alignment must follow content semantics, not arbitrary column position.** Names, codes, numbers, rarity, stats, materials, and other compact data are centered by default. Explanatory prose, notes, prose-style effects, acquisition methods, locations, and quest-name lists are left aligned. Implement this with source-aware shared CSS or explicit static markup; JavaScript must not infer or repair alignment semantics at runtime.
14. **Every user-reported regression that establishes a corrected specification must be recorded in this guide in the same implementation item.** Add a regression test where practical. Do not later reintroduce behavior that the user explicitly identified as wrong.
15. **Public UI copy must use clear reader-facing Japanese rather than developer-facing field names, camelCase, internal identifiers, or unexplained mixed-language abbreviations.** Labels such as `Shop Lv`, `ShopLv`, `shopLv`, and `ショップLv` are prohibited in visible UI; use `ショップレベル`. Conventional game terms such as HP, GP, DLC, PSNOVA, and official names may remain when they are standard and immediately understandable in context.
16. **All table column headers must be centered.** Body-cell alignment may remain semantic, including left-aligned prose, notes, locations, and quest lists, but those body rules must never override the visual centering of the actual header row.
17. **Do not add automatic in-page section navigation bars.** The generated `ページ内` link strip was judged unnecessary and must remain removed. Use the page structure, headings, sidebar, search, and purpose-built navigation only where they add clear value.
18. **Guide and data pages should begin with a concise reader-facing introduction, normally about three sentences.** Explain what the page covers, what can be compared or checked, and how the information is useful. Avoid placeholder-like one-line descriptions or copied wiki fragments.
19. **All pale-blue UI surfaces used by data tables must use the same existing UI token, `var(--accent-soft)`.** Do not introduce page-specific pale-blue hex colors for table headers or blue emphasis cells. Semantic non-blue status colors may remain distinct where they convey gameplay meaning.
20. **Data tables must use restrained 1px grid lines based on the shared border token.** Grid lines should improve row/column tracking without becoming visually dominant; do not return to heavy dark borders or 1px colored gaps between every cell.
21. **Public page titles follow one naming convention.** The homepage title is exactly `PSNOVA攻略サイト`. Every other public page title is `PSNOVA攻略サイト - XXXXX`, where `XXXXX` is the concise reader-facing page name such as `武器`, `防具`, `初心者Q&A`, or `ナックル`. The title suffix, main visible page heading, metadata mapping, and actual page purpose must not contradict one another. Do not use reversed forms such as `武器 | PSNOVA攻略`, verbose SEO keyword chains, or a generic `PSNOVA 攻略サイト` title on a specific content page. Prefer the same convention in raw HTML; runtime metadata must not be used to conceal a knowingly incorrect source title.
22. **Never hotlink site-display assets from external websites.** Images, fonts, CSS, JavaScript, and other visual/runtime assets used by the public site must be stored in this repository and referenced with local `/PSNOVA/...` paths. Do not use remote image URLs, CDN asset URLs, or other external-site asset references. Intentional reader navigation such as approved affiliate links is a separate concern and is not an asset hotlink.
23. **Do not increase the number of public CSS files.** The public CSS file count must never exceed two. `docs/css/style.css` owns shared/sitewide styles and `docs/css/page.css` owns page-specific styles such as homepage and weapon UI. Extend or consolidate these existing owners instead of adding another stylesheet; further consolidation may reduce the count, but stylesheet proliferation is prohibited.

## Correction-derived invariants

- Preserve the user-approved PSNOVA color palette. Do not automatically darken or replace site colors solely to satisfy automated contrast checks. Automated axe audits intentionally exclude `color-contrast` unless the user explicitly requests color-accessibility enforcement.

- Mobile navigation keeps a logical keyboard focus path: shared initialization moves `#menubar_hdr` into `#container > header` before interaction; opening the攻略 drawer moves focus to its first link; Escape closes the drawer and returns focus to the trigger. Do not use positive `tabindex` values to repair focus order.

- Dynamic widgets must expose valid accessible names and ARIA semantics. The site-data search is an editable `combobox` controlling `#site-search-results`; rendered affiliate image links must have a discernible accessible name even when their remote images use empty alt.

- Every public page footer exposes the site-information pages `/PSNOVA/copyright.html` and `/PSNOVA/issue.html`. Keep all public pages reachable from `/PSNOVA/` through internal navigation; do not silence the orphan-page regression test with allow-lists.

- Every public HTML page must remain reachable from `/PSNOVA/` through public internal links, including links supplied by the shared sidebar. `tests/test_public_navigation_reachability.py` guards against orphan public pages.

- Public `<img>` elements declare both numeric `width` and `height` using the source image's intrinsic dimensions. CSS remains responsible for responsive rendered sizing; the HTML dimensions reserve the correct aspect ratio before image load and reduce layout shift.

- Public pages load the four shared head scripts (`openclose.js`, `fixmenu_pagetop.js`, `menubar.js`, `sidebar.js`) with `defer`. Public HTML must not contain inline initialization scripts; shared components initialize themselves from external JS after parsing while preserving document-order execution.

- Every public page explicitly declares the repository-owned `/PSNOVA/img/logo.png` as its favicon. Keep favicon resources local to the repository and do not introduce external icon hotlinks.

- Homepage descriptive tables use explicit row-header semantics: the label cell at the start of each 商品概要 and 公式サイト row is `<th scope="row">`. Reserve `scope="col"` for actual column headers.

- The shared `#sub` sidebar is generated by `docs/js/sidebar.js` as a native `<aside id="sub">` containing the named攻略 navigation. Do not regress the complementary sidebar landmark to a generic `div`.

- Every public page uses exactly one native `<main id="main">` landmark for its primary content. The sitewide skip link targets this element with `href="#main"`; do not regress it to a generic `div` or duplicate the main landmark.

- Every public page begins with a keyboard-accessible skip link to `#main`. Keep the link visually hidden until focus so keyboard and assistive-technology users can bypass repeated site navigation.

- Use `python tools/psnova_quality.py finish` as the normal post-fix quality gate. It runs `git diff --check` and the complete pytest suite after every fix, and automatically runs the full Playwright UI-health suite only on every fifth completed fix. Use `targeted` only for changes that directly affect browser UI behavior, and use `inventory` to list remaining static audit candidates.

- Active repository text files use LF line endings on every platform via `.gitattributes` (`* text=auto eol=lf`). Historical material under `reference/` and `docs/pages/分類中/` is excluded from newline normalization and must remain byte-preserved.

- Public HTML uses the modern HTML shell: do not restore obsolete `X-UA-Compatible` metadata or redundant `type="text/javascript"` attributes on classic scripts.

- Local Playwright UI health tests are designed for full logical-CPU parallelism: use `fullyParallel: true` and `workers: '100%'`. The local test server must use a maximum OS socket backlog, threaded request handling, and HTTP/1.1 persistent connections. Published `kylekatann.github.io/PSNOVA/` assets must be fulfilled directly from repository files rather than re-fetched through the localhost server. Do not reduce worker count as a workaround for connection-refusal failures; fix the shared test infrastructure instead.

These are specifications established by user review and must be treated as regression constraints:

- Public CSS has two owners only: `docs/css/style.css` for shared/sitewide styles and `docs/css/page.css` for page-specific styles. Do not create a third public stylesheet; add rules to the appropriate existing owner instead.
- Rarity presentation has exactly one CSS owner in `docs/css/style.css`, and the weapon-page rarity display is the canonical visual specification for the whole site: `★` badge treatment, tabular numerals, and the 1-3 blue / 4-6 green / 7-9 red / 10-12 orange / 13-15 violet color scale. `page.css` must not contain rarity styling. Shared JavaScript may add rarity classes/attributes without rewriting source text; if source HTML already contains a visible `★`, suppress only the decorative pseudo-star so `★★` is never displayed.
- Data tables retain the compact original-wiki treatment: pale blue header/emphasis surfaces, compact padding, restrained 1px separation, and modern scrolling/search/sort behavior. Removing runtime HTML repair must not remove this visual treatment.
- All table pale-blue UI surfaces use the same `var(--accent-soft)` color across every page. Table body cells use neutral surfaces unless a semantic status color is intentionally required.
- Tables use subtle 1px grid lines in the shared border color so rows and columns remain easy to track without visually heavy borders.
- Table column headers are always centered and use static semantic source markup with `<thead>` and `<th scope="col">`. Semantic left alignment applies only to body content such as notes, explanations, locations, acquisition methods, and quest lists.
- Legacy table compatibility styling is prohibited. Shared CSS must not branch on obsolete `bgcolor`, all-`th` body rows, missing `<thead>`, or first-row position to infer historical Wiki markup. Fix current public source HTML statically instead.
- `docs/pages/分類中/` is historical staging/reference material, not a live public-site source. Do not rewrite it during public-page modernization, and keep it excluded from the GitHub Pages build.
- Public labels must be natural reader-facing Japanese. Developer-facing or unexplained labels such as `Shop Lv`, `shopLv`, and `ショップLv` must not appear; display `ショップレベル` instead.
- Automatic in-page navigation strips such as the former `ページ内` bar are intentionally not used and must not be restored.
- Weapon section headings show exactly one weapon icon. Do not combine a CSS background weapon icon with an injected `<img>` for the same heading. Row/category icons may remain where intentionally separate.
- The weapon landing-page catalog shows one existing native weapon PNG beside each of the 11 weapon-type labels. These selector cards must not regress to text-only cards, and icon visibility must not depend on runtime JavaScript.
- Individual weapon detail pages use an ordinary static `<h2>` weapon-type heading above one static weapon table. The table must not be wrapped in `<details>` / `<summary>` and must not rely on JavaScript to force a disclosure widget open.
- On desktop (`min-width: 801px`), weapon search/filter toolbars use `position: sticky` and remain visible near the top of the viewport after the reader scrolls to them. They use no card shadow. Weapon table headers must remain in normal document flow on every viewport and must never use `position: sticky`; `.table-scroll` owns horizontal overflow, so sticky descendant headers can resolve their offset against that wrapper and appear below body rows. No table column may be fixed or horizontally sticky.
- `class.html` is the four-class guide (Hunter, Ranger, Force, Buster), not weapon data. `skill.html` is skill data, not armor data. Do not overwrite these pages with copied content from another data page.
- The Gigantes page includes the トアス種, ゴルドス種, and アフォル種 families in addition to the other Gigantes families. They must not be removed or reclassified as ordinary enemies without explicit evidence and approval.
- On desktop (`min-width: 801px`), Gigantes data tables must fit within the main content width and must not use horizontal scrolling. On mobile (`max-width: 800px`), `.gigantes-table-scroll` may scroll horizontally.
- In Gigantes tables, each entry in the `難易度SH以降での出現クエスト` column must stay on one line; existing explicit `<br>` separators between quest entries remain. The adjacent `備考` column is the flexible wrapping column and should absorb width by wrapping prose.
- Multi-stage Gigantes names must use an explicit cell-internal `<br>` before stage labels such as `(第一段階)`, `(第二段階)`, and `(第三段階)` rather than relying on arbitrary browser text wrapping.
- The Gigantes page labels the first table `大型ギガンテスデータ` and the second table `小型ギガンテスデータ`. Both tables use the same Gigantes table-layout rules: no horizontal scrolling on desktop, horizontal scrolling on mobile, wrapping in `備考`, and no automatic wrapping within each `難易度SH以降での出現クエスト` entry.
- The material-page `コア` table preserves the archived source Wiki rarity as visible star values, for example `スモール・コア = ★1`, `ダーカー・コア = ★2`, and `ギガンテス・コア = ★7`. The archived Wiki's same-color numeric padding around the colored star, for example `02 + ★2 + 00`, is presentation/sorting scaffolding rather than gameplay data and must never be imported as values such as `200`, `500`, `1400`, or `1500`.
- The armor-page `シールドユニット` table preserves the archived source Wiki rarity as visible `★1` through `★15` values. Archived zero-width/zero-font sorting padding, for example `★ + font-size:0px 0 + 1`, is sorting scaffolding rather than gameplay data and must never be imported as `01` through `09` or used to remove the visible `★` marker.
- The attachment-page `アタッチパーツ` table preserves the archived source Wiki rarity as visible `★1` through `★10` values. Archived zero-font numeric prefixes such as `01` before visible `★1` are sorting scaffolding and must never replace the visible star rarity with plain `1` through `10` or padded values.
- Weapon-page rarity values `1` through `9` must not be zero-padded as `01` through `09`; the archived Wiki's hidden zero-font prefix is sorting scaffolding rather than gameplay data.
- The Pile weapon section uses the archived Pile dataset, beginning with `パイル` at rarity `3`, 打撃力 `579`, and 射撃力 `529`; it must never duplicate the Rod weapon dataset.
- Table alignment is semantic: explanatory text and quest-name lists are left aligned; compact labels, names, attributes, rarity, numbers, and status values are centered.
- Affiliate/PR presentation on desktop uses two equal-width banner slots with equal visual height and fills the available content width cleanly. On mobile it collapses to one visible banner column. The PR disclosure remains clearly visible.
- All public pages should use the available main-content width naturally. Ordinary body copy must not have a global readable-line-length cap such as `max-width: 82ch` that leaves a conspicuous unused right gutter. Intentional compact UI components may define their own widths, but ordinary `#main` paragraphs should fill the available column.
- Public-facing site copy must not direct visitors to GitHub, GitHub Issues, Pull Requests, repository contribution channels, or similar GitHub-based reporting instructions. Hosting/infrastructure URLs under `kylekatann.github.io` may remain where technically required, but they must not be presented as a contribution or correction workflow.
- Reader-facing guide/data pages use concise introductory copy, normally about three sentences, that states the page scope, the key comparison/check points, and the practical use of the information.
- Search/browser page titles use exactly `PSNOVA攻略サイト` for the homepage and `PSNOVA攻略サイト - XXXXX` for every other public page. `XXXXX` must identify the linked page itself; for example, the weapon landing page is `PSNOVA攻略サイト - 武器`, not a generic site title.
- Primary navigation text must remain immediately readable at normal desktop and mobile viewing sizes while preserving compact guide-site density. The current baseline is 16px for the top/mobile navigation, 14px for primary sidebar links, 13px for nested weapon links, and 12px for sidebar group labels; do not reduce these without an explicit design decision.
- Public-site display assets must never be loaded from external websites. Store every image/font/CSS/JS asset in the repository and reference it locally; do not solve missing artwork with hotlinks or CDN URLs.
- Homepage product visuals are part of their information tables, not separate cards or adjacent blocks. In `商品概要`, the PS Vita package occupies a rightmost table cell spanning the product rows. In `公式サイトへのリンク`, each PSNOVA/PSO2 logo occupies the rightmost cell of its matching link row, and `©SEGA` stays inside that official-image cell.
- On mobile, internal data-table cells do not auto-wrap because the tables are horizontally scrollable. All internal data tables use `.table-scroll` as the single horizontal scroll container. No body or header column is fixed or sticky; the first column scrolls horizontally together with every other column.

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
- For data tables, the original PSNOVA wiki/HTML is an approved internal reference: use compact cells, restrained 1px grid lines, the shared pale-blue UI token for header/emphasis surfaces, and existing native category icons where available.
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

13. Add in-page category navigation for large data pages. **Removed by user review: automatic in-page navigation is intentionally not used.**
14. Normalize table semantics statically in source HTML using `thead`, `tbody`, `th`, and `td` correctly. **Implemented for current public pages: runtime normalization remains prohibited. Historical staging material under `docs/pages/分類中/` is excluded from the public build rather than rewritten.**
15. Remove deprecated presentational HTML such as `bgcolor`, `border`, and inline table styling from current public source HTML and replace it with shared CSS. **Implemented for current public data tables; runtime cleanup remains prohibited.**
16. Remove duplicate/conflicting CSS rules while preserving behavior. **Implemented**
17. Reduce hard-coded absolute internal URLs where safe. **Implemented**
18. Give every important page a unique descriptive `<title>`. **In progress: the rendered title convention is standardized; legacy raw HTML titles must be migrated to the same convention as pages are statically cleaned.**
19. Give every important page a unique meta description. **Implemented via shared page metadata; migrate legacy raw HTML metadata during static page cleanup.**
20. Remove obsolete `meta keywords` tags. **In progress: remove them statically from remaining legacy pages rather than relying on runtime cleanup.**
21. Add canonical URLs. **In progress: canonical values are mapped, but legacy pages should receive static canonical tags during source cleanup.**
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
- Public title metadata follows `PSNOVA攻略サイト` on the homepage and `PSNOVA攻略サイト - XXXXX` on every other public page, with `XXXXX` matching the page purpose.
- Internal links use expected paths and do not unintentionally change established public URLs.
- Data tables retain expected row counts or known sentinel records when refactored.
- Public HTML must already be semantically valid before JavaScript executes. Tests should detect raw markup defects instead of relying on browser repair or runtime JavaScript normalization.
- Public data-table cells must stay inside explicit `<tr>...</tr>` rows, and rows must close explicitly rather than relying on browser HTML repair.
- Runtime JavaScript must not create/replace semantic table tags, convert `th`/`td`, remove legacy table attributes/styles, or clean malformed source text/data.
- Data-table alignment keeps ordinary compact data centered while explanatory prose, notes, acquisition methods, locations, and quest-name lists remain left aligned without runtime JavaScript inference.
- Actual table column headers remain centered even when semantic body-cell alignment rules are added later.
- Public UI must not expose developer-facing labels or unexplained shop-level abbreviations such as `Shop Lv`, `shopLv`, or `ショップLv`; use `ショップレベル`.
- Automatic in-page navigation assets/loaders must remain absent unless the user explicitly reverses this specification.
- Migrated historical pages retain sentinel guide content while excluding archived Wiki/Wayback chrome, analytics, ad code, and edit controls.
- Internal data pages do not display large illustrative JPEG screenshots; compact native PNG icons remain allowed.
- Data-table styling keeps compact density, `var(--accent-soft)` as the only pale-blue UI surface token, restrained 1px shared-border grid lines, and native weapon icon mapping while preserving semantic `thead/tbody/th/td` structure.
- Table styling must not reintroduce old standalone pale-blue values such as `#e0e8f0`, `#eef5ff`, or blue-colored 1px gap backgrounds for ordinary cell separation.
- The modern visual layer retains defined contrast tokens for cool navy navigation, white surfaces, PSNOVA indigo accents, and muted blue links.
- The palette must not regress to copied Game8 yellow accent values.
- Repository-root `reference/` remains present after cleanup work.
- User-corrected specifications in `Correction-derived invariants` remain covered by static regression tests where feasible.
- Ordinary public-page body copy must not reintroduce a global fixed `max-width` that creates an unused right gutter inside `#main`.
- Public-facing HTML must not reintroduce GitHub contribution/reporting copy such as GitHub Issues, Pull Requests, or `github.com` contribution links.
- Individual weapon detail headings must remain permanently expanded and must not expose a clickable disclosure/collapse affordance.
- Guide/data pages keep useful concise introductions instead of reverting to placeholder one-line wiki fragments.
- The weapon landing-page catalog keeps one static native PNG icon per weapon card and does not rely on runtime JavaScript to supply those icons.
- Public-site display assets must not use external `http://` or `https://` sources; image/font/CSS/JS references must resolve to repository-local `/PSNOVA/...` assets.
- Homepage product visuals must be table cells, not sibling cards: the Vita package uses the rightmost `商品概要` cell with `rowspan`, and the PSNOVA/PSO2 artwork sits in the rightmost cell of its corresponding official-link row with `©SEGA` kept inside an official-image cell.
- Mobile internal tables use one `.table-scroll` horizontal scroller, keep automatic wrapping disabled, and do not freeze any column. The first column must scroll with the rest of the table on weapon, enemy, Gigantes, material, and other internal data pages.
- Core-material rarity tests preserve source-reference star-rarity sentinels and reject hidden-padding-derived values such as `100`, `200`, `500`, `1400`, and `1500` inside the `コア` table.
- Armor rarity tests preserve source-reference `★1` through `★15` values and reject hidden zero-padding values such as `01` through `09` in the shield-unit rarity column.
- Attachment rarity tests preserve source-reference `★1` through `★10` values and reject zero-font sort prefixes or plain-number replacements in the attachment rarity column.

Tests belong under `tests/` and should use the Python standard library where possible so the repository has no unnecessary test dependency.
Add tests alongside each implementation item. The GitHub Actions `tests` workflow must not run on `push` or `pull_request`; trigger it manually once with `workflow_dispatch` after the planned implementation batch is complete.

## Definition of done for each item

An implementation item is ready for final validation when:

- The change is implemented.
- Relevant automated tests are added or updated when feasible.
- The public-site behavior is not knowingly regressed on desktop or mobile.
- User-corrected specifications affected by the item are recorded or refreshed in `Correction-derived invariants`.
- The item has its own clear commit.

The implementation batch is complete only after the manually triggered final GitHub Actions run passes.

## Data safety

Do not silently alter gameplay values, names, materials, rarity, shop levels, or other source data while changing layout or code structure.
When a data correction is needed, make it a separate change with its own evidence and test/sentinel update.

## Editing constraints

- Existing pages must be corrected by directly editing only the target text or markup whenever possible.
- Do not rewrite an entire HTML page or regenerate the full document as a new string for a local correction.
- Do not manually create or manipulate Git blobs, trees, or indexes as an editing method.
- When one implementation item touches multiple files, edit each file normally and independently, then commit the completed item together when the tooling supports that workflow.
- After every edit, inspect the diff. If the diff expands beyond the intended target, stop that method and return to a smaller edit.
- Regression tests must be limited to the minimum assertions that directly detect the reported defect.
- In ChatGPT chat mode, repository source/page changes must be performed by local partial-edit commands supplied in the chat. Do not write source/page files directly through the GitHub Contents API, Git Database API, blob/tree/index operations, or other whole-file replacement methods.
- Prefer a minimal `git apply` patch for chat-driven edits. Run `git apply --check` before `git apply`; `sed`, PowerShell text replacement, or an editor replacement may be used when they produce a smaller and safer targeted edit.
- After applying a chat-provided edit, inspect `git diff -- <target paths>` before staging or committing. If unrelated changes appear, revert that edit and use a smaller patch.
- GitHub APIs/connectors may continue to be used read-only for auditing, source/reference comparison, history inspection, searching, and diff verification unless the user explicitly overrides this rule.

## Static metadata ownership

- Public title, description, canonical, and OpenGraph metadata are owned by static source HTML. Do not restore `page-meta.js` or runtime metadata repair.