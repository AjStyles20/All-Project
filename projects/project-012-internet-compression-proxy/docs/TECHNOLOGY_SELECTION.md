# P004 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Service: reverse gateway in front of one origin | Pass 004 §3 trust model; no client install, no forward proxy. |
| Language | Python 3.11+ | Project OS default; adequate for a research gateway. A production gateway would more likely be nginx/Envoy plus a worker. |
| HTTP | FastAPI/Starlette + uvicorn; httpx upstream with redirects off | Same stack as the other projects. |
| Codecs | Pillow (libwebp), Python gzip | Conventional codecs only (Pass 004 §10); no GPU, no learned compression. |
| Fidelity | PSNR on full image; SSIM on a 128 px greyscale thumbnail | No numpy dependency; the SSIM is an approximation and is labelled as one. |
| Network | Modelled (bandwidth + RTT) | netem is not available on Windows; stated as the main limitation. |
| Storage / cache | None | Removes cache-poisoning and private-caching risks for the first version. |
