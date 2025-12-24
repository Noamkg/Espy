from network import WLAN, STA_IF
from machine import Pin
from time import sleep

NETWORK = "shablool"
PASSWORD = "0542477381"
def connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    led = Pin(2, Pin.OUT)
    if not wlan.isconnected():
        wlan.connect(NETWORK, PASSWORD)
    if wlan.isconnected():
        print("Connected!")
        led.value(1)
        sleep(0.4)
        led.value(0)
    