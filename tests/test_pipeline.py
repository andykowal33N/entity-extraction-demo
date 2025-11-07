from pathlib import Path
from src.entity_extraction.pipeline import load_config, Pipeline

def test_smoke():
    cfg = load_config("configs/default.yaml")
    p = Pipeline(cfg)
    out = p.run()
    assert isinstance(out, list)
    assert Path(cfg.io["output_path"]).exists()
