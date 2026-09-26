from __future__ import annotations
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field

class ExpressionType(StrEnum):
    IDIOM = "IDIOM"
    REFLEXIVE_VERB = "REFLEXIVE_VERB"
    VERB_PREPOSITION = "VERB_PREPOSITION"
    REFLEXIVE_VERB_PREPOSITION = "REFLEXIVE_VERB_PREPOSITION"
    NOMEN_VERB = "NOMEN_VERB"
    FUNCTION_VERB = "FUNCTION_VERB"
    ADJECTIVE_PREPOSITION = "ADJECTIVE_PREPOSITION"
    COLLOCATION = "COLLOCATION"
    CONNECTOR = "CONNECTOR"
    FIXED_CONSTRUCTION = "FIXED_CONSTRUCTION"

class SlotType(StrEnum):
    LEMMA = "LEMMA"
    REFLEXIVE = "REFLEXIVE"
    PREPOSITION = "PREPOSITION"
    PARTICLE = "PARTICLE"
    OBJECT = "OBJECT"
    CLAUSE = "CLAUSE"
    PRONOMINAL_ADVERB = "PRONOMINAL_ADVERB"

class Token(BaseModel):
    i: int
    text: str
    lemma: str
    pos: str = ""
    tag: str = ""
    dep: str = ""
    head: int | None = None
    morph: dict[str, list[str]] = Field(default_factory=dict)

class Slot(BaseModel):
    id: str
    type: SlotType
    lemma: str | None = None
    alternatives: list[str] = Field(default_factory=list)
    case: list[str] = Field(default_factory=list)
    prep: str | None = None
    optional: bool = False

class ExpressionPattern(BaseModel):
    id: str
    canonical: str
    type: ExpressionType
    head_lemma: str
    slots: list[Slot]
    meaning_tr: list[str] = Field(default_factory=list)
    cefr: str | None = None
    priority: int = 50
    allow_passive: bool = True
    allow_flexible_order: bool = True
    notes: str | None = None

class ExpressionMatch(BaseModel):
    pattern_id: str
    canonical: str
    type: ExpressionType
    meaning_tr: list[str]
    token_indices: list[int]
    surface: str
    confidence: float
    evidence: list[str] = Field(default_factory=list)

class Analysis(BaseModel):
    text: str
    tokens: list[Token]
    expressions: list[ExpressionMatch]
    unmatched_token_indices: list[int]
    metadata: dict[str, Any] = Field(default_factory=dict)
