import machine
from time import sleep
import lib.ssd1306 as ssd1306

morse_code_dict = {
    'a': '.-',     'b': '-...',   'c': '-.-.',   'd': '-..',
    'e': '.',      'f': '..-.',   'g': '--.',    'h': '....',
    'i': '..',     'j': '.---',   'k': '-.-',    'l': '.-..',
    'm': '--',     'n': '-.',     'o': '---',    'p': '.--.',
    'q': '--.-',   'r': '.-.',    's': '...',    't': '-',
    'u': '..-',    'v': '...-',   'w': '.--',    'x': '-..-',
    'y': '-.--',   'z': '--..'
}
def morse_decoder(message):


    led = machine.Pin(2, machine.Pin.OUT)
    for charachter in message: 
        code = morse_code_dict[charachter.lower()]
        for symbol in code:
            led.value(1)
            sleep(0.05) if symbol == "." else sleep(0.2)
            led.value(0)
            sleep(0.2)
        sleep(0.2)