import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os
import webrtcvad
import threading

# _print = print
def _print(*args,**kwarghs):
    pass 


class VoiceActivityDetector:
    def __init__(self, frame_duration_ms=30, padding_duration_ms=300, vad_aggressiveness=3):
        self.vad = webrtcvad.Vad(vad_aggressiveness)
        self.frame_duration_ms = frame_duration_ms
        self.padding_duration_ms = padding_duration_ms
        self.original_num_padding_frames = padding_duration_ms // frame_duration_ms
        self.num_padding_frames = self.original_num_padding_frames
        self.frames = []
        self.triggered = False
        self.has_spoken = False

    def process_frame(self, frame):
        is_speech = self.vad.is_speech(frame, 16000)
        _print(is_speech,"      ",end="\r")
        if not self.triggered:
            self.frames.append(frame)
            if is_speech:
                self.triggered = True
                self.has_spoken = True
                self.frames = self.frames[-self.original_num_padding_frames:]  # Keep only the last few frames
                print("speech detected")
        else:
            self.frames.append(frame)
            if not is_speech and self.has_spoken:
                self.num_padding_frames -= 1
                print(f'Silence countdown: {self.num_padding_frames}')
                if self.num_padding_frames == 0:
                    print('silence detected...')
                    return False  # Stop recording
            elif is_speech:
                self.num_padding_frames = self.original_num_padding_frames
        return True

    def record(self, fs=16000):
        self.stop_recording = threading.Event()  # Use an event to signal stopping

        def callback(indata, frames, time, status):
            if status:
                print(status)
            if not self.process_frame(indata):
                self.stop_recording.set()  # Signal to stop recording

        with sd.RawInputStream(samplerate=fs, blocksize=int(fs * self.frame_duration_ms / 1000), channels=1, dtype='int16', callback=callback):
            while not self.stop_recording.is_set():  # Wait until stop signal is received
                sd.sleep(100)  # Short sleep to remain responsive
        return np.frombuffer(b''.join(self.frames), dtype=np.int16), fs

def get_user_response():
    vad = VoiceActivityDetector()
    print("Please start speaking, when finished, pause and the recording will end...")
    recording, fs = vad.record()

    print('Saving the recording...')
    output_filename = "temporary.wav"
    write(output_filename, fs, recording)  # Save as WAV file
    print(f"Recording saved as {output_filename}")


if __name__ == "__main__":
    while True:
        get_user_response()