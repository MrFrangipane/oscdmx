from threading import Thread
from . import dmx
#from . import audio
from . import osc_server
from . import osc_client
from .shared import Shared


def main(samplerate, tablet_ip):
    shared = Shared()

    osc = osc_server.OSC(shared)

    thread_osc_server = Thread(target=osc.run)
    thread_osc_client = Thread(target=osc_client.run, args=(shared, tablet_ip))
    thread_dmx = Thread(target=dmx.run, args=(shared, ))

    thread_osc_server.start()
    thread_osc_client.start()
    thread_dmx.start()

    #audio.start(samplerate, shared)
