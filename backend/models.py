from pydantic import BaseModel, Field


class HighlightRequest(BaseModel):
    html: str = Field(..., min_length=1)
    page_title: str = Field(..., min_length=1)
    page_url: str = Field(..., min_length=1)
    hostname: str | None = None
    captured_at: str = Field(..., min_length=1)


class HealthResponse(BaseModel):
    status: str
    document_path: str
    version: str


class HighlightResponse(BaseModel):
    status: str
    message: str
    highlight_number: int | None = None
    article_url: str | None = None
