import secrets
import time
import machine
import network

def connect():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(secrets.wifi_ssid, secrets.wifi_password)
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())
    except OSError:
        print('[FATAl] Cannot connect to WiFi')
        time.sleep(10)
        machine.reset()
