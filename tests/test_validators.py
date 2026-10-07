from __future__ import annotations

from typing import Any, Dict, List

from src.reporting.exporters import export_results


def summarize_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    totals = {
        "total": len(results),
        "active": sum(1 for item in results if item.get("status") == "active"),
        "inactive": sum(1 for item in results if item.get("status") == "inactive"),
        "locked": sum(1 for item in results if item.get("status") == "locked"),
        "suspended": sum(1 for item in results if item.get("status") == "suspended"),
        "invalid": sum(1 for item in results if item.get("status") == "invalid"),
        "error": sum(1 for item in results if item.get("status") == "error"),
        "tfa_required": sum(1 for item in results if item.get("details", {}).get("2fa_enabled") is True),
    }
    return totals


def generate_report(results: List[Dict[str, Any]], output_path: str = "report", file_format: str = "pdf") -> Dict[str, Any]:
    summary = summarize_results(results)
    exported_path = export_results(results, output_path, file_format)
    return {
        "summary": summary,
        "format": file_format,
        "exported_path": exported_path,
    }
