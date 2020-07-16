import pyaudio
import numpy as np
import aubio
import signal
from pythonosc.udp_client import SimpleUDPClient
from typing import List, NamedTuple, Tuple

from DMXEnttecPro import Controller


class ClientInfo(NamedTuple):
    ip: str
    port: int
    address: str


class BeatPrinter:
    def __init__(self):
        self.state: int = 0
        self.spinner = "▚▞"

    def print_bpm(self, bpm: float):
        print(f"{self.spinner[self.state]}\t{bpm:.1f} BPM")
        self.state = (self.state + 1) % len(self.spinner)


class BeatDetector:
    def __init__(self, buf_size, client_infos, verbose):
        self.buf_size = buf_size
        self.client_infos = client_infos
        self.verbose = verbose
        self.samplerate = 44100
        self.time = 0.0
        self.time_beat = 0.0
        self.bpm = 0

        self.dmx = Controller('/dev/ttyUSB0', auto_submit=True)

        self.on = False
        self.on_buffers = 0

        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=self.buf_size,
            stream_callback=self._pyaudio_callback
        )

        fft_size = self.buf_size * 2
        self.tempo = aubio.tempo("default", fft_size, self.buf_size, self.samplerate)

        # Set up OSC clients to send beat data to
        self.osc_clients = [(SimpleUDPClient(x.ip, x.port), x.address) for x in self.client_infos]
        self.spinner = BeatPrinter()

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        signal = np.frombuffer(in_data, dtype=np.float32)
        beat = self.tempo(signal)

        self.time += (float(frame_count) / float(self.samplerate))

        if self.tempo.get_confidence() > 0.05 and beat[0]:
            self.time_beat = self.time
            self.bpm = self.tempo.get_bpm()
            self.on = True
        #
        # if self.bpm:
        #     period = 60.0 / self.bpm
        #     self.on = (self.time - self.time_beat) % period == 0

        if self.on:
            self.on_buffers += 1

        if self.on_buffers > 5:
            self.on = False
            self.on_buffers = 0

        self.dmx.set_channel(1, int(self.on) * 255)

        return None, pyaudio.paContinue  # Tell pyAudio to continue

    def __del__(self):
        self.stream.close()
        self.pyaudio.terminate()


def main():
    client_infos = [ClientInfo('192.168.0.1', 5000, '/test')]
    bd = BeatDetector(128, client_infos, verbose=True)

    signal.pause()  # Audio processing happens in separate thread, so put this thread to sleep


if __name__ == "__main__":
    main()
