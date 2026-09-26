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
 def resolve_expression_meanings(self,tokens:list[Token],expressions:list[ExpressionMatch])->None:
  token_map={token.i:token for token in tokens}
  for expression in expressions:
   base=expression.meaning_tr[0] if expression.meaning_tr else None
   base=self._realize_bound_slots(base,expression,token_map) if base else base
   if not base:
    expression.contextual_meaning_tr=None
   else:
    expression.contextual_meaning_tr=self._realize_finite_verb(base,expression,tokens)

 def _realize_bound_slots(self,meaning:str,expression:ExpressionMatch,token_map:dict[int,Token])->str:
  recipient=next((slot for slot in expression.bound_slots if slot.slot_id=="recipient"),None)
  if recipient and recipient.token_indices:
   token=token_map.get(recipient.token_indices[0])
   if token:
    dative={
     "mir":"bana","dir":"sana","ihm":"ona","ihr":"ona","uns":"bize","euch":"size","ihnen":"onlara","Ihnen":"size",
    }.get(token.text, None) or {
     "ich":"bana","du":"sana","er":"ona","sie":"ona","es":"ona","wir":"bize","ihr":"size",
    }.get(token.lemma.lower())
    if dative and meaning.startswith("birine "): return dative+" "+meaning[len("birine "):]
  return meaning

 def _realize_finite_verb(self,meaning:str,expression:ExpressionMatch,tokens:list[Token])->str:
  matched=set(expression.token_indices)
  participle=next((t for t in tokens if t.i in matched and "Part" in t.morph.get("VerbForm",[])),None)
  if not participle: return self._negate_tr(meaning) if expression.negated else meaning
  auxiliary=next((t for t in tokens if t.pos=="AUX" and t.head is None),None)
  if not auxiliary: return self._negate_tr(meaning) if expression.negated else meaning
  subject=next((t for t in tokens if t.head==auxiliary.i and t.dep in {"sb","nsubj"}),None)
  if not subject: return self._negate_tr(meaning) if expression.negated else meaning
  person=(subject.morph.get("Person") or auxiliary.morph.get("Person") or [None])[0]
  number=(subject.morph.get("Number") or auxiliary.morph.get("Number") or [None])[0]
  if person=="2" and number=="Sing":
   forms={
    " yapmak":(" yaptın"," yapmadın")," etmek":(" ettin"," etmedin"),
    " olmak":(" oldun"," olmadın")," almak":(" aldın"," almadın")," vermek":(" verdin"," vermedin"),
   }
   for infinitive,(positive,negative) in forms.items():
    if meaning.endswith(infinitive):
     return meaning[:-len(infinitive)]+(negative if expression.negated else positive)
  return self._negate_tr(meaning) if expression.negated else meaning

 def _negate_tr(self,meaning:str)->str:
  replacements=((" yapmak"," yapmamak"),(" etmek"," etmemek"),(" olmak"," olmamak"),(" almak"," almamak"),(" vermek"," vermemek"))
  for positive,negative in replacements:
   if meaning.endswith(positive): return meaning[:-len(positive)]+negative
  return f"{meaning} (olumsuz)"

 def word_meanings(self,tokens:list[Token],expressions:list[ExpressionMatch])->list[TokenMeaning]:
  self.resolve_expression_meanings(tokens,expressions)
  by_token={}
  for expression in expressions:
   for index in expression.token_indices: by_token.setdefault(index,[]).append(expression)
  output=[]
  for token in tokens:
   entry=SEED_WORDS.get(token.lemma.lower(),{}); dictionary=entry.get("meanings",[])
   related=sorted(by_token.get(token.i,[]),key=lambda item:item.rank,reverse=True)
   contextual=(related[0].contextual_meaning_tr or (related[0].meaning_tr[0] if related[0].meaning_tr else None)) if related else (dictionary[0] if dictionary else None)
   lexical=None
   if "noun" in entry:
    article,singular,plural=entry["noun"]; lexical=LexicalForm(article=article,singular=singular,plural=plural)
   notes=[]; low=token.text.lower()
   if low in PRONOMINAL_USAGE:
    contextual,prep,explanation=PRONOMINAL_USAGE[low]
    notes.append(UsageNote(kind="PRONOMINAL_ADVERB",label=f"da(r) + {prep}",explanation_tr=explanation,source=low,refers_to="önceki nesne/olay/durum"))
   output.append(TokenMeaning(token_index=token.i,lemma=token.lemma,contextual_meaning_tr=contextual,dictionary_meanings_tr=dictionary,lexical_form=lexical,usage_notes=notes))
  return output
