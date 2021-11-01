import secrets
from app.ota_updater import OTAUpdater

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/szymonbultrowicz/esp32-soil-moisture-sensor', main_dir='app')
    o.install_update_if_available_after_boot(secrets.wifi_ssid, secrets.wifi_password)

def boot():
    download_and_install_update_if_available()
    import app.start

boot()
