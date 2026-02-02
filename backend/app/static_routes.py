from __future__ import annotations

import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["static"])


@router.get("/manifest.json")
def manifest() -> FileResponse:
    path = os.getenv("MANIFEST_PATH", "/app/public/manifest.json")
    return FileResponse(path)
