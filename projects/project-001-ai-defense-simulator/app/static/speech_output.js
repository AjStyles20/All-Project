(() => {
  const root = document.querySelector("[data-tts-controls]");
  if (!root) return;

  const listen = root.querySelector("[data-tts-listen]");
  const pause = root.querySelector("[data-tts-pause]");
  const resume = root.querySelector("[data-tts-resume]");
  const stop = root.querySelector("[data-tts-stop]");
  const rate = root.querySelector("[data-tts-rate]");
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
  let mode = null;
  let paused = false;

  const selectedRate = () => {
    const value = Number.parseFloat(rate?.value || "1");
    return [0.75, 1, 1.25, 1.5].includes(value) ? value : 1;
  };

  const setStatus = (message) => { status.textContent = message; };

  const setPlaybackButtons = ({ active = false, isPaused = false } = {}) => {
    stop.disabled = !active;
    pause.disabled = !active || isPaused;
    resume.disabled = !active || !isPaused;
  };

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
    mode = null;
    paused = false;
    setPlaybackButtons();
  };

  const playBrowserSpeech = () => {
    if (!browserSpeechAvailable || !questionText) {
      throw new Error("Browser speech unavailable");
    }
    stopBrowserSpeech();
    utterance = new window.SpeechSynthesisUtterance(questionText);
    utterance.rate = selectedRate();
    mode = "browser";
    paused = false;
    utterance.addEventListener("end", () => {
      utterance = null;
      mode = null;
      paused = false;
      setPlaybackButtons();
      setStatus("Reviewer audio finished.");
    }, { once: true });
    utterance.addEventListener("error", () => {
      utterance = null;
      mode = null;
      paused = false;
      setPlaybackButtons();
      setStatus("Local reviewer speech could not be played. Read the question text above.");
    }, { once: true });
    setPlaybackButtons({ active: true, isPaused: false });
    setStatus(`Playing reviewer question with local browser speech at ${selectedRate()}×.`);
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
    audio.playbackRate = selectedRate();
    mode = "server";
    paused = false;
    audio.addEventListener("ended", () => {
      cleanupServerAudio();
      mode = null;
      paused = false;
      setPlaybackButtons();
      setStatus("Reviewer audio finished.");
    }, { once: true });
    audio.addEventListener("error", () => {
      cleanupServerAudio();
      mode = null;
      paused = false;
      setPlaybackButtons();
      setStatus("Reviewer audio could not be played.");
    }, { once: true });
    setPlaybackButtons({ active: true, isPaused: false });
    setStatus(`Playing reviewer question at ${selectedRate()}×.`);
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

  pause.addEventListener("click", () => {
    if (mode === "server" && audio && !audio.paused) {
      audio.pause();
      paused = true;
    } else if (mode === "browser" && browserSpeechAvailable && window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      paused = true;
    } else {
      return;
    }
    setPlaybackButtons({ active: true, isPaused: true });
    setStatus("Reviewer audio paused.");
  });

  resume.addEventListener("click", async () => {
    if (mode === "server" && audio && paused) {
      audio.playbackRate = selectedRate();
      await audio.play();
      paused = false;
    } else if (mode === "browser" && browserSpeechAvailable && paused) {
      window.speechSynthesis.resume();
      paused = false;
    } else {
      return;
    }
    setPlaybackButtons({ active: true, isPaused: false });
    setStatus(`Reviewer audio resumed at ${selectedRate()}×.`);
  });

  rate.addEventListener("change", () => {
    if (mode === "server" && audio) {
      audio.playbackRate = selectedRate();
      setStatus(`Reviewer audio speed changed to ${selectedRate()}×.`);
      return;
    }
    if (mode === "browser" && utterance) {
      setStatus("Speed change will apply the next time you replay this browser-spoken question.");
    }
  });

  stop.addEventListener("click", () => {
    cleanup();
    setStatus("Reviewer audio stopped.");
  });

  window.addEventListener("beforeunload", cleanup, { once: true });
})();
