from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle


def export_results(results: Iterable[Dict[str, Any]], output_path: str, file_format: str = "csv") -> str:
    rows = list(results)
    if not rows:
        rows = [{"email": "", "status": "empty"}]

    output_path = str(output_path)
    target = Path(output_path)
    if not target.parent.exists():
        target.parent.mkdir(parents=True, exist_ok=True)

    file_format = file_format.lower()
    if file_format == "csv":
        out = target.with_suffix(".csv")
        df = pd.DataFrame(rows)
        df.to_csv(out, index=False)
        return str(out)
    if file_format == "json":
        out = target.with_suffix(".json")
        with open(out, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, default=str)
        return str(out)
    if file_format == "excel":
        out = target.with_suffix(".xlsx")
        df = pd.DataFrame(rows)
        df.to_excel(out, index=False)
        return str(out)
    if file_format == "html":
        out = target.with_suffix(".html")
        df = pd.DataFrame(rows)
        html = df.to_html(index=False)
        out.write_text(html, encoding="utf-8")
        return str(out)
    if file_format == "pdf":
        out = target.with_suffix(".pdf")
        doc = SimpleDocTemplate(str(out), pagesize=letter)
        elements = []
        table_data = [[key for key in rows[0].keys()] ]
        for row in rows:
            table_data.append([str(row.get(key, "")) for key in rows[0].keys()])
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        doc.build(elements)
        return str(out)

    raise ValueError(f"Unsupported export format: {file_format}")
