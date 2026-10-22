---
name: learn-layered
description: A visual learning framework for understanding one concept or several connected concepts. Begin with a visual and analogy, then grow one concrete example by adding one meaningful part per layer. Let the subject determine the layer count; consider interactive HTML for connected systems.
---

# Learn Layered

A framework for learning one concept or a collection of connected concepts. Teach the subject itself. Do not describe a teaching plan instead of teaching. Let the learner see one idea, connect it to something familiar, and progressively recognize it in a complete working example.

## Choose the shape

Respect the learner's chosen format and existing conversation preferences. Otherwise distinguish:

- **One concept:** a compact visual and analogy, then a small real example that grows cumulatively until the learning goal is met. Keep this in the conversation; HTML is not the default.
- **A collection of connected concepts:** consider interactive HTML when navigation, comparison, state changes or relationships would make the system easier to understand. A difficult concept alone does not justify building a website.

If the scope/format is genuinely unclear and would change the work substantially, ask one short question: “One concept step by step, or an interactive view of the whole system?” Do not ask a format question every time or reconfirm an explicit choice. If the topic is broad, narrow to a coherent example unless the learner wants the entire system.

## Pick the visual by what it explains

1. **Prefer an actual image** for spatial relationships, physical intuition or a memorable analogy that benefits from a picture. Use an available image-generation tool or a suitable existing illustration; make the picture carry meaning, not decoration. Explain briefly what each important element represents.
2. **Use a flow or rich diagram** when a short sequence, branch, boundary or relationship explains the concept sufficiently. Use available inline diagrams or diagram tools; a flow does not require a whole HTML lesson.
3. **Use text notation** when the idea is so simple that a small sketch or a few words are clearer. Do not default to ASCII boxes merely because they are convenient.

Do not create an image for every layer. Reuse or extend the first mental model. If image tools or HTML are unavailable, disclose the limitation briefly and use the best available representation; never claim to have generated an image that is only a text sketch.

## Grow one example; do not fill a five-stage template

The subject determines the number of layers. “Tiny,” “bigger,” and “complete” describe the example's increasing concreteness, not three mandatory layers or visible lesson titles.

- Start with a meaningful visual and a familiar analogy. These can share a layer when the image itself conveys the analogy. Map its important parts to the real subject.
- After the analogy, switch to the smallest concrete version of the real example. Keep that example, its actors, values, and visual positions throughout.
- Add **one meaningful part per layer**. Retain earlier parts and highlight only the addition. Show the same data or action moving through the expanding system. A layer can reveal a mechanism already hidden inside an earlier box.
- Use actual mechanism titles: “The request arrives,” “Choose the handler,” “Read the body,” rather than “Tiny,” “Bigger,” and “Complete.”
- Add as many intermediate layers as the subject needs. Don't jump from a two-line snippet to a full implementation, replace the example with a different one, or restart the diagram every time.
- Finish when the parts form the concrete outcome the learner asked about. Reveal the runnable implementation or detailed trace only after its pieces have been explained. Avoid unrelated production boilerplate.

For example, a server lesson might start with a restaurant kitchen analogy, then follow **one browser request**: send → arrive → route → read the body → validate → look up data → compute → respond → render. Those are possible mechanisms for that subject, not a mandatory list for every lesson. Show previously introduced mechanisms alongside each addition.

When a new part solves a real limitation, show the limitation and the value added. Do not invent failures merely to justify another layer. Give all necessary layers when requested; otherwise begin with a coherent small layer and let the learner steer without a quiz or approval gate after every step.

## Keep it understandable

- Few words, concrete nouns, short labels. Let pictures, changes and examples do the work.
- Explain a new term where it first becomes necessary, not in an opening glossary.
- Prefer a visible before/after or a worked action over another paragraph. Label diagrams by what changes and what the learner should notice.
- When the learner says they do not understand, change the representation or reduce the step size. Do not merely repeat the explanation with more words.
- Keep analogies distinguishable from facts. Simplify honestly; mark illustrative data, pseudocode and important omitted conditions.
- Verify unstable, uncertain or security-critical claims with authoritative sources. Keep source detail secondary to the lesson.

## Interactive system lessons

When HTML is appropriate or requested, use rich scenes, mock interfaces, tokens/cards, meaningful diagrams and small demonstrations—not walls of text embedded in a webpage. Make one layer visible at a time, with direct navigation and an optional all-layers view. Put technical details behind expansion. Respect reduced motion and keyboard access.

If the lesson is primarily a workflow and `$acetate-flow` is available, use its JSON renderer instead of rewriting the interface. It is optional: this skill works independently and does not require that skill, a browser, HTML, or image tools. Keep the cumulative example and subject-driven layer count even when the presentation is interactive.
