from __future__ import annotations
from .models import ExpressionMatch, LexicalForm, Token, TokenMeaning, UsageNote
from .translation import NullTranslationProvider, TranslationProvider

SEED_WORDS={
 "gefallen":{"meanings":["iyilik","jest"],"noun":("der","Gefallen","Gefallen")},
 "rücksicht":{"meanings":["dikkat","özen","göz önünde bulundurma"],"noun":("die","Rücksicht","Rücksichten")},
 "weg":{"meanings":["yol"],"noun":("der","Weg","Wege")},
 "machen":{"meanings":["yapmak","etmek"]},"suchen":{"meanings":["aramak","araştırmak"]},
 "kochen":{"meanings":["yemek pişirmek","kaynatmak"]},
 "passieren":{"meanings":["olmak","meydana gelmek","bir yerden geçmek"]},
 "glauben":{"meanings":["inanmak","sanmak"]},"nehmen":{"meanings":["almak"]},
 "tun":{"meanings":["yapmak","etmek"]},"interessieren":{"meanings":["ilgilendirmek","ilgilenmek"]},
 "bekommen":{"meanings":["almak","elde etmek","edinmek"]},
 "rundfunkanstaltung":{"meanings":["yayın kuruluşu","radyo-televizyon kurumu"],"noun":("die","Rundfunkanstalt","Rundfunkanstalten")},
 "was":{"meanings":["ne","neyi"]},"wir":{"meanings":["biz"]},
 "land":{"meanings":["ülke"],"noun":("das","Land","Länder")},
 "sprache":{"meanings":["dil"],"noun":("die","Sprache","Sprachen")},
 "wort":{"meanings":["kelime","sözcük"],"noun":("das","Wort","Wörter")},
 "frage":{"meanings":["soru"],"noun":("die","Frage","Fragen")},
 "video":{"meanings":["video"],"noun":("das","Video","Videos")},
 "sonne":{"meanings":["güneş"],"noun":("die","Sonne","Sonnen")},
 "freund":{"meanings":["arkadaş","dost"],"noun":("der","Freund","Freunde")},
 "kontext":{"meanings":["bağlam"],"noun":("der","Kontext","Kontexte")},
 "fantasie":{"meanings":["hayal gücü","fantezi"],"noun":("die","Fantasie","Fantasien")},
 "sponsor":{"meanings":["sponsor"],"noun":("der","Sponsor","Sponsoren")},
 "suche":{"meanings":["arama"],"noun":("die","Suche","Suchen")},
 "tutor":{"meanings":["özel öğretmen","eğitmen"],"noun":("der","Tutor","Tutoren")},
 "physik":{"meanings":["fizik"],"noun":("die","Physik","Physiken")},
 "universität":{"meanings":["üniversite"],"noun":("die","Universität","Universitäten")},
 "ökonomie":{"meanings":["ekonomi"],"noun":("die","Ökonomie","Ökonomien")},
 "option":{"meanings":["seçenek"],"noun":("die","Option","Optionen")},
 "widerstand":{"meanings":["direnç","karşı koyma"],"noun":("der","Widerstand","Widerstände")},
 "ding":{"meanings":["şey","nesne"],"noun":("das","Ding","Dinge")},
 "stimme":{"meanings":["ses","oy"],"noun":("die","Stimme","Stimmen")},
 "homepage":{"meanings":["ana sayfa","web sitesi"],"noun":("die","Homepage","Homepages")},
 "erfolg":{"meanings":["başarı"],"noun":("der","Erfolg","Erfolge")},
 "spaß":{"meanings":["eğlence","keyif"],"noun":("der","Spaß","Späße")},
 "sprechen":{"meanings":["konuşmak"]},
 "bedeuten":{"meanings":["anlamına gelmek"]},
 "benutzen":{"meanings":["kullanmak"]},
 "beantworten":{"meanings":["cevaplamak"]},
 "studieren":{"meanings":["üniversitede okumak","öğrenim görmek"]},
 "zeigen":{"meanings":["göstermek"]},
 "denken":{"meanings":["düşünmek"]},
 "schaffen":{"meanings":["başarmak","yapabilmek"]},
 "hören":{"meanings":["duymak","dinlemek"]},
 "schreiben":{"meanings":["yazmak"]},
 "verbessern":{"meanings":["iyileştirmek","geliştirmek"]},
 "finden":{"meanings":["bulmak"]},
 "lernen":{"meanings":["öğrenmek"]},
 "kauf":{"meanings":["satın alma","alış"] ,"noun":("der","Kauf","Käufe")},
 "vertun":{"meanings":["boşa harcamak","yanlış kullanmak"]},
 "verschieben":{"meanings":["ertelemek","kaydırmak","yerini değiştirmek"]},
 "aufschieben":{"meanings":["ertelemek","sonraya bırakmak"]},
 "auf":{"meanings":["üzerinde","üzerine","-e/-a (bağlama göre)"]},
 "in":{"meanings":["içinde","içine","-de/-da (bağlama göre)"]},
 "sich":{"meanings":["kendini / kendisine (dönüşlü zamir)"]},
 "über":{"meanings":["hakkında","üzerinde","üzerinden"]},
 "bei":{"meanings":["yanında","-de/-da","nezdinde (bağlama göre)"]},
 "bedanken":{"meanings":["teşekkür etmek"]},
 "so":{"meanings":["böyle","öyle","bu şekilde"]},
 "aussehen":{"meanings":["görünmek","gibi görünmek"]},
 "aufstehen":{"meanings":["ayağa kalkmak","yataktan kalkmak"]},
 "anfangen":{"meanings":["başlamak"]},
 "ankommen":{"meanings":["varmak","gelip ulaşmak"]},
 "mitmachen":{"meanings":["katılmak","birlikte yapmak"]},
 "weitergehen":{"meanings":["devam etmek","ilerlemeye devam etmek"]},
}
PRONOMINAL_USAGE={
 "damit":("bununla / bunu yaparak","mit","Önceden söylenen bir nesneye, olaya veya duruma tekrar ad vermeden gönderme yapar."),
 "darauf":("bunun üzerine / buna","auf","Önceden söylenen bir şeye veya duruma 'auf' ilişkisiyle gönderme yapar."),
 "davon":("bundan / bunun hakkında","von","Önceden söylenen bir şeye veya duruma 'von' ilişkisiyle gönderme yapar."),
 "daran":("buna / bunda","an","Önceden söylenen bir şeye veya duruma 'an' ilişkisiyle gönderme yapar."),
 "dafür":("bunun için / buna karşılık","für","Önceden söylenen bir şeye veya duruma 'für' ilişkisiyle gönderme yapar."),
}
LEXICAL_PROVIDER_POS={"NOUN","PROPN","VERB","ADJ","ADV"}
class MeaningResolver:
 def __init__(self,lexical_provider:TranslationProvider|None=None):
  self.lexical_provider=lexical_provider or NullTranslationProvider()

 def lexical_meanings(self,lemma:str,pos:str="VERB")->list[str]:
  entry=SEED_WORDS.get(lemma.lower(),{})
  dictionary=list(entry.get("meanings",[]))
  if not dictionary and pos in LEXICAL_PROVIDER_POS:
   fallback=self.lexical_provider.translate(lemma)
   if fallback: dictionary=[fallback]
  return dictionary

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

 def _pluralize_tr(self,meaning:str)->str:
  word=meaning.strip()
  if not word or " " in word or word.endswith(("lar","ler")): return meaning
  back_vowels=set("aıou")
  front_vowels=set("eiöü")
  vowels=[char for char in word.lower() if char in back_vowels|front_vowels]
  if not vowels: return meaning
  return word+("lar" if vowels[-1] in back_vowels else "ler")

 def word_meanings(self,tokens:list[Token],expressions:list[ExpressionMatch])->list[TokenMeaning]:
  self.resolve_expression_meanings(tokens,expressions)
  by_token={}
  for expression in expressions:
   for index in expression.token_indices: by_token.setdefault(index,[]).append(expression)
  output=[]
  for token in tokens:
   entry=SEED_WORDS.get(token.lemma.lower(),{}); dictionary=self.lexical_meanings(token.lemma,token.pos)
   related=sorted(by_token.get(token.i,[]),key=lambda item:item.rank,reverse=True)
   contextual=(related[0].contextual_meaning_tr or (related[0].meaning_tr[0] if related[0].meaning_tr else None)) if related else (dictionary[0] if dictionary else None)
   lexical=None
   noun_forms=entry.get("noun")
   if noun_forms:
    article,singular,plural=noun_forms
    lexical=LexicalForm(article=article,singular=singular,plural=plural)
   if not related and contextual and token.pos in {"NOUN","PROPN"}:
    should_pluralize=False
    if noun_forms:
     _,singular,plural=noun_forms
     surface=token.text.casefold()
     if surface==plural.casefold():
      should_pluralize=True
     elif surface!=singular.casefold() and "Plur" in token.morph.get("Number",[]):
      should_pluralize=True
    elif "Plur" in token.morph.get("Number",[]):
     should_pluralize=True
    if should_pluralize:
     contextual=self._pluralize_tr(contextual)
   notes=[]; low=token.text.lower()
   if low in PRONOMINAL_USAGE:
    contextual,prep,explanation=PRONOMINAL_USAGE[low]
    notes.append(UsageNote(kind="PRONOMINAL_ADVERB",label=f"da(r) + {prep}",explanation_tr=explanation,source=low,refers_to="önceki nesne/olay/durum"))
   output.append(TokenMeaning(token_index=token.i,lemma=token.lemma,contextual_meaning_tr=contextual,dictionary_meanings_tr=dictionary,lexical_form=lexical,usage_notes=notes))
  return output
