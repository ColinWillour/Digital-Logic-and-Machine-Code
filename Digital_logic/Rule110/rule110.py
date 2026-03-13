from myhdl import *

#Number of cells
NCELLS = 16 
CELLCHARS = ['.', '*']

@block 
def DFF(q, d, clock, reset):
    """ D flip flop

        q: data out
        d: data in
    """

    @always_seq(clock.posedge, reset=reset)
    def dff_logic():
        q.next = d

    return dff_logic

############### Do not change the code above this line

@block
def NextCellGen(live, l, m, r):
    """ Decide the state of the middle cell in the next generation 

    Input: 
        l, m, r : the current state of cells

    Output:
        live: the state of the middle cell in the next generation
    """

    @always_comb
    def rule110_logic():
        # TODO
        live.next = (not l and not m and r) or (not l and m and not r) or (not l and m and r) or (l and not m and r) or (l and m and not r)


    return rule110_logic


@block
def Rule110_Machine(cells, clock, reset):
    """ Multiplier

    Output:
        cells, a list of 16 one-bit signals.
        Each cell has an initial value after reset is released. 
        cells[15] is the left most cell and cells[0] is the right-most one.
        cells[15], cells[14], ..., cells[1], cells[0]
    """

    # Output signals of NextCellGen blocks 
    # next_cells[0] is not used.
    next_cells = [Signal(bool(0)) for x in range(NCELLS - 1)]

    # TODO
    # It is fine if your code only works for 16 cells.
    # Recall that the right-most cell (cells[0]) and the 
    # left-most cells (cells[15]) do not change.

    # Step 1. 
    # Create 14 NextCellGen nodes.
    # You could use a for loop, but it is not necessary in this assignment
    # u01 = NextCellGen(next_cells[1], ...)
    # u02 = NextCellGen(...
    u01 = NextCellGen(next_cells[ 1], cells[ 2], cells[ 1], cells[ 0])
    u02 = NextCellGen(next_cells[ 2], cells[ 3], cells[ 2], cells[ 1])
    u03 = NextCellGen(next_cells[ 3], cells[ 4], cells[ 3], cells[ 2])
    u04 = NextCellGen(next_cells[ 4], cells[ 5], cells[ 4], cells[ 3])
    u05 = NextCellGen(next_cells[ 5], cells[ 6], cells[ 5], cells[ 4])
    u06 = NextCellGen(next_cells[ 6], cells[ 7], cells[ 6], cells[ 5])
    u07 = NextCellGen(next_cells[ 7], cells[ 8], cells[ 7], cells[ 6])
    u08 = NextCellGen(next_cells[ 8], cells[ 9], cells[ 8], cells[ 7])
    u09 = NextCellGen(next_cells[ 9], cells[10], cells[ 9], cells[ 8])
    u10 = NextCellGen(next_cells[10], cells[11], cells[10], cells[ 9])
    u11 = NextCellGen(next_cells[11], cells[12], cells[11], cells[10])
    u12 = NextCellGen(next_cells[12], cells[13], cells[12], cells[11])
    u13 = NextCellGen(next_cells[13], cells[14], cells[13], cells[12])
    u14 = NextCellGen(next_cells[14], cells[15], cells[14], cells[13])

    # Step 2.
    # instantiate 16 DFFs
    # cells[0] always gets its current value
    # there should be 16 DFFs, for 16 cells.
    dff00 = DFF(cells[ 0], cells[ 0], clock, reset)
    dff01 = DFF(cells[ 1], next_cells[ 1], clock, reset)
    dff02 = DFF(cells[ 2], next_cells[ 2], clock, reset)
    dff03 = DFF(cells[ 3], next_cells[ 3], clock, reset)
    dff04 = DFF(cells[ 4], next_cells[ 4], clock, reset)
    dff05 = DFF(cells[ 5], next_cells[ 5], clock, reset)
    dff06 = DFF(cells[ 6], next_cells[ 6], clock, reset)
    dff07 = DFF(cells[ 7], next_cells[ 7], clock, reset)
    dff08 = DFF(cells[ 8], next_cells[ 8], clock, reset)
    dff09 = DFF(cells[ 9], next_cells[ 9], clock, reset)
    dff10 = DFF(cells[10], next_cells[10], clock, reset)
    dff11 = DFF(cells[11], next_cells[11], clock, reset)
    dff12 = DFF(cells[12], next_cells[12], clock, reset)
    dff13 = DFF(cells[13], next_cells[13], clock, reset)
    dff14 = DFF(cells[14], next_cells[14], clock, reset)
    dff15 = DFF(cells[15], cells[15], clock, reset)


    return instances()

def     print_cells(cycle_number, cells):
    char_list = [ CELLCHARS[int(x)] for x in cells]
    display = ''.join(reversed(char_list))
    print(f"Cycle {cycle_number:2} {display}")

if __name__ == "__main__":
    ACTIVE_LOW, INACTIVE_HIGH = 0, 1

    @block
    def testbench(args):

        # set the initial values of the cells
        # the right-most bit is for cells[0]
        assert len(args.initialvalues) >= 1
        cells = []
        istr = -1
        for i in range(NCELLS): 
            if istr < 0:        # reuse from the right end
                istr = len(args.initialvalues) - 1      
            iv = args.initialvalues[istr] == '1'
            istr -= 1
            cells.append(Signal(iv))

        clock = Signal(bool(0))
        reset = ResetSignal(ACTIVE_LOW, active=0, isasync=True)

        tut = Rule110_Machine(cells, clock, reset)

        HALF_PERIOD = delay(5)

        @always(HALF_PERIOD)
        def clockGen():
            clock.next = not clock

        @instance
        def stimulus():
            # release reset after 1 time unit
            yield delay(1)
            reset.next = INACTIVE_HIGH

            # print the initial values
            yield delay(1)
            print_cells(0, cells)

            for cycle_number in range(1, args.ncycles): 
                # wait for a negative edge to read the output
                yield clock.negedge
                print_cells(cycle_number, cells)

            raise StopSimulation()

        return tut, clockGen, stimulus

    import argparse
    parser = argparse.ArgumentParser(description='Rule 110 cellular automaton.')
    parser.add_argument('ncycles', nargs='?', type=int, default=16, help='number of cycles')
    parser.add_argument('--initialvalues', nargs='?', type=str, default="1001", help='the initial values')
    parser.add_argument('--trace', action='store_true', help='generate trace file')

    args = parser.parse_args()
    tb = testbench(args)
    tb.config_sim(trace=args.trace)
    tb.run_sim()

