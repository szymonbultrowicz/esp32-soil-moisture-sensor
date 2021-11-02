import machine
import network
import secrets
from app.ota_updater import OTAUpdater

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(secrets.wifi_ssid, secrets.wifi_password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def download_and_install_update_if_available():
    o = OTAUpdater(secrets.github_url, main_dir='app', headers={'Authorization', f'token {secrets.github_token}'})
    if o.install_update_if_available():
        print('Rebooting...')
        machine.reset()

def boot():
    connect()
    download_and_install_update_if_available()
    import app.start

boot()
