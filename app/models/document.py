from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    size_bytes: int
    chunks_count: int
    preview: str
