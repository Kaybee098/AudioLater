# Visual System Diagrams

The diagrams use Mermaid syntax and reflect the current project modules and the finalized edge pipeline.

## End-to-end pipeline

```mermaid
flowchart LR
    A[WAV file or microphone] --> B[Audio capture and framing]
    B --> C[transcribe_engine.py\nWhisper base-q5_1]
    C --> D[Spanish transcript in memory]
    D --> E[translate_engine.py\nHelsinki-NLP/opus-mt-es-en\nINT8 CTranslate2]
    E --> F[English translated text]
    F --> G[TTS_Engine.py\nPiper ONNX]
    G --> H[English WAV output]
```

## Process sequence

```mermaid
sequenceDiagram
    participant App as main_translator.py
    participant STT as transcribe_engine.py
    participant W as whisper-cli.exe
    participant MT as translate_engine.py
    participant TTS as TTS_Engine.py
    participant FS as Local filesystem

    App->>STT: transcribe_audio(file_path)
    STT->>W: subprocess.run(cwd=Transcriber, -m ggml-base-q5_1.bin, -l es, -tp 0.0, -bs 5, -mc 0, -nt)
    W-->>STT: return code / stdout / stderr
    STT-->>App: Spanish transcript string
    App->>MT: translate_text(transcript)
    MT-->>App: English text
    App->>TTS: text_to_speech(translation, output_name)
    TTS-->>FS: Write English WAV
    App-->>App: Release the STT process memory before continued execution
```

The STT subprocess is intentionally isolated so its RAM can be released before the MT and TTS stages begin, which reduces maximum memory pressure on the board.

## Module relationship

```mermaid
graph TD
    Root[Repository]
    Root --> Req[requirements.txt]
    Root --> Docs[docs]
    Root --> App[audio_translator]
    Root --> VEnv[venv/]

    App --> Main[main_translator.py]
    App --> Convert[convert_mach_trans.py]
    App --> Transcriber[Transcriber]
    App --> Translator[Translator]
    App --> Voices[Voices]
    App --> Piper[Piper/]

    Convert --> HF[Helsinki-NLP/opus-mt-es-en]
    Convert --> MTModel[opus-mt-es-en-int8]
    MTModel --> MTFiles[model.bin + tokenizer + vocab]

    Transcriber --> Engine[transcribe_engine.py]
    Engine --> Whisper[Whisper/whisper-cli.exe]
    Engine --> WhisperModel[ggml-base-q5_1.bin]

    Translator --> NMT[translate_engine.py]
    Voices --> TTS[TTS_Engine.py]
    Piper --> PiperRuntime[Piper runtime / ONNX]
```
