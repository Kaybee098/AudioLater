# System Architecture

## Scope and implementation status

This repository is an offline Spanish-to-English edge translation prototype. The intended product path is **speech-to-text (STT) -> machine translation (MT) -> text-to-speech (TTS)**. At the current revision, the STT wrapper and MT conversion utility are implemented; `audio_translator/main_translator.py` is empty and the checked-in `Piper/` and `Voices/` directories are empty. The diagrams describe the target runtime contract, not a claim that the end-to-end path already executes.

## High-level architecture

```text
Audio source
   |
   v
Whisper.cpp CLI + ggml-tiny-q8_0.bin
   |  Spanish transcript
   v
ArgosMT / Helsinki-NLP opus-mt-es-en
converted with CTranslate2 INT8
   |  English text
   v
Piper runtime + en_US-ryan-low voice (ONNX)
   |
   v
English audio output
```

All inference is local. No cloud API, network request, or remote service is required after the executable and model assets have been provisioned. The conversion script does require network access the first time it downloads the Hugging Face model.

## Component breakdown

### STT engine

`audio_translator/Transcriber/test_whisper.py` resolves `whisper-cli.exe` and `ggml-tiny-q8_0.bin` relative to its own directory. It invokes Whisper with Spanish language selection (`-l es`) and text output, then reads the generated transcript from either `<input stem>.txt` or `<input filename>.txt`. The current wrapper does not yet expose timestamp/context/thread flags.

The bundled Windows directory contains the Whisper CLI and CPU backend DLLs, but the quantized model is an ignored deployment asset and must be placed beside the executable.

### Translation engine

`audio_translator/convert_mach_trans.py` creates `opus-mt-es-en-int8` from `Helsinki-NLP/opus-mt-es-en` using CTranslate2's Transformers converter and `quantization="int8"`. The local model directory contains `model.bin`, `config.json`, and `shared_vocabulary.json`. Runtime integration is not yet present in `main_translator.py`; a production wrapper should load the CTranslate2 model once and pass tokenized Spanish text to its translator API.

INT8 weights reduce memory bandwidth and storage pressure and can improve CPU throughput on supported hardware. Accuracy and latency must be measured for the target language domain before release.

### TTS engine

The intended TTS stage is Piper, using the local Piper runtime under `audio_translator/Piper/` and an English ONNX voice such as `Voices/en_US-ryan-low.onnx` with its JSON metadata. These assets are currently absent from the checkout, so TTS provisioning and subprocess/API invocation remain deployment work.

### Orchestration

`main_translator.py` is the intended application boundary for input acquisition, stage sequencing, error handling, and output naming. It is currently empty. The production implementation should keep models warm, use bounded queues for streaming, and expose a batch mode for WAV files.

## Hardware and edge considerations

- **Memory:** budget for the Whisper model, CTranslate2 model, Piper voice, Python/runtime overhead, and audio buffers simultaneously. Measure resident set size after all models are loaded, not only file sizes.
- **Quantization:** Whisper `Q8_0` and MT `INT8` reduce footprint and memory traffic at a modest accuracy cost. Validate word error rate and translation quality against representative speech.
- **Threads:** the wrapper defaults to `max(1, CPU count - 1)`. On a shared wearable or SBC, a lower fixed value can reduce thermal throttling and preserve responsiveness. Benchmark 1, 2, 4, and available-core configurations.
- **Buffers:** use bounded in-memory audio/text queues for streaming. Backpressure is preferable to unbounded RAM growth when synthesis is slower than capture.
- **Thermals and power:** sustained CPU inference on a Pi Zero 2W or similar board may throttle. Prefer short utterance windows, voice activity detection, warm processes, and scheduled benchmarks under the expected enclosure.
- **Offline security:** package exact binaries, model checksums, and licenses. Disable network-dependent fallback behavior in the deployed image.
- **Targets:** x86_64 Windows is the current bundled runtime target. Raspberry Pi/ARM Linux is a deployment target requiring native ARM builds and compatible model/runtime assets.
