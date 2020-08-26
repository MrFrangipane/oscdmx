import time
from DMXEnttecPro import Controller
from . import dmx_programs


PROGRAMS = [
    dmx_programs.blackout,
    dmx_programs.rainbow_wave,
    dmx_programs.steps,
    dmx_programs.strobe
]


class Phase:
    def __init__(self):
        self._last_time = time.time()
        self.eigth = 0
        self.fourth = 0
        self.half = 0
        self.one = 0
        self.absolute = 0

    def update(self, last_beat, bpm):
        now = time.time()

        self.absolute = (now - last_beat) * (bpm / 60.0)

        phase_delta = (now - self._last_time) * (bpm / 60.0)
        self._last_time = time.time()

        self.eigth += phase_delta * .125
        self.fourth += phase_delta * .25
        self.half += phase_delta * .5
        self.one += phase_delta

    def __repr__(self):
        return "<Phase(one={:0.2f} absolute={:0.2f})>".format(self.one, self.absolute)


def run(shared):
    dmx = Controller('/dev/ttyUSB0')
    dmx.set_all_channels(0)
    dmx.submit()

    phase = Phase()

    while True:
        info = shared.get()
        last_beat = info['last_beat']
        bpm = info['bpm']

        if shared.debug_on:
            dmx_programs.debug(shared, dmx, phase)

        elif shared.auto_on:
            dmx_programs.auto(shared, dmx, phase)

        else:
            phase.update(last_beat, bpm)
            PROGRAMS[shared.program_index](shared, dmx, phase)

        dmx.submit()
        time.sleep(0.01)
