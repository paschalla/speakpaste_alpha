import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import queue
import time
import tempfile
import os
import sys

# --- Configuration ---
# The duration of silence (in seconds) that will trigger the recording to stop.
# This is the primary configuration for silence detection.
SILENCE_DURATION_S = 3.0

# Threshold for detecting silence. Adjust based on your microphone sensitivity.
SILENCE_THRESHOLD = 0.01

# Chunk size for processing. A larger size is more efficient but adds latency.
# 4096 is a good balance.
CHUNK_SIZE = 4096

# A constant for documentation, explaining the downstream requirement of the transcriber.
REQUIRED_WHISPER_SR = 16000


class AudioRecorder:
    """
    A class to handle real-time audio recording from the default input device,
    with automatic time-based silence detection to stop the recording.
    """

    def __init__(self):
        self._q = queue.Queue()
        self._recording = False
        try:
            self.device_sample_rate = sd.query_devices(kind='input')['default_samplerate']
        except Exception as e:
            print("Error: Could not query the default audio input device.", file=sys.stderr)
            print(f"Please ensure a microphone is connected and configured in your system. Details: {e}", file=sys.stderr)
            raise

    def _is_silent(self, data_chunk): 
        """Returns 'True' if the given audio chunk is silent."""
        rms = np.sqrt(np.mean(data_chunk**2))
        return rms < SILENCE_THRESHOLD

    def _audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio chunk."""
        if status:
            print(f"Audio callback status: {status}", file=sys.stderr)
        if self._recording:
            self._q.put(indata.copy())

    def record_audio(self):
        """
        Starts the recording process and saves the audio to a temporary WAV file
        upon detecting a fixed duration of silence (defined by SILENCE_DURATION_S above)

        Returns:
            str: The file path to the temporary WAV file.
        """
        self._q = queue.Queue()
        self._recording = True
        audio_data = []

        print(f"Using device sample rate: {int(self.device_sample_rate)} Hz.")
        print(f"Listening... Will stop after {SILENCE_DURATION_S} seconds of silence.")

        # Initialize the timer for silence detection.
        time_of_last_sound = time.time()

        try:
            with sd.InputStream(
                samplerate=self.device_sample_rate,
                channels=1,
                blocksize=CHUNK_SIZE,
                dtype="float32",
                callback=self._audio_callback,
            ):
                while self._recording:
                    chunk = self._q.get()
                    audio_data.append(chunk)

                    if self._is_silent(chunk):
                        # If silent, check if the silence duration has been reached.
                        if time.time() - time_of_last_sound > SILENCE_DURATION_S:
                            print("Silence duration exceeded, stopping recording.")
                            self._recording = False
                    else:
                        # If not silent, reset the timer.
                        time_of_last_sound = time.time()

        except Exception as e:
            print(f"An error occurred during recording: {e}", file=sys.stderr)
            return None

        print("Recording stopped. Saving audio...")
        if not audio_data:
            print("No audio data was recorded.", file=sys.stderr)
            return None
            
        full_audio = np.concatenate(audio_data, axis=0)

        temp_fd, temp_path = tempfile.mkstemp(suffix=".wav")
        os.close(temp_fd)

        write(temp_path, int(self.device_sample_rate), full_audio)
        print(f"Audio saved to temporary file: {temp_path}")

        return temp_path


# This block allows for direct testing of the recorder module.
if __name__ == "__main__":
    print("Preparing to test audio recording.")
    
    try:
        recorder = AudioRecorder()
        temp_file_path = recorder.record_audio()

        if temp_file_path and os.path.exists(temp_file_path):
            print(f"\nTest successful. Audio was recorded and saved to:")
            print(temp_file_path)
            print(f"\nNext step: Test this file with the transcriber:")
            print(f"python transcriber.py {temp_file_path}")
        else:
            print("\nTest failed. Audio file was not created.")
    except Exception as e:
        print(f"\nFailed to initialize recorder. Error: {e}", file=sys.stderr)
