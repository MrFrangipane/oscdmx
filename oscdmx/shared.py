

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

    BPM_DEFAULT = 120

    def __init__(self):
        self.bpm = self.BPM_DEFAULT
        self.bpm_multiplier = 1
        self.confidence = 0
        self.color = 1, 1, 1

        self.program_index = 3

        self.color_mode = self.COLOR_MANUAL
        self.phase_mode = self.PHASE_NORMAL

        self.strobe_speed = 0
        self.is_white = True

        self.debug_channel = 0
        self.debug_value = 0

        self.auto_on = False

    def get(self):
        return {'bpm': self.bpm, 'bpm_multiplier': self.bpm_multiplier}
