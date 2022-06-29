import colorsys
from pythonosc import dispatcher
from pythonosc import osc_server


class OSC:
    def __init__(self, shared, host, port, verbose=False):
        self.shared = shared
        self.clients = dict()

        self.dispatcher_ = dispatcher.Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer((host, port), self.dispatcher_)

        self.hue = 0
        self.lightness = 0
        self._color_changed = False

        self.verbose = verbose

        print(f'Serving forever {host}:{port}')

    def _handle(self, address, value):
        if self.verbose:
            print(address, value)

        if address == '/program_select':
            self.shared.program_index = value

        elif address == '/bpm_value' and value:
            self.shared.bpm = 80 + value * 80

        elif address.endswith('/color'):
            self.hue = value
            self.lightness = 1.0
            self._color_changed = True

        elif address.endswith('/white'):
            if self.shared.color_mode == self.shared.COLOR_MANUAL:
                self.shared.is_white = True

        elif address == '/strobe_speed':
            self.shared.strobe_speed = 240 + int(value * 13)

        elif address == '/debug/channel':
            self.shared.debug_channel = int(value + 1)

        elif address == '/debug/value':
            self.shared.debug_value = int(value * 255)

        elif address.endswith('/color_mode'):
            value = int(value)
            if value in (1, 2, 3, 4):
                self.shared.is_white = False

            self.shared.color_mode = value

        if self._color_changed:
            self.shared.color = colorsys.hsv_to_rgb(self.hue, 1.0, self.lightness)
            self.shared.is_white = False
            self._color_changed = False

    def run(self):
        self.server.dispatcher.set_default_handler(self._handle)
        self.server.serve_forever()
