from german_language_engine.hover import HoverBuilder
from german_language_engine.meaning import MeaningResolver
from german_language_engine.models import BoundSlot, ExpressionMatch, ExpressionType, Token
from german_language_engine.resolver import MatchResolver

def test_noun_has_article_singular_plural():
 tokens=[Token(i=0,text="Gefallen",lemma="Gefallen",pos="NOUN")]
 item=MeaningResolver().word_meanings(tokens,[])[0]
 assert (item.lexical_form.article,item.lexical_form.singular,item.lexical_form.plural)==("der","Gefallen","Gefallen")

def test_damit_usage_is_pronominal_adverb():
 tokens=[Token(i=0,text="damit",lemma="damit",pos="ADV")]
 item=MeaningResolver().word_meanings(tokens,[])[0]
 assert item.contextual_meaning_tr=="bununla / bunu yaparak"
 assert item.usage_notes[0].label=="da(r) + mit"

def test_expression_precedes_noun_detail():
 tokens=[Token(i=0,text="Gefallen",lemma="Gefallen",pos="NOUN"),Token(i=1,text="getan",lemma="tun",pos="VERB")]
 expression=ExpressionMatch(pattern_id="nvv.gefallen_tun",canonical="jemandem einen Gefallen tun",type=ExpressionType.NOMEN_VERB,meaning_tr=["birine iyilik yapmak"],token_indices=[0,1],surface="Gefallen getan",confidence=.95,rank=100,grammar_hint="+ Dat. · tun → getan")
 meanings=MeaningResolver().word_meanings(tokens,[expression]); hover=HoverBuilder(MatchResolver()).build(tokens,[expression],meanings)
 assert hover[0].primary_expressions[0].canonical=="jemandem einen Gefallen tun"
 assert hover[0].lexical_form.article=="der"


def test_negated_expression_exposes_contextual_negative_meaning():
 tokens=[Token(i=0,text="Gefallen",lemma="Gefallen",pos="NOUN"),Token(i=1,text="getan",lemma="tun",pos="VERB")]
 expression=ExpressionMatch(pattern_id="nvv.gefallen_tun",canonical="jemandem einen Gefallen tun",type=ExpressionType.NOMEN_VERB,meaning_tr=["birine iyilik yapmak"],token_indices=[0,1],surface="Gefallen getan",confidence=.95,rank=100,negated=True,negation_token_indices=[2])
 meanings=MeaningResolver().word_meanings(tokens,[expression])
 assert expression.contextual_meaning_tr=="birine iyilik yapmamak"
 assert meanings[0].contextual_meaning_tr=="birine iyilik yapmamak"


def test_bound_dative_recipient_is_realized_before_negation():
 tokens=[
  Token(i=0,text="mir",lemma="ich",pos="PRON",morph={"Case":["Dat"]}),
  Token(i=1,text="Gefallen",lemma="Gefallen",pos="NOUN"),
  Token(i=2,text="getan",lemma="tun",pos="VERB"),
 ]
 expression=ExpressionMatch(
  pattern_id="nvv.gefallen_tun",canonical="jemandem einen Gefallen tun",type=ExpressionType.NOMEN_VERB,
  meaning_tr=["birine iyilik yapmak"],token_indices=[0,1,2],surface="mir Gefallen getan",
  confidence=.95,rank=100,negated=True,negation_token_indices=[3],
  bound_slots=[BoundSlot(slot_id="recipient",token_indices=[0],surface="mir",case=["Dat"])],
 )
 meanings=MeaningResolver().word_meanings(tokens,[expression])
 assert expression.contextual_meaning_tr=="bana iyilik yapmamak"
 assert meanings[0].contextual_meaning_tr=="bana iyilik yapmamak"
