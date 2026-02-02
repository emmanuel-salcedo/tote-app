from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse

from app.auth import require_session
from app.qr import generate_qr_data_uri, generate_qr_png
from app.tote_repo import get_tote

router = APIRouter(prefix="/totes", tags=["qr"], dependencies=[Depends(require_session)])


@router.get("/{tote_id}/qr")
def get_tote_qr(tote_id: int) -> Response:
    tote = get_tote(tote_id)
    if not tote:
        raise HTTPException(status_code=404, detail="Tote not found")
    png = generate_qr_png(tote["qr_value"])
    return Response(content=png, media_type="image/png")


@router.get("/{tote_id}/qr/print", response_class=HTMLResponse)
def print_tote_qr(tote_id: int) -> HTMLResponse:
    tote = get_tote(tote_id)
    if not tote:
        raise HTTPException(status_code=404, detail="Tote not found")

    qr_uri = generate_qr_data_uri(tote["qr_value"])
    tote_label = tote["tote_name"] or f"Tote {tote['tote_number']}"

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Print QR</title>
        <style>
          body {{ margin: 0; font-family: Arial, sans-serif; }}
          .page {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; width: 8.5in; height: 11in; padding: 0.25in; box-sizing: border-box; gap: 0.25in; }}
          .label {{ border: 1px dashed #999; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
          .label img {{ width: 2.2in; height: 2.2in; }}
          .label .text {{ margin-top: 0.1in; font-size: 14pt; }}
        </style>
      </head>
      <body>
        <div class="page">
          {''.join([f'<div class="label"><img src="{qr_uri}" /><div class="text">{tote_label}</div></div>' for _ in range(4)])}
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
