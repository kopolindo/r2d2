# test alex
import RPi.GPIO as gpio
import signal,sys,time,random

# define signal handler to gracefully exit
def signal_handler(sig, frame):
    gpio.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# define ANODE number (my LEDs have two anodes and one common cathode)
ANODE_NUM=2
# set gpio mode and 74HC595 PINs
gpio.setmode(gpio.BOARD)
DS=11
SH=13
ST=15
# initialize board
gpio.setup(DS,gpio.OUT)
gpio.setup(SH,gpio.OUT)
gpio.setup(ST,gpio.OUT)

# define time to sleep
pause = 0.003

# input: none
# output: none
# it just provides a rising edge for the ST_CP pin (clock)
def tick():
    time.sleep(pause)
    gpio.output(SH,1)
    time.sleep(pause)
    gpio.output(SH,0)

# input: none
# output: none
# it just provides a rising edge for the SH_CP pin (latch)
def latch():
    time.sleep(pause)
    gpio.output(ST,1)
    time.sleep(pause)
    gpio.output(ST,0)

# input: none
# output: none
# it is just an alias, syntactic sugar
def push_bit(bit):
    gpio.output(DS,bit)

# input: list of bits (HIGH/LOW) (eg: [1,0,1,0,0,1,0,1] = red,red,green,green)
# output: none
# it pushes vbits (HIHG/LOW) to the shift register and outputs them
def set_list(l):
    # must be reversed, you push and shift, push and shift, etc
    for bit in reversed(l):
        # for every bit pushed...
        push_bit(bit)
        # ...one clock (rising edge) to memorize it
        tick()
    # at last a rising edge on the latch pin will output serialized values
    latch()

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
            set_list(random_color_list(4))
        gpio.cleanup()
    # if file input is provided than use that configuration
    else:
        color_list = input_from_file(sys.argv[1])
        while True:
            for c in color_list:
                set_list(c)
        gpio.cleanup()
