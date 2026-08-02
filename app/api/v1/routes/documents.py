from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import require_admin
from app.db.session import get_db_session
from app.models.document import DocumentUploadResponse
from app.services.document_ingestion import ingest_document

MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 Mo

router = APIRouter()


@router.post("/documents", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_db_session),
) -> DocumentUploadResponse:
    content = await file.read()

    if not file.filename:
        raise HTTPException(status_code=400, detail="Le fichier doit avoir un nom")

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413, detail="Fichier trop volumineux (max 50 Mo)"
        )

    try:
        result = await ingest_document(session, file.filename, content)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return DocumentUploadResponse(
        filename=file.filename,
        status=result["status"],
        size_bytes=len(content),
        chunks_count=result["chunks_count"],
        preview=result["preview"],
    )
