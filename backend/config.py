from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    clipscribe_host: str = "127.0.0.1"
    clipscribe_port: int = 8765
    clipscribe_document_path: str = "documents/Research.docx"
    clipscribe_log_level: str = "INFO"

    @property
    def document_path(self) -> Path:
        path = Path(self.clipscribe_document_path)
        if not path.is_absolute():
            path = ROOT_DIR / path
        return path

    @property
    def state_path(self) -> Path:
        return self.document_path.parent / ".clipscribe_state.json"

    @property
    def logs_dir(self) -> Path:
        logs = ROOT_DIR / "logs"
        logs.mkdir(exist_ok=True)
        return logs


settings = Settings()
