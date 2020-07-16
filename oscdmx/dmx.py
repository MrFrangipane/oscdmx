import time
from DMXEnttecPro import Controller


def run(shared):
    last_beat = 0
    previous_last_beat = 0

    color = 0.25, 1.0, 1.0

    dmx = Controller('/dev/ttyUSB0')

    while True:
        # Wait for beat
        while last_beat == previous_last_beat:
            info = shared.get()
            last_beat = info['last_beat']
            time.sleep(0.01)
        previous_last_beat = last_beat

        # Do stuff
        dmx.set_channel(2, int(color[0] * 255))
        dmx.set_channel(3, int(color[1] * 255))
        dmx.set_channel(4, int(color[2] * 255))
        dmx.submit()

        time.sleep(0.025)

        dmx.set_channel(2, 0)
        dmx.set_channel(3, 0)
        dmx.set_channel(4, 0)
        dmx.submit()
