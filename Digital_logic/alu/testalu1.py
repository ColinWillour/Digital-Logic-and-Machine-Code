from myhdl import intbv, delay, instance, StopSimulation, bin
import argparse
from alu1 import *

# testbench itself is a block
@block
def testbench(args):

    # create signals
    result = Signal(bool(0))
    carryout = Signal(bool(0))

    a, b, carryin, binvert = [Signal(bool(0)) for i in range(4)]

    # operation has two bits
    # its underlying data type is integer bit vector (intbv)
    operation = Signal(intbv(0)[2:])

    # instantiating a block
    alu1 = ALU1bit(a, b, carryin, binvert, operation, result, carryout)

    # an ad hoc module for the input
    @instance
    def stimulus():
        print("op a b cin binv | cout res")
        for op in args.op:
            assert 0 <= op <= 3
            for i in range(16):
                # use MyHDL intbv to split bits, instead of shift and AND
                binvert.next, carryin.next, b.next, a.next = intbv(i)[4:]
                operation.next = op
                yield delay(10)
                print("{} {} {} {}   {}    | {}    {}".format(
                    bin(op, 2), 
                    int(a), int(b), int(carryin), int(binvert), 
                    int(carryout), int(result)))

        raise StopSimulation()

    return alu1, stimulus

parser = argparse.ArgumentParser(description='Testing 1-bit ALU. Updated Sep 2025.')
parser.add_argument('op', type=int, nargs='*', 
        default=[2], help='operations')
parser.add_argument('--trace', action='store_true', help='generate trace')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose')

args = parser.parse_args()
if args.verbose:
    print(args)

tb = testbench(args)
tb.config_sim(trace=args.trace)
tb.run_sim()
