

class Shared:
    COLOR_MANUAL = 0
    COLOR_AUTO_NORMAL = 1
    COLOR_AUTO_HALF = 2
    COLOR_AUTO_FOURTH = 3
    COLOR_AUTO_EIGTH = 4

    PHASE_NORMAL = 0
    PHASE_HALF = 1
    PHASE_FOURTH = 2
    PHASE_EIGTH = 3

    BPM_DEFAULT = 30

    def __init__(self):
        self.bpm = self.BPM_DEFAULT
        self.last_beat = 0
        self.confidence = 0
        self.color = 1, 1, 1

        self.program_index = 3

        self.color_mode = self.COLOR_MANUAL
        self.phase_mode = self.PHASE_NORMAL

        self.debug_on = False
        self.debug = [0.0] * 8

        self.auto_on = False

    def get(self):
        return {'bpm': self.bpm, 'last_beat': self.last_beat}

    def __repr__(self):
        return "bpm: {:.1f}, last beat {:.2f}, confidence {:.3f}".format(
            self.bpm, self.last_beat, self.confidence
        )
