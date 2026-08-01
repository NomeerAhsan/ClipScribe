const DEFAULT_BACKEND_URL = "http://127.0.0.1:8765";
const CAPTURE_DELAY_MS = 120;
const DUPLICATE_WINDOW_MS = 2000;

let captureTimer = null;
let lastCapturedSignature = "";
let lastCapturedAt = 0;

function serializeSelection(range) {
  const container = document.createElement("div");
  container.appendChild(range.cloneContents());
  return container.innerHTML.trim();
}

function selectionSignature(text, url) {
  return `${url}|${text}`;
}

function showToast(message, type = "info") {
  const existing = document.getElementById("clipscribe-toast");
  if (existing) {
    existing.remove();
  }

  const toast = document.createElement("div");
  toast.id = "clipscribe-toast";
  toast.textContent = message;
  toast.style.cssText = [
    "position: fixed",
    "bottom: 24px",
    "right: 24px",
    "z-index: 2147483647",
    "padding: 12px 16px",
    "border-radius: 10px",
    "font: 13px/1.4 Segoe UI, sans-serif",
    "color: #fff",
    "box-shadow: 0 8px 24px rgba(0,0,0,0.18)",
    "pointer-events: none",
    type === "error" ? "background:#dc2626" : type === "success" ? "background:#16a34a" : "background:#2563eb",
  ].join(";");
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

async function isEnabled() {
  const result = await chrome.storage.local.get(["enabled"]);
  return result.enabled !== false;
}

function scheduleCapture() {
  clearTimeout(captureTimer);
  captureTimer = setTimeout(captureSelection, CAPTURE_DELAY_MS);
}

async function captureSelection() {
  if (!(await isEnabled())) {
    return;
  }

  const selection = window.getSelection();
  if (!selection || selection.isCollapsed || !selection.rangeCount) {
    return;
  }

  const text = selection.toString().trim();
  if (!text) {
    return;
  }

  const signature = selectionSignature(text, window.location.href);
  const now = Date.now();
  if (signature === lastCapturedSignature && now - lastCapturedAt < DUPLICATE_WINDOW_MS) {
    return;
  }

  const range = selection.getRangeAt(0);
  const html = serializeSelection(range);

  const payload = {
    html,
    page_title: document.title || window.location.hostname,
    page_url: window.location.href,
    hostname: window.location.hostname,
    captured_at: new Date().toISOString(),
  };

  try {
    const response = await chrome.runtime.sendMessage({
      type: "HIGHLIGHT_CAPTURED",
      payload,
    });

    if (!response?.ok) {
      throw new Error(response?.error || "Background worker did not confirm save");
    }

    lastCapturedSignature = signature;
    lastCapturedAt = now;
    showToast("ClipScribe: saved to Word", "success");
  } catch (error) {
    console.error("[ClipScribe]", error);
    const message = String(error?.message || error);
    if (message.includes("Receiving end does not exist") || message.includes("Extension context invalidated")) {
      showToast("ClipScribe: refresh this page, then try again", "error");
    } else {
      showToast(`ClipScribe: ${message}`, "error");
    }
  }
}

document.addEventListener("mouseup", scheduleCapture, true);
document.addEventListener("keyup", scheduleCapture, true);

console.info("[ClipScribe] Content script loaded on", window.location.href);
