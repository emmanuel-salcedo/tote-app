from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.auth import require_session

router = APIRouter(tags=["checkout-ui"], dependencies=[Depends(require_session)])


@router.get("/checkout", response_class=HTMLResponse)
def checkout_page() -> HTMLResponse:
    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Checkout</title>
        <style>
          body { margin: 0; font-family: Arial, sans-serif; background: #f6f6f6; }
          .container { padding: 24px; max-width: 640px; margin: 0 auto; }
          .card { background: #fff; padding: 16px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
          label { display: block; margin: 10px 0 6px; font-weight: 600; }
          input, textarea { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; }
          .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
          .cta { margin-top: 16px; display: inline-block; padding: 10px 14px; background: #111; color: #fff; border-radius: 8px; text-decoration: none; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Checkout Item</h1>
          <div class="card">
            <label>Item ID</label>
            <input placeholder="e.g. 42" />

            <div class="row">
              <div>
                <label>Checked Out To</label>
                <input placeholder="Name" />
              </div>
              <div>
                <label>Due Date</label>
                <input type="date" />
              </div>
            </div>

            <label>Notes</label>
            <textarea rows="3" placeholder="Optional notes"></textarea>

            <a class="cta" href="#">Checkout</a>
            <a class="cta" style="background:#444;" href="#">Check-in</a>
          </div>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
