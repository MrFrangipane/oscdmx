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

        self.par_hue = 0
        self.par_lightness = 0
        self._par_changed = False

        self.verbose = verbose

        print(f'Serving forever {host}:{port}')

    def _handle(self, address, value):
        if self.verbose:
            print(address, value)

        #
        # BARS

        if address == '/program_select':
            self.shared.program_index = value

        elif address == '/bpm/value' and value:
            self.shared.bpm = 80 + value * 80
            self.shared.strobe_speed = 240 + int(value * 13)

        elif address == '/color/hue':
            self.hue = value
            self.lightness = 1.0
            self._color_changed = True

        elif address == '/color/white':
            if self.shared.color_mode == self.shared.COLOR_MANUAL:
                self.shared.is_white = True

        elif address == '/debug/channel':
            self.shared.debug_channel = int(value + 1)

        elif address == '/debug/value':
            self.shared.debug_value = int(value * 255)

        elif address == '/color/mode':
            value = int(value)
            if value in (1, 2, 3, 4):
                self.shared.is_white = False

            self.shared.color_mode = value

        elif address == '/bpm/multiplier':
            self.shared.bpm_multiplier = [0.25, 0.5, 1, 2, 4][value]

        if self._color_changed:
            self.shared.color = colorsys.hsv_to_rgb(self.hue, 1.0, self.lightness)
            self.shared.is_white = False
            self._color_changed = False

        #
        # PARS

        elif address == '/par/selector':
            self.shared.par.current = value
            self.shared.par.changed = True

        elif address == '/hue/hue':
            self.par_hue = value
            self._par_changed = True

        elif address == '/hue_factor':
            self.par_lightness = value
            self._par_changed = True

        elif address == '/uv_factor':
            self.shared.par.uv = value
            self.shared.par.changed = True

        elif address == '/amber_factor':
            self.shared.par.amber = value
            self.shared.par.changed = True

        elif address == '/white_factor':
            self.shared.par.white = value
            self.shared.par.changed = True

        if self._par_changed:
            self.shared.par.color = colorsys.hsv_to_rgb(self.par_hue, 1.0, self.par_lightness)
            self.shared.par.changed = True
            self._par_changed = False

    def run(self):
        self.server.dispatcher.set_default_handler(self._handle)
        self.server.serve_forever()
