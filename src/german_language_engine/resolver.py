from __future__ import annotations
from .models import ExpressionMatch, ExpressionPattern

TYPE_WEIGHT = {
    "IDIOM": 40, "FIXED_CONSTRUCTION": 38, "FUNCTION_VERB": 35,
    "REFLEXIVE_VERB_PREPOSITION": 34, "NOMEN_VERB": 32,
    "VERB_PREPOSITION": 28, "REFLEXIVE_VERB": 25,
    "ADJECTIVE_PREPOSITION": 24, "COLLOCATION": 20, "CONNECTOR": 18,
}

class MatchResolver:
    def resolve(self, matches:list[ExpressionMatch], patterns:dict[str,ExpressionPattern]) -> list[ExpressionMatch]:
        def score(m:ExpressionMatch):
            p=patterns[m.pattern_id]
            return (p.priority + TYPE_WEIGHT.get(m.type.value,0) + len(m.token_indices)*3 + m.confidence*10)
        accepted=[]
        occupied=set()
        for m in sorted(matches,key=score,reverse=True):
            overlap=occupied.intersection(m.token_indices)
            # Nested matches are suppressed: learner sees the most informative chunk.
            if overlap: continue
            accepted.append(m); occupied.update(m.token_indices)
        return sorted(accepted,key=lambda m:min(m.token_indices))
