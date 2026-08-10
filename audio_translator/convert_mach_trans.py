import ctranslate2

print("Downloading and converting Hugging Face model to INT8...")

# 1. Point to the Hugging Face model
converter = ctranslate2.converters.TransformersConverter("Helsinki-NLP/opus-mt-es-en")

# 2. Convert and save it to a new folder in your current directory
converter.convert(
    output_dir="opus-mt-es-en-int8", 
    quantization="int8",
    force=True # Overwrites if the folder already exists
)

print("Success! The INT8 model has been saved to the 'opus-mt-es-en-int8' folder.")