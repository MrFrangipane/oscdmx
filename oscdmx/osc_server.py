import colorsys
from pythonosc import dispatcher
from pythonosc import osc_server


HOST = '0.0.0.0'
PORT_IN = 8000
PORT_OUT = 9000

shared = None
clients = dict()

dispatcher_ = dispatcher.Dispatcher()
server = osc_server.ThreadingOSCUDPServer((HOST, PORT_IN), dispatcher_)


def _handle(address, value):
    global clients
    global shared

    print(address, value)

    if address == '/rainbow/color':
        shared.color = colorsys.hsv_to_rgb(value/255.0, 1.0, 1.0)

    elif address == '/bpm/reset_detection' and value:
        shared.detection_reset = True

    elif address == '/debug/on':
        shared.debug_on = value

    elif address.startswith('/debug/select/1/'):
        bar_index = int(address[-1]) - 1
        shared.debug[bar_index] = value

    elif address.startswith('/rainbow/speed_color/') and value:
        mode_index = int(address[-3]) - 1
        shared.color_mode = mode_index

    elif address.startswith('/rainbow/speed_lightness/') and value:
        mode_index = int(address[-3]) - 1
        shared.phase_mode = mode_index


def run(shared_):
    global shared
    global server

    shared = shared_

    server.dispatcher.set_default_handler(_handle)
    server.serve_forever()
