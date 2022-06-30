from threading import Thread
from oscdmx import dmx
from oscdmx import osc_server
from oscdmx.shared import Shared


def main(server_host, server_port, verbose):
    shared = Shared()

    osc = osc_server.OSC(shared, server_host, server_port, verbose)

    thread_osc_server = Thread(target=osc.run)
    thread_dmx = Thread(target=dmx.run, args=(shared, ))

    thread_osc_server.start()
    thread_dmx.start()
