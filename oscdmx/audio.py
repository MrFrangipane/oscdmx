import time
import aubio
import pyaudio
import numpy as np
from .shared import Shared


BUFFER_SIZE = 128
SAMPLERATE = 44100

shared = Shared()
tempo = aubio.tempo("default", BUFFER_SIZE * 2, BUFFER_SIZE, SAMPLERATE)


def start(shared_):
    global shared
    shared = shared_

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLERATE,
        input=True,
        frames_per_buffer=BUFFER_SIZE,
        stream_callback=_audio_callback
    )


def _audio_callback(in_data, frame_count, time_info, status):
    global shared
    global tempo
    signal = np.frombuffer(in_data, dtype=np.float32)
    beat = tempo(signal)
    confidence = tempo.get_confidence()

    if beat[0] and confidence > 0.1:
        shared.bpm = tempo.get_bpm()
        shared.last_beat = time.time()
        shared.confidence = confidence

    return None, pyaudio.paContinue
