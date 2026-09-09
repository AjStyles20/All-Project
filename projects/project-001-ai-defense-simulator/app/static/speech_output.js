(() => {
  const root = document.querySelector("[data-tts-controls]");
  if (!root) return;

  const listen = root.querySelector("[data-tts-listen]");
  const stop = root.querySelector("[data-tts-stop]");
  const status = root.querySelector("[data-tts-status]");
  const endpoint = root.dataset.endpoint;
  const serverConfigured = root.dataset.serverConfigured === "true";
  const questionText = (root.dataset.questionText || "").trim();
  const browserSpeechAvailable = (
    "speechSynthesis" in window && typeof window.SpeechSynthesisUtterance === "function"
  );

  let audio = null;
  let objectUrl = null;
  let utterance = null;

  const setStatus = (message) => { status.textContent = message; };

  const cleanupServerAudio = () => {
    if (audio) {
      audio.pause();
      audio.src = "";
      audio = null;
    }
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }
  };

  const stopBrowserSpeech = () => {
    if (browserSpeechAvailable) {
      window.speechSynthesis.cancel();
    }
    utterance = null;
  };

  const cleanup = () => {
    cleanupServerAudio();
    stopBrowserSpeech();
    stop.disabled = true;
  };

  const playBrowserSpeech = () => {
    if (!browserSpeechAvailable || !questionText) {
      throw new Error("Browser speech unavailable");
    }
    stopBrowserSpeech();
    utterance = new window.SpeechSynthesisUtterance(questionText);
    utterance.addEventListener("end", () => {
      utterance = null;
      stop.disabled = true;
      setStatus("Reviewer audio finished.");
    }, { once: true });
    utterance.addEventListener("error", () => {
      utterance = null;
      stop.disabled = true;
      setStatus("Local reviewer speech could not be played. Read the question text above.");
    }, { once: true });
    stop.disabled = false;
    setStatus("Playing reviewer question with local browser speech.");
    window.speechSynthesis.speak(utterance);
  };

  const playServerSpeech = async () => {
    if (!endpoint) throw new Error("Server speech endpoint unavailable");
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
      cleanupServerAudio();
      stop.disabled = true;
      setStatus("Reviewer audio finished.");
    }, { once: true });
    audio.addEventListener("error", () => {
      cleanupServerAudio();
      stop.disabled = true;
      setStatus("Reviewer audio could not be played.");
    }, { once: true });
    stop.disabled = false;
    setStatus("Playing reviewer question.");
    await audio.play();
  };

  if (!serverConfigured && (!browserSpeechAvailable || !questionText)) {
    listen.disabled = true;
    setStatus("Reviewer speech is unavailable in this browser. Read the question text above.");
  }

  listen.addEventListener("click", async () => {
    cleanup();
    listen.disabled = true;
    try {
      if (serverConfigured) {
        setStatus("Preparing reviewer audio…");
        try {
          await playServerSpeech();
          return;
        } catch (_serverError) {
          cleanupServerAudio();
          if (!browserSpeechAvailable) throw _serverError;
          setStatus("Server reviewer audio is unavailable. Using local browser speech.");
        }
      }
      playBrowserSpeech();
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
