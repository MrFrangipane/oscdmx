import math
import colorsys


def debug(shared, dmx, phase):
    for bar in range(8):
        start = 6 * bar
        dmx.set_channel(start + 2, int(shared.color[0] * 255 * shared.debug[bar]))
        dmx.set_channel(start + 3, int(shared.color[1] * 255 * shared.debug[bar]))
        dmx.set_channel(start + 4, int(shared.color[2] * 255 * shared.debug[bar]))


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

    color = {
        shared.COLOR_MANUAL: shared.color,
        shared.COLOR_AUTO_NORMAL: colorsys.hsv_to_rgb(phase.one, 1.0, 1.0),
        shared.COLOR_AUTO_EIGTH: colorsys.hsv_to_rgb(phase.eigth, 1.0, 1.0),
        shared.COLOR_AUTO_FOURTH: colorsys.hsv_to_rgb(phase.fourth, 1.0, 1.0),
        shared.COLOR_AUTO_HALF: colorsys.hsv_to_rgb(phase.half, 1.0, 1.0)
    }[shared.color_mode]

    for i in range(8):
        channel = i * 6
        dmx.set_channel(channel + 2, int(color[0] * 255 * cos[i]))
        dmx.set_channel(channel + 3, int(color[1] * 255 * cos[i]))
        dmx.set_channel(channel + 4, int(color[2] * 255 * cos[i]))
