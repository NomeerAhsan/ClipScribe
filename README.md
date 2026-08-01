# ClipScribe

**Highlight the web. Build your research document.**

ClipScribe captures text you highlight on any webpage and appends it—with formatting and source metadata—to a local Microsoft Word document.

## How it works

1. Start the local Python backend
2. Load the Chrome extension
3. Highlight text on any webpage
4. Open `documents/Research.docx` — your excerpt is already there

## Requirements

- Python 3.12+
- Google Chrome
- Microsoft Word or any app that opens `.docx` files

## Setup

### 1. Backend

```bash
cd clipscribe
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
python run.py
```

The API runs at `http://127.0.0.1:8765`.

> **Note:** There is no file named `backend.app`. The backend lives in `backend/app.py`. You can start it with either `python run.py` or `python -m backend.app`.

### 2. Chrome extension

1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select the `browser-extension` folder

### 3. Verify

1. Click the ClipScribe extension icon
2. Click **Check connection** — you should see the document path
3. Highlight text on any webpage
4. Check `documents/Research.docx`

**Tip:** Close `Research.docx` in Word while capturing highlights. Word locks the file while it is open, which prevents new highlights from being saved.

## Project structure

```
clipscribe/
├── backend/              # FastAPI app (entry point: backend/app.py)
├── browser-extension/    # Chrome MV3 extension
├── documents/            # Generated Research.docx (gitignored)
├── tests/
├── run.py                # Start the backend server
├── requirements.txt
└── .env.example
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Backend status and document path |
| POST | `/highlights` | Append a highlight to the Word document |

## Configuration

Copy `.env.example` to `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLIPSCRIBE_HOST` | `127.0.0.1` | Bind address |
| `CLIPSCRIBE_PORT` | `8765` | API port |
| `CLIPSCRIBE_DOCUMENT_PATH` | `documents/Research.docx` | Output file |
| `CLIPSCRIBE_LOG_LEVEL` | `INFO` | Log verbosity |

## Development

```bash
pytest
```
