from __future__ import annotations
from typing import Dict, Any, List
from dataclasses import dataclass
import yaml
from .utils import read_texts, preprocess, export_records
from .spacy_model import SpacyNER

@dataclass
class Config:
    run_name: str
    model: Dict[str, Any]
    io: Dict[str, Any]
    processing: Dict[str, Any]
    export: Dict[str, Any]

def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return Config(**cfg)

def dedupe_entities(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for e in entities:
        key = (e["text"], e["label"], e["start_char"], e["end_char"])
        if key in seen: 
            continue
        seen.add(key)
        out.append(e)
    return out

class Pipeline:
    def __init__(self, config: Config):
        self.config = config
        backend = config.model.get("backend", "spacy").lower()
        if backend != "spacy":
            raise NotImplementedError(f"Backend '{backend}' not implemented yet.")
        self.model = SpacyNER(config.model.get("spacy_model", "en_core_web_sm"))

    def run(self) -> List[Dict[str, Any]]:
        cfg = self.config
        texts = read_texts(cfg.io["input_path"])
        texts = [preprocess(t, lowercase=cfg.processing["lowercase"], strip_whitespace=cfg.processing["strip_whitespace"]) for t in texts]

        batch_ents = self.model.infer(texts, include_scores=cfg.export.get("include_scores", True))

        records: List[Dict[str, Any]] = []
        for i, (text, ents) in enumerate(zip(texts, batch_ents)):
            if cfg.processing.get("dedupe_entities", True):
                ents = dedupe_entities(ents)
            rec = {
                "id": i,
                "text": text if cfg.processing.get("include_context", True) else None,
                "entities": ents
            }
            records.append(rec)

        export_records(cfg.io["output_path"], records, fmt=cfg.export.get("format", "jsonl"))
        return records
