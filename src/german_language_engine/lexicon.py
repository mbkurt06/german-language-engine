from __future__ import annotations
from importlib.resources import files
import yaml
from .models import ExpressionPattern

class ExpressionLexicon:
    def __init__(self, patterns: list[ExpressionPattern]):
        self.patterns = patterns
        self.by_head: dict[str, list[ExpressionPattern]] = {}
        for p in patterns:
            self.by_head.setdefault(p.head_lemma.lower(), []).append(p)

    @classmethod
    def bundled(cls) -> "ExpressionLexicon":
        path = files("german_language_engine").joinpath("data/expressions.yml")
        return cls.from_yaml(path.read_text(encoding="utf-8"))

    @classmethod
    def from_yaml(cls, raw: str) -> "ExpressionLexicon":
        data = yaml.safe_load(raw) or []
        return cls([ExpressionPattern.model_validate(item) for item in data])

    def candidates(self, head_lemma: str) -> list[ExpressionPattern]:
        return self.by_head.get(head_lemma.lower(), [])
