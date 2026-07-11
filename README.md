# EduAR — AI-Driven Augmented Reality System For Spatially Anchored Diagram Learning

EduAR is a single-page, mobile-first web app that lets students explore 3D educational models — organs, cells, plants, minerals, planets, and more — in augmented reality. Point your camera at a real surface, place a labeled 3D model on it, and walk around it as if it were sitting on your desk. Built entirely as one `index.html` file with no backend or build step required.

<img width="320" height="420" alt="Screenshot 2026-07-11 172958" src="https://github.com/user-attachments/assets/15b22b8d-185c-4a51-b743-2f24e18bc305" />
<img width="320" height="420" alt="Screenshot 2026-07-11 171043" src="https://github.com/user-attachments/assets/645896aa-2e39-4cc3-8ed8-d81fa20e661d" />
<img width="320" height="420" alt="Screenshot 2026-07-11 173326" src="https://github.com/user-attachments/assets/c6327cac-07c5-4cb4-ad12-98b219e81c1c" />

## Features

- **AR model placement** — Uses WebXR (with a non-WebXR camera fallback) and Three.js to place and view 3D models in your real environment.
- **Labeled anatomy overlays** — Each model ships with hotspot labels (e.g. "Pulmonary Vein," "Left Atrium") anchored to precise 3D coordinates, complete with connector lines, info chips, and a bottom-sheet detail panel.
- **AI-powered scan mode** — Point your camera at a real-world object and have it identified and matched against the model library using a vision-language model (Groq / Qwen2.5-VL).
- **Quiz mode** — Test your knowledge of labeled parts with an interactive quiz and scorekeeper, including a results/review screen.
- **Guided tours** — Step-by-step walkthroughs that fly the camera to each label in sequence with narration.
- **Text-to-speech narration** — High-quality voice narration via the ElevenLabs API, with automatic fallback to the browser's native Web Speech API.
- **Multilingual support** — Labels and narration are available in English, Hindi, Tamil, Kannada, Malayalam, Telugu, and French, powered by NLLB-200 translation and ElevenLabs' multilingual voice model.
- **Curated content library** — Organized by category (Biology, Chemistry, Earth Science) → subject → model, spanning human anatomy, cell biology, botany, atomic structure, geology, and space.
- **Favorites & recents** — Quickly jump back into recently viewed or bookmarked models.
- **Dark, distinctive UI** — Custom design system (Syne + Space Mono typography, dark theme) tuned for phones, tablets, and laptops.

## Content Library

Model metadata, descriptions, and label coordinates live in [`content.json`](./content.json):

| Category | Subjects | Models |
|---|---|---|
| Biology | Human Systems, Cell Biology, Botany | 21 |
| Chemistry | Atomic Structure | 1 |
| Earth Science | Geology, Space | 4 |

Each model entry includes a name, short/long description, thumbnail, 3D model reference (`.glb`), 2D diagram fallback, and a set of labels with 3D dot positions, focus/zoom regions, and camera orientations for guided tours.

## Tech Stack

- **Three.js** (r128) — 3D rendering and scene management
- **WebXR Device API** — AR sessions on supported devices, with a camera-based fallback for others
- **Groq API (Qwen2.5-VL)** — vision-language model used for camera-based model scanning/matching
- **ElevenLabs API** — text-to-speech narration (`eleven_multilingual_v2` model)
- **Web Speech API** — built-in browser fallback for narration when ElevenLabs is unavailable
- **NLLB-200** — machine translation for multilingual labels and quiz content
- Vanilla HTML/CSS/JS — no framework, no bundler, no build step

### Required assets

`content.json` references 3D models, thumbnails, and diagrams under an `assets/` folder (e.g. `assets/models/heart.glb`, `assets/thumbnails/heart.jpg`, `assets/diagrams/heart.png`). Make sure this folder is present alongside `index.html` and `content.json` with matching filenames.

### API keys

Scan mode (Groq/Qwen2.5-VL) and premium narration (ElevenLabs) call third-party APIs and require valid API keys to be configured. Without keys, the app still works using the built-in Web Speech API for narration; scan mode will be unavailable.

## Motivation

EduAR was built to make abstract educational diagrams tangible — instead of memorizing a flat textbook diagram of a heart or a cell, students can place a 3D model in their own space, rotate it, tap on labeled parts, and quiz themselves, all from a phone browser.

## 📄 License

Add your preferred license here (e.g. MIT).
