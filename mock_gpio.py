from threading import Thread
from queue import Queue
import time, random

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

class pi74HC595:
    def __init__(self,ds,st,sh,daisy=1):
        self.DS=ds
        self.ST=st
        self.SH=sh
        self.daisy=daisy
        self.LED_NUM=self.daisy*4

queue = Queue(10)

class Consumer(Thread):
    def run(self):
        global queue
        while True:
            bit = queue.get()
            queue.task_done()
            print("Consumed one bit from queue [{}]".format(bit))
            time.sleep(random.random())

reg = pi74HC595(11,13,15,1)
Consumer().start()
