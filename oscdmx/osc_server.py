import colorsys
from pythonosc import dispatcher
from pythonosc import osc_server


HOST = '0.0.0.0'
PORT_IN = 8000
PORT_OUT = 9000


class OSC:
    def __init__(self, shared):
        self.shared = shared
        self.clients = dict()

        self.dispatcher_ = dispatcher.Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer((HOST, PORT_IN), self.dispatcher_)

        self.hue = 0
        self.lightness = 0
        self._color_changed = False

    def _handle(self, address, value):
        print(address, value)

        if address == '/rainbow/color':
            self.hue = value
            self._color_changed = True

        elif address == '/rainbow/lightness':
            self.lightness = value
            self._color_changed = True

        elif address == '/debug/on':
            self.shared.debug_on = value

        elif address.startswith('/debug/select/1/'):
            bar_index = int(address[-1]) - 1
            self.shared.debug[bar_index] = value

        elif address.startswith('/rainbow/speed_color/') and value:
            mode_index = int(address[-3]) - 1
            self.shared.color_mode = mode_index

        elif address.startswith('/rainbow/speed_lightness/') and value:
            mode_index = int(address[-3]) - 1
            self.shared.phase_mode = mode_index

        elif address.startswith('/program_select/1/') and value:
            program_index = int(address[-1]) - 1
            self.shared.program_index = program_index

        elif address.startswith('/bpm/value') and value:
            self.shared.bpm = value

        elif address == '/auto/on':
            self.shared.auto_on = value

        if self._color_changed:
            self.shared.color = colorsys.hsv_to_rgb(self.hue / 255.0, 1.0, self.lightness / 255.0)
            self._color_changed = False

    def run(self):
        self.server.dispatcher.set_default_handler(self._handle)
        self.server.serve_forever()
