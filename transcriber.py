import sys
import os
from faster_whisper import WhisperModel
import time

# --- Configuration ---
# We use the 'small' model as it offers a great balance of speed and accuracy
# for punctuation and capitalization, running efficiently on the CPU.
MODEL_SIZE = "small"

# As determined by our hardware analysis, we will run inference on the CPU.
DEVICE = "cpu"

# 'int8' is a compute type that provides a significant speed-up on modern CPUs
# with a minimal impact on accuracy.
COMPUTE_TYPE = "int8"


class Transcriber:
    """
    A class to handle the transcription of audio files using the faster-whisper
    library. It loads the model once and can be reused for multiple files.
    """

    def __init__(self):
        """
        Initializes the Transcriber and loads the specified whisper model into memory.
        """
        print(f"Initializing transcriber...")
        print(f"Loading model: '{MODEL_SIZE}' (this may take a moment on first run)...")
        self._model = None
        try:
            self._model = WhisperModel(
                model_size_or_path=MODEL_SIZE,
                device=DEVICE,
                compute_type=COMPUTE_TYPE,
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading whisper model: {e}", file=sys.stderr)
            print("Please ensure you have a stable internet connection for the first download.", file=sys.stderr)
            print("Also verify that your CTranslate2 backend is installed correctly.", file=sys.stderr)
            raise

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribes the given audio file and returns the full text.

        Args:
            audio_path (str): The path to the audio file (e.g., a .wav file).

        Returns:
            str: The transcribed text with punctuation and capitalization.
        """
        if not self._model:
            print("Model is not loaded. Cannot transcribe.", file=sys.stderr)
            return ""
            
        if not os.path.exists(audio_path):
            print(f"Audio file not found at path: {audio_path}", file=sys.stderr)
            return ""

        print(f"Transcribing audio file: {audio_path}")
        start_time = time.time()

        try:
            # The 'transcribe' method returns an iterator of segment objects.
            segments, info = self._model.transcribe(audio_path, beam_size=5)

            print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

            # We join the 'text' property of each segment to form the full text.
            # Using a generator expression and join is efficient.
            full_text = "".join(segment.text for segment in segments).strip()

        except Exception as e:
            print(f"An error occurred during transcription: {e}", file=sys.stderr)
            return ""

        end_time = time.time()
        duration = end_time - start_time
        print(f"Transcription completed in {duration:.2f} seconds.")

        return full_text


# This block allows for direct testing of the transcriber module.
if __name__ == "__main__":
    # Check if a file path is provided as a command-line argument.
    if len(sys.argv) < 2:
        print("\n--- Testing Instructions ---")
        print("This script tests the transcription functionality.")
        print("Usage: python transcriber.py <path_to_audio_file>")
        print("\nExample workflow:")
        print("1. Run 'python recorder.py' to record a test audio file.")
        print("   (It will print the path to the saved .wav file, e.g., /tmp/xyz.wav)")
        print("2. Run this script with that path:")
        print("   python transcriber.py /tmp/xyz.wav")
        sys.exit(1)

    audio_file = sys.argv[1]

    try:
        # 1. Initialize the transcriber (this loads the model)
        transcriber = Transcriber()
        
        # 2. Transcribe the audio file
        transcribed_text = transcriber.transcribe_audio(audio_file)

        # 3. Print the result
        if transcribed_text:
            print("\n--- Transcription Result ---")
            print(transcribed_text)
            print("--------------------------")
        else:
            print("\nTranscription failed or produced no text.")

    except Exception as e:
        print(f"\nAn error occurred during the test run: {e}", file=sys.stderr)