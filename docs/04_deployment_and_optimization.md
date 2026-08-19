# Deployment and Optimization Guide

## Environment setup

### Windows development

```powershell
cd C:\path\to\edge_and_optimization_on_wearable_AI_audio_translator
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux / Raspberry Pi

```bash
cd /path/to/edge_and_optimization_on_wearable_AI_audio_translator
python3 -m venv venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The requirements pin Argos Translate, CTranslate2, SentencePiece, Transformers, ONNX Runtime, and Flask. Confirm that the Python version and wheels are available for the target architecture; the pinned `onnxruntime` and other packages may require an ARM-compatible build or a target-specific version.

### Executable and model prerequisites

For the current Windows STT wrapper, provision the Whisper release files in `audio_translator/Transcriber/`, including `whisper-cli.exe`, its matching `whisper.dll`/GGML CPU DLLs, and `ggml-tiny-q8_0.bin`. The wrapper will fail fast if any of these or the input WAV is missing.

For TTS, provision Piper under `audio_translator/Piper/` and the voice pair under `audio_translator/Voices/`. The current checkout has neither. The MT model can be generated with `python audio_translator/convert_mach_trans.py`; network access is needed for the first conversion, and the resulting directory must remain available at the working directory used by the converter/runtime.

## Current smoke test

With a Whisper model and audio fixture installed:

```powershell
python audio_translator/Transcriber/test_whisper.py
```

The command should print the transcript captured from Whisper stdout. This validates STT only. The current wrapper does not accept an audio argument or thread option. No current command validates the complete STT -> MT -> TTS path because `main_translator.py` is empty and the Piper assets are absent.

## Optimization techniques

### Avoid unnecessary disk round trips

The wrapper captures Whisper stdout and returns the transcript in memory, avoiding an intermediate transcript file. Once orchestration is implemented, pass that string directly to the MT tokenizer. Keep disk writes only for final audio, diagnostics, or explicitly requested transcripts.

### Reduce latency at the CLI boundary

The wrapper uses `--no-timestamps` and `--no-context` for independent short utterances. Confirm that the bundled Whisper build supports these flags; for streaming, use an API or pipe contract that avoids polling for generated files.

### Tune CPU threading

Add a configurable thread argument to the wrapper and benchmark it on the actual board. Start with 1, 2, and the number of physical cores; leave headroom for capture, MT, TTS, and the operating system. Watch wall time, peak RSS, temperature, and power together.

### Keep models warm and queues bounded

Load each model once per process. Use a bounded audio queue, explicit utterance limits, and backpressure. Parallelize independent stage work only when memory and thermal budgets allow it; serialized stages can be preferable on small SBCs.

### Measure quality as well as speed

Record real-time factor, first-result latency, sustained throughput, peak RSS, CPU utilization, temperature, and battery draw. Pair those metrics with Spanish STT word error rate and human-reviewed English translation quality. Quantization should be accepted only after a representative accuracy check.

## Embedded deployment checklist

- [ ] Build `whisper.cpp` natively or cross-compile for the target ARM ABI; enable the correct CPU/GGML backend for the board.
- [ ] Build Piper and its dependencies for ARM Linux, or obtain a compatible release binary. Confirm the ONNX Runtime provider and voice model compatibility.
- [ ] Copy `ggml-tiny-q8_0.bin`, the Piper voice `.onnx` and `.json`, and the CTranslate2 model directory into versioned asset locations.
- [ ] Replace Windows `.exe`/`.dll` assumptions with ARM Linux executable paths and shared libraries.
- [ ] Validate SentencePiece/CTranslate2 wheels or build/install target-specific packages for the chosen Python version.
- [ ] Implement and test `main_translator.py` with explicit batch and streaming modes before field deployment.
- [ ] Add SHA-256 checksums, model licenses, startup dependency checks, and structured error logs.
- [ ] Benchmark on Raspberry Pi Zero 2W and CM4 separately; do not transfer workstation thread settings blindly.
- [ ] Add watchdog/restart behavior, bounded storage for outputs, and thermal/power monitoring.
- [ ] Run a no-network acceptance test from a clean target image.
