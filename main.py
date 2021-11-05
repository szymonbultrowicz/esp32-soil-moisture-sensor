import machine
from app.updater import updater
from app.wlan import connect


def download_and_install_update_if_available():
    if updater.install_update_if_available():
        print('Rebooting...')
        machine.reset()

def boot():
    connect()
    download_and_install_update_if_available()

    from app import start as app
    app.start()

boot()
