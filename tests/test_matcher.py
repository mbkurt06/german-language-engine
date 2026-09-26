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
