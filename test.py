from time import sleep
import time, signal, sys, random, os
if os.uname().machine == "armv6l":
    from pi74HC595 import pi74HC595
    import RPi.GPIO as gpio

# CONSTANTS
pause = 0.2
LED_NUM = 72
SREG_LED_NUM = 4
DAISY_CHAIN_NUM = int(LED_NUM/SREG_LED_NUM)

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
print(f"daisy chaining {DAISY_CHAIN_NUM} registers")
shift_register = my_register(11,15,13,DAISY_CHAIN_NUM)

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

def matrix_from_file(ifile):
    color_list = []
    matrix = []
    with open(ifile) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        row = []
        for c in line:
            row.append(c)
        matrix.append(row)
    return matrix

def from_color_to_bit(color_list):
    bit_list = []
    for c in color_list:
        if c == "r" or c == "R":
            bit_list.append(1)
            bit_list.append(0)
        elif c == "g" or c == "G":
            bit_list.append(0)
            bit_list.append(1)
        elif c == "0" or c == "o" or c == "O" or c == " ":
            bit_list.append(0)
            bit_list.append(0)
    return bit_list

def matrix_to_list(M):
    out = []
    row_n = len(M)
    col_n = len(M[0])
    for j in range(col_n):
        for i in range(row_n-1,-1,-1):
            out.append(M[i][j])
    return out

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
        matrix = matrix_from_file(sys.argv[1])
        color_list = matrix_to_list(matrix)
        bit_list = from_color_to_bit(color_list)
        while True:
            #for c in color_list:
            shift_register.set_by_list(bit_list)
            sleep(pause)
        gpio.cleanup()
