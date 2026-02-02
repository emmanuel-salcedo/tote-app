from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.auth import require_session

router = APIRouter(tags=["scan"], dependencies=[Depends(require_session)])


@router.get("/scan", response_class=HTMLResponse)
def scan_page() -> HTMLResponse:
    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>QR Scan</title>
        <style>
          body { margin: 0; font-family: Arial, sans-serif; background: #f6f6f6; }
          .container { padding: 24px; max-width: 560px; margin: 0 auto; }
          .card { background: #fff; padding: 16px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
          .camera { width: 100%; height: 320px; background: #111; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #bbb; }
          .hint { margin-top: 12px; color: #666; }
          .cta { margin-top: 16px; display: inline-block; padding: 10px 14px; background: #111; color: #fff; border-radius: 8px; text-decoration: none; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Scan a Tote QR</h1>
          <div class="card">
            <div class="camera">Camera preview will appear here</div>
            <div class="hint">Grant camera access to scan a tote QR.</div>
            <a class="cta" href="/">Back</a>
          </div>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
