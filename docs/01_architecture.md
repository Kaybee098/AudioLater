# System Architecture

## Scope and implementation status

This repository implements an offline Spanish-to-English edge translation pipeline across three stages: speech-to-text (STT), machine translation (MT), and text-to-speech (TTS). The final architecture is built around a quantified Whisper runtime, a compact CTranslate2 OPUS MT model, and a local Piper voice engine. The project is designed to keep model lifecycles local, process text in memory, and release each stage before moving to the next stage.

## High-level architecture

```text
Audio source
   |
   v
Whisper.cpp CLI + ggml-base-q5_1.bin
   |  Spanish transcript in memory
   v
Helsinki-NLP/opus-mt-es-en -> INT8 CTranslate2
   |  English text in memory
   v
Piper runtime + ONNX voice model
   |
   v
English audio output
```

All inference is local, and the design intentionally keeps the STT subprocess isolated so memory can be released before the MT and TTS workloads begin. This reduces RAM pressure and makes the pipeline more suitable for an edge target such as Raspberry Pi Zero 2W or a small CM4-class SBC.

## Component breakdown

### STT engine

The transcriber is implemented in `audio_translator/Transcriber/transcribe_engine.py` and loads `audio_translator/Transcriber/Whisper/whisper-cli.exe` plus the quantized Whisper base model `ggml-base-q5_1.bin` (~85MB). The stage is intentionally short-lived and isolated inside a subprocess: it loads the backend, transcribes the input WAV, and releases memory before the MT stage begins.

The current CLI parameter set is tuned around low variance and low hallucination risk:

- `-m <MODEL_PATH>`
- `-l es`
- `-tp 0.0`
- `-bs 5`
- `-mc 0`
- `-nt`

This combination keeps the decode deterministic and suppresses context bleeding across utterances.

### Translation engine

The machine translation layer is a local `Helsinki-NLP/opus-mt-es-en` conversion produced by `audio_translator/convert_mach_trans.py` and stored in `audio_translator/Translator/opus-mt-es-en-int8`. The model is converted to `INT8` with CTranslate2, and the local generated directory includes the converted model payload plus tokenizer assets (`source.spm`, `target.spm`, `vocab.json`, and metadata).

The runtime uses the local translator engine in `audio_translator/Translator/translate_engine.py`, which loads the model once and then translates Spanish text in memory. `sacremoses` is required for punctuation and subword normalization so Spanish token boundaries and capitalization remain robust in the target language output.

### TTS engine

The TTS stage is composed of the Piper runtime under `audio_translator/Piper/` and voice payloads under `audio_translator/Voices/`. The expected voice model footprint is roughly 60MB on disk and ~75MB in RAM while the engine is active, depending on the exact runtime and model build.

### Orchestration

`audio_translator/main_translator.py` orchestrates the end-to-end flow:

1. Transcribe the incoming WAV with Whisper.
2. Pass the resulting Spanish transcript directly into the translator engine.
3. Feed the English sentence to Piper and write the output WAV file.

This stage sequencing avoids writing intermediate text files for normal operation and keeps the translation pipeline in memory for latency-sensitive edge targets.

## Hardware and edge considerations

- **Memory profile:** the design is built around a sequential 512MB envelope. A typical target profile is approximately 50MB for the headless OS, 160MB for Whisper base-q5_1, 55MB for the CTranslate2 INT8 model, and 75MB for Piper synthesis. The expected system peak is about 280-320MB, which is comfortably inside a 512MB Raspberry Pi Zero 2W target.
- **Quantization:** Whisper `base-q5_1` and CTranslate2 `INT8` are selected to minimize disk and RAM pressure while preserving acceptable accuracy for short Spanish utterances.
- **Threading and CPU affinity:** the runtime should use a fixed low-thread setting for the target board (for example 1-4 threads depending on the model), and it should avoid overloading the system while the TTS stage is active.
- **Sequential memory release:** Whisper runs as an isolated C++ subprocess; once it exits, its memory is released before the MT/TTS stages begin. This reduces the chances of a simultaneous peak exceeding the board budget.
- **Offline runtime:** all required components are packaged locally and intentionally avoid network dependencies after the first model conversion.
- **Deployment targets:** the architecture is targeted to ARM Linux and compact SBCs, with Windows used as a development and validation host for the current build.
