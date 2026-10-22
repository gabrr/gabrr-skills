---
name: acetate-flow
description: Create interactive workflow diagrams as an AI-assisted alternative to Mermaid. Identify data, tools, AI calls, and decisions, with a side panel for inspecting each node's inputs and outputs. Generate standalone HTML from JSON, with animated branches and light/dark mode. Use for workflow diagrams, not general app screens.
---

# Acetate Flow

An AI-assisted alternative to Mermaid for interactive workflow diagrams: identify what each piece is, then open its side panel to inspect concrete inputs and outputs. Help the user author workflow JSON and reuse the renderer, so they can understand the diagram by watching and clicking, with minimal reading. AI assists authoring; the generated HTML does not call a model.

## Default workflow

1. Read [JSON format](references/json-format.md). Model operations, intelligence calls, data artifacts, decisions and outputs. Show independent data inputs as payload edges.
2. Create or edit a small `<name>.flow.json` beside the requested HTML. Start with [minimal.json](assets/minimal.json) for a new subject, or [classification.json](assets/classification.json) for the existing transaction diagram. Reuse `samples` references instead of repeating large example payloads.
3. Run `python3 <skill-dir>/scripts/create_flow.py /absolute/output.html --config /absolute/name.flow.json`. For an authorized update to that existing output, add `--force`. The script validates the graph and embeds the JSON into a complete offline HTML file. No server, fetch, build tool, or runtime dependency is needed.
4. Check all scenario paths, inspectors, branches, repeated playback, pause/resume and theme switching with available local tooling. Distinguish simulated checks from browser layout verification.
5. Return the HTML's absolute clickable path and a brief outcome. Keep future workflow edits in JSON; do not regenerate or read the full renderer for ordinary content changes.

## View rules

- Full-window canvas; no branding header, visible page heading, status banner, counters or explanatory footer.
- Content-sized boxes with **8px padding on every side**. Preserve consistent border width across active states; recompute arrow endpoints from measured dimensions.
- Tiny bottom-right legend. One small bottom-center dock: scenario choices alongside icon playback controls. Small sun/moon toggle top-right, with remembered preference and system-theme default.
- Distinguish paid intelligence (robot), deterministic tools, generated data, code branches and final outputs. Use brief titles and real example payloads, revealing details only in the inspector.
- Two-finger scrolling pans; pinch zooms around the pointer. Keep generous space around the board so nodes can move clear of fixed controls. Manual pan/zoom disables Follow; Fit recenters. Include small zoom buttons and keyboard +/−/0.
- Playback loops continuously while running. Preserve pause, previous/next, reset, speed, follow and fit. Inspection or hiding the tab pauses; returning/closing does not silently resume.
- Preserve accessible labels, focus handling, keyboard dialog controls and reduced-motion behavior. Keep example data honest about simulations; HTML performs no real research or AI calls.

Read [view-rules.md](references/view-rules.md) for renderer changes, visual tokens and interaction details. Read [classification-example.md](references/classification-example.md) only for the original transaction proposal; do not impose its domain rules on other workflows.

`assets/renderer.html` contains the reusable engine and `{{FLOW_JSON}}` insertion slot. Change it only when presentation or behavior needs to change. Keep domain-specific logic out of this renderer. A JSON workflow still uses tokens; savings come from reusing code and editing only changed content, not from the format alone.
