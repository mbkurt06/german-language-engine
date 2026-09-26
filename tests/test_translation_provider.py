from german_language_engine.engine import GermanLanguageEngine
from german_language_engine.models import Token


class FakeNLP:
    def parse(self, text):
        return [
            Token(i=0, text="Propaganda", lemma="Propaganda", pos="NOUN"),
            Token(i=1, text="Dummheit", lemma="Dummheit", pos="NOUN"),
        ]


class FakeTranslationProvider:
    values = {
        "Propaganda": "propaganda",
        "Dummheit": "aptallık",
        "Propaganda Dummheit": "Propaganda, aptallık.",
    }

    def translate(self, text):
        return self.values.get(text)


def test_provider_supplies_sentence_and_unknown_word_meanings():
    provider = FakeTranslationProvider()
    engine = GermanLanguageEngine(
        nlp=FakeNLP(),
        sentence_meaning_provider=provider,
        lexical_meaning_provider=provider,
    )

    result = engine.analyze("Propaganda Dummheit")

    assert result.sentence_meaning_tr == "Propaganda, aptallık."
    assert result.hover[0].contextual_word_meaning_tr == "propaganda"
    assert result.hover[1].contextual_word_meaning_tr == "aptallık"
    assert result.hover[1].dictionary_meanings_tr == ["aptallık"]
