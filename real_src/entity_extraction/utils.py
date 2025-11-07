from __future__ import annotations
import json, csv, pathlib
from typing import Iterable, List, Dict, Any, Generator
import pandas as pd

def read_texts(path: str | pathlib.Path) -> List[str]:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    if p.suffix.lower() == ".txt":
        return [line.strip("\n") for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    if p.suffix.lower() == ".csv":
        df = pd.read_csv(p)
        if "text" not in df.columns:
            raise ValueError("CSV must have a 'text' column.")
        return df["text"].dropna().astype(str).tolist()
    if p.suffix.lower() == ".jsonl":
        out = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                if "text" in obj and obj["text"]:
                    out.append(str(obj["text"]))
        return out
    raise ValueError(f"Unsupported input type: {p.suffix}")

def export_records(path: str | pathlib.Path, records: Iterable[Dict[str, Any]], fmt: str = "jsonl") -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "jsonl":
        with p.open("w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    elif fmt == "csv":
        recs = list(records)
        if not recs:
            p.write_text("", encoding="utf-8"); return
        keys = sorted({k for r in recs for k in r.keys()})
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(recs)
    else:
        raise ValueError(f"Unsupported export format: {fmt}")

def preprocess(text: str, *, lowercase: bool, strip_whitespace: bool) -> str:
    if strip_whitespace:
        text = " ".join(text.split())
    if lowercase:
        text = text.lower()
    return text
