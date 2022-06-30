import math
import colorsys


BAR_CH_COUNT = 6
CH_RAINBOW = 1
CH_RED = 2  # 0 - 255
CH_GREEN = 3  # 0 - 255
CH_BLUE = 4  # 0 - 255
CH_STROBE = 5  # 1 - 20 Hz
CH_AUTO_CHASE = 6  # SOUND > 240


class PAR:
    FIRST_CHANNEL = 50
    CH_COUNT = 6
    CH_RED = 0
    CH_GREEN = 1
    CH_BLUE = 2
    CH_WHITE = 3
    CH_AMBER = 4
    CH_UV = 5


def _color(shared, phase):
    if shared.is_white:
        return 1.0, 1.0, 1.0

    return {
        shared.COLOR_MANUAL: shared.color,
        shared.COLOR_AUTO_NORMAL: colorsys.hsv_to_rgb(phase.one, 1.0, 1.0),
        shared.COLOR_AUTO_EIGTH: colorsys.hsv_to_rgb(phase.eigth, 1.0, 1.0),
        shared.COLOR_AUTO_FOURTH: colorsys.hsv_to_rgb(phase.fourth, 1.0, 1.0),
        shared.COLOR_AUTO_HALF: colorsys.hsv_to_rgb(phase.half, 1.0, 1.0)
    }[shared.color_mode]


def auto(shared, dmx, phase):
    for i in range(8):
        channel = i * 6
        dmx.set_channel(channel + 1, 0)
        dmx.set_channel(channel + 2, 0)
        dmx.set_channel(channel + 3, 0)
        dmx.set_channel(channel + 4, 0)
        dmx.set_channel(channel + 5, 0)
        dmx.set_channel(channel + 6, 250)


def debug(shared, dmx, phase):
    dmx.set_channel(shared.debug_channel, shared.debug_value)


def rainbow_wave(shared, dmx, phase):
    phase_ = {
        shared.PHASE_NORMAL: phase.one,
        shared.PHASE_EIGTH: phase.eigth,
        shared.PHASE_FOURTH: phase.fourth,
        shared.PHASE_HALF: phase.half,
    }[shared.phase_mode]

    cos = [0.0] * 8
    for i in range(8):
        cos[i] = math.cos(2.0 * (phase_ + 0.125 * i) * math.pi) * 0.5 + 0.5

    color = _color(shared, phase)

    for i in range(8):
        channel = i * 6

        dmx.set_channel(channel + 1, 0)
        dmx.set_channel(channel + 2, int(color[0] * 255 * cos[i]))
        dmx.set_channel(channel + 3, int(color[1] * 255 * cos[i]))
        dmx.set_channel(channel + 4, int(color[2] * 255 * cos[i]))
        dmx.set_channel(channel + 5, 0)
        dmx.set_channel(channel + 6, 0)


def steps(shared, dmx, phase):
    phase_ = {
        shared.PHASE_NORMAL: phase.one,
        shared.PHASE_EIGTH: phase.eigth,
        shared.PHASE_FOURTH: phase.fourth,
        shared.PHASE_HALF: phase.half,
    }[shared.phase_mode]

    color = _color(shared, phase)

    values = [0.0] * 8
    for i in range(8):
        phase_threshold = i * .125
        values[i] = (abs(phase_ % 1 - phase_threshold) < 0.1) * 255

    values = [
        values[6],
        values[4],
        values[2],
        values[0],
        values[1],
        values[3],
        values[5],
        values[7]
    ]

    for i, value in enumerate(values):
        channel = i * 6

        dmx.set_channel(channel + 1, 0)
        dmx.set_channel(channel + 2, int(color[0] * value))
        dmx.set_channel(channel + 3, int(color[1] * value))
        dmx.set_channel(channel + 4, int(color[2] * value))
        dmx.set_channel(channel + 5, 0)
        dmx.set_channel(channel + 6, 0)


def strobe(shared, dmx, phase):
    for bar in range(8):
        i = bar * BAR_CH_COUNT
        color = _color(shared, phase)

        dmx.set_channel(i + CH_RAINBOW, 0)
        dmx.set_channel(i + CH_RED, int(color[0] * 255))
        dmx.set_channel(i + CH_GREEN, int(color[1] * 255))
        dmx.set_channel(i + CH_BLUE, int(color[2] * 255))
        dmx.set_channel(i + CH_STROBE, shared.strobe_speed)
        dmx.set_channel(i + CH_AUTO_CHASE, 0)


def blackout(shared, dmx, phase):
    for bar in range(8):
        i = bar * BAR_CH_COUNT
        dmx.set_channel(i + CH_RED, 0)
        dmx.set_channel(i + CH_GREEN, 0)
        dmx.set_channel(i + CH_BLUE, 0)
