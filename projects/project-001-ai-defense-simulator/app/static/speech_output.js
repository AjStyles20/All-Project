(() => {
  const root = document.querySelector("[data-tts-controls]");
  if (!root) return;

  const listen = root.querySelector("[data-tts-listen]");
  const stop = root.querySelector("[data-tts-stop]");
  const status = root.querySelector("[data-tts-status]");
  const endpoint = root.dataset.endpoint;
  const configured = root.dataset.configured === "true";
  let audio = null;
  let objectUrl = null;

  const setStatus = (message) => { status.textContent = message; };
  const cleanup = () => {
    if (audio) {
      audio.pause();
      audio.src = "";
      audio = null;
    }
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }
    stop.disabled = true;
  };

  listen.addEventListener("click", async () => {
    if (!configured || !endpoint) return;
    cleanup();
    listen.disabled = true;
    setStatus("Preparing reviewer audio…");
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Accept": "audio/mpeg" },
        credentials: "same-origin",
      });
      if (!response.ok) throw new Error("Reviewer audio is unavailable.");
      const blob = await response.blob();
      if (blob.type && blob.type !== "audio/mpeg") throw new Error("Unexpected audio format.");
      objectUrl = URL.createObjectURL(blob);
      audio = new Audio(objectUrl);
      audio.addEventListener("ended", () => {
        cleanup();
        setStatus("Reviewer audio finished.");
      }, { once: true });
      audio.addEventListener("error", () => {
        cleanup();
        setStatus("Reviewer audio could not be played.");
      }, { once: true });
      stop.disabled = false;
      setStatus("Playing reviewer question.");
      await audio.play();
    } catch (_error) {
      cleanup();
      setStatus("Reviewer audio is unavailable. Read the question text above.");
    } finally {
      listen.disabled = false;
    }
  });

  stop.addEventListener("click", () => {
    cleanup();
    setStatus("Reviewer audio stopped.");
  });

  window.addEventListener("beforeunload", cleanup, { once: true });
})();
