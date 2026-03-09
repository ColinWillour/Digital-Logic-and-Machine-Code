from myhdl import *

#tag: 291a1b2d23916cdbd649F25

#Number of bits in multiplicand and multiplier.
NUM_BITS = 8

@block 
def RegisterLoad(dout, din, en, load_data, load, clock, reset):
    """ register with enable 

        dout: data out
        din: data in
        en:  write enable
        load: if asserted, load_data will be saved in register
        load_data: data loaded into register when load is asserted

        load_data is aved in register if load = 1
        din is saved in register if load = 0 and en = 1
        Otherwise, dout is not changed
    """

    @always_seq(clock.posedge, reset=reset)
    def logic_seq():
        if load:
            dout.next = load_data
        elif en: 
            dout.next = din

    return logic_seq

@block 
def RegisterShiftLeft(dout, load_data, en, load, clock, reset):
    """ shift left register with load

        register is set to load_data if load is 1
        register is shifted left by 1 if en is 1 and load is 0
        Otherwise, register is not changed.

        The bit shifted in is always 0.

        Note: 
        If load_data is narrower (has fewer bits) than dout, 
        it is 0 extended. 
    """

    @always_seq(clock.posedge, reset=reset)
    def logic_seq():
        if load: 
            dout.next = load_data
        elif en:
            dout.next = (dout << 1)
    return logic_seq

@block 
def RegisterShiftRight(dout, load_data, en, load, clock, reset):
    """ shift right register with load

        register is set to load_data if load is 1
        register is shifted right by 1 if en is 1 and load is 0
        Otherwise, register is not changed.

        The bit shifted in is always 0.
    """

    @always_seq(clock.posedge, reset=reset)
    def logic_seq():
        if load: 
            dout.next = load_data
        elif en:
            dout.next = (dout >> 1)
    return logic_seq

@block
def Adder(s, a, b):
    """
        s = a + b
    """
    @always_comb
    def adder_logic():
        s.next = a + b

    return adder_logic

@block
def Control(done, p_en, s_en, test, load, clock, reset): 
    """ Control module

    Input:
        load:   Load signal to the multiplier. Reset the internal counter.
        test:   Informaton from y to determine the enable signals for registers.

        clock and reset.

    Output:
        done:   Multiplication is done. Determined by a counter.
        p_en:   Write enable for register p
        s_en:   Shift enable for both registers x and y.
    """

    # signals for internal counter
    counter_in = Signal(0)  # input of the counter register
    counter = Signal(0)     # output of the counter

    # counter logic
    @always_seq(clock.posedge, reset=reset)
    def logic_seq():
        counter.next = counter_in

    @always_comb
    def logic_comb():
        if load:
            counter_in.next = 0
            done.next = 0
            p_en.next = 0
            s_en.next = 0
        elif counter == NUM_BITS:
            counter_in.next = counter 
            done.next = 1
            p_en.next = 0
            s_en.next = 0
        else:
            counter_in.next = counter + 1
            done.next = 0
            p_en.next = test
            s_en.next = 1

    return logic_seq, logic_comb

############### Do not change the code above this line

@block
def TestGen(test, y):
    """ Set the test signal (a single bit) going into the control module

    Input:  y, the 8-bit output of register y
    Output: test, the single bit going into the control module
    """

    @always_comb
    def testgen():
        # TODO:
        # We can use the value of individual bits in y like y[0], y[1], ...
        # y[0] means "get the value of bit 0 in y"
        test.next = y[0]

    return testgen

@block
def Mul_ww(p, x_init, y_init, load, done, clock, reset):
    """ Multiplier

    Input:
        x_init, y_init, load, clock, reset

    Output:
        p, done

    p:  the product

        p = x_init * y_init when done is asserted

    x_init: initial value of x, the multiplicand
    y_init: initial value of y, the multiplier

    load:
        1:  load x_init and y_init into x and y registers. Also clear p.
        0:  work mode

    done:
        0: not done
        1: done. result is available in p

    """
    
    W = len(x_init)
    W2 = W + W

    # create signals
    # W2 bits 0's, to be loaded into register p
    w2_0 = Signal(intbv(0)[W2:])      
    adder_out = Signal(modbv(0)[W2:]) # output of adder

    # x and y are the output of registers x and y
    x    = Signal(modbv(0)[W2:]) 
    y    = Signal(modbv(0)[W:])
    # p is one of arguments (ports) of the multiplier
    
    # enable signal for p, x, and y registers
    p_en = Signal(bool(0))  
    shift_en = Signal(bool(0)) # x and y sare the same shift enable signal

    # test signal from register y to the control
    test = Signal(bool(0))

    # Example of instantiating an existing module
    # instantiate register P
    # pay attention to the signals  
    u_reg_p = RegisterLoad(p, adder_out, p_en, w2_0, load, clock, reset)

    # TODO:
    # instantiate x and y registers, control, and adder

    # x_init and y_init are the load_data signal to registers x and y,
    # respectively. To make things easier, we connect x_init to regiser x
    # directly, instead of 0 extending it to a 16-bit signal.

    u_reg_x = RegisterShiftLeft(x, x_init, shift_en, load, clock, reset)
    u_reg_y = RegisterShiftRight(y, y_init, shift_en, load, clock, reset) 
    u_adder = Adder(adder_out, p, x)
    u_control = Control(done, p_en, shift_en, test, load, clock, reset)
    u_testgen = TestGen(test, y)

    ##################################################
    # There is no need to change any lines below. 
    ##################################################
    # Monitor for testing
    # it is not really part of the circuit
    # we place it here to monitor internal signals
    @instance
    def monitor():
        cycle_number = 0
        wl = [3, 4, W2, W2, max(W, 8), 4, 4, 4] 
        fmt_str = ' '.join(["{:"+str(_)+"}" for _ in wl])
        print(fmt_str.format("cnt", "load", "p", "x", 
            "y", "p_en", "s_en", "done"))
        while 1:
            yield clock.posedge
            # wait all signals are updated after positive edge
            yield delay(2) 
            print(fmt_str.format(
                cycle_number, int(load), bin(p, W2), bin(x, W2), bin(y, W), 
                int(p_en), int(shift_en), int(done)))
            cycle_number += 1

    return instances()

