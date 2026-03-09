from myhdl import Signal, block, always_comb, instances

#tag: f03eb9870a35b37dfa50s26

@block
def Not(c, a):
    """ Not gate

        c = not a

        a --|>o-- c
    """
    @always_comb
    def comb_logic():
        # generate the output with a logical expression
        c.next = not a

    return comb_logic

@block
def And2(c, a, b):
    """ 2-input AND gate

        c = a and b

        a -->|```.
             |    :--> c
        b -->|..-`
    """

    @always_comb
    def comb_logic():
        # generate the output with a logical expression
        c.next = a and b

    return comb_logic


@block
def Or2(c, a, b):
    """ 2-input OR gate

    c = a or b

    """
#    a -->\\--.
#          |   :--> c
#    b -->//..-`

    @always_comb
    def comb_logic():
        # TODO
        # generate the output with a logical expression
        c.next = a or b

    return comb_logic

@block
def Mux2(c, a, b, s):
    """ 2-1 Multiplexor.

    c -- mux output
    a, b -- data inputs
    s -- control input: select b if s is asserted, otherwise a

           s
           |
           v
          +-+
    a -->| 0 |
         |   |--> c
    b -->| 1 |
          +-+
    """

    @always_comb
    def mux_logic():
        # TODO
        # generate the output with a logical expression
        # do not use if-else
        c.next = (s and b) or (not s and a)

    return mux_logic

@block
def Mux2_gates(c, a, b, s):
    """ 2-1 Multiplexor.

    We build this variant with logical gates (instead of logical epxressions) to
    demonstrate how to build hierarchal blocks (blocks made of other blocks).

    c -- mux output
    a, b -- data inputs
    s -- control input: select b if s is asserted, otherwise a


       s
       |
       *----------->|``-.  and1
       |            |    :------+
    a -+----------->|..-`       |
                                +--->\\--.
       |                              |   :--> c
       |      nots              +--->//..-`
       +--|>o------>|``-.  and2 |
                    |    :------+
    b ------------->|..-`

    """

     # internal signals
    nots = Signal(bool(0))
    and1 = Signal(bool(0))
    and2 = Signal(bool(0))


    # Instances of gates (variable names, e.g. "u_not", do not really matter)
    u_not = Not(nots, s)
    u_and1 = And2(and1, s, a)
    u_and2 = And2(and2, nots, b)
    u_or = Or2(c, and1, and2)

    # return all instances created above
    return instances()


@block
def Mux4(z, a, b, c, d, s):
    """ 4-1 Multiplexor.

    z: mux output

    a, b, c, d: data inputs. Single bits.

    s: select signal. Two bits.
       0 for a, 1 for b, 2 for c, and 3 for d

          +-- s1
          |
          | +--s0
          v v
          +--+
    a -->| 00 |
         |    |
    b -->| 01 |
         |    |--> z
    c -->| 10 |
         |    |
    d -->| 11 |
          +--+
    """

    @always_comb
    def mux_logic():
        # TODO

        # Generate z from a, b, c, d and s

        # copy values to s1 and s0, which are easier to type
        # in your expression
        s1, s0 = s[1], s[0]
        z.next = ((not s1 and not s0 and a) or
                  (not s1 and     s0 and b) or
                  (    s1 and not s0 and c) or
                  (    s1 and     s0 and d))

    return mux_logic

@block
def Adder1bit(a, b, carryin, carryout, s):
    """ 1-bit adder
    Input:
        a, b, and carryin.

    Output:
        s:  sum
        carryout: carryout


             +--- carryin
             v
         +-------+
    a -->|       |
         |   +   | --> s
    b -->|       |
         +-------+
             |
             +---> carryout
    """

    @always_comb
    def comb_adder():
        # TODO
        # Generate s and carryout from a, b, and carryin
        # The lecture slides have the logical expressions.
        # They are short enough so we use one line for adder_sum and
        # one line for carryout. Remember ".next".
        # For example,
        # s.next =
        # carryout.out =
        s.next = a ^ b ^ carryin
        carryout.next = ((a and b) or (a and carryin) or (b and carryin))

    return comb_adder

@block
def ALU1bit(a, b, carryin, binvert, operation, result, carryout):

    """ 1-bit ALU

    Output:
        result and carryout

    Input:
        a, b, carryin, binvert, and operation

    operation has two bits. All other signals have only 1 bit.


         +-- carryin
         |
         | +-- binvert
         | |
         | | +-- operation
         v v v
         +---+
         |    \\
    a--> |     \\
         |      \\
         \\       |
          \\      |
            >     |--> result
          //      |
         //       |
         |      //
    b--> |     //
         |    //
         +---+
           |
           +--> carryout

    """

    # internal signals
    notb = Signal(bool(0))
    signal0 = Signal(bool(0))   # always 0

    # TODO
    # Create signals

    # For example, we create the signal `notb`, which is the output of the NOT gate
    # (already created above)

    # We need to create all the signals in the diagram
    # e.g., the output of 2-1 mux, the output of the AND gate, and so on
    inputb = Signal(bool(0))
    andb = Signal(bool(0))
    orb = Signal(bool(0))
    sumb = Signal(bool(0))

    # instantiating gates/blocks
    # here is an example to place the NOT gate
    u_not = Not(notb, b)

    # the name u_not is not critical.
    # you can name them u_not, u_mux2, and so on,
    # or just u1, u2, u3, ...

    # continue to instantiate other gates/modules
    # like 2-1 MUX and AND
    u_mux2 = Mux2(inputb, b, notb, binvert)
    u_and = And2(andb, a, inputb)
    u_or = Or2(orb, a, inputb)
    u_add = Adder1bit(a, inputb, carryin, carryout, sumb)
    u_op = Mux4(result, andb, orb, sumb, signal0, operation)

    ##########################################
    # No need to change the lines below

    # return all the functions/submodules
    # we could list them explicitly, like u_not, u1, u2, and so on
    return instances()

