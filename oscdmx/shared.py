

class Shared:
    def __init__(self):
        self.bpm = 0
        self.last_beat = 0
        self.confidence = 0

    def get(self):
        return {'bpm': self.bpm, 'last_beat': self.last_beat}

    def __repr__(self):
        return "bpm: {:.1f}, last beat {:.2f}, confidence {:.3f}".format(
            self.bpm, self.last_beat, self.confidence
        )
