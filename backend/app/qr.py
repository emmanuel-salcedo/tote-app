from __future__ import annotations

import base64
import io
import qrcode


def generate_qr_png(data: str) -> bytes:
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr_data_uri(data: str) -> str:
    png = generate_qr_png(data)
    b64 = base64.b64encode(png).decode("ascii")
    return f"data:image/png;base64,{b64}"
