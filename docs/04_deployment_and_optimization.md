# Deployment and Optimization Guide

## Environment setup

### Windows development

```powershell
cd C:\path\to\edge_and_optimization_on_wearable_AI_audio_translator
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install sacremoses
```

### Linux / Raspberry Pi

```bash
cd /path/to/edge_and_optimization_on_wearable_AI_audio_translator
python3 -m venv venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install sacremoses
```

The project uses dependencies that include `ctranslate2`, `transformers`, `sentencepiece`, `onnxruntime`, `argostranslate`, and `sacremoses`. The `sacremoses` package is important for punctuation and token normalization in the Spanish-to-English OPUS pipeline.

### Executable and model prerequisites

For the current end-to-end deployment, the following assets must be present:

- `audio_translator/Transcriber/Whisper/whisper-cli.exe`
- `audio_translator/Transcriber/ggml-base-q5_1.bin`
- `audio_translator/Translator/opus-mt-es-en-int8/`
- `audio_translator/Piper/`
- `audio_translator/Voices/`

The Whisper stage should be kept isolated in a short-lived process so the memory footprint is released before the MT and TTS stages begin.

## Current smoke test

```powershell
python audio_translator/main_translator.py --show-transcript
```

This runs the full local pipeline and prints the transcribed Spanish text and the translated English output. The lower-level transcriber can also be called directly for STT-only validation:

```powershell
python audio_translator/Transcriber/transcribe_engine.py
```

## Optimization techniques

### Avoid unnecessary disk round trips

The final runtime passes transcript text in memory from the Whisper stage to the MT stage without writing a sidecar text file. This keeps memory overhead low and reduces latency for short utterance translation.

### Use deterministic Whisper decoding

The finalized runtime parameters should be tuned to the opposite of high-randomness decoding:

- `-l es`
- `-tp 0.0`
- `-bs 5`
- `-mc 0`
- `-nt`

This keeps the inference deterministic and prevents cross-context contamination from earlier transcripts or prompts.

### Keep the C++ subprocess isolated

Whisper should be started as a short-lived C++ process, allowed to finish its transcription, and then released before the MT and TTS workloads begin. This preserves the hardware headroom required for a Pi Zero 2W-style deployment target.

### Tune CPU threading

Use a fixed CPU thread count appropriate to the target board and avoid overcommitting the system while the TTS stage is active. The memory-first edge policy is more important than maximizing STT concurrency.

### Segment and measure throughput under the 512MB envelope

Use the following edge benchmark profile as a design reference:

- Headless OS: ~50MB
- STT peak (base-q5_1): ~160MB
- MT peak (CTranslate2 INT8): ~55MB
- TTS peak (Piper ONNX): ~75MB
- Total sequential peak: ~280-320MB

This keeps the workload well within a 512MB target envelope.

## Embedded deployment checklist

- [ ] Build `whisper.cpp` for the target ARM ABI and place the runtime under `audio_translator/Transcriber/Whisper/`.
- [ ] Download or build the `ggml-base-q5_1.bin` model and keep it local to the project.
- [ ] Convert `Helsinki-NLP/opus-mt-es-en` to the local `audio_translator/Translator/opus-mt-es-en-int8` folder.
- [ ] Install `sacremoses` for punctuation and token normalization.
- [ ] Provision Piper and ONNX voice files under `audio_translator/Piper/` and `audio_translator/Voices/`.
- [ ] Validate `audio_translator/main_translator.py` on a Raspberry Pi Zero 2W or CM4-class board.
- [ ] Measure wall clock latency, peak RSS, and temperature under load.
- [ ] Keep all model assets version-pinned and checksum-verified for field deployment.
- [ ] Validate cold-start and warm-start behavior separately.
- [ ] Restrict the production image to offline-only execution paths.
