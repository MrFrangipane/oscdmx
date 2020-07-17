from threading import Thread
from . import osc
from . import dmx
from . import audio
from .shared import Shared


def main(samplerate):
    shared = Shared()

    thread_osc = Thread(target=osc.run, args=(shared, ))
    thread_dmx = Thread(target=dmx.run, args=(shared, ))

    thread_osc.start()
    thread_dmx.start()
    audio.start(samplerate, shared)
