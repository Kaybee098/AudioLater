# Component and Pipeline Reference

## `Transcriber/test_whisper.py`

### Constants

- `SCRIPT_DIR: Path`: absolute directory containing the wrapper.
- `EXE_PATH: Path`: `SCRIPT_DIR / "whisper-cli.exe"`.
- `MODEL_PATH: Path`: `SCRIPT_DIR / "ggml-tiny-q8_0.bin"`.

### `transcribe_audio`

```python
transcribe_audio(file_path: str) -> str
```

`file_path` is currently treated as a path relative to `Transcriber/`; the wrapper prepends `SCRIPT_DIR` unconditionally. Absolute-path support is therefore not implemented in the current file.

The function validates the executable, model, and input file before launching a child process. It runs:

```text
whisper-cli.exe -m ggml-tiny-q8_0.bin -l es -f <audio>
  --no-timestamps --no-context
```

`subprocess.run` captures stdout and stderr in memory. A nonzero CLI status becomes `RuntimeError` with the native diagnostic when one is available; successful stdout is returned directly as the Spanish transcript for the MT stage. No intermediate transcript file is created.

### Command-line entry point

```powershell
python audio_translator/Transcriber/test_whisper.py
```

The script has no argparse-based CLI. It always transcribes `test_audio.wav`, and that file must exist at `audio_translator/Transcriber/test_audio.wav`.

## `audio_translator/convert_mach_trans.py`

This script has no functions or CLI arguments. Running it constructs a `ctranslate2.converters.TransformersConverter` for `Helsinki-NLP/opus-mt-es-en` and calls:

```python
converter.convert(
    output_dir="opus-mt-es-en-int8",
    quantization="int8",
    force=True,
)
```

It downloads/loads the source model through Transformers, writes a CTranslate2 model to the current working directory, and overwrites an existing output directory. Run it from the repository root so the documented output path is stable:

```powershell
python audio_translator/convert_mach_trans.py
```

## `audio_translator/main_translator.py`

The file is currently empty. There is no implemented CLI, streaming loop, batch mode, argument parser, model loading, or output contract to call today. The intended production API should define explicit input/output paths, language direction, thread count, and mode, then:

1. Load Whisper, CTranslate2, and Piper assets once.
2. Process a bounded utterance or WAV batch.
3. Pass transcript text to MT without temporary transcript files.
4. Pass translated text to Piper and write a WAV result.
5. Return nonzero exit status and actionable diagnostics on stage failure.

Do not advertise `python audio_translator/main_translator.py` as an operational end-to-end command until this implementation exists.

## Model and runtime specifications

| Stage | Asset / source | Precision | Format/backend | Current status |
|---|---|---:|---|---|
| STT | `ggml-tiny-q8_0.bin` | Q8_0 (8-bit weight quantization) | GGML/GGUF-family Whisper.cpp CLI | Required beside `whisper-cli.exe`; not returned by inventory |
| MT | `Helsinki-NLP/opus-mt-es-en` | INT8 after conversion | CTranslate2 `model.bin`, CPU runtime | Converted directory is present locally; wrapper absent |
| MT source alternative | `translate-es_en-1_9.argosmodel` | Package-defined | Argos Translate | Asset is present locally but not used by current scripts |
| TTS | `en_US-ryan-low.onnx` plus JSON | ONNX model-defined | Piper / ONNX Runtime | Not present in current `Voices/` directory |

The local CTranslate2 directory is identified by `config.json`, `shared_vocabulary.json`, and `model.bin`; it is not a Transformers checkpoint directory. The production loader must use the matching CTranslate2 API and tokenizer rather than assuming a PyTorch model.
