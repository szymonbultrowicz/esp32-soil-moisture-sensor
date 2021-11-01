# main.py

import json
from time import sleep, sleep_ms
import network
from machine import ADC, Pin
from app.mqtt_robust import MQTTClient
from ubinascii import hexlify
import secrets

MIN_READING = 1150
MAX_READING = 3100

device_id = f'esp32-{hexlify(network.WLAN().config("mac")).decode()}'

class Sensor:
    def __init__(self, hass_id, sense_pin_no, power_pin_no):
        self.id = hass_id
        self.sense_pin = ADC(Pin(sense_pin_no))
        self.sense_pin.atten(ADC.ATTN_11DB)
        self.power_pin = Pin(power_pin_no, Pin.OUT, value=0)

    def read(self):
        self.power_pin.on()
        sleep_ms(50)
        reading = self.sense_pin.read()
        self.power_pin.off()
        return reading

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(secrets.wifi_ssid, secrets.wifi_password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def connect_mqtt():
    client = MQTTClient(device_id, secrets.mqtt_broker_addr)
    client.connect()
    return client

def send_reading(client, flower_id, moisture):
    msg = json.dumps({
        "soil_moisture": moisture
    })
    topic = f'homeassistant/sensor/flower-{flower_id}/state'
    print(f'Sending reading to MQTT topic {topic}: {msg}')
    client.publish(topic, msg)

def start():
    do_connect()

    sensors = [Sensor('USWSWTT4UK', 36, 13)]
    mqtt_client = connect_mqtt()

    print(device_id)

    while True:
        for sensor in sensors:
            moisture_reading = sensor.read()
            moisture_percentage = round(convert(moisture_reading, MIN_READING, MAX_READING, 100, 0))
            print(f'{sensor.id}: {moisture_reading} {str(moisture_percentage)}%')
            if mqtt_client is not None:
                send_reading(mqtt_client, sensor.id, max(moisture_percentage, 0))
            else:
                print("MQTT client empty - skipping")
        sleep(5)

start()
