import time
from pythonosc import udp_client


PORT_OUT = 9000
INTERVAL = 0.1


def run(shared, server_ip):
    client = udp_client.SimpleUDPClient(server_ip, PORT_OUT)
    beat_led = 1

    while True:
        now = time.time()

        bpm_label = "BPM : {:.1f}".format(shared.bpm)
        client.send_message('/bpm/label', bpm_label)

        bpm_confidence = "CONFIDENCE : {:.2f}".format(shared.confidence)
        client.send_message('/bpm/confidence', bpm_confidence)

        if now - shared.last_beat < INTERVAL:
            client.send_message('/bpm/led_a', beat_led)
            client.send_message('/bpm/led_b', 1 - beat_led)
            beat_led = 1 - beat_led

        time.sleep(INTERVAL)
