---
version: 1
slug: "docs-hub-index-html"
primary_target: "docs/hub/index.html"
related_targets: []
---

# Surface brief — DSE Hub index (docs/hub/index.html)

Scope: the hub page only. Visitor mode: **Operate** — the task is finding a paper or topic in two taps.

Audience: DSE candidates self-revising, mostly on phones, at night. Job: filter subject/year/paper or topic, then drill via deep links. Constraints: static GitHub Pages, no backend, keep every function (reel pickers, both modes, PWA install, per-question links). Copy register: 書面語.

## Direction contract

THESIS: The hub looks like the student's own phone — an iOS-native index tool, true black, inset grouped list, one accent. It refuses the gradient-and-glow dark that reads as generated.

OWN-WORLD: near-black ground (#000000) with elevated surfaces two steps up (#0d0d0f, #17181c), hairline separators at ~8–12% white, system type stack (SF Pro / PingFang TC / Noto Sans TC fallbacks), a single system-blue accent reserved for active state and links, tabular numerals for years and counts. Subject identity rides small colored dots before subject names — never filled tag backgrounds, never gradients.

STORY: The student opens the hub and understands it in one second because it behaves like every app on their phone: segmented control for mode, inset fields for filters, wheel sheet to pick, grouped rows with a chevron to leave into the viewer.

FIRST VIEWPORT: Compact header — "DSE Hub" wordmark with 安裝 ghost button right, page title below. Sticky filter bar: segmented control (按年份/按課題) then three inset filter fields (科目/年份/卷別) in one row on desktop, stacked on narrow phones. Count line ("共 N 卷"). Inset grouped list rows: leading tabular year, title + muted meta with subject dot, trailing chevron; separators hairline, group edges 12px radius. Footer one muted line.

FORM: The category standard (canon), taken through the standing exit — position: the deliberate default, not the roll's assignment. SEED REFERENCE: seed:53641ae54238ad10.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
