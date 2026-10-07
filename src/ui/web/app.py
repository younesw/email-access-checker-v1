from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.batch.processor import batch_check
from src.core.email_checker import check_email
from src.reporting.exporters import export_results

app = FastAPI(title="Email Access Checker API", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "email-access-checker"}


@app.post("/check")
def check_endpoint(payload: Dict[str, str]) -> Dict[str, Any]:
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Both email and password are required")
    return check_email(email, password)


@app.post("/batch")
def batch_endpoint(payload: List[Dict[str, str]]) -> Dict[str, Any]:
    return batch_check(payload)


@app.post("/upload")
async def upload_results(file: UploadFile = File(...)) -> Dict[str, Any]:
    contents = await file.read()
    suffix = Path(file.filename or "data.json").suffix.lower()
    if suffix == ".csv":
        import pandas as pd
        df = pd.read_csv(file.file)
        records = df.to_dict(orient="records")
    elif suffix in {".json", ".jsn"}:
        records = json.loads(contents.decode("utf-8"))
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or JSON.")

    result = batch_check(records)
    return result


@app.get("/results")
def results() -> Dict[str, List[Dict[str, Any]]]:
    return {"results": []}


@app.post("/export")
def export_endpoint(payload: Dict[str, Any]) -> JSONResponse:
    results = payload.get("results", [])
    output_path = payload.get("output_path", "results_export")
    file_format = payload.get("format", "csv")
    try:
        file_path = export_results(results, output_path, file_format)
        return JSONResponse({"status": "ok", "path": file_path, "format": file_format})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
