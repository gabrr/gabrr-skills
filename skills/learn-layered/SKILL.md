---
name: learn-layered
description: Teach a difficult concept through a visual, an analogy, and increasingly concrete examples—tiny, bigger, then complete. Use for layered explanations or requests to understand how something works. For several connected concepts, consider an interactive visual lesson instead of a single explanation.
---

# Learn Layered

Teach the subject itself. Do not describe a teaching plan instead of teaching. Let the learner see one idea, connect it to something familiar, and progressively recognize it in a complete working example.

## Choose the shape

Respect the learner's chosen format and existing conversation preferences. Otherwise distinguish:

- **One concept:** a compact visual explanation followed by analogy, tiny example, bigger example, complete example. Keep this in the conversation; HTML is not the default.
- **A collection of connected concepts:** consider interactive HTML when navigation, comparison, state changes or relationships would make the system easier to understand. A difficult concept alone does not justify building a website.

If the scope/format is genuinely unclear and would change the work substantially, ask one short question: “One concept step by step, or an interactive view of the whole system?” Do not ask a format question every time or reconfirm an explicit choice. If the topic is broad, narrow to a coherent example unless the learner wants the entire system.

## Pick the visual by what it explains

1. **Prefer an actual image** for spatial relationships, physical intuition or a memorable analogy that benefits from a picture. Use an available image-generation tool or a suitable existing illustration; make the picture carry meaning, not decoration. Explain briefly what each important element represents.
2. **Use a flow or rich diagram** when a short sequence, branch, boundary or relationship explains the concept sufficiently. Use available inline diagrams or diagram tools; a flow does not require a whole HTML lesson.
3. **Use text notation** when the idea is so simple that a small sketch or a few words are clearer. Do not default to ASCII boxes merely because they are convenient.

Do not create an image for every layer. Reuse or extend the first mental model. If image tools or HTML are unavailable, disclose the limitation briefly and use the best available representation; never claim to have generated an image that is only a text sketch.

## Build the layers

Keep the same subject, actors and example throughout. Each layer adds one conceptual part, while making the previous parts more concrete.

1. **Visual:** show the central idea before introducing terminology. Identify only the few parts needed to read the picture.
2. **Analogy:** connect that idea to something familiar. Map the analogy to the real parts, and name its main limit when it would otherwise mislead.
3. **Tiny example:** show the smallest actual instance. For software, a short runnable fragment or an explicit input/output is often enough.
4. **Bigger example:** extend that same instance with the next necessary mechanism. When useful, show the limitation that makes this addition necessary and what it improves. Do not manufacture problems merely to follow a template.
5. **Complete example:** connect the pieces into one realistic end-to-end case. Show the concrete result and how the earlier pieces participate. “Complete” is relative to the learning goal; avoid production boilerplate that obscures it.

These are teaching stages, not a quota of five messages. Split a stage when it contains multiple new ideas; combine trivial transitions. Give all necessary layers when requested. Otherwise start with a small coherent layer and let the learner steer; don't force a quiz or approval after every step.

## Keep it understandable

- Few words, concrete nouns, short labels. Let pictures, changes and examples do the work.
- Explain a new term where it first becomes necessary, not in an opening glossary.
- Prefer a visible before/after or a worked action over another paragraph. Label diagrams by what changes and what the learner should notice.
- When the learner says they do not understand, change the representation or reduce the step size. Do not merely repeat the explanation with more words.
- Keep analogies distinguishable from facts. Simplify honestly; mark illustrative data, pseudocode and important omitted conditions.
- Verify unstable, uncertain or security-critical claims with authoritative sources. Keep source detail secondary to the lesson.

## Interactive system lessons

When HTML is appropriate or requested, use rich scenes, mock interfaces, tokens/cards, meaningful diagrams and small demonstrations—not walls of text embedded in a webpage. Make one layer visible at a time, with direct navigation and an optional all-layers view. Put technical details behind expansion. Respect reduced motion and keyboard access.

If the lesson is primarily a workflow and `$acetate-flow` is available, use its JSON renderer instead of rewriting the interface. It is optional: this skill works independently and does not require that skill, a browser, HTML, or image tools. Keep the analogy → tiny → bigger → complete progression even when the presentation is interactive.
