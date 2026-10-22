# gabrr-skills

A catalog of independent skills. Pick what you need.

| Skill | Purpose |
| --- | --- |
| [Acetate Flow](#acetate-flow) | An AI-assisted alternative to Mermaid, with typed nodes and inspectable data. |
| [Learn Layered](#learn-layered) | A visual learning framework for one concept or several connected concepts. |

## acetate-flow

Describe a workflow; AI builds the diagram from JSON. Clearly distinguish **data, tools, AI, and decisions**. Click a node to inspect its inputs and outputs in a side panel.

The example below shows Acetate’s proposed classification workflow.

![Acetate workflow: extraction, grouping, context, classification and web research](assets/acetate-flow.gif)

```text
$acetate-flow Show statement extraction, grouping, context retrieval,
classification, and web research for low-confidence results.
```

[Example HTML](examples/acetate-classification.html) · [Edit its JSON](skills/acetate-flow/assets/classification.json) · [Skill](skills/acetate-flow/SKILL.md)

## learn-layered

Understand one concept—or a whole system of concepts—through visuals, analogy, and one concrete example that grows a part at a time. The subject determines the layers.

![How servers work: a kitchen analogy becomes one browser request, expanded mechanism by mechanism](assets/learn-layered.gif)

```text
$learn-layered How do servers work? Start with a kitchen analogy,
then follow one real browser request as each part is added.
```

```text
$learn-layered Explain OAuth, identity, and sessions together.
Use interactive HTML.
```

[Follow the example](examples/how-servers-work.md) · [Run it](examples/how-servers-work.py) · [Skill](skills/learn-layered/SKILL.md)

Images, flows, or text for individual concepts; interactive HTML when connected concepts benefit from it.

<details>
<summary>Install in Codex</summary>

Install either skill by asking Codex:

```text
Use $skill-installer to install:
https://github.com/gabrr/gabrr-skills/tree/main/skills/acetate-flow
```

For Learn Layered, use `https://github.com/gabrr/gabrr-skills/tree/main/skills/learn-layered` instead. Each skill works independently.

Or copy whole skill folders into `.agents/skills/`.

</details>

<details>
<summary>Generate the example locally</summary>

Python 3; no server or runtime dependencies:

```sh
python3 skills/acetate-flow/scripts/create_flow.py /tmp/acetate.html \
  --config skills/acetate-flow/assets/classification.json
```

Open the output in your browser. Add `--force` to replace an existing output.

[JSON format](skills/acetate-flow/references/json-format.md). GIFs are illustrated previews, not screen recordings. Regenerate with `python3 scripts/render-previews.py` (requires Pillow).

All examples use fictional data and make no real payments or AI calls.

</details>

[MIT license](LICENSE)
