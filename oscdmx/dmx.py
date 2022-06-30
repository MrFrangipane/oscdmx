import time
from DMXEnttecPro import Controller
import dmx_programs


PROGRAMS = [
    dmx_programs.blackout,
    dmx_programs.rainbow_wave,
    dmx_programs.steps,
    dmx_programs.strobe,
    dmx_programs.debug
]


class Phase:
    def __init__(self):
        self._last_time = time.time()
        self.eigth = 0
        self.fourth = 0
        self.half = 0
        self.one = 0

    def update(self, bpm):
        now = time.time()

        phase_delta = (now - self._last_time) * (bpm / 60.0)
        self._last_time = time.time()

        self.eigth += phase_delta * .125
        self.fourth += phase_delta * .25
        self.half += phase_delta * .5
        self.one += phase_delta

    def __repr__(self):
        return "<Phase(one={:0.2f})>".format(self.one)


def par_update(dmx, par_info):
    offset = dmx_programs.PAR.FIRST_CHANNEL + par_info['current'] * dmx_programs.PAR.CH_COUNT
    dmx.set_channel(offset + dmx_programs.PAR.CH_RED, int(par_info['color'][0] * 255))
    dmx.set_channel(offset + dmx_programs.PAR.CH_GREEN, int(par_info['color'][1] * 255))
    dmx.set_channel(offset + dmx_programs.PAR.CH_BLUE, int(par_info['color'][2] * 255))
    dmx.set_channel(offset + dmx_programs.PAR.CH_WHITE, int(par_info['white'] * 255))
    dmx.set_channel(offset + dmx_programs.PAR.CH_AMBER, int(par_info['amber'] * 255))
    dmx.set_channel(offset + dmx_programs.PAR.CH_UV, int(par_info['uv'] * 255))


def run(shared):
    dmx = Controller('/dev/ttyUSB0')
    dmx.set_all_channels(0)
    dmx.submit()

    phase = Phase()

    while True:
        info = shared.get()

        if shared.par.changed:
            par_info = vars(shared.par)
            par_update(dmx, par_info)
            shared.par.changed = False

        phase.update(info['bpm'] * info['bpm_multiplier'])

        PROGRAMS[shared.program_index](shared, dmx, phase)

        dmx.submit()
        time.sleep(0.01)
