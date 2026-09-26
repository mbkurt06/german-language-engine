from __future__ import annotations

from .models import ExpressionMatch, Token, TokenMeaning

# Small seed resource. This is deliberately separate from expression matching so a
# production dictionary/translation provider can replace or extend it later.
SEED_WORD_MEANINGS_TR: dict[str, list[str]] = {
    "machen": ["yapmak", "etmek"],
    "suchen": ["aramak", "araştırmak"],
    "kochen": ["yemek pişirmek", "kaynatmak"],
    "passieren": ["olmak", "meydana gelmek", "bir yerden geçmek"],
    "glauben": ["inanmak", "sanmak"],
    "nehmen": ["almak"],
    "rücksicht": ["dikkat", "özen", "göz önünde bulundurma"],
    "interessieren": ["ilgilendirmek", "ilgilenmek"],
    "weg": ["yol"],
}


class MeaningResolver:
    def word_meanings(
        self, tokens: list[Token], expressions: list[ExpressionMatch]
    ) -> list[TokenMeaning]:
        by_token: dict[int, list[ExpressionMatch]] = {}
        for expression in expressions:
            for index in expression.token_indices:
                by_token.setdefault(index, []).append(expression)

        output = []
        for token in tokens:
            dictionary = SEED_WORD_MEANINGS_TR.get(token.lemma.lower(), [])
            contextual = None
            related = sorted(
                by_token.get(token.i, []), key=lambda item: item.rank, reverse=True
            )
            # The expression meaning is a useful contextual fallback. A later semantic
            # provider may refine this to a token-specific sense.
            if related and related[0].meaning_tr:
                contextual = related[0].meaning_tr[0]
            elif dictionary:
                contextual = dictionary[0]
            output.append(
                TokenMeaning(
                    token_index=token.i,
                    lemma=token.lemma,
                    contextual_meaning_tr=contextual,
                    dictionary_meanings_tr=dictionary,
                )
            )
        return output
