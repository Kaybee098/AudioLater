# Documentation Runtime Tracker

## Workspace Inventory

Inventory captured from the workspace on 2026-08-19. Binary model files and some runtime assets are present locally but are ignored by `.gitignore`; they must be provisioned separately for a clean deployment.

```text
edge_and_optimization_on_wearable_AI_audio_translator/
├── .gitignore
├── README.md
├── requirements.txt
├── audio_translator/
│   ├── LICENSE
│   ├── README.md
│   ├── convert_mach_trans.py
│   ├── main_translator.py                    # currently empty scaffold
│   ├── translate-es_en-1_9.argosmodel        # ignored Argos model asset
│   ├── Piper/                                # directory currently empty
│   ├── Voices/                               # directory currently empty
│   └── Transcriber/
│       ├── test_whisper.py
│       ├── test_audio.wav
│       ├── test_audio.wav.txt
│       ├── whisper-cli.exe
│       ├── whisper.dll
│       ├── whisper-bench.exe
│       ├── whisper-command.exe
│       ├── whisper-lsp.exe
│       ├── whisper-quantize.exe
│       ├── whisper-server.exe
│       ├── whisper-stream.exe
│       ├── whisper-talk-llama.exe
│       ├── whisper-vad-speech-segments.exe
│       ├── ggml.dll
│       ├── ggml-base.dll
│       ├── ggml-cpu-x64.dll
│       ├── ggml-cpu-alderlake.dll
│       ├── ggml-cpu-cannonlake.dll
│       ├── ggml-cpu-cascadelake.dll
│       ├── ggml-cpu-haswell.dll
│       ├── ggml-cpu-icelake.dll
│       ├── ggml-cpu-sandybridge.dll
│       ├── ggml-cpu-skylakex.dll
│       ├── ggml-cpu-sse42.dll
│       ├── SDL2.dll
│       ├── command.exe
│       ├── main.exe
│       ├── bench.exe
│       ├── stream.exe
│       ├── wchess.exe
│       ├── test-vad.exe
│       ├── test-vad-full.exe
│       ├── test-common-utf8.exe
│       ├── parakeet.dll
│       ├── parakeet-cli.exe
│       ├── parakeet-quantize.exe
│       ├── test-parakeet.exe
│       ├── test-parakeet-full-diffusion.exe
│       ├── test-parakeet-full-gb1.exe
│       ├── test-parakeet-full-jfk.exe
│       └── (ggml-tiny-q8_0.bin is expected here but was not returned by the workspace inventory)
├── opus-mt-es-en-int8/
│   ├── config.json
│   ├── model.bin
│   └── shared_vocabulary.json
└── (venv/ exists locally and is ignored)
```

### Tracked versus provisioned assets

- Tracked source/configuration: `README.md`, `requirements.txt`, Python scripts, licenses, and model configuration files.
- Locally provisioned/ignored assets: Whisper model weights, Argos model, Piper runtime, Piper voice files, converted CTranslate2 model directory, and Python virtual environment.
- The current checkout has no files inside `audio_translator/Piper/` or `audio_translator/Voices/`, so TTS cannot run until those assets are installed.

## Documentation Phases

- [x] Phase 1 - Workspace analysis and execution tracking
- [x] Phase 2 - System architecture and data flow documentation
- [x] Phase 3 - Renderable Mermaid diagrams
- [x] Phase 4 - Component and API reference
- [x] Phase 5 - Setup, optimization, and deployment guide
- [x] Phase 6 - Master README update

## Implementation Status

- [ ] Whisper CLI wrapper implemented and verified against the sample transcript path (current bundled CLI exits with code `3236495362`)
- [x] Hugging Face to CTranslate2 INT8 conversion utility present
- [ ] End-to-end orchestrator implementation in `main_translator.py`
- [ ] Piper runtime and voice provisioning for this checkout
- [ ] Automated integration test covering STT -> MT -> TTS
