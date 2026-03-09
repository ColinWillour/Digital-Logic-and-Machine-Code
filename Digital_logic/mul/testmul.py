from myhdl import *
from mul import * 

ACTIVE_LOW, INACTIVE_HIGH = 0, 1

@block
def testbench(num_lists):
    n = NUM_BITS
    n2 = n + n

    multiplicand = Signal(intbv(0)[n:])
    multiplier = Signal(intbv(0)[n:])
    product = Signal(intbv(0)[n2:])
    load = Signal(bool(1))
    done = Signal(bool(0))

    clock   = Signal(bool(0))
    reset = ResetSignal(ACTIVE_LOW, active=0, isasync=True)

    tut = Mul_ww(product, multiplicand, multiplier, load, done, clock, reset)

    HALF_PERIOD = delay(10)

    @always(HALF_PERIOD)
    def clockGen():
        clock.next = not clock

    @instance
    def stimulus():

        # all input changes happen after the negative edge
        # yield clock.negedge

        # release reset
        reset.next = INACTIVE_HIGH

        # delay for signals to become stable after clock edge
        delayp = delay(3)

        for (x, y) in [ (num_lists[i], num_lists[i+1]) for i in range(0, len(num_lists) - 1) ]: 
            # specify the initial values
            # the output is formatted for 8-bit numbers
            multiplicand.next = x
            multiplier.next = y
            load.next = 1
            # wait for the rising edge of the clock  
            yield clock.posedge
            # wait a little to release load
            yield delayp
            load.next = 0

            # just wait until it's done
            while not done:
                yield clock.posedge
                yield delayp        # it takes a while for done to set

            # additional clock for checking
            yield clock.posedge     
            yield delayp

            # check if the result is correct
            if x * y != product:
                print("Error:p!={}".format(bin(x * y, n2)))
            print("{}*{}={}".format(x, y, int(product)))

        raise StopSimulation()

    return tut, clockGen, stimulus

import argparse
parser = argparse.ArgumentParser(description='Multiplier. Revised in Oct 2025.')
parser.add_argument('numbers', nargs='*', type=int, default=[255, 255], help='List of numbers')
parser.add_argument('--trace', action='store_true', help='generate trace file')

args = parser.parse_args()
if len(args.numbers) <= 1:
    print("Error: specify at least two numbers.")
    exit(1)

tb = testbench(args.numbers)
tb.config_sim(trace=args.trace)
tb.run_sim()
