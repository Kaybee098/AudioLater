# Documentation Runtime Tracker

## Workspace Inventory

Inventory captured from the finalized workspace state. The repository follows a root-level virtual environment and a local edge pipeline with the transcriber, translator, and TTS stages bound to the project filesystem.

```text
edge_and_optimization_on_wearable_AI_audio_translator/
├── .gitignore
├── README.md
├── requirements.txt
├── venv/
├── audio_translator/
│   ├── LICENSE
│   ├── README.md
│   ├── main_translator.py                 # full pipeline orchestrator
│   ├── convert_mach_trans.py             # Hugging Face -> INT8 CTranslate2 converter
│   ├── Piper/                            # Piper runtime assets (provisioned on device)
│   ├── Translator/
│   │   ├── translate_engine.py            # CTranslate2 OPUS MT engine
│   │   └── opus-mt-es-en-int8/
│   │       ├── config.json
│   │       ├── model.bin
│   │       ├── source.spm
│   │       ├── target.spm
│   │       ├── tokenizer_config.json
│   │       ├── vocab.json
│   │       └── shared_vocabulary.json
│   ├── Transcriber/
│   │   ├── transcribe_engine.py          # local Whisper CLI wrapper
│   │   ├── ggml-base-q5_1.bin            # Whisper base 5-bit quantized model
│   │   ├── test_audio2.wav               # local Spanish sample
│   │   └── Whisper/
│   │       └── whisper-cli.exe           # Whisper CLI binary
│   └── Voices/
│       ├── TTS_Engine.py                 # Piper TTS wrapper
│       └── ...                           # ONNX voice payloads and metadata
├── docs/
│   ├── runtime_tracker.md
│   ├── 01_architecture.md
│   ├── 02_diagrams.md
│   ├── 03_pipeline_reference.md
│   └── 04_deployment_and_optimization.md
└── venv/
```

### Tracked versus provisioned assets

- Tracked source/configuration: project scripts, README, docs, and package metadata.
- Provisioned deployment assets: Whisper quantized model, CLI runtime, converted MT model folder, Piper runtime, TTS ONNX voice files, and the root Python environment.
- Local runtime footprint remains intentionally compact for edge deployments; model and binary assets are kept outside Git tracking and loaded only when required.

## Documentation Phases

- [x] Phase 1 - Workspace analysis and execution tracking
- [x] Phase 2 - System architecture and data flow documentation
- [x] Phase 3 - Mermaid diagrams updated to current module names and model stack
- [x] Phase 4 - Component and API reference updated to the finalized implementation
- [x] Phase 5 - Setup, optimization, and deployment guide updated for root `venv` and edge deployment profile
- [x] Phase 6 - Root README aligned to the working project structure

## Implementation Status

- [x] Whisper base model and transcriber runtime path finalized (`ggml-base-q5_1.bin` + `transcribe_engine.py`)
- [x] CTranslate2 OPUS MT conversion pipeline finalized and documented
- [x] End-to-end orchestrator implemented in `audio_translator/main_translator.py`
- [x] Piper TTS wrapper and voice modules are included in the project structure
- [x] Memory and RAM envelope documentation updated for a 512MB edge target
