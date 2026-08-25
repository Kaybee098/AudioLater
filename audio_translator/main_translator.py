import argparse

try:
	from .Transcriber.transcribe_engine import transcribe_audio
	from .Translator.translate_engine import translate_text
except ImportError:
	from Transcriber.transcribe_engine import transcribe_audio
	from Translator.translate_engine import translate_text


def translate_audio(audio_path: str) -> tuple[str, str]:
	"""Transcribe Spanish audio and translate the result to English in memory."""
	transcript = transcribe_audio(audio_path)
	translation = translate_text(transcript)
	return transcript, translation


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Translate Spanish audio to English using local edge models."
	)
	parser.add_argument(
		"audio",
		nargs="?",
		default="test_audio2.wav",
		help="Audio path, relative to Transcriber, or an absolute path.",
	)
	parser.add_argument(
		"--show-transcript",
		action="store_true",
		help="Print the Spanish transcript before the English translation.",
	)
	args = parser.parse_args()

	transcript, translation = translate_audio(args.audio)
	if args.show_transcript:
		print(f"Spanish: {transcript}")
	print(f"English: {translation}")


if __name__ == "__main__":
	main()
