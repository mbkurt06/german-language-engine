from __future__ import annotations
from .lexicon import ExpressionLexicon
from .matcher import StructuralMatcher
from .models import Analysis
from .nlp import NLPAdapter, SpacyGermanAdapter
from .resolver import MatchResolver

class GermanLanguageEngine:
    def __init__(self, nlp:NLPAdapter|None=None, lexicon:ExpressionLexicon|None=None):
        self.nlp=nlp or SpacyGermanAdapter()
        self.lexicon=lexicon or ExpressionLexicon.bundled()
        self.matcher=StructuralMatcher()
        self.resolver=MatchResolver()

    def analyze(self,text:str)->Analysis:
        tokens=self.nlp.parse(text)
        candidates=[]
        seen=set()
        for token in tokens:
            for pattern in self.lexicon.candidates(token.lemma):
                key=(pattern.id,token.i)
                if key in seen: continue
                seen.add(key)
                candidates.extend(self.matcher.match(tokens,pattern))
        patterns={p.id:p for p in self.lexicon.patterns}
        expressions=self.resolver.resolve(candidates,patterns)
        covered={i for m in expressions for i in m.token_indices}
        unmatched=[t.i for t in tokens if t.i not in covered and t.pos!="PUNCT"]
        return Analysis(
            text=text,tokens=tokens,expressions=expressions,unmatched_token_indices=unmatched,
            metadata={"candidate_matches":len(candidates),"lexicon_size":len(self.lexicon.patterns)}
        )
