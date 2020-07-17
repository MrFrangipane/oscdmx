import platform
from oscdmx.app import main


if __name__ == '__main__':
    if platform.architecture() == '64bit':
        main(samplerate=44100)
    else:
        main(samplerate=48000)  # Raspberry -> PiSound
