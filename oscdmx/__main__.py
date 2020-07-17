import platform
from oscdmx.app import main


if __name__ == '__main__':
    if platform.architecture()[0] == '64bit':
        main(samplerate=44100, tablet_ip='192.168.0.10')  # Desktop: Fireface / Freebox router
    else:
        main(samplerate=48000, tablet_ip='192.168.1.101')  # Raspberry: PiSound / Wifi router
