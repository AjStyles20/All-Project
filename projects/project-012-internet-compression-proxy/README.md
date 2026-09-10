# P012 — Internet Compression and Optimization Proxy System

## Class
GENERAL / PRODUCT SYSTEM

## Working problem
Design an application-level proxy intended to reduce transferred data and improve perceived responsiveness in bandwidth-constrained environments.

## Research before implementation
Research must establish what optimization remains technically possible under HTTPS/TLS, HTTP/2, HTTP/3/QUIC, content encodings, CDNs, browser security, caching, image/media transcoding, proxy trust models, VPN/proxy interactions, privacy, and mobile-network constraints.

## Current status
NOT STARTED — high-priority systems research candidate after P011.

## Guardrail
Performance claims must be measured against controlled baselines. The project must not claim to accelerate encrypted traffic unless the mechanism and trust boundary make that technically possible and ethically acceptable.
