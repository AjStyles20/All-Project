# P009 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Windows desktop program with a local web dashboard | Screen capture and foreground-window tracking need OS access a browser cannot have (Technology standard §3). The dashboard is served only to 127.0.0.1. |
| Language | Python 3.11+ | Project OS default; Pass 003 feasibility note. |
| OS access | `ctypes` to user32, kernel32, crypt32 | No extra native dependencies. |
| Capture and encoding | Pillow `ImageGrab`, WebP | Already a common dependency; WebP keeps images small. |
| Encryption | Windows DPAPI | Key tied to the user's Windows account; no key file to lose or leak. |
| Storage | SQLite + one encrypted file per image | Simple, local, easy to delete completely. |
| Dashboard | FastAPI + plain HTML/CSS/JS | Same as P001 and P007. |
| Text recognition | None yet | Candidate: the offline Windows OCR engine. Not added in this version. |
| Network / AI services | None | Nothing leaves the computer. |
| macOS / Linux | Not supported | The program refuses to record there. |
