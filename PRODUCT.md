# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Hong Kong DSE candidates (S4–S6) revising on their own, mostly on phones, Cantonese-speaking. Their job: find a past paper by year or by topic fast, then drill questions in focused sessions. Teachers may assign from it, but students self-revising are the primary audience (user-confirmed 2026-11-12).

## Product Purpose

DSE Hub is the index door to a past-paper question bank: filter by subject / year / paper, or by topic tag, then deep-link straight into the per-question viewer (BANK_URL) for concentrated revision. Success = a student reaches the exact paper or topic they need in two taps and trusts what is listed.

## Positioning

It only lists what the question database actually contains (只顯示資料庫已有內容) — no dead links, no aspirational catalog — and links at question granularity with topic tags, not just whole-paper PDFs.

## Operating Context

Static site on GitHub Pages, no backend. Catalog data compiled into `docs/hub/data.js`; question metadata in `docs/data.js`. Installed as a PWA (manifest + service worker + add-to-home-screen flow). Students arrive, filter, and leave into the viewer; sessions are short and repeated daily during exam season.

## Capabilities and Constraints

- Two browse modes: 按年份 (papers by year/subject/paper) and 按課題 (questions by topic tag); mobile wheel-picker (reel) for filter selection.
- Question rows carry subject, year, paper, question number, and up to 3 topic tags; every row deep-links into the viewer with a per-question hash.
- Scope of this engagement: the hub page (`docs/hub/`) only; the linked viewer keeps its current look for now.
- Stack is fixed: plain HTML/CSS/JS, no framework, must stay GitHub-Pages static.

## Brand Commitments

- Name: DSE Hub.
- UI copy register: standard written Chinese (書面語), user-confirmed 2026-11-12 — not written Cantonese.
- Dark ground is a user-confirmed commitment; the redesign stays dark but drops the gradient/glow treatment for a flat, professional minimalist field.
- Standing visual preference (user-confirmed 2026-11-12, canon round): the category standard, executed at the craft level of Apple system dark apps — true black ground, system type stack, zero decoration, platform-native component vocabulary (segmented control, wheel-picker sheet, inset grouped list).

## Evidence on Hand

- `docs/hub/data.js` CATALOG: real papers actually in the database (math 數學必修部分, econ 經濟, chem 化學, bio 生物, phys 物理; years ~2012–2025; 卷一/卷二 etc.; 中文/英文 papers).
- `docs/data.js` QB questions with subject/year/paper/qno/title/tags.
- No logos, no photography, no testimonials — the design must not fabricate any.

## Product Principles

1. Show only what exists; every listed item is reachable.
2. Two taps from open to drilling — filters are the product.
3. Quiet professional trust over decoration; students are studying, not shopping.
4. Mobile-first; desktop is the same interaction on a wider field.

## Accessibility & Inclusion

Reading-age-appropriate 書面語; WCAG-AA contrast on the dark ground; large tap targets for phone use in bed at night.
