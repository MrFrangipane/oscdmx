from threading import Thread
import dmx
import osc_server
from shared import Shared


def main(server_host, server_port, verbose):
    shared = Shared()

    osc = osc_server.OSC(shared, server_host, server_port, verbose)

    thread_osc_server = Thread(target=osc.run)
    thread_dmx = Thread(target=dmx.run, args=(shared, ))

    thread_osc_server.start()
    thread_dmx.start()
