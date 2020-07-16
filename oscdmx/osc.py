import time


def run(shared):
    last_beat = 0
    previous_last_beat = 0

    clients = list()

    while True:
        # Wait for beat
        while last_beat == previous_last_beat:
            info = shared.get()
            last_beat = info['last_beat']
            time.sleep(0.01)
        previous_last_beat = last_beat

        # Do stuff
        print(shared)
