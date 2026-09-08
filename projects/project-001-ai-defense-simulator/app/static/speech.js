(() => {
  "use strict";

  const MAX_RECORDING_MS = 120000;

  function chooseMimeType() {
    const candidates = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/ogg;codecs=opus",
      "audio/mp4",
    ];
    if (typeof MediaRecorder === "undefined") return null;
    return candidates.find((type) => MediaRecorder.isTypeSupported(type)) || "";
  }

  function releaseStream(stream) {
    if (!stream) return;
    stream.getTracks().forEach((track) => track.stop());
  }

  function initControls(root) {
    const configured = root.dataset.configured === "true";
    const endpoint = root.dataset.endpoint;
    const start = root.querySelector("[data-record-start]");
    const stop = root.querySelector("[data-record-stop]");
    const cancel = root.querySelector("[data-record-cancel]");
    const transcribe = root.querySelector("[data-record-transcribe]");
    const status = root.querySelector("[data-record-status]");
    const answer = document.getElementById("answer");

    let recorder = null;
    let stream = null;
    let chunks = [];
    let recordedBlob = null;
    let timer = null;
    let discardOnStop = false;

    function setStatus(text) {
      status.textContent = text;
    }

    function resetRecording({ keepBlob = false } = {}) {
      if (timer) window.clearTimeout(timer);
      timer = null;
      releaseStream(stream);
      stream = null;
      recorder = null;
      chunks = [];
      if (!keepBlob) recordedBlob = null;
      stop.disabled = true;
      cancel.disabled = true;
      transcribe.disabled = !recordedBlob;
      start.disabled = !configured;
    }

    if (!configured) {
      setStatus("Speech transcription is not configured. Use the text answer box.");
      return;
    }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === "undefined") {
      start.disabled = true;
      setStatus("This browser does not support the required microphone recording APIs. Use the text answer box.");
      return;
    }

    start.addEventListener("click", async () => {
      try {
        recordedBlob = null;
        discardOnStop = false;
        transcribe.disabled = true;
        stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        const mimeType = chooseMimeType();
        recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
        chunks = [];
        recorder.addEventListener("dataavailable", (event) => {
          if (!discardOnStop && event.data && event.data.size > 0) chunks.push(event.data);
        });
        recorder.addEventListener("stop", () => {
          if (discardOnStop) {
            resetRecording();
            discardOnStop = false;
            setStatus("Recording cancelled. No audio was sent.");
            return;
          }
          const type = recorder.mimeType || mimeType || "audio/webm";
          recordedBlob = new Blob(chunks, { type });
          resetRecording({ keepBlob: true });
          if (recordedBlob.size > 0) {
            setStatus("Recording stopped. Select Transcribe recording if you choose to send the audio for transcription.");
          } else {
            recordedBlob = null;
            transcribe.disabled = true;
            setStatus("No audio was captured. You can record again or type your answer.");
          }
        }, { once: true });
        recorder.start(1000);
        start.disabled = true;
        stop.disabled = false;
        cancel.disabled = false;
        setStatus("Recording in progress. Microphone access is active.");
        timer = window.setTimeout(() => {
          if (recorder && recorder.state === "recording") {
            recorder.stop();
            setStatus("Recording reached the 120-second limit and was stopped. It has not been sent anywhere.");
          }
        }, MAX_RECORDING_MS);
      } catch (error) {
        resetRecording();
        setStatus("Microphone access failed or was denied. You can continue by typing your answer.");
      }
    });

    stop.addEventListener("click", () => {
      if (recorder && recorder.state === "recording") recorder.stop();
    });

    cancel.addEventListener("click", () => {
      if (recorder && recorder.state === "recording") {
        discardOnStop = true;
        try { recorder.stop(); } catch (_) { resetRecording(); }
      } else {
        resetRecording();
        setStatus("Recording cancelled. No audio was sent.");
      }
    });

    transcribe.addEventListener("click", async () => {
      if (!recordedBlob || recordedBlob.size === 0 || !endpoint) return;
      transcribe.disabled = true;
      start.disabled = true;
      setStatus("Sending the recorded audio for transcription…");
      const form = new FormData();
      const mime = recordedBlob.type || "audio/webm";
      const ext = mime.startsWith("audio/ogg") ? "ogg" : mime.startsWith("audio/mp4") ? "mp4" : "webm";
      form.append("audio", recordedBlob, `answer.${ext}`);
      try {
        const response = await fetch(endpoint, {
          method: "POST",
          body: form,
          credentials: "same-origin",
          headers: { "X-Requested-With": "Project001Speech" },
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok || typeof payload.transcript !== "string") {
          throw new Error("transcription failed");
        }
        answer.value = payload.transcript.slice(0, 8000);
        answer.focus();
        recordedBlob = null;
        transcribe.disabled = true;
        start.disabled = false;
        setStatus("Transcription complete. Review and edit the answer text before selecting Submit for feedback.");
      } catch (error) {
        transcribe.disabled = false;
        start.disabled = false;
        setStatus("Transcription failed. The answer was not submitted. You can retry, record again, or type your answer.");
      }
    });
  }

  document.querySelectorAll("[data-speech-controls]").forEach(initControls);
})();
