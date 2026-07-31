from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.document_extraction import extract_text
from app.services.text_chunking import chunk_text
from app.services.embeddings import embed_chunks
from app.services.hashing import compute_content_hash
from app.db.vector_store import add_chunks
from app.db.document_repository import get_document_by_filename, upsert_document

UPLOAD_DIR = Path("data/uploads")


def save_uploaded_file(filename: str, content: bytes) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / filename
    file_path.write_bytes(content)
    return file_path


async def ingest_document(session: AsyncSession, filename: str, content: bytes) -> dict:
    content_hash = compute_content_hash(content)

    existing = await get_document_by_filename(session, filename)

    if existing and existing.content_hash == content_hash:
        return {
            "status": "unchanged",
            "chunks_count": existing.chunks_count,
            "preview": "",
        }

    file_path = save_uploaded_file(filename, content)

    text = extract_text(file_path)
    chunks = chunk_text(text)

    embeddings = embed_chunks(chunks)
    add_chunks(document_id=filename, chunks=chunks, embeddings=embeddings)

    await upsert_document(
        session=session,
        filename=filename,
        content_hash=content_hash,
        chunks_count=len(chunks),
    )

    status = "updated" if existing else "new"

    return {
        "status": status,
        "chunks_count": len(chunks),
        "preview": text[:300],
    }