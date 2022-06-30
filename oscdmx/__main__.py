import sys

from oscdmx.app import main


if __name__ == '__main__':

    verbose = "--verbose" in sys.argv or '-v' in sys.argv

    main(
        server_host='0.0.0.0',
        server_port=8000,
        verbose=verbose
    )
