## test alex
from pi74HC595 import pi74HC595
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
shift_register = pi74HC595(11,13,15)

if __name__ == "__main__":
    while True:
        shift_register.set_by_list([0, 1, 0, 1, 0, 1, 0, 1])
        shift_register.set_by_list([1, 0, 1, 0, 1, 0, 1, 0])
