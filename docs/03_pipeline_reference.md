# Component and Pipeline Reference

## `audio_translator/Transcriber/transcribe_engine.py`

### Constants

- `SCRIPT_DIR: Path`: absolute directory containing the transcriber module.
- `EXE_PATH: Path`: `SCRIPT_DIR / "Whisper" / "whisper-cli.exe"`.
- `MODEL_PATH: Path`: `SCRIPT_DIR / "ggml-base-q5_1.bin"`.

### `transcribe_audio`

```python
transcribe_audio(file_path: str) -> str
```

`file_path` may be supplied as a relative path inside `Transcriber/` or as an absolute filesystem path. The wrapper resolves relative input files against the transcriber directory and validates the existence of the executable, model weight, and audio file before launching the subprocess.

The final runtime command is built around the Whisper decoder settings for deterministic and low-hallucination transcription:

```text
whisper-cli.exe -m <MODEL_PATH> -l es -tp 0.0 -bs 5 -mc 0 -nt -f <audio>
```

The subprocess is isolated and returns transcript text in memory rather than writing a `.txt` artifact for normal execution. The text is then passed directly into the translation stage.

### Command-line usage

```powershell
python audio_translator/Transcriber/transcribe_engine.py
```

The module is the STT wrapper and is used by the orchestrator rather than being the final user-facing app entry point.

## `audio_translator/Translator/translate_engine.py`

The translation engine loads the converted CTranslate2 model at `audio_translator/Translator/opus-mt-es-en-int8` and translates Spanish text to English in memory. It relies on the tokenizer assets generated during conversion and uses `ctranslate2.Translator` on the CPU to keep the runtime compact and latency-friendly.

### Runtime contract

```python
translate_text(text: str) -> str
```

The function trims the input, loads the model/tokenizer once, and returns the translated English sentence directly to the caller without creating a temporary file.

## `audio_translator/convert_mach_trans.py`

This script converts the Hugging Face model `Helsinki-NLP/opus-mt-es-en` into a compact INT8 CTranslate2 graph and writes it to the project’s `Translator` directory.

```python
converter.convert(
    output_dir=str(OUTPUT_DIR),
    quantization="int8",
    force=True,
)
```

It also saves the tokenizer to the same folder so local inference remains self-contained and offline.

### Model conversion command

```powershell
python audio_translator/convert_mach_trans.py
```

The generated model directory is:

```text
audio_translator/Translator/opus-mt-es-en-int8/
```

## `audio_translator/main_translator.py`

This is the primary runtime entry point for the complete offline translation pipeline. It orchestrates the sequence:

1. Load and call `transcribe_audio()`.
2. Pass the Spanish transcript directly to `translate_text()`.
3. Pass the English result into the Piper TTS wrapper.
4. Emit the final synth output and latency metrics.

### CLI usage

```powershell
python audio_translator/main_translator.py --show-transcript
```

The file is the current canonical runner for the full pipeline and is the entry point referenced across the deployment and architecture guides.

## Model and runtime specifications

| Stage | Asset / source | Precision | Format / backend | Notes |
|---|---|---:|---|---|
| STT | `ggml-base-q5_1.bin` | Q5_1 | Whisper.cpp / GGML | ~85MB, low-variance decode |
| MT | `Helsinki-NLP/opus-mt-es-en` | INT8 | CTranslate2 / CPU | ~75MB disk, ~55MB RAM |
| TTS | Piper ONNX voice | ONNX model-defined | Piper / ONNX Runtime | ~60MB disk, ~75MB RAM |
| Alternative MT | `.argosmodel` | package-defined | Argos Translate | Modular alternative, not primary runtime |

The CTranslate2 directory includes `model.bin`, tokenizer assets, and shared token metadata; it is designed to be loaded directly in offline mode without a cloud dependency. `sacremoses` supports punctuation and token normalization for more stable Spanish-to-English translation output.
