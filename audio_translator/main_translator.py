import argparse
import sys
import time
from pathlib import Path

# Ensure the root directory (audio_translator) is in Python's import search path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import each stage engine from its respective subfolder
from Transcriber.transcribe_engine import transcribe_audio
from Translator.translate_engine import translate_text
from Voices.TTS_Engine import text_to_speech


def run_full_pipeline(
    audio_path: str, output_voice_name: str = "translated_speech.wav"
) -> dict:
    """Executes the full 3-stage offline translation pipeline:

    1. STT (Quantized Whisper): Audio (.wav) -> Spanish Text
    2. NMT (Argos Translate):   Spanish Text -> English Text
    3. TTS (Piper ONNX):        English Text -> Synthesized Audio (.wav)
    """
    total_start_time = time.time()

    # --- Stage 1: Speech-to-Text ---
    t0 = time.time()
    print(f"\n[1/3] Transcribing Spanish audio: '{audio_path}'...")
    transcript = transcribe_audio(audio_path)
    stt_latency = time.time() - t0
    print(f"      └── Completed in {stt_latency:.2f}s")

    # --- Stage 2: Machine Translation ---
    t1 = time.time()
    print(f"[2/3] Translating Spanish text to English...")
    translation = translate_text(transcript)
    nmt_latency = time.time() - t1
    print(f"      └── Completed in {nmt_latency:.2f}s")

    # --- Stage 3: Text-to-Speech ---
    t2 = time.time()
    print(f"[3/3] Synthesizing English speech with Piper TTS...")
    audio_output = text_to_speech(translation, output_name=output_voice_name)
    tts_latency = time.time() - t2
    print(f"      └── Completed in {tts_latency:.2f}s")

    total_latency = time.time() - total_start_time

    return {
        "transcript": transcript,
        "translation": translation,
        "output_audio": audio_output,
        "metrics": {
            "stt_latency": stt_latency,
            "nmt_latency": nmt_latency,
            "tts_latency": tts_latency,
            "total_latency": total_latency,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wearable AI Audio Translator: Offline Edge Pipeline."
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default="test_audio2.wav",
        help="Path to the input Spanish .wav file (default: test_audio2.wav)",
    )
    parser.add_argument(
        "--show-transcript",
        action="store_true",
        help="Print the raw Spanish transcript.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="translated_speech.wav",
        help="Custom output filename for the synthesized audio.",
    )
    args = parser.parse_args()

    # Execute pipeline
    results = run_full_pipeline(
        audio_path=args.audio, output_voice_name=args.output_name
    )

    # Display Summary
    print("\n" + "=" * 60)
    print("           PIPELINE EXECUTION COMPLETE")
    print("=" * 60)
    if args.show_transcript:
        print(f"Original (Spanish) : {results['transcript']}")
    print(f"Translation (English): {results['translation']}")
    print(f"Synthesized Audio  : {results['output_audio']}")
    print("-" * 60)
    print("Performance / Latency Metrics:")
    print(f"  • STT Latency   : {results['metrics']['stt_latency']:.2f}s")
    print(f"  • NMT Latency   : {results['metrics']['nmt_latency']:.2f}s")
    print(f"  • TTS Latency   : {results['metrics']['tts_latency']:.2f}s")
    print(f"  • Total Pipeline: {results['metrics']['total_latency']:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()