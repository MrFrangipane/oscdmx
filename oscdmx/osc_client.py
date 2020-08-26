import time
from pythonosc import udp_client


PORT_OUT = 9000
INTERVAL = 0.1


def run(shared, server_ips):
    clients = [udp_client.SimpleUDPClient(server_ip, PORT_OUT) for server_ip in server_ips]

    while True:
        bpm_label = "BPM : {:.1f}".format(shared.bpm)
        for client in clients:
            client.send_message('/bpm/label', bpm_label)

        time.sleep(INTERVAL)
