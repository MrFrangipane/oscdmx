"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import time
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from DMXEnttecPro import Controller


def int_clamp(value, start=0, end=256):
    return max(start, min(end, int(value)))


class Logic:
    RAINBOW = 0

    def __init__(self, osc):
        self.osc = osc
        self.dmx = Controller('/dev/ttyUSB0', auto_submit=True)
        self.dmx_address = 1
        self.rainbow_value = 0

    def dmx_channel(self, addr, value):
        self.dmx_address = int(value)
        self.osc.set('octostrip/dmx_label', "DMX addr: {}".format(self.dmx_address))

    def rainbow(self, addr, value):
        self.rainbow_value = int(value)
        self.dmx.set_channel(self.dmx_address + self.RAINBOW - 1, self.rainbow_value)


class OSC:
    def __init__(self, ip, port_in, port_out):
        self.logic = Logic(self)
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.set_default_handler(self.handle)
        self.server = osc_server.ThreadingOSCUDPServer((ip, port_in), self.dispatcher)
        self.port_out = port_out
        self.do_mapping()

    def do_mapping(self):
        self.dispatcher.map('/octostrip/dmx_channel', self.logic.dmx_channel)
        self.dispatcher.map('/octostrip/rainbow', self.logic.rainbow)

    def set(self, addr, value):
        client_ip, client_port = self.server.get_request()[1]
        client = udp_client.SimpleUDPClient(client_ip, self.port_out)
        client.send_message(addr, value)

    def handle(self, address, *args):
        print(address, args)

    def serve_forever(self):
        self.server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port-in", type=int, default=8000, help="The port to listen on")
    parser.add_argument("--port-out", type=int, default=9000, help="The port to send to")
    args = parser.parse_args()

    # osc = OSC(args.ip, args.port_in, args.port_out)
    # osc.serve_forever()

    dmx = Controller('/dev/ttyUSB0')
    dmx.set_all_channels(0)
    dmx.submit()

    program = [
        {2: 255, 5: 240},
        {2: 255, 5: 250},
        {2: 255, 5: 230},
        {2: 255, 5: 250},
        {2: 255, 5: 230},
        {2: 255, 5: 250},
        {2: 255, 5: 240},
        {2: 255, 5: 250},
    ]

    program = [
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
        {2: 255, 3: 255, 4: 255,},
    ]

    for i, bar in enumerate(program):
        for ch, v in bar.items():
            dmx.set_channel(i * 6 + ch, v)
            print(i * 6 + ch, v)
    dmx.submit()
