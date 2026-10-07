from __future__ import annotations

import json
from pathlib import Path

import typer

from src.batch.processor import batch_check
from src.core.email_checker import check_email
from src.reporting.exporters import export_results
from src.reporting.generator import generate_report

app = typer.Typer(help="Email Access Checker CLI")


@app.command("check")
def check_command(email: str = typer.Option(..., "--email"), password: str = typer.Option(..., "--password")) -> None:
    result = check_email(email, password)
    typer.echo(json.dumps(result, indent=2, default=str))


@app.command("batch")
def batch_command(file: str = typer.Option(..., "--file"), output: str = typer.Option("results.json", "--output")) -> None:
    accounts = []
    path = Path(file)
    if path.suffix.lower() == ".csv":
        import pandas as pd
        df = pd.read_csv(path)
        accounts = df.to_dict(orient="records")
    elif path.suffix.lower() in {".json", ".jsn"}:
        with path.open("r", encoding="utf-8") as handle:
            accounts = json.load(handle)
    else:
        raise typer.BadParameter("Supported batch formats: CSV or JSON")

    output_payload = batch_check(accounts)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            json.dump(output_payload, handle, indent=2, default=str)
    typer.echo(json.dumps(output_payload, indent=2, default=str))


@app.command("schedule")
def schedule_command(file: str = typer.Option(..., "--file"), interval: str = typer.Option("24h", "--interval")) -> None:
    from src.batch.scheduler import schedule_jobs
    result = schedule_jobs(file, interval=interval)
    typer.echo(json.dumps(result, indent=2, default=str))


@app.command("report")
def report_command(input_file: str = typer.Option(..., "--input"), fmt: str = typer.Option("pdf", "--format"), output: str = typer.Option("report", "--output")) -> None:
    if input_file.endswith(".json"):
        with open(input_file, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        results = payload.get("results", payload)
    else:
        results = []
    exported = generate_report(results, output_path=output, file_format=fmt)
    typer.echo(json.dumps(exported, indent=2, default=str))


@app.command("api")
def api_command(host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    from src.ui.web.api import app as api_app
    uvicorn.run(api_app, host=host, port=port)


@app.command("dashboard")
def dashboard_command(host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    from src.ui.web.app import app as dashboard_app
    uvicorn.run(dashboard_app, host=host, port=port)


if __name__ == "__main__":
    app()
