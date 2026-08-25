from pathlib import Path

import ctranslate2
from transformers import AutoTokenizer

print("Downloading and converting Hugging Face model to INT8...")

MODEL_NAME = "Helsinki-NLP/opus-mt-es-en"
OUTPUT_DIR = Path(__file__).resolve().parent / "Translator" / "opus-mt-es-en-int8"

converter = ctranslate2.converters.TransformersConverter(MODEL_NAME)

converter.convert(
    output_dir=str(OUTPUT_DIR),
    quantization="int8",
    force=True,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Success! The INT8 model and tokenizer were saved to {OUTPUT_DIR}.")