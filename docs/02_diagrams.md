# Visual System Diagrams

The diagrams use Mermaid syntax and can be rendered by GitHub, VS Code Markdown preview, or a Mermaid-compatible documentation site.

## End-to-end pipeline

```mermaid
flowchart LR
    A[WAV file or microphone] --> B[Audio capture and framing]
    B --> C[whisper-cli.exe\nQ8_0 Whisper model]
    C --> D[Spanish tokenized text]
    D --> E[ArgosMT / Helsinki-NLP\nCTranslate2 INT8]
    E --> F[English translated text]
    F --> G[Piper TTS\nONNX voice]
    G --> H[English WAV output]
```

## Process sequence

```mermaid
sequenceDiagram
    participant App as main_translator.py
    participant STT as test_whisper.py
    participant W as whisper-cli.exe
    participant FS as Local filesystem
    participant MT as CTranslate2 MT
    participant TTS as Piper

    App->>STT: transcribe_audio(file_path, threads)
    STT->>FS: Resolve input, executable, and model paths
    STT->>W: subprocess.run(cwd=Transcriber, -m model, -l es, -f input)
    Note over W: --no-timestamps --no-context
    W-->>STT: return code/stdout/stderr
    STT-->>App: Spanish transcript string in memory
    App->>MT: Tokenize and translate in memory
    MT-->>App: English text
    App->>TTS: Send text and voice configuration
    TTS-->>FS: Write English WAV
    App-->>App: Apply bounded buffers or batch result handling
```

The current repository implements the STT sequence only. The MT and TTS calls are the integration contract for the pending orchestrator.

## Module relationship

```mermaid
graph TD
    Root[Repository]
    Root --> Req[requirements.txt]
    Root --> Docs[docs]
    Root --> App[audio_translator]
    Root --> MTModel[opus-mt-es-en-int8]

    App --> Convert[convert_mach_trans.py]
    Convert --> HF[Helsinki-NLP/opus-mt-es-en]
    Convert --> MTModel
    App --> Main[main_translator.py\nempty scaffold]
    App --> Transcriber[Transcriber]
    Transcriber --> Wrapper[test_whisper.py]
    Wrapper --> Whisper[whisper-cli.exe]
    Wrapper --> WhisperModel[ggml-tiny-q8_0.bin\nprovisioned asset]
    App --> Piper[Piper/\ncurrently empty]
    App --> Voices[Voices/\ncurrently empty]
    Voices --> Voice[en_US-ryan-low.onnx + JSON\nprovisioned asset]
    MTModel --> MTFiles[model.bin + config + vocabulary]
```
