# Transaction example: proposed behavior

Use this when the requested diagram concerns the original Acetate classifier proposal. The template is a learning demonstration, not evidence that these features are implemented in Studio.

## Sequence

File → read as text → statement text → Gemini extraction → full structured transactions → deterministic grouping → compact lookup groups → context retrieval → relevant context → Jev first pass → initial answers → confidence gate.

Confident path: gate → results, skipping web research.

Research path: gate → low-confidence subset → same grouping function → compact research request → web research agent → additional context → Jev second pass → results.

Both Jev calls receive ALL original transactions. First also receives retrieved context; second receives original and web context. Draw these preserved full-data inputs explicitly as payload edges.

## Data invariants

- Grouping compacts lookup/research work; it never deletes or merges payments in the full list. Preserve original row IDs, dates, amounts, currency and description.
- Example: 2 OPENAI + 3 PARK*ZONE payments → 2 initial lookup groups; the 3 uncertain parking rows → 1 research request. Keep all 5 output rows.
- First retrieval checks relevant user corrections/known evidence; a miss gives empty context. A past correction is contextual evidence, not an unconditional merchant rule.
- Deterministic grouping is an assumption for this proposal, not proof semantic grouping never needs intelligence.
- Web research gets a public merchant question. Keep row-ID mapping local; do not send identity, card details, dates, amounts, full statement, or private correction history to public search.
- Sources are cited facts about merchant activity, not proof of a user's personal payment arrangement. Research provider is undecided; do not imply Parallel or LangChain is already selected.
- Gemini extracts structured fields; Jev classifies. Jev is paid TypeSafe intelligence; it need not be described as a conventional general-purpose LLM. Verify live product claims if changing them; keep this example conceptual.
- Threshold .80 and confidence values are illustrative, not measured accuracy or chosen production policy. High confidence does not guarantee correctness.
- Only one second classification pass. No recursive research loop.
- Final data sorts confidence ascending with per-row `needs_review`, so uncertain rows appear first. No separate “still low → review” or research-error branch in this agreed view. Add failure flows only when explicitly requested.
- All transaction fixtures and parking.example source are fictional. No real extraction, research, model call, or learning occurs in the HTML.

## Inspector examples

The asset preserves complete JSON for each step, including mapping, query, citation, and classifications. Reference output order after second pass: t3 (.64), t4 (.73), t5 (.92), t1 (.96), t2 (.96). t3 and t4 need review under the example .80 threshold.

The fixture has a correction ID as retrieval evidence. It does not implement correction persistence, training, or a general “reason changed” audit field. If requested, design that explicitly rather than claiming the view already provides it.
