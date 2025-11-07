from __future__ import annotations
import typer
from .pipeline import load_config, Pipeline

app = typer.Typer(help="Entity Extraction Pipeline CLI")

@app.command("run")
def run(config: str = typer.Option("configs/default.yaml", "--config", "-c", help="Path to config YAML")):
    cfg = load_config(config)
    p = Pipeline(cfg)
    records = p.run()
    typer.echo(f"✅ Pipeline complete: wrote {len(records)} records to {cfg.io['output_path']}")

if __name__ == "__main__":
    app()
