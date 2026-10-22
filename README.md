# gabrr-skills

Two skills. See the result, then try a prompt.

## acetate-flow

The Acetate classification workflow: models, tools, data, and a research branch.

![Acetate workflow: extraction, grouping, context, classification and web research](assets/acetate-flow.gif)

```text
$acetate-flow Show statement extraction, grouping, context retrieval,
classification, and web research for low-confidence results.
```

[Example HTML](examples/acetate-classification.html) · [Edit its JSON](skills/acetate-flow/assets/classification.json) · [Skill](skills/acetate-flow/SKILL.md)

## learn-layered

One concrete example, built piece by piece. The subject decides how many layers.

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

Images preferred; flows or text when simpler. HTML for connected systems.

<details>
<summary>Install in Codex</summary>

Ask Codex:

```text
Use $skill-installer to install both:
https://github.com/gabrr/gabrr-skills/tree/main/skills/acetate-flow
https://github.com/gabrr/gabrr-skills/tree/main/skills/learn-layered
```

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
