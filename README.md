# Edge & Optimization on Wearable AI Audio Translator

An offline, edge-oriented audio translation prototype designed to convert spoken Spanish into English using local speech recognition, machine translation, and text-to-speech components. The project is structured around lightweight, deployable AI assets that can run without relying on cloud services.

---

## 1. Project Overview

This repository explores a wearable-style, low-latency translation pipeline for edge hardware. It combines:

- speech-to-text for local audio transcription,
- neural machine translation for Spanish-to-English conversion, and
- text-to-speech synthesis for spoken English output.

The goal is to provide a practical foundation for running translation workloads locally on resource-constrained devices such as single-board computers or embedded systems.

---

## 2. Key Features

- Offline-first translation workflow with local model assets
- Support for converting Hugging Face translation models to compact INT8 format
- Local speech recognition and synthesis components using bundled model files
- Lightweight directory structure suitable for experimentation and edge deployment
- Modular scripts for translation model conversion and application entry points

---

## 3. Tech Stack & Hardware

### Programming Languages
- Python 3

### Core Libraries and Frameworks
- CTranslate2 for efficient model inference and conversion
- Transformers for loading and preparing compatible model pipelines
- ONNX-based voice assets for local text-to-speech generation
- Local model artifacts such as Argos Translate and CTranslate2-compatible translation weights

### Target Hardware / Runtime Environment
- Edge devices such as Raspberry Pi, Jetson boards, or other ARM/x86_64 systems
- Any workstation with sufficient CPU and memory to run local inference
- Best results are typically achieved on systems with:
  - a modern CPU,
  - available RAM for model loading,
  - and enough storage for downloaded or bundled model files

> [!NOTE]
> This project is intended for local experimentation and edge deployment, but runtime performance depends heavily on the host hardware and the size of the loaded models.

---

## 4. Directory Architecture

```text
edge_and_optimization_on_wearable_AI_audio_translator/
├── README.md                                 # Project documentation
├── audio_translator/                        # Main application workspace
│   ├── convert_mach_trans.py                # Converts a Hugging Face translation model to INT8
│   ├── main_translator.py                   # Entry point for the translation pipeline
│   ├── ggml-tiny-q8_0.bin                   # Local speech-to-text model asset
│   ├── translate-es_en-1_9.argosmodel       # Local Argos translation model asset
│   ├── Piper/                                # Piper text-to-speech runtime assets
│   ├── Voices/                               # Local voice model files for TTS
│   │   ├── en_US-ryan-low.onnx               # Voice model file
│   │   └── en_US-ryan-low.onnx.json          # Voice model metadata
│   └── README.md                             # Project-specific notes inside the app folder
└── opus-mt-es-en-int8/                      # Converted machine translation model directory
    ├── config.json                           # Model configuration
    └── shared_vocabulary.json                # Shared token vocabulary
```

---

## 5. Prerequisites & Installation

### Prerequisites

Before installing dependencies, make sure you have:

- Python 3.9+ installed
- A terminal or PowerShell session available
- Internet access if you want to download or convert additional model files

### Windows PowerShell Setup

```powershell
cd C:\path\to\edge_and_optimization_on_wearable_AI_audio_translator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install ctranslate2 transformers sentencepiece
```

### Linux / macOS Setup

```bash
cd /path/to/edge_and_optimization_on_wearable_AI_audio_translator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install ctranslate2 transformers sentencepiece
```

### Model Assets

The repository already includes several local assets, but if you want to regenerate the translation model, run the conversion script from the project directory.

---

## 6. Usage / Execution

### Convert a Translation Model to INT8

The repository includes a conversion utility that downloads and converts a Hugging Face Spanish-to-English model into a compact INT8 format.

```bash
python audio_translator/convert_mach_trans.py
```

This script uses CTranslate2 to create a local model folder named `opus-mt-es-en-int8` in the workspace.

### Run the Translator Entry Point

```bash
python audio_translator/main_translator.py
```

> [!WARNING]
> The current entry script is a scaffold and may require further implementation before it fully executes the full speech-to-text, translation, and speech synthesis workflow end to end.

### Expected Workflow

1. Load local speech-to-text assets.
2. Transcribe incoming audio.
3. Translate the recognized text.
4. Synthesize the translated text into spoken English.

---

## 7. Notes for Reproducibility

- Keep the model directories near the repository root or adjust paths in your scripts if you move them.
- Long model downloads and conversions may take significant time and disk space.
- For edge hardware, smaller quantized models often provide a better balance between memory usage and throughput.

---

## 8. License

This project is distributed under the license included in the repository. Please review the license file before redistribution or commercial use.
