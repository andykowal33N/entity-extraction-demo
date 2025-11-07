from __future__ import annotations
from typing import List, Dict, Any
import spacy

class SpacyNER:
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError as e:
            raise RuntimeError(
                f"SpaCy model '{model_name}' not found. "
                f"Install via: python -m spacy download {model_name}"
            ) from e

    def infer(self, texts: List[str], include_scores: bool = True) -> List[List[Dict[str, Any]]]:
        docs = list(self.nlp.pipe(texts, disable=["tagger", "parser", "lemmatizer"]))
        outputs: List[List[Dict[str, Any]]] = []
        for doc in docs:
            ents = []
            for ent in doc.ents:
                ents.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "score": getattr(ent, "kb_id_", None) if include_scores else None  # spaCy small model doesn't give scores
                })
            outputs.append(ents)
        return outputs
