from pathlib import Path

import ctranslate2
from transformers import AutoTokenizer

SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_DIR = SCRIPT_DIR / "opus-mt-es-en-int8"
MODEL_NAME = "Helsinki-NLP/opus-mt-es-en"
SOURCE_LANG = "es"
TARGET_LANG = "en"

_translator = None
_tokenizer = None


def setup_translation_model(
    model_dir: Path = MODEL_DIR,
    inter_threads: int = 1,
    intra_threads: int = 0,
) -> None:
    """Load the local INT8 OPUS-MT model and tokenizer once."""
    global _translator, _tokenizer

    model_file = model_dir / "model.bin"
    if not model_file.exists():
        raise FileNotFoundError(
            f"CTranslate2 model weights not found at {model_file}. "
            "Run convert_mach_trans.py first."
        )

    try:
        _tokenizer = AutoTokenizer.from_pretrained(
            str(model_dir),
            local_files_only=True,
        )
    except (OSError, ValueError) as error:
        raise FileNotFoundError(
            f"Tokenizer files are missing from {model_dir}. "
            "Regenerate the model with convert_mach_trans.py."
        ) from error

    _translator = ctranslate2.Translator(
        str(model_dir),
        device="cpu",
        inter_threads=inter_threads,
        intra_threads=intra_threads,
    )


def translate_text(text: str) -> str:
    """Translate Spanish text to English in memory using the INT8 model."""
    global _translator, _tokenizer

    cleaned_text = text.strip()
    if not cleaned_text:
        return ""

    if _translator is None or _tokenizer is None:
        setup_translation_model()

    source_tokens = _tokenizer.convert_ids_to_tokens(
        _tokenizer.encode(cleaned_text, add_special_tokens=True)
    )
    results = _translator.translate_batch(
        [source_tokens],
        beam_size=1,
    )
    target_tokens = results[0].hypotheses[0]
    return _tokenizer.decode(
        _tokenizer.convert_tokens_to_ids(target_tokens),
        skip_special_tokens=True,
    ).strip()


if __name__ == "__main__":
    sample_text = "Hola, buenos días. ¿Cómo estás hoy?"
    print(f"Original ({SOURCE_LANG}): {sample_text}")
    print(f"Translated ({TARGET_LANG}): {translate_text(sample_text)}")
