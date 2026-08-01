const enabledInput = document.getElementById("enabled");
const backendUrlInput = document.getElementById("backendUrl");
const statusEl = document.getElementById("status");
const saveButton = document.getElementById("save");
const checkButton = document.getElementById("check");

async function loadSettings() {
  const result = await chrome.storage.local.get(["enabled", "backendUrl"]);
  enabledInput.checked = result.enabled !== false;
  if (result.backendUrl) {
    backendUrlInput.value = result.backendUrl;
  }
}

function setStatus(message, type = "info") {
  statusEl.textContent = message;
  statusEl.dataset.type = type;
}

saveButton.addEventListener("click", async () => {
  await chrome.storage.local.set({
    enabled: enabledInput.checked,
    backendUrl: backendUrlInput.value.trim(),
  });
  setStatus("Settings saved", "success");
});

checkButton.addEventListener("click", async () => {
  const backendUrl = backendUrlInput.value.trim();
  setStatus("Checking connection...", "info");

  try {
    const response = await fetch(`${backendUrl}/health`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    setStatus(`Connected · ${data.document_path}`, "success");
  } catch (error) {
    setStatus(`Backend unreachable: ${error.message}`, "error");
  }
});

loadSettings();
