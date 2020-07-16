import time
import platform
import colorsys
import threading
import aubio
import pyaudio
import numpy as np
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from DMXEnttecPro import Controller


HOST = '0.0.0.0'
PORT_IN = 8000
PORT_OUT = 9000
BUFFER_SIZE = 128


class BeatDetector:
    def __init__(self, samplerate):
        self.samplerate = samplerate
        self.on = False
        self.bpm = 0
        self.color = 1, 0, 0
        self.client = None
        self.bmp_led = 0

        # DMX
        self.dmx = Controller('/dev/ttyUSB0')

        # AUDIO
        self.py_audio = pyaudio.PyAudio()
        self.stream = None
        self.tempo = None

        # OSC
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.set_default_handler(self.handle)
        self.server = osc_server.ThreadingOSCUDPServer((HOST, PORT_IN), self.dispatcher)

    def start(self):
        threading.Thread(target=self.server.serve_forever).start()
        threading.Thread(target=self.osc_loop).start()
        self.audio_start()
        self.dmx_loop()

    def _audio_callback(self, in_data, frame_count, time_info, status):
        signal = np.frombuffer(in_data, dtype=np.float32)
        beat = self.tempo(signal)
        if beat[0]:
            self.on = True
            self.bpm = self.tempo.get_bpm()

        return None, pyaudio.paContinue

    def handle(self, address, value):
        if self.client is None:
            client_ip, _ = self.server.get_request()[1]
            self.client = udp_client.SimpleUDPClient(client_ip, PORT_OUT)

        if address == '/octostrip/rainbow':
            self.color = colorsys.hsv_to_rgb(value/255.0, 1.0, 1.0)

    def audio_start(self):
        self.stream = self.py_audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=BUFFER_SIZE,
            stream_callback=self._audio_callback
        )
        fft_size = BUFFER_SIZE * 2
        self.tempo = aubio.tempo("default", fft_size, BUFFER_SIZE, self.samplerate)

    def osc_loop(self):
        while True:
            if self.on and self.client is not None:
                self.bmp_led = 1 - self.bmp_led

                self.client.send_message('/octostrip/bpm_led_a', self.bmp_led)
                self.client.send_message('/octostrip/bpm_led_b', 1 - self.bmp_led)
                self.client.send_message('/octostrip/bpm_label', f'BPM : {self.bpm:.1f}')

            else:
                time.sleep(0.005)

    def dmx_loop(self):
        while True:
            if self.on:
                self.dmx.set_channel(2, int(self.color[0] * 255))
                self.dmx.set_channel(3, int(self.color[1] * 255))
                self.dmx.set_channel(4, int(self.color[2] * 255))
                self.dmx.submit()

                time.sleep(0.05)

                self.dmx.set_channel(2, 0)
                self.dmx.set_channel(3, 0)
                self.dmx.set_channel(4, 0)
                self.dmx.submit()
                self.on = False

            time.sleep(0.005)

    def __del__(self):
        self.stream.close()
        self.py_audio.terminate()


def main():
    if platform.architecture()[0] == '64bit':
        samplerate = 44100
    else:
        samplerate = 48000

    bd = BeatDetector(samplerate)
    bd.start()


if __name__ == "__main__":
    main()
