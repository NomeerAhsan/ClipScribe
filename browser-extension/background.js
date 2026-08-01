const DEFAULT_BACKEND_URL = "http://127.0.0.1:8765";

async function getBackendUrl() {
  const result = await chrome.storage.local.get(["backendUrl"]);
  return result.backendUrl || DEFAULT_BACKEND_URL;
}

async function setBadge(text, color) {
  try {
    await chrome.action.setBadgeText({ text });
    await chrome.action.setBadgeBackgroundColor({ color });
  } catch (error) {
    console.warn("[ClipScribe] Could not update badge:", error);
  }
}

async function sendHighlight(payload) {
  const backendUrl = await getBackendUrl();

  try {
    const response = await fetch(`${backendUrl}/highlights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.status === 409) {
      await setBadge("DUP", "#888888");
      return { ok: true, duplicate: true };
    }

    if (!response.ok) {
      let detail = await response.text();
      try {
        const parsed = JSON.parse(detail);
        detail = parsed.detail || detail;
      } catch {
        // keep raw text
      }
      throw new Error(detail || `Request failed (${response.status})`);
    }

    await setBadge("OK", "#16a34a");
    return { ok: true, duplicate: false };
  } catch (error) {
    console.error("[ClipScribe]", error);
    await setBadge("ERR", "#dc2626");
    throw error;
  } finally {
    setTimeout(() => setBadge("", "#16a34a"), 2000);
  }
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type !== "HIGHLIGHT_CAPTURED") {
    return;
  }

  sendHighlight(message.payload)
    .then((result) => sendResponse(result))
    .catch((error) => sendResponse({ ok: false, error: String(error.message || error) }));

  return true;
});

console.info("[ClipScribe] Background service worker ready");
