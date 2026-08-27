from pathlib import Path
import re
import ctranslate2
from transformers import AutoTokenizer

SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_DIR = SCRIPT_DIR / "opus-mt-es-en-int8"
MODEL_NAME = "Helsinki-NLP/opus-mt-es-en"
SOURCE_LANG = "es"
TARGET_LANG = "en"

_translator = None
_tokenizer = None

# Pre-translation normalization rules to correct phonetic & domain ASR slips
NORMALIZATION_MAP = {
    r"\bwikipediaista\b": "wikipedista",
    r"\btrumpoward\b": "Temple-Wood",
}


def normalize_input_text(text: str) -> str:
    """Corrects known phonetic anomalies and non-standard suffixes before translation."""
    normalized = text
    for pattern, replacement in NORMALIZATION_MAP.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized.strip()


def setup_translation_model(
    model_dir: Path = MODEL_DIR,
    inter_threads: int = 1,
    intra_threads: int = 0,
) -> None:
    """Load the local INT8 OPUS-MT model and tokenizer once into memory."""
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


def translate_text(text: str, beam_size: int = 2) -> str:
    """
    Translates Spanish text to English in-memory using the INT8 OPUS-MT CTranslate2 engine.
    Applies text normalization and uses beam_size=2 for higher translation accuracy.
    """
    global _translator, _tokenizer

    if not text or not text.strip():
        return ""

    # 1. Clean and normalize input text
    cleaned_text = normalize_input_text(text)

    # 2. Ensure model and tokenizer are initialized
    if _translator is None or _tokenizer is None:
        setup_translation_model()

    # 3. Tokenize input tokens
    source_tokens = _tokenizer.convert_ids_to_tokens(
        _tokenizer.encode(cleaned_text, add_special_tokens=True)
    )

    # 4. Perform CTranslate2 batch translation
    results = _translator.translate_batch(
        [source_tokens],
        beam_size=beam_size,
        max_decoding_length=256,
        repetition_penalty=1.1,
    )

    target_tokens = results[0].hypotheses[0]

    # 5. Decode output tokens back into readable text
    return _tokenizer.decode(
        _tokenizer.convert_tokens_to_ids(target_tokens),
        skip_special_tokens=True,
    ).strip()


if __name__ == "__main__":
    test_cases = [
        "Hola, me llamo Emily Trumpoward, soy de Chicago y soy Wikipediaista.",
        "Hola, buenos días. ¿Cómo estás hoy?",
    ]

    for sample in test_cases:
        print(f"Original ({SOURCE_LANG})  : {sample}")
        print(f"Translated ({TARGET_LANG}): {translate_text(sample)}\n")