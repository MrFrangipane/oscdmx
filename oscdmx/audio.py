import time
import aubio
import pyaudio
import numpy as np


BUFFER_SIZE = 128

tempo = None
shared = None
samplerate = None


def start(samplerate_, shared_):
    global shared
    global tempo
    global samplerate

    shared = shared_
    samplerate = samplerate_

    tempo = aubio.tempo("default", BUFFER_SIZE * 2, BUFFER_SIZE, samplerate)

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=samplerate,
        input=True,
        frames_per_buffer=BUFFER_SIZE,
        stream_callback=_audio_callback
    )


def _audio_callback(in_data, frame_count, time_info, status):
    global tempo
    global shared
    global samplerate

    if shared.detection_reset:
        tempo = aubio.tempo("default", BUFFER_SIZE * 2, BUFFER_SIZE, samplerate)
        shared.bpm = shared.BPM_DEFAULT
        shared.detection_reset = False

    signal = np.frombuffer(in_data, dtype=np.float32)
    beat = tempo(signal)
    confidence = tempo.get_confidence()

    if beat[0] and confidence > 0.02:
        shared.bpm = tempo.get_bpm()
        shared.last_beat = time.time()
        shared.confidence = confidence

    return None, pyaudio.paContinue
