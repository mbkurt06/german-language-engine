from __future__ import annotations

from .hover import HoverBuilder
from .lexicon import ExpressionLexicon
from .matcher import StructuralMatcher
from .meaning import MeaningResolver
from .models import Analysis
from .nlp import NLPAdapter, SpacyGermanAdapter
from .resolver import MatchResolver


class GermanLanguageEngine:
    def __init__(
        self,
        nlp: NLPAdapter | None = None,
        lexicon: ExpressionLexicon | None = None,
    ):
        self.nlp = nlp or SpacyGermanAdapter()
        self.lexicon = lexicon or ExpressionLexicon.bundled()
        self.matcher = StructuralMatcher()
        self.resolver = MatchResolver()
        self.meaning_resolver = MeaningResolver()
        self.hover_builder = HoverBuilder(self.resolver)

    def analyze(self, text: str) -> Analysis:
        tokens = self.nlp.parse(text)
        candidates = []
        seen = set()
        for token in tokens:
            for pattern in self.lexicon.candidates(token.lemma):
                key = (pattern.id, token.i)
                if key in seen:
                    continue
                seen.add(key)
                for match in self.matcher.match(tokens, pattern):
                    match.grammar_hint = pattern.grammar_hint
                    candidates.append(match)

        patterns = {pattern.id: pattern for pattern in self.lexicon.patterns}
        expressions = self.resolver.resolve(candidates, patterns)
        meanings = self.meaning_resolver.word_meanings(tokens, expressions)
        hover = self.hover_builder.build(tokens, expressions, meanings)
        covered = {i for match in expressions for i in match.token_indices}
        unmatched = [
            token.i for token in tokens if token.i not in covered and token.pos != "PUNCT"
        ]
        return Analysis(
            text=text,
            tokens=tokens,
            expressions=expressions,
            token_meanings=meanings,
            hover=hover,
            unmatched_token_indices=unmatched,
            metadata={
                "candidate_matches": len(candidates),
                "lexicon_size": len(self.lexicon.patterns),
                "ux_policy": "context-first-dictionary-second",
            },
        )
