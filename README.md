# gabrr-skills

Reusable agent skills by Gabriel Oliveira.

| Skill | What it does |
| --- | --- |
| [acetate-flow](skills/acetate-flow/SKILL.md) | Turns workflow JSON into a compact, interactive HTML diagram. Expandable data, branches, looping playback, and light/dark mode. |
| [learn-layered](skills/learn-layered/SKILL.md) | Teaches through a visual, analogy, tiny example, bigger example, and complete example. Chooses images, flows or text to fit the idea; considers interactive HTML for connected systems. |

## Install in Codex

Ask Codex:

```text
Use $skill-installer to install these skills:
https://github.com/gabrr/gabrr-skills/tree/main/skills/acetate-flow
https://github.com/gabrr/gabrr-skills/tree/main/skills/learn-layered
```

Or copy the desired skill folder into your repository's `.agents/skills/` directory. Include the whole folder, not just `SKILL.md`.

## Use

```text
$learn-layered Help me understand idempotency.
```

```text
$acetate-flow Show an order moving through validation, payment,
and fulfillment, with a branch for declined payment.
```

`learn-layered` does not need a server, Python, or a particular image tool. Available tools determine which visual formats it can produce. `acetate-flow` requires Python 3 to generate HTML; its output opens directly in a browser without a server or runtime dependencies.

## Generate a diagram directly

From this repository:

```sh
python3 skills/acetate-flow/scripts/create_flow.py /tmp/example.html \
  --config skills/acetate-flow/assets/minimal.json
```

Edit the JSON for content changes; reuse the renderer. See the [JSON format](skills/acetate-flow/references/json-format.md). The generator refuses to overwrite an existing file unless you pass `--force`.

The bundled classification example is fictional and describes a proposed workflow. It does not connect to an app, run AI calls, or perform web research.

## License

[MIT](LICENSE).
