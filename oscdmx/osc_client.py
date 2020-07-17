import time
from pythonosc import udp_client


PORT_OUT = 9000


def run(shared, server_ip):
    client = udp_client.SimpleUDPClient(server_ip, PORT_OUT)
    beat_led = 1
    print(server_ip)

    while True:
        now = time.time()

        bpm_label = "BPM : {:.1f}".format(shared.bpm)
        client.send_message('/octostrip/bpm_label', bpm_label)

        if now - shared.last_beat < 0.1:
            client.send_message('/octostrip/bpm_led_a', beat_led)
            client.send_message('/octostrip/bpm_led_b', 1 - beat_led)
            beat_led = 1 - beat_led

        time.sleep(.1)
