import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EXE_PATH = SCRIPT_DIR / "whisper-cli.exe"
MODEL_PATH = SCRIPT_DIR / "ggml-tiny-q8_0.bin"


def transcribe_audio(file_path: str) -> str:
    input_path = SCRIPT_DIR / file_path

    if not EXE_PATH.exists():
        raise FileNotFoundError(f"Executable not found: {EXE_PATH}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    command = [
        str(EXE_PATH),
        "-m", str(MODEL_PATH),
        "-l", "es",
        "-f", str(input_path),
        "--no-timestamps",
        "--no-context",
    ]
    result = subprocess.run(
        command,
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        details = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
        raise RuntimeError(f"Whisper failed with exit code {result.returncode}: {details}")

    return result.stdout.strip()

print(transcribe_audio("test_audio.wav"))