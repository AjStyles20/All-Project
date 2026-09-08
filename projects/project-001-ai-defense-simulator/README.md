# Project 001 — AI Virtual Audience / Presentation & Defense Simulator

## Purpose
A professional, source-grounded practice system for presentations, defenses, vivas, interviews, and technical/research review. Users provide their own materials; the system is designed to generate questions and feedback that remain traceable to those materials rather than relying on opaque unsupported scoring.

## Current Status
Project active. Feature 001 — provenance-aware TXT/Markdown ingestion and workspace-scoped lexical retrieval — is implemented on PR #1 and has passed independent logic, API integration, and live API smoke testing in the verifier environment. User-device/runtime verification remains outstanding.

## Approved MVP Foundation
- FastAPI + Python backend
- SQLite persistence
- lightweight server-rendered frontend
- provenance-aware document ingestion
- inspectable retrieval, beginning with SQLite FTS5
- provider adapters for later LLM, embedding, STT, and TTS services

## Important Boundaries
The current implementation does **not** yet provide PDF/DOCX/PPTX extraction, semantic retrieval, LLM question generation, answer evaluation, speech input/output, presentation-quality scoring, avatars, VR, or completed UI screens.

Research remains active across approximately 1990-present to establish historical prior art and avoid exaggerated novelty claims.
