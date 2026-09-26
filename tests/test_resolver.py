from german_language_engine.models import ExpressionMatch, ExpressionPattern, ExpressionType
from german_language_engine.resolver import MatchResolver


def p(pid, typ, priority):
    return ExpressionPattern(
        id=pid, canonical=pid, type=typ, head_lemma="x", slots=[], priority=priority
    )


def m(pid, typ, idx):
    return ExpressionMatch(
        pattern_id=pid,
        canonical=pid,
        type=typ,
        meaning_tr=[],
        token_indices=idx,
        surface="",
        confidence=0.9,
    )


def test_long_specific_expression_wins_overlap():
    patterns = {
        "idiom": p("idiom", ExpressionType.IDIOM, 90),
        "verb": p("verb", ExpressionType.VERB_PREPOSITION, 50),
    }
    out = MatchResolver().resolve(
        [
            m("verb", ExpressionType.VERB_PREPOSITION, [2, 4]),
            m("idiom", ExpressionType.IDIOM, [1, 2, 4]),
        ],
        patterns,
    )
    assert [x.pattern_id for x in out] == ["idiom"]
