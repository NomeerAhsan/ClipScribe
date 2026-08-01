import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.document_writer import DocumentWriter
from backend.models import HealthResponse, HighlightRequest, HighlightResponse

VERSION = "0.1.0"


def configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.clipscribe_log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(settings.logs_dir / "clipscribe.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings.document_path.parent.mkdir(parents=True, exist_ok=True)
    logging.getLogger("clipscribe").info("ClipScribe backend started on %s:%s", settings.clipscribe_host, settings.clipscribe_port)
    yield


app = FastAPI(title="ClipScribe", version=VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

writer = DocumentWriter(settings.document_path, settings.state_path)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        document_path=str(settings.document_path),
        version=VERSION,
    )


@app.post("/highlights", response_model=HighlightResponse)
def create_highlight(payload: HighlightRequest) -> HighlightResponse:
    try:
        status, highlight_number = writer.append_highlight(
            html=payload.html,
            page_title=payload.page_title,
            page_url=payload.page_url,
            captured_at=payload.captured_at,
        )
    except Exception as exc:
        logging.getLogger("clipscribe").exception("Failed to append highlight")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if status == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="Duplicate highlight skipped",
        )

    return HighlightResponse(
        status="saved",
        message="Highlight appended to document",
        highlight_number=highlight_number,
        article_url=payload.page_url,
    )


def main() -> None:
    import uvicorn

    uvicorn.run(
        "backend.app:app",
        host=settings.clipscribe_host,
        port=settings.clipscribe_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
