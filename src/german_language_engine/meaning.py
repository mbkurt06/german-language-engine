from __future__ import annotations
from .models import ExpressionMatch, LexicalForm, Token, TokenMeaning, UsageNote

SEED_WORDS={
 "gefallen":{"meanings":["iyilik","jest"],"noun":("der","Gefallen","Gefallen")},
 "rücksicht":{"meanings":["dikkat","özen","göz önünde bulundurma"],"noun":("die","Rücksicht","Rücksichten")},
 "weg":{"meanings":["yol"],"noun":("der","Weg","Wege")},
 "machen":{"meanings":["yapmak","etmek"]},"suchen":{"meanings":["aramak","araştırmak"]},
 "kochen":{"meanings":["yemek pişirmek","kaynatmak"]},
 "passieren":{"meanings":["olmak","meydana gelmek","bir yerden geçmek"]},
 "glauben":{"meanings":["inanmak","sanmak"]},"nehmen":{"meanings":["almak"]},
 "tun":{"meanings":["yapmak","etmek"]},"interessieren":{"meanings":["ilgilendirmek","ilgilenmek"]},
}
PRONOMINAL_USAGE={
 "damit":("bununla / bunu yaparak","mit","Önceden söylenen bir nesneye, olaya veya duruma tekrar ad vermeden gönderme yapar."),
 "darauf":("bunun üzerine / buna","auf","Önceden söylenen bir şeye veya duruma 'auf' ilişkisiyle gönderme yapar."),
 "davon":("bundan / bunun hakkında","von","Önceden söylenen bir şeye veya duruma 'von' ilişkisiyle gönderme yapar."),
 "daran":("buna / bunda","an","Önceden söylenen bir şeye veya duruma 'an' ilişkisiyle gönderme yapar."),
 "dafür":("bunun için / buna karşılık","für","Önceden söylenen bir şeye veya duruma 'für' ilişkisiyle gönderme yapar."),
}
class MeaningResolver:
 def word_meanings(self,tokens:list[Token],expressions:list[ExpressionMatch])->list[TokenMeaning]:
  by_token={}
  for expression in expressions:
   for index in expression.token_indices: by_token.setdefault(index,[]).append(expression)
  output=[]
  for token in tokens:
   entry=SEED_WORDS.get(token.lemma.lower(),{}); dictionary=entry.get("meanings",[])
   related=sorted(by_token.get(token.i,[]),key=lambda item:item.rank,reverse=True)
   contextual=related[0].meaning_tr[0] if related and related[0].meaning_tr else (dictionary[0] if dictionary else None)
   lexical=None
   if "noun" in entry:
    article,singular,plural=entry["noun"]; lexical=LexicalForm(article=article,singular=singular,plural=plural)
   notes=[]; low=token.text.lower()
   if low in PRONOMINAL_USAGE:
    contextual,prep,explanation=PRONOMINAL_USAGE[low]
    notes.append(UsageNote(kind="PRONOMINAL_ADVERB",label=f"da(r) + {prep}",explanation_tr=explanation,source=low,refers_to="önceki nesne/olay/durum"))
   output.append(TokenMeaning(token_index=token.i,lemma=token.lemma,contextual_meaning_tr=contextual,dictionary_meanings_tr=dictionary,lexical_form=lexical,usage_notes=notes))
  return output
