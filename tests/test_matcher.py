from german_language_engine.lexicon import ExpressionLexicon
from german_language_engine.matcher import StructuralMatcher
from german_language_engine.models import Token

LEX=ExpressionLexicon.bundled()
M=StructuralMatcher()

def t(i,text,lemma,pos="X",dep="",head=None,morph=None):
    return Token(i=i,text=text,lemma=lemma,pos=pos,dep=dep,head=head,morph=morph or {})

def pattern(pid):
    return next(p for p in LEX.patterns if p.id==pid)

def test_in_kauf_genommen_passive():
    toks=[
      t(0,"Das","das","PRON","sb",4), t(1,"wurde","werden","AUX","aux",4),
      t(2,"in","in","ADP","mo",3), t(3,"Kauf","Kauf","NOUN","nk",4),
      t(4,"genommen","nehmen","VERB","ROOT",None)
    ]
    m=M.match(toks,pattern("idiom.in_kauf_nehmen"))
    assert m and m[0].canonical=="etwas in Kauf nehmen"

def test_reflexive_pronominal_adverb():
    toks=[
      t(0,"Dafür","dafür","ADV","op",3), t(1,"interessiere","interessieren","VERB","ROOT",None),
      t(2,"ich","ich","PRON","sb",1), t(3,"mich","ich","PRON","oa",1,{"Reflex":["Yes"]})
    ]
    m=M.match(toks,pattern("reflexiv.interessieren_fuer"))
    assert m
    assert any("pronominal-adverb" in e for e in m[0].evidence)

def test_ruecksicht_darauf():
    toks=[
      t(0,"Darauf","darauf","ADV","op",4),t(1,"müssen","müssen","AUX","aux",4),
      t(2,"wir","wir","PRON","sb",4),t(3,"Rücksicht","Rücksicht","NOUN","oa",4),
      t(4,"nehmen","nehmen","VERB","ROOT",None)
    ]
    assert M.match(toks,pattern("nvv.ruecksicht_nehmen"))

def test_decision_passive():
    toks=[
      t(0,"Die","der","DET","nk",1),t(1,"Entscheidung","Entscheidung","NOUN","sb",3),
      t(2,"wurde","werden","AUX","aux",3),t(3,"getroffen","treffen","VERB","ROOT",None)
    ]
    assert M.match(toks,pattern("nvv.entscheidung_treffen"))


def test_gefallen_tun_detects_keinen_as_negation():
    toks=[
      t(0,"Nein","nein","PART","ng",3), t(1,",",",","PUNCT","punct",0),
      t(2,"damit","damit","ADV","mo",3), t(3,"hast","haben","AUX","ROOT",None),
      t(4,"du","du","PRON","sb",3), t(5,"mir","ich","PRON","da",8,{"Case":["Dat"]}),
      t(6,"keinen","kein","DET","nk",7,{"Case":["Acc"]}),
      t(7,"Gefallen","gefallen","NOUN","oa",8,{"Case":["Acc"]}),
      t(8,"getan","tun","VERB","oc",3), t(9,".",".","PUNCT","punct",3)
    ]
    matches=M.match(toks,pattern("nvv.gefallen_tun"))
    assert matches
    assert matches[0].negated is True
    assert matches[0].negation_token_indices == [6]
    recipient=next(slot for slot in matches[0].bound_slots if slot.slot_id=="recipient")
    assert recipient.token_indices == [5]
    assert recipient.surface == "mir"
    assert recipient.case == ["Dat"]


def test_gefallen_tun_positive_is_not_negated():
    toks=[
      t(0,"Du","du","PRON","sb",3),
      t(1,"mir","ich","PRON","da",3,{"Case":["Dat"]}),
      t(2,"einen","ein","DET","nk",3,{"Case":["Acc"]}),
      t(3,"Gefallen","gefallen","NOUN","oa",4,{"Case":["Acc"]}),
      t(4,"getan","tun","VERB","ROOT",None)
    ]
    matches=M.match(toks,pattern("nvv.gefallen_tun"))
    assert matches
    assert matches[0].negated is False
    assert matches[0].negation_token_indices == []
