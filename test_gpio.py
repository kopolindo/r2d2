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
def tick():
    time.sleep(pause)
    gpio.output(SH,1)
    time.sleep(pause)
    gpio.output(SH,0)

def latch():
    time.sleep(pause)
    gpio.output(ST,1)
    time.sleep(pause)
    gpio.output(ST,0)

def push_bit(bit):
    gpio.output(DS,bit)

def set_list(l):
    for bit in reversed(l):
        push_bit(bit)
        tick()
    latch()

def random_color_list(color_num):
    out = []
    for i in range(color_num):
        first=random.randint(0,1)
        out.append(first)
        out.append(abs(1-first))
    return out

if __name__ == "__main__":
    color_list = []
    with open(sys.argv[1]) as f:
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
    while True:
        set_list(random_color_list(4))
    # for i in range(0,len(color_list)):
    #     #print("Line {} is bit list {}".format(content[i],color_list[i]))
    #     set_list(color_list[i])
    gpio.cleanup()
