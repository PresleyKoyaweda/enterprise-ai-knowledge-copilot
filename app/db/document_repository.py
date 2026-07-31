from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document


async def get_document_by_filename(session: AsyncSession, filename: str) -> Document | None:
    result = await session.execute(select(Document).where(Document.filename == filename))
    return result.scalar_one_or_none()


async def upsert_document(
    session: AsyncSession,
    filename: str,
    content_hash: str,
    chunks_count: int,
) -> Document:
    existing = await get_document_by_filename(session, filename)

    if existing:
        existing.content_hash = content_hash
        existing.chunks_count = chunks_count
        existing.ingested_at = datetime.now(timezone.utc)
    else:
        existing = Document(
            filename=filename,
            content_hash=content_hash,
            chunks_count=chunks_count,
            ingested_at=datetime.now(timezone.utc),
        )
        session.add(existing)

    await session.commit()
    await session.refresh(existing)

    return existing