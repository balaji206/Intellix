import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.services.parser import SUPPORTED
from app.services.pipeline import index_file, retrieve

router = APIRouter()


class SearchRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


@router.post("/index")
def index_document(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in SUPPORTED:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Allowed: {sorted(SUPPORTED)}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        return index_file(tmp_path, filename=file.filename)
    except ValueError as e:
        raise HTTPException(422, str(e))
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@router.post("/search")
def search_documents(req: SearchRequest):
    return {"question": req.question, "results": retrieve(req.question, req.limit)}