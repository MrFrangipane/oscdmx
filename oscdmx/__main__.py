import platform
from oscdmx.app import main


if __name__ == '__main__':
    if platform.architecture()[0] == '64bit':
        main(samplerate=44100, tablet_ips=['192.168.0.20'])  # Freebox : Galaxy
    else:
        main(samplerate=48000, tablet_ips=['192.168.1.101', '192.168.1.103'])  # TPLink : Galaxy / iPad
