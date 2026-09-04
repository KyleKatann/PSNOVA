# PSNOVA Agent Rules

These rules are the repository-level source of truth for modernization work.

## Core rules

1. The user's newest explicit requirement is canonical. Do not preserve an older implementation merely because it already exists.
2. Record stable design corrections and invariants in this file when they are discovered.
3. `reference/` and `docs/pages/分類中/` are historical/read-only material and are excluded from public modernization unless the user explicitly asks otherwise.
4. Runtime JavaScript must not repair source HTML or game data. Allowed runtime behavior is limited to search/filter/sort/navigation, UI state classes, rarity presentation attributes, scroll-wrapper enhancement, and other explicitly approved interaction state. Do not build `thead`/`tbody`, convert `th`/`td`, repair malformed tables, normalize source game text, or clean obsolete source attributes at runtime.
5. Public CSS is limited to `docs/css/style.css` and `docs/css/page.css`.
6. Weapon-table headers stay in normal flow and must never become sticky.
7. Rarity presentation uses the canonical groups ★1-3 blue, 4-6 green, 7-9 red, 10-12 orange, and 13-15 purple. `docs/css/style.css` owns the presentation and runtime JS may only attach `data-rarity`/presentation state without changing the underlying game data.
8. One table has one horizontal scroll owner. Do not create nested competing scroll regions.
9. Public-source modernization must preserve game text, numeric data, URLs, and user-visible meaning unless the user explicitly asks to change content.
10. Shared public behavior belongs in shared assets rather than duplicated inline markup or scripts.
11. Keep regression tests aligned with the current production contract rather than historical implementation details.
12. Do not hide known failures by weakening tests or adding broad allow-lists.
13. Prefer native HTML semantics over ARIA reconstruction when source markup can express the structure directly.
14. Public pages must remain usable on desktop, mobile, keyboard, touch, and zoomed layouts.
15. One issue equals one commit. Keep unrelated cleanup out of the same commit.
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

- Dynamic widgets must expose valid accessible names and ARIA semantics. The site-data search is an editable `combobox` controlling `#site-search-results`: its visible Search button and Enter key use the same submit path, ArrowDown/ArrowUp move the active option through `aria-activedescendant`, popup options remain outside the normal Tab sequence, and Escape dismisses the popup. Rendered affiliate image links must have a discernible accessible name even when their remote images use empty alt.

- Every public page footer exposes the site-information pages `/PSNOVA/copyright.html` and `/PSNOVA/issue.html`. Keep all public pages reachable from `/PSNOVA/` through internal navigation; do not silence the orphan-page regression test with allow-lists.

- Every public HTML page must remain reachable from `/PSNOVA/` through public internal links, including links supplied by the shared sidebar. `tests/test_public_navigation_reachability.py` guards against orphan public pages.

- Public `<img>` elements declare both numeric `width` and `height` using the source image's intrinsic dimensions. CSS remains responsible for responsive rendered sizing; the HTML dimensions reserve the correct aspect ratio before image load and reduce layout shift.

- Public pages load the four shared head scripts (`openclose.js`, `fixmenu_pagetop.js`, `menubar.js`, `sidebar.js`) with `defer`. Public HTML must not contain inline initialization scripts; shared components initialize themselves from external JS after parsing while preserving document-order execution.

- Every public page explicitly declares the repository-owned `/PSNOVA/img/logo.png` as its favicon. Keep favicon resources local to the repository and do not introduce external icon hotlinks.

- Homepage descriptive tables use explicit row-header semantics: the label cell at the start of each 商品概要 and 公式サイト row is `<th scope="row">`. Reserve `scope="col"` for actual column headers.
