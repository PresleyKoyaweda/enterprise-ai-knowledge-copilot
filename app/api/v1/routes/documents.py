from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.models.document import DocumentUploadResponse
from app.services.document_ingestion import ingest_document
from app.core.dependencies import require_admin

MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 Mo

router = APIRouter()


@router.post("/documents", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_admin),
) -> DocumentUploadResponse:
    content = await file.read()

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 50 Mo)")

    try:
        chunks, text = ingest_document(file.filename, content)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return DocumentUploadResponse(
        filename=file.filename,
        size_bytes=len(content),
        chunks_count=len(chunks),
        preview=text[:300],
    )