from threading import Thread
from queue import Queue
from collections import deque
import time, random, signal, sys

"""
      __ __
Q1  -|  ^  |- Q0
Q2  -|     |- VCC
Q3  -|     |- DS [11]
Q4  -|     |- OE (Low Active)
Q5  -|     |- SH_CP (Clock) [15]
Q6  -|     |- ST_CP (Latch) [13]
Q7  -|     |- Master
GND -|_____|- Q7'

"""

GREEN = '\u001b[32m'
RED = '\u001b[31m'
ORANGE ='\033[38;2;255;165;0m'
RESET = '\u001b[0m'
queue = Queue(10)

# define signal handler to gracefully exit
def signal_handler(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class pi74HC595:
    bit_list = [0,0,0,0,0,0,0,0]
    def __init__(self,ds,st,sh,daisy=1):
        self.DS=ds
        self.ST=st
        self.SH=sh
        self.daisy=daisy
        self.LED_NUM=self.daisy*4
    def set_by_list(self,l):
       self.bit_list = l

class Producer(Thread):
    def run(self):
        global queue
        while True:
            # List of 8 bits. [(1,0)=RED, (0,1)=GREEN]
            bit_list = deque(random_color_list(4)) 
            bit = bit_list[0] 
            bit_list.rotate(-1)
            queue.put(bit)
            #print(f"Enqueued {bit}, remaining bit_list = {bit_list}")
            time.sleep(0.02)

def random_color_list(color_num):
    out = []
    for i in range(color_num):
        first=random.randint(0,1)
        out.append(first)
        # if one pin is HIGH the other pin must be LOW
        # otherwise you'll have orange
        out.append(abs(1-first))
    return out
class Consumer(Thread):
    reg = pi74HC595(11,13,15,4)
    clock_time = 0.02
    bit_counter = 0
    total_pin = reg.LED_NUM*2
    bit_list = []
    LED_list = []
    def print_LED(self):
        iterable_bit_list = iter(self.reg.bit_list)
        for pin1,pin2 in zip(iterable_bit_list,iterable_bit_list):
            if pin1 and not pin2:
                self.LED_list.append(f"[{RED}∅{RESET}]")
            if pin2 and not pin1:
                self.LED_list.append(f"[{GREEN}∅{RESET}]")
            if not pin1 and not pin2:
                self.LED_list.append("[∅]")
            if pin1 and pin2:
                self.LED_list.append(f"[{ORANGE}∅{RESET}]")
        for LED in self.LED_list:
            print(LED,end='')
        #print()
        print('',end='\r')
        self.LED_list = []
    def clock(self):
        time.sleep(self.clock_time)
    def latch(self):
        self.reg.set_by_list(self.bit_list)
        self.bit_counter = 0
        self.bit_list = []
    def run(self):
        global queue
        while True:
            bit = queue.get()
            self.bit_list.append(bit)
            queue.task_done()
            #print("Consumed one bit from queue [{}]".format(bit))
            self.clock()
            self.bit_counter+=1
            #print(f"counter = {self.bit_counter}")
            if self.bit_counter == self.total_pin:
                self.latch()
                self.print_LED()

if __name__ == "__main__":
    Producer().start()
    Consumer().start()
