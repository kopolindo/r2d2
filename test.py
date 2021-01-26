# test alex
from pi74HC595 import pi74HC595
import RPi.GPIO as gpio
import signal,sys,time,random

class LED(object):
    def __init__(self, pin1: int, pin2: int):
        self.pin1=pin1 # pin anodo sx
        self.pin2=pin2 # pin anodo dx

def signal_handler(sig, frame):
    gpio.cleanup()
    sys.exit(0)

def random_LED_color():
    out = []
    first=random.randint(0,1)
    out.append(first)
    out.append(abs(1-first))
    return out

def random_list():
    out = []
    for i in range(4):
        out += random_LED_color()
    return out

signal.signal(signal.SIGINT, signal_handler)
gpio.setmode(gpio.BOARD)
shift_register = pi74HC595(11,13,15)

if __name__ == "__main__":
    while True:
        # all green
        #shift_register.set_by_list([0, 1, 0, 1, 0, 1, 0, 1])
        #time.sleep(0.1)
        # all red
        print("RED")
        shift_register.set_by_list([1, 0, 1, 0, 1, 0, 1, 0])
        time.sleep(1)
        # red,green,green,green
        print("GREEN")
        shift_register.set_by_list([1, 0, 0, 1, 0, 1, 0, 1])
        time.sleep(1)
        """
        shift_register.clear()
        print("First LED green")
        shift_register.set_by_list([1, 0, 0, 0, 0, 0, 0, 0])
        time.sleep(2)
        """
