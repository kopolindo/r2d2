from pi74HC595 import pi74HC595
import RPi.GPIO as gpio
from time import sleep
import time, signal, sys, random

class my_register(pi74HC595):
    def set_by_list(self,l=list):
        super(my_register,self).set_by_list(list(reversed(l)))

# define signal handler to gracefully exit
def signal_handler(sig, frame):
    gpio.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

gpio.setmode(gpio.BOARD)
#shift_register = pi74HC595(11,15,13,2)
shift_register = my_register(11,15,13,1)

pause = 0.3
LED_NUM = 8

# input: number of color list you want (eg:4)
# output: list of random colors (eg:[1,0,0,1,0,1,0,1] = red,green,green,green)
def random_color_list(color_num):
    out = []
    for i in range(color_num):
        first=random.randint(0,1)
        out.append(first)
        # if one pin is HIGH the other pin must be LOW
        # otherwise you'll have orange
        out.append(abs(1-first))
    return out

# input: filename path
# output: color list [[1,0,1,0,1,0,1,0],[0,1,1,0,0,1,1,0],...]
def input_from_file(ifile):
    color_list = []
    with open(ifile) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        colors = []
        for c in line:
            if c == "r" or c == "R":
                colors += [1,0]
            elif c == "g" or c == "G":
                colors += [0,1]
        color_list += [colors]
    return color_list

if __name__ == "__main__":
    # I choose to use sys.argv instead of argparse for sake of brevity
    # If there is no file input argument than random color list is used
    if len(sys.argv) == 1:
        while True:
            shift_register.set_by_list(random_color_list(LED_NUM))
            sleep(pause)
        gpio.cleanup()
    # if file input is provided than use that configuration
    else:
        color_list = input_from_file(sys.argv[1])
        while True:
            for c in color_list:
                shift_register.set_by_list(c)
                sleep(pause)
        gpio.cleanup()
