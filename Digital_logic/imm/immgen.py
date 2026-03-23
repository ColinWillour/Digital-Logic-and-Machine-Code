from myhdl import block, always_comb, intbv, concat, instances

"""
tag: CAF039043FBCCC351938AS26

The ImmGen module generates the 32-bit imm from an instruction word.  

Supported instruction types:

    opcode      instructions 

    000 0011    I, LW ...
    001 0011    I, ANDI, ORI, ...
    110 0111    I, JALR
    010 0011    S
    110 0011    SB 
    110 1111    UJ, JAL
    011 0111    U, LUI

    See the paragraph at the end of Section 4.3 in textbook for comments about
    generating immediate for R, Load, Store, and branches.

"""

@block
def ImmGen(imm, inst):

    # internal signals
    I, S, SB, U, UJ = [Signal(False) for _ in range(5)]

    @always_comb
    def  generate_instr_type():
        # only use the higher 5 bits in opcode
        # a is inst[6], b is inst[5], and so on
        a, b, c, d, e = inst[7:2]

        # f covers both bit 1 and bit 0
        f = bool(inst[1]) and bool(inst[0])

        # 010 0011    S
        S.next = not a and b and not c and not d and not e and f

        # generate I, SB, UJ, and U below
        # double check how your code sets signal values.
        #       I.next = ...   # not I = 
        #       SB.next = 
        #       UJ.next = 
        #       U.next = 
        # TODO

        # I
        # abc def
        # 000 0011    I, LW ...
        # 001 0011    I, ANDI, ORI, ...
        # 110 0111    I, JALR
        lw = not a and not b and not c and not d and not e and f # 000 0011
        many = not a and not b and c and not d and not e and f # 001 0011
        jalr = a and b and not c and not d and e and f # 110 0111
        I.next = lw or many or jalr
        SB.next = a and b and not c and not d and not e and f # 110 0011
        UJ.next = a and b and not c and d and e and f # 110 1111
        U.next = not a and b and c and not d and e and f # 011 0111

        # 110 0011    SB 

        # 110 1111    UJ, JAL

        # 011 0111    U, LUI

    @always_comb
    def  set_imm31():
        # logic expression for imm[0]
        imm.next[ 0] = I and inst[20] or S and inst[7]

        # generate imm[1] to imm[30]
        # TODO
        imm.next[ 1] = I and inst[21] or S and inst[ 8] or SB and inst[ 8] or UJ and inst[21]
        imm.next[ 2] = I and inst[22] or S and inst[ 9] or SB and inst[ 9] or UJ and inst[22]
        imm.next[ 3] = I and inst[23] or S and inst[10] or SB and inst[10] or UJ and inst[23]
        imm.next[ 4] = I and inst[24] or S and inst[11] or SB and inst[11] or UJ and inst[24] 

        imm.next[ 5] = I and inst[25] or S and inst[25] or SB and inst[25] or UJ and inst[25]
        imm.next[ 6] = I and inst[26] or S and inst[26] or SB and inst[26] or UJ and inst[26]
        imm.next[ 7] = I and inst[27] or S and inst[27] or SB and inst[27] or UJ and inst[27]
        imm.next[ 8] = I and inst[28] or S and inst[28] or SB and inst[28] or UJ and inst[28]
        imm.next[ 9] = I and inst[29] or S and inst[29] or SB and inst[29] or UJ and inst[29]
        imm.next[10] = I and inst[30] or S and inst[30] or SB and inst[30] or UJ and inst[30]

        imm.next[11] = I and inst[31] or S and inst[31] or SB and inst[7] or UJ and inst[20]

        imm.next[12] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[12] or U and inst[12]
        imm.next[13] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[13] or U and inst[13]
        imm.next[14] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[14] or U and inst[14]
        imm.next[15] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[15] or U and inst[15]
        imm.next[16] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[16] or U and inst[16]
        imm.next[17] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[17] or U and inst[17]
        imm.next[18] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[18] or U and inst[18]
        imm.next[19] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[19] or U and inst[19]

#
        imm.next[20] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[20]
        imm.next[21] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[21]
        imm.next[22] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[22]
        imm.next[23] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[23]
        imm.next[24] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[24]
        imm.next[25] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[25]
        imm.next[26] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[26]
        imm.next[27] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[27]
        imm.next[28] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[28]
        imm.next[29] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[29]
        imm.next[30] = I and inst[31] or S and inst[31] or SB and inst[31] or UJ and inst[31] or U and inst[30]
        # imm[31] is always inst[31]
        imm.next[31] = inst[31]

    return instances()

# do not need to change any lines below
@block
def ImmGen0(imm, instruction):
    """Generate imm from instruction.

    Behavior description.
    """

    @always_comb
    def comb_logic():

        # 20 sign bits, all 0 or all 1
        sign20 = intbv(0-instruction[31])[20:]  

        bv32 = intbv(0)[32:]

        opcode = instruction[7:]
        if opcode == 0x23: # S
            bv32 = concat(sign20, instruction[32:25], instruction[12:7])
        elif opcode == 0x63: # SB
            bv32 = concat(sign20, instruction[7], instruction[31:25], 
                          instruction[12:8], bool(0))
        elif opcode == 0x6F: # UJ
            bv32 = concat(sign20[12:], instruction[20:12], instruction[20], 
                          instruction[31:25], instruction[25:21], bool(0))
        elif opcode == 0x37: # U
            bv32 = concat(instruction[32:12], intbv(0)[12:])
        else:  # all other instructions are considered as I type
            # opcode in [0x03, 0x13, 0x67]: # I
            bv32 = concat(sign20, instruction[32:20])

        # set the imm signal
        imm.next = bv32

    return comb_logic

if __name__ == "__main__":
    from myhdl import intbv, delay, instance, Signal, StopSimulation, bin
    import argparse

    # testbench itself is a block
    @block
    def test_comb(args):

        instruction = Signal(intbv(0x33)[32:])
        imm_a = Signal(intbv(0)[32:])
        imm_b = Signal(intbv(0)[32:])

        # instantiating a block
        dut_a = ImmGen0(imm_a, instruction)
        dut_b = ImmGen(imm_b, instruction)

        @instance
        def stimulus():

            for i in args.instruction:
                print(i.lower())

                # set the input
                instruction.next = int(i, 0) 

                # wait
                yield delay(10)

                # compare the results
                print(bin(imm_a, 32))
                print(bin(imm_b, 32))

                if imm_a != imm_b: 
                    s = bin(imm_a ^ imm_b, 32)
                    print(s.replace("0", " ").replace("1", "^"))

            # stop simulation
            raise StopSimulation()

        return dut_a, dut_b, stimulus

    parser = argparse.ArgumentParser(description='Testing ImmGen. Generate imm from instruction words.')
    parser.add_argument('instruction', nargs="+", help='instruction word')
    parser.add_argument('--trace', action='store_true', help='generate trace')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')

    args = parser.parse_args()
    if args.verbose:
        print(args)

    tb = test_comb(args)
    tb.config_sim(trace=args.trace)
    tb.run_sim()
