from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.ui.web.api import app as api_app

app = FastAPI(title="Email Access Checker Dashboard", version="1.0.0")
app.mount("/api", api_app)


@app.get("/", response_class=HTMLResponse)
def dashboard_index() -> str:
    return """
    <html>
      <head>
        <title>Email Access Checker Dashboard</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: #e2e8f0; }
          .card { background: #111827; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
          .button { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>Email Access Checker Dashboard</h1>
          <p>Upload a CSV or JSON file to process email account checks.</p>
          <button class="button" onclick="location.href='/api/docs'">Open API Docs</button>
        </div>
      </body>
    </html>
    """
