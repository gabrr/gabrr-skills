# JSON authoring

Build with `python3 <skill-dir>/scripts/create_flow.py output.html --config name.flow.json`.
Output is a self-contained HTML file. Keep the source JSON beside it for future edits. The builder refuses overwrite unless `--force` is provided; it validates before writing. Omitting `--config` uses the bundled classification example.

## Model

| Field | Value |
| --- | --- |
| `title` | Browser-tab title, no visible heading |
| `board` | Optional `{width:1180, height:1040, scale:1}` logical canvas and fit multiplier |
| `readyText` | Optional screen-reader-only ready description |
| `nodes` | Nonempty array of nodes |
| `edges` | Array of directed connections |
| `scenarios` | Nonempty array of selectable paths |
| `samples` | Optional named reusable JSON values |
| `labels` | Optional `[{x,y,text}]` for free-positioned short branch labels |

Node:

```json
{"id":"classify","kind":"ai","x":340,"y":94,
 "title":"Classify","subtitle":"Paid AI",
 "input":"Rows + context","output":"Categories",
 "description":"Classify every original row.",
 "data":{"transactions":{"$ref":"rows"}},
 "note":"Illustrative output.","narration":"Classifying the rows."}
```

- `id`, `kind`, `x`, `y`, `title` required. Coordinates are the node **center**, in unscaled board pixels. Width/height come from content, not JSON. Optional text fields default empty. `data` defaults null.
- Kinds: `data`, `tool`, `ai`, `agent`, `rule`, `output`, `error`. Add an error only when the requested workflow needs it.
- IDs begin with a letter, followed by letters, digits, `_` or `-`. They must be unique within nodes/scenarios. Avoid ambiguous edge IDs such as `a-b → c` and `a → b-c` together.
- Place centers explicitly for the desired visual story. The renderer measures boxes and adjusts connector endpoints automatically; it does not implement a general graph layout algorithm. Leave room for the widest label. Changing content may require moving centers or route waypoints.

Edge:

```json
{"from":"rows","to":"classify","kind":"payload",
 "sourcePort":"right","targetPort":"top",
 "via":[[650,94],[650,240],[340,240]],
 "label":"All rows","labelX":480,"labelY":230}
```

Only `from` and `to` required. Default routing uses orthogonal segments and direction-appropriate ports. Optional `kind` is `payload` (dashed supplemental input) or `error`. Ports: left/right/top/bottom. `via` supplies intermediate board coordinates; endpoints still attach to measured boxes. A label requires `labelX`/`labelY`. Use only one edge per directed node pair.

Scenario:

```json
{"id":"success","label":"Classify once",
 "path":["rows","classify","results"],
 "data":{"results":{"answers":{"$ref":"confidentAnswers"}}}}
```

The first scenario is selected initially. Its path must contain existing nodes connected by execution edges in the stated direction. Payload edges are additional inputs, not path steps. Every payload edge into a visited consumer lights up when that consumer is reached. Paths wrap automatically after dwelling on their last node. One-node paths are valid.

Scenario `data` replaces the entire example payload for the named node; it is not a deep merge. Without an override, use the node's `data`. This is how different routes show different confidence/results without domain code in the engine.

## Shared examples

```json
"samples":{"rows":[{"id":"t1","description":"OPENAI"}]}
```

Inside node data, scenario data, or another sample, `{"$ref":"rows"}` inserts that sample when the inspector opens. References are local names, never paths or URLs. No evaluation, arbitrary expressions, or remote fetching. Missing/circular references fail validation. An object with exactly the one `$ref` property is reserved for this feature. Any other JSON object is literal data.

Write concrete outputs or scenario overrides instead of JavaScript functions. Keep computation, credentials and real model calls out of the diagram.
