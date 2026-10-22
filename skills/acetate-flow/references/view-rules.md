# Renderer design and behavior

Read this when changing the shared renderer. Ordinary workflow changes belong in JSON; see [json-format.md](json-format.md).

## Surface and visual language

Canvas: 100% width × `100dvh`, native scroll with one viewport of empty space on every side, centered board wrapper, subtle 16px dot grid. No visible header, title, branding, counters, progress banner, or footer. Keep descriptive browser title and screen-reader status.

Nodes use intrinsic width/height, 8px padding, 6px corners, grid layout: type icon/tag plus expand indicator, short title, optional subtitle. Reference typography: ~11.5px title, 9px subtitle, 8px type tag. No fixed 166×76 constraint. Active styling must not change geometry. Measure boxes before routing and again on resize; ports meet their borders.

| Kind | Appearance | Meaning |
| --- | --- | --- |
| ai | Robot, warm fill | Paid intelligence |
| agent | Robot, warm fill, AI + web label | Intelligence with web tools |
| tool | Wrench, neutral fill | Deterministic transformation/retrieval |
| data | Database, pale blue | Data artifact |
| rule | Diamond, dashed border | Code branch |
| output | Document, pale green | Visible result |

An external service is not automatically deterministic. Label the actual behavior. Intelligence is one component inside a workflow; don't call the whole diagram an agent by default.

Light tokens: ink #101010, muted #646866, rules #d8d8d2, paper #f7f7f5, brand #174b59, blue #2f6f7e, gold #8a642f; canvas #fcfcfb.
Dark: canvas #171e1b, surfaces #222b26, ink #e5eae7, muted #a1ada7, rule #35423e, brand #9ccfd6, blue #8fc4cd. System Helvetica/Arial, monospace tags/JSON. Inline SVG icons; no external fonts or dependencies.

Small sun/moon icon button top-right, reflecting the action available. Initial theme uses saved choice, otherwise system preference. Persist under `acetate-flow-theme`; storage failures must not break rendering. Theme applies to nodes, connectors/labels/arrows, dock, controls, legend, inspector, JSON and backdrop.

Tiny bottom-right legend sits above a compact bottom-center floating dock. The dock combines scenario buttons and icon controls in one row; narrow displays can scroll it horizontally. Keep accessible labels/tooltips despite the small visual footprint.

## Canvas navigation

Two-finger scrolling pans horizontally and vertically, including when the whole board fits. Ctrl-wheel/trackpad pinch zooms around the pointer; handle Safari gesture events without double zooming. Two-touch gestures combine pinch and translation. Keep the page and fixed dock unscaled. Manual pan/zoom disables Follow so playback does not pull the canvas back. Empty space lets edge nodes clear fixed overlays.

Small − / percentage / + / Fit controls; keyboard +/− zooms and 0 fits. Fit recenters configured bounds. Reset/scenario changes restore the home position. Zoom is bounded to 5–400%; saved initial scale remains configurable. Follow positions must include the board wrapper offset.

## Connections and playback

SVG arrows sit behind nodes. Idle edges are muted; traversed edges turn blue. Dashed payload edges indicate independently retained data. Do not animate them as extra execution steps; illuminate them when the consumer becomes active. Active node has a halo, visited nodes a quieter border; inactive branches remain visible.

The SVG dot follows the current path via getTotalLength/getPointAtLength. Play starts the selected path, then loops indefinitely with a one-interval dwell on the terminal node. Wrap clears old highlights without drawing a false output-to-input connector. Exactly one requestAnimationFrame chain; pause cancels it and hides the dot. Resume retains elapsed interval time (terminal Play restarts at the beginning).

Manual previous/next/reset pause. Manual next stops at terminal; previous can reach ready. Scenario selection pauses/resets. Inspection and hidden-tab events pause; close/return does not auto-resume. Reduced motion suppresses the moving dot and transitions, preserving discrete steps.

Speed intervals: 1600/950/450ms. Follow scrolls when the active box leaves the viewport. Fit uses configured board bounds; content changes that extend beyond the board need a larger board. Sizing requests apply relative to the current view. A saved example scale is not a universal design rule.

## Inspectors and rendering

Click any node: purpose, input → output, pretty example JSON, short caveat, Copy JSON. Example references resolve from local config samples; scenario overrides select different data. No executable workflow expressions.

Dialog: labelled aria-modal, backdrop, close, Escape, focus trap, return focus to trigger, synchronized aria-hidden. Clipboard failure keeps JSON selectable. Render external labels/data with textContent; innerHTML is restricted to fixed SVG icon markup. Builder escapes `<`, `>` and `&` in embedded JSON to prevent script termination. Never add eval for user configuration.

## Renderer map

- `config` from inline `application/json`; `nodes`, `edges`, `scenarios`, `paths` derived generically.
- `route`, `port`, `layoutNodes`: measured dimensions, optional ports/waypoints and arrow endpoints.
- `resolveData`, `inspect`, `closeInspector`: local references and data presentation.
- `pause`, `render`, `tick`: path state, generic payload lighting, playback.
- `zoom`, theme handlers: fitting, resize and sun/moon persistence.
- `icons`, `kindNames`, CSS: shared visual language.

Keep DOM IDs synchronized with handlers. Renderer slot `{{FLOW_JSON}}` occurs exactly once. Python builder owns validation and embedding; the browser makes no network requests.

## Verification

Check each scenario's IDs/edges, intended branch and terminal, repeated loops, pause/resume, one animation chain, scenario switching, every inspector payload, sample references, theme storage and labels, manual navigation, resize/fit, pointer-anchored pinch, two-axis panning at Fit, manual-navigation Follow cancellation, zoom limits and dialog keyboard/focus. Confirm no script/link runtime dependencies. Browser screenshots verify layout; simulated DOM checks do not.

The classification and an unrelated workflow were exercised in simulated DOM tests during packaging. Recheck after engine changes rather than treating this as proof of future versions.
