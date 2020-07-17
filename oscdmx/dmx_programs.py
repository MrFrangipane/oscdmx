import math
import colorsys


def rainbow_wave(shared, dmx, phase):
    cos_1 = math.cos(phase.one * 2.0 * math.pi) * 0.5 + 0.5
    cos_2 = math.cos((phase.one + 0.125) * 2.0 * math.pi) * 0.5 + 0.5
    cos_3 = math.cos((phase.one + 0.25) * 2.0 * math.pi) * 0.5 + 0.5
    cos_4 = math.cos((phase.one + 0.375) * 2.0 * math.pi) * 0.5 + 0.5
    cos_5 = math.cos((phase.one + 0.5) * 2.0 * math.pi) * 0.5 + 0.5
    cos_6 = math.cos((phase.one + 0.625) * 2.0 * math.pi) * 0.5 + 0.5
    cos_7 = math.cos((phase.one + 0.75) * 2.0 * math.pi) * 0.5 + 0.5
    cos_8 = math.cos((phase.one + 0.875) * 2.0 * math.pi) * 0.5 + 0.5

    if shared.color_mode == shared.COLOR_MANUAL:
        color = shared.color

    elif shared.color_mode == shared.COLOR_AUTO_NORMAL:
        color = colorsys.hsv_to_rgb(phase.one, 1.0, 1.0)

    elif shared.color_mode == shared.COLOR_AUTO_EIGTH:
        color = colorsys.hsv_to_rgb(phase.eigth, 1.0, 1.0)

    elif shared.color_mode == shared.COLOR_AUTO_FOURTH:
        color = colorsys.hsv_to_rgb(phase.fourth, 1.0, 1.0)

    elif shared.color_mode == shared.COLOR_AUTO_HALF:
        color = colorsys.hsv_to_rgb(phase.half, 1.0, 1.0)

    dmx.set_channel(2, int(color[0] * 255 * cos_1))
    dmx.set_channel(3, int(color[1] * 255 * cos_1))
    dmx.set_channel(4, int(color[2] * 255 * cos_1))

    dmx.set_channel(8, int(color[0] * 255 * cos_2))
    dmx.set_channel(9, int(color[1] * 255 * cos_2))
    dmx.set_channel(10, int(color[2] * 255 * cos_2))

    dmx.set_channel(14, int(color[0] * 255 * cos_3))
    dmx.set_channel(15, int(color[1] * 255 * cos_3))
    dmx.set_channel(16, int(color[2] * 255 * cos_3))

    dmx.set_channel(20, int(color[0] * 255 * cos_4))
    dmx.set_channel(21, int(color[1] * 255 * cos_4))
    dmx.set_channel(22, int(color[2] * 255 * cos_4))

    dmx.set_channel(26, int(color[0] * 255 * cos_5))
    dmx.set_channel(27, int(color[1] * 255 * cos_5))
    dmx.set_channel(28, int(color[2] * 255 * cos_5))

    dmx.set_channel(32, int(color[0] * 255 * cos_6))
    dmx.set_channel(33, int(color[1] * 255 * cos_6))
    dmx.set_channel(34, int(color[2] * 255 * cos_6))

    dmx.set_channel(38, int(color[0] * 255 * cos_7))
    dmx.set_channel(39, int(color[1] * 255 * cos_7))
    dmx.set_channel(40, int(color[2] * 255 * cos_7))

    dmx.set_channel(44, int(color[0] * 255 * cos_8))
    dmx.set_channel(45, int(color[1] * 255 * cos_8))
    dmx.set_channel(46, int(color[2] * 255 * cos_8))
