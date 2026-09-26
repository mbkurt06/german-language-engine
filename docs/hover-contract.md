# Hover contract — Context first, dictionary second

The primary consumer is a subtitle/reader UI where a learner hovers one German token.

## Display order
1. **Expression/chunk first** — all relevant expressions containing the token, ranked by pedagogical specificity.
2. **Meaning in this sentence** — contextual Turkish meaning.
3. **Compact grammar hint** — e.g. `auf + Akk.`, `reflexiv`, `trennbar`, `Perfekt: ist passiert`.
4. **Word meaning in context**.
5. **Dictionary meanings** — secondary/collapsible.

## Nested analyses
Overlap is not a reason to delete useful information. For `beim Kochen`, a UI may show both the concrete phrase and the productive grammar construction `beim + substantivierter Infinitiv`. The resolver ranks them instead of discarding one.

## Example
Hovering `Rücksicht` in `Darauf müssen wir Rücksicht nehmen.` should conceptually produce:

```json
{
  "token": "Rücksicht",
  "primary_expressions": [{
    "canonical": "auf jemanden/etwas Rücksicht nehmen",
    "meaning_tr": ["birini/bir şeyi dikkate almak"],
    "grammar_hint": "auf + Akk."
  }],
  "contextual_word_meaning_tr": "birini/bir şeyi dikkate almak",
  "dictionary_meanings_tr": ["dikkat", "özen", "göz önünde bulundurma"]
}
```

The UI remains short; deeper dictionary/grammar detail is available only on demand.
