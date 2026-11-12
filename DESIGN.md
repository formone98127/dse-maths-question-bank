---
name: DSE Hub
description: An iOS-native index door to a DSE past-paper bank — true black, inset grouped list, one system blue.
colors:
  ground: "#000000"
  surface-card: "#1c1c1e"
  surface-pressed: "#2c2c2e"
  ink: "#ffffff"
  ink-secondary: "rgba(235, 235, 245, 0.64)"
  ink-tertiary: "rgba(235, 235, 245, 0.42)"
  separator: "rgba(84, 84, 88, 0.48)"
  accent: "#0a84ff"
  accent-text: "#409cff"
  accent-tint: "rgba(10, 132, 255, 0.16)"
  seg-track: "rgba(118, 118, 128, 0.24)"
  seg-thumb: "#636366"
  scrollbar: "#3a3a3c"
  dot-math: "#ff453a"
  dot-econ: "#32d74b"
  dot-chem: "#64d2ff"
  dot-bio: "#ff9f0a"
  dot-phys: "#bf5af2"
typography:
  display:
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Helvetica Neue", Arial, sans-serif'
    fontSize: "clamp(24px, 5vw, 30px)"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  title:
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Helvetica Neue", Arial, sans-serif'
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Helvetica Neue", Arial, sans-serif'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  picker-item:
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Helvetica Neue", Arial, sans-serif'
    fontSize: "17px"
    fontWeight: 400
    lineHeight: "44px"
  label:
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Helvetica Neue", Arial, sans-serif'
    fontSize: "12px"
    fontWeight: 400
    letterSpacing: "0.02em"
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "16px"
  pill: "17px"
spacing:
  xs: "4px"
  sm: "6px"
  md: "8px"
  lg: "10px"
  xl: "12px"
  gutter: "16px"
components:
  install-button:
    backgroundColor: "{colors.accent-tint}"
    textColor: "{colors.accent-text}"
    rounded: "{rounded.pill}"
    height: "34px"
    padding: "0 14px"
  install-button-hover:
    backgroundColor: "rgba(10, 132, 255, 0.26)"
  install-button-pressed:
    backgroundColor: "rgba(10, 132, 255, 0.32)"
  seg-control:
    backgroundColor: "{colors.seg-track}"
    rounded: "9px"
    padding: "2px"
  seg-thumb:
    backgroundColor: "{colors.seg-thumb}"
    textColor: "{colors.ink}"
    rounded: "7.5px"
    padding: "6px 18px"
  filter-field:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    height: "40px"
    padding: "0 12px"
  filter-field-pressed:
    backgroundColor: "{colors.surface-pressed}"
  filter-field-filtered:
    textColor: "{colors.accent-text}"
  list-card:
    backgroundColor: "{colors.surface-card}"
    rounded: "{rounded.lg}"
  list-row:
    textColor: "{colors.ink}"
    height: "56px"
    padding: "10px 16px"
  picker-sheet:
    backgroundColor: "{colors.surface-card}"
    rounded: "16px 16px 0 0"
    width: "min(440px, 100%)"
  picker-item:
    textColor: "rgba(235, 235, 245, 0.75)"
    height: "44px"
  picker-item-selected:
    textColor: "{colors.ink}"
  subject-dot:
    size: "7px"
  empty-state:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.lg}"
    padding: "36px 24px"
---

# Design System: DSE Hub

## Overview

**Creative North Star: "The Student's Own Phone"**

The hub disguises itself as a native part of the student's phone. True-black ground, the operating system's own type stack, and Apple's platform component vocabulary — segmented control, inset grouped list, wheel-picker sheet, tinted capsule — so a DSE candidate opening it at night understands it in one second because it behaves like every other app on their device. The world explicitly refuses the gradient-and-glow dark that reads as generated: no glows, no shadows, no decorative color, no loaded fonts.

Structure comes from three quiet devices: a two-step tonal elevation (ground → card → pressed), hairline separators at half a pixel, and a single system-blue accent reserved almost entirely for action — active state, links, and the install capsule's tint. Subject identity never interrupts this calm: each subject rides a 7px colored dot before its name, and nowhere else. Years and counts always render in tabular numerals so figures align down the list.

The system is built for one surface (the hub index at `docs/hub/`), shipped as a static GitHub Pages site and installed as a PWA; UI copy is standard written Chinese (書面語), a durable brand commitment. Body text is fixed at 15px with no Dynamic-Type-style scaling — a deliberate choice at this scope. The surface's one authored motion is the wheel-picker sheet's ride-up; everything else only transitions on tap state.

**Key Characteristics:**
- True-black ground (#000000) with exactly two elevated tones above it (#1c1c1e cards, #2c2c2e pressed)
- One accent (system blue) plus five subject dot colors that appear only as 7px dots
- System type stack, never a loaded webfont; tabular numerals for years and counts
- iOS component vocabulary: segmented control, inset grouped list (12px radius, 56px rows), wheel-picker bottom sheet, tinted capsule
- Half-pixel hairlines and a functional nav-bar blur; zero shadows, zero gradients as decoration
- 書面語 UI copy; standalone PWA display hides the install button; reduced-motion kills the sheet animation

## Colors

A near-monochrome dark field in iOS system values, structured entirely by luminance steps and alpha, with one blue for action and five dot hues for subject identity.

### Primary
- **System Blue** (#0a84ff): the only accent. Appears as the segmented control's active tint context, the focus ring (2px, rgba(10,132,255,0.65)), text selection (rgba(10,132,255,0.4)), and as tint fill beneath it. Rare by design.
- **Accessible Blue** (#409cff): the same blue lightened for text on dark — used for link-styled text (sheet 取消/完成 buttons) and for field buttons in their filtered state. Blue text is always this value, never #0a84ff.
- **Blue Tint Fill** (rgba(10,132,255,0.16)): the accent as a surface — the install capsule's background, deepening to 0.26 on hover and 0.32 on press.

### Neutral
- **True Black** (#000000): the ground. Page background, theme color, manifest background. Nothing sits darker.
- **Elevated Graphite** (#1c1c1e): every raised surface — list cards, field buttons, the picker sheet, empty state, install tip. One step up from ground. (The direction contract's indicative values #0d0d0f/#17181c shipped as #1c1c1e/#2c2c2e — the canonical iOS system colors standing in for the contract's estimates, same two-step elevation.)
- **Pressed Slate** (#2c2c2e): the second and final step — pressed fields, the close-icon disc, and the deepest interactive fills. There is no third step.
- **Pure White** (#ffffff): primary ink — titles, years, active states.
- **Secondary Ink** (rgba(235,235,245,0.64)): the workhorse muted text — meta lines, labels, footer, count line. A faint cool cast, never neutral gray.
- **Tertiary Ink** (rgba(235,235,245,0.42)): the faintest legitimate text — chevrons, field arrows, empty-state icon. Also the default dot color before a subject override.
- **Hairline Separator** (rgba(84,84,88,0.48)): 0.5px row separators and the sheet header rule — iOS's separator value, never full-opacity white.
- **Segmented Track** (rgba(118,118,128,0.24)) and **Segmented Thumb** (#636366): the mode switch's sunken track and active pill.
- **Scrollbar Graphite** (#3a3a3c): thin scrollbar thumb on the black track — the browser surface themed, not hidden.

### Tertiary
- **Subject dots** — Math Red (#ff453a 數學), Econ Green (#32d74b 經濟), Chem Ice Blue (#64d2ff 化學), Bio Amber (#ff9f0a 生物), Phys Violet (#bf5af2 物理): identity colors, each appearing exclusively as a 7px circle before the subject name in list rows.

### Named Rules
**The One Blue Rule.** System Blue is the only accent on any screen. It marks active state, links, and the install capsule — nothing decorative, never a second hue, and blue text is always #409cff on dark.
**The Dots Stay Dots Rule.** Subject colors exist only as 7px dots. They never fill tag backgrounds, never color text, never gradient, never scale up.

## Typography

**Display Font:** the system stack — -apple-system, BlinkMacSystemFont, SF Pro Text, PingFang TC, Noto Sans TC, Microsoft JhengHei, Helvetica Neue, Arial (sans-serif fallback)
**Body Font:** the same stack; one family serves every role

**Character:** The type is deliberately the phone's own voice — no loaded fonts, no display faces, no personality beyond weight and size. Latin glyphs take SF Pro on Apple devices; Chinese falls to PingFang TC / Noto Sans TC / JhengHei. Hierarchy is built from a compact 12–17px ramp plus one clamp-sized page title.

### Hierarchy
- **Display** (700, clamp(24px, 5vw, 30px), line-height 1.25, letter-spacing −0.015em): the page title 「香港中學文憑歷屆試題資料庫」 — the only scaled text on the page.
- **Title** (600, 15px, line-height 1.4): row titles, the leading year figure, sheet header title, brand wordmark (the brand at secondary ink).
- **Body** (400, 15px, line-height 1.5): the base; all body and control text derives from it (14.5px row titles and field values sit just under it).
- **Picker Item** (400→600 selected, 17px, 44px leading): wheel-sheet options — the largest UI text after the title, per iOS picker convention.
- **Label** (400, 12–12.5px, letter-spacing 0.02em): field labels, count line, meta lines, footer — secondary ink, often tabular.

### Named Rules
**The System Face Rule.** Never load a webfont or name a display face. The stack is the identity; on Apple devices it resolves to SF Pro / PingFang TC and that is the intended look.
**The Tabular Figure Rule.** Every year, count, or numeric column renders `font-variant-numeric: tabular-nums` so figures align vertically (the leading year column also holds a 3.8em minimum so rows align regardless of digits).

*(Body is fixed at 15px — no Dynamic-Type-style scaling. A documented deliberate choice at this scope.)*

## Layout

One column, centered, maximum width 680px, with 16px side gutters (14px on narrow phones). Content is a single vertical flow: compact header (brand row + page title) → sticky filter bar → results list → one-line footer.

The filter bar is sticky at the top with the iOS nav-bar material — rgba(10,10,10,0.78) under saturate(180%) blur(20px), closed by a 0.5px white-alpha edge (rgba(255,255,255,0.08)). Inside: the segmented control above a row of three inset filter fields (8px gaps; labels 4px above controls). At 480px and below the fields stack vertically. Rows are whole-row links on a three-column grid (year / body / chevron), min-height 56px, 10px vertical and 16px horizontal padding, 14px column gap (10px narrow). Safe-area insets are honored at the footer and sheet bottom. Spacing rhythm is tight and iOS-native: 4 / 6 / 8 / 10 / 12 / 16px.

## Elevation & Depth

No shadows exist anywhere in this system — depth is purely tonal, in exactly two steps: the true-black ground, Elevated Graphite (#1c1c1e) for everything raised, and Pressed Slate (#2c2c2e) reserved for pressed state and the deepest interactive fills. Interaction feedback is a white-alpha wash on top of the step (hover rgba(255,255,255,0.045), press rgba(255,255,255,0.08) on rows; the sheet's center band is the same 0.08 wash). The one blur in the system is functional, not decorative: the sticky filter bar's nav-bar material. The sheet's scrim is a flat rgba(0,0,0,0.55).

### Named Rules
**The Two-Step Rule.** Elevation is ground → card → pressed. No third tone, no box-shadow, no glow, no gradient. If a surface needs to feel higher, it is the wrong solution — the list should be shorter.

## Shapes

Rounded, platform-native corners throughout: 12px for grouped list cards and the empty state, 10px for inset filter fields, 8px for small controls (sheet text buttons, picker highlight band), 16px on the sheet's top corners only, 9px/7.5px concentric on the segmented control, and full capsules made by radius = half height (17px on the 34px install button). Separators are hairlines — 0.5px, never 1px or more. Chevrons and field arrows are bordered squares rotated (8px, 1.8–2px tertiary-ink borders, rotated −45°/45°) — drawn, never glyph icons.

### Named Rules
**The Hairline Rule.** Dividers are 0.5px separator gray (rgba(84,84,88,0.48)); edges are 0.5px white-alpha. Never 1px, never opaque white, never a gap-instead-of-line.

## Components

Each component is an iOS platform piece translated to CSS; behavior matches the platform before it invents.

### Buttons
- **Shape:** full capsule for the install button (17px radius on 34px height); 8px radius for sheet text buttons; 50% for the 28px close-icon disc.
- **Tinted capsule (安裝):** accent-tint fill (rgba(10,132,255,0.16)) with accessible-blue 13.5px/600 text, padding 0 14px; hover deepens to 0.26, press to 0.32; installed state dims to 0.6 opacity; hidden entirely under `display-mode: standalone`.
- **Sheet links (取消/完成):** borderless accessible-blue 15px text on 8px rounded hotspots; hover adds a 0.06 white wash; 完成 is 600 weight.
- **Focus:** global focus-visible ring — 2px solid rgba(10,132,255,0.65), 2px offset.

### Chips
Not used. Filtering is expressed through field buttons and the wheel sheet, never chips.

### Cards / Containers
- **Inset grouped list:** one Elevated Graphite card (12px radius) whose rows separate by 0.5px hairlines inset by the row padding; the card clips its children (no outer border, no shadow).
- **Empty state:** the same card language — graphite, 12px radius, centered 26px inline-SVG search mark in tertiary ink above 14px secondary text.
- **Install tip:** graphite card at 14px radius with white 14px strong line over 13.5px secondary body.

### Inputs / Fields
Filter fields are button-styled insets: 40px tall, 10px radius, graphite fill, 14.5px value text left-aligned, a drawn chevron-right arrow in tertiary ink. States: placeholder (請選擇, secondary ink), filtered (accessible blue, 600 weight), hover #242426, press Pressed Slate. Tapping opens the wheel sheet — fields never type.

### Navigation
The sticky blurred filter bar (above) plus the segmented control for mode: rgba(118,118,128,0.24) track (9px radius, 2px inset, min-width 180px), active pill #636366 at 7.5px radius with white 600 label, inactive labels secondary ink lifting to white on hover, 0.15s ease. List rows are whole-row links opening the viewer in a new tab.

### Wheel-Picker Sheet (signature)
The surface's signature component and only authored motion. Bottom sheet, min(440px, 100%) wide, graphite, 16px top corners, 38×5px grabber at 22% white, header row (取消 / title / 完成) over a hairline. The wheel: 220px window, 44px items at 17px, scroll-snapped, with an 8px-radius highlight band (0.08 white wash) at 88–132px and mask fades to transparent over 0–44px and 176–220px; unselected items at rgba(235,235,245,0.75), selected pure white 600. Opens with the ride-up — `translateY(60%) → none` over 0.42s cubic-bezier(0.32,0.72,0,1) — over a 0.25s fading rgba(0,0,0,0.55) scrim. Scroll settles by snapping (80ms debounce), items are tap-to-select, focus moves to 完成 on open and returns to the invoking field on close. `prefers-reduced-motion` removes the animation entirely.

### Subject Dot
A 7px circle, inline before the subject name in row meta lines — five fixed hues (數學 red, 經濟 green, 化學 ice, 生物 amber, 物理 violet) and tertiary-ink as the fallback for unknown subjects.

*(One data-derived asymmetry: topic-mode rows label papers in English — 「Paper 1A」 — because the paper number is parsed from question metadata, while year-mode rows show the catalog's Chinese paper names — 「卷一甲」. Both are acceptable HK usage; consistent within each mode.)*

## Do's and Don'ts

### Do:
- **Do** keep elevation to the two shipped steps — #1c1c1e for raised surfaces on the #000000 ground, #2c2c2e only for pressed state.
- **Do** keep every subject color a 7px dot; the dot precedes the subject name and nothing else.
- **Do** render all years and counts in tabular numerals (`font-variant-numeric: tabular-nums`).
- **Do** use #409cff (not #0a84ff) whenever blue appears as text on the dark ground.
- **Do** keep list rows 56px tall whole-row links with the drawn chevron at trailing edge.
- **Do** theme the browser surface: blue text selection, blue focus-visible ring, thin #3a3a3c scrollbar.
- **Do** hide the install button under `display-mode: standalone` and kill the sheet animation under `prefers-reduced-motion: reduce`.
- **Do** write UI copy in 書面語 (standard written Chinese).

### Don't:
- **Don't** add shadows, glows, or gradients — the world refuses the gradient-and-glow dark; the only gradient in the code is the wheel's functional alpha mask.
- **Don't** introduce a second accent hue or use subject colors as fills, text, or tag backgrounds.
- **Don't** load a webfont or replace the system type stack.
- **Don't** draw separators heavier than a 0.5px hairline or in opaque white.
- **Don't** animate beyond the sheet ride-up and tap-state transitions (0.12–0.15s ease).
- **Don't** scale body text dynamically — 15px fixed is the documented choice at this scope.
- **Don't** use glyph/icon fonts; icons are inline SVG or drawn CSS borders.
