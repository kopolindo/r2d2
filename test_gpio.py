# test alex
import RPi.GPIO as gpio
import signal,sys,time

class LED(object):
    def __init__(self, pin1: int, pin2: int):
        self.pin1=pin1 # pin anodo sx
        self.pin2=pin2 # pin anodo dx

# define all LEDs
LED1=LED(0,1)
LED2=LED(2,3)
LED3=LED(4,5)
LED4=LED(6,7)

# define signal handler to gracefully exit
def signal_handler(sig, frame):
    gpio.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# set gpio mode and 74HC595 PINs
gpio.setmode(gpio.BOARD)
DS=11
SH=13
ST=15
# initialize board
gpio.setup(DS,gpio.OUT)
gpio.setup(SH,gpio.OUT)
gpio.setup(ST,gpio.OUT)

def clock():
    time.sleep(0.1)
    gpio.output(SH,1)
    time.sleep(0.1)
    gpio.output(SH,0)

def latch():
    time.sleep(0.1)
    gpio.output(ST,1)
    time.sleep(0.1)
    gpio.output(ST,0)

def LED_color(LED,color):
    if color == "RED":
        pin = LED.pin1
    elif color ==  "GREEN":
        pin = LED.pin2
    useful_clocks = pin + 1
    padding_clocks = 8 - useful_clocks
    print("I want {} HIGH, so I need {} clocks".format(pin,useful_clocks))
    for p in range(padding_clocks):
        gpio.output(DS,0)
        clock()
    for i in range(useful_clocks):
        if i == 0:
            gpio.output(DS,1)
        else:
            gpio.output(DS,0)
        clock()

if __name__ == "__main__":
    LED_color(LED4,"RED")
    latch()
    gpio.cleanup()
    """while 1:
        for y in range(8):
            val = 0
            if (y % 2) == 0:
                val = 1
            # value to push and shift
            gpio.output(DS,val)
            time.sleep(0.1)
            # CLOCK: shift val (1-0)
            clock()
            # clear DATA pin
            gpio.output(DS,0)
            # LATCH: output shifted DATA
            latch()

        for y in range(8):
            val = 1
            if (y % 2) == 0:
                val = 0
            # value to push and make shift
            gpio.output(DS,val)
            time.sleep(0.1)
            # CLOCK: shift val (1-0)
            gpio.output(SH,1)
            time.sleep(0.1)
            gpio.output(SH,0)
            # clear DATA pin
            gpio.output(DS,0)
            # LATCH: output shifted DATA
            gpio.output(ST,1)
            time.sleep(0.1)
            gpio.output(ST,0)
        """
