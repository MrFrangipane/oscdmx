

class Shared:
    COLOR_MANUAL = 0
    COLOR_AUTO_NORMAL = 1
    COLOR_AUTO_HALF = 2
    COLOR_AUTO_FOURTH = 3
    COLOR_AUTO_EIGTH = 4

    def __init__(self):
        self.bpm = 0
        self.last_beat = 0
        self.confidence = 0
        self.color = 1, 1, 1

        self.color_mode = self.COLOR_MANUAL

        self.debug_on = True
        self.debug = [0.0] * 8

    def get(self):
        return {'bpm': self.bpm, 'last_beat': self.last_beat}

    def __repr__(self):
        return "bpm: {:.1f}, last beat {:.2f}, confidence {:.3f}".format(
            self.bpm, self.last_beat, self.confidence
        )
