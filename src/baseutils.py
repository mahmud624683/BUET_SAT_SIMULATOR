from monosat import *
import converts
import time
import math

LOGIC_VALUE_ZERO = "0"
LOGIC_VALUE_ONE = "1"

PRIMARY_INPUT = "pin"
PRIMARY_OUTPUT = "pout"
KEY_INPUT = "kin"
INTERMEDIATE_WIRE = "inwire"



def finddip(pinwires, keywires, interwires, poutwires, list_dip, list_orgcirc, keyin1, keyin2, exe_time):

    discinp = [None] * len(pinwires)

    outxored_right = [None] * len(poutwires)

    if list_dip:
        iter = len(list_dip)
    else:
        iter = 0

    outxnored_left = []

    dip_list = []

    for i in range(0, len(pinwires)):
        discinp[i] = Var()
        discinp[i].symbol = pinwires[i].name + "_" + str(iter)

    output_list1 = converts.circuit2bool(interwires, poutwires, discinp, keyin1)
    output_list2 = converts.circuit2bool(interwires, poutwires, discinp, keyin2)

    if list_dip:
        print("============================================= iteration: {}".format(len(list_dip)))

        output_list_temp1 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin1)
        output_list_temp2 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin2)

        for j in range(0, len(output_list_temp1)):
            outxnored_left.append(Xnor(output_list_temp1[j], list_orgcirc[len(list_dip) - 1][j]))
            outxnored_left.append(Xnor(output_list_temp2[j], list_orgcirc[len(list_dip) - 1][j]))

        for i in range(0, len(list_dip)):
            for j in range(0, len(list_dip[i])):
                if str(list_dip[i][j].value()) == "True":
                    Assert(list_dip[i][j])
                elif str(list_dip[i][j].value()) == "False":
                    Assert(Not(list_dip[i][j]))

        Assert(And(outxnored_left))

    else:
        print("============================================= iteration: {}".format(0))
        left_codition = Var(true())
        dip_assert = Var(true())

    for i in range(0, len(poutwires)):
        outxored_right[i] = Xor(output_list1[i], output_list2[i]) #different outputs
        
    new_time = time.time()
    result = Solve(Or(outxored_right))  
    new_time = time.time() - new_time
    

    if result:
        #print("SAT")
        return 1, discinp, new_time+exe_time
    else:
        #print("UNSAT")
        return -1, discinp, new_time+exe_time


def double_dip(pinwires, keywires, interwires, poutwires, list_dip, list_orgcirc, keyin1, keyin2, keyin3, keyin4, exe_time):

    discinp = [None] * len(pinwires)

    outxored_right1 = [None] * len(poutwires)
    outxored_right2 = [None] * len(poutwires)
    outxored_right3 = [None] * len(poutwires)
    outxored_right4 = [None] * len(poutwires)

    outxnored_right1 = [None] * len(poutwires)
    outxnored_right2 = [None] * len(poutwires)

    key_xored = [None] * len(keywires)

    if list_dip:
        iter = len(list_dip)
    else:
        iter = 0

    outxnored_left = []

    dip_list = []

    for i in range(0, len(pinwires)):
        discinp[i] = Var()
        discinp[i].symbol = pinwires[i].name + "_" + str(iter)

    output_list1 = converts.circuit2bool(interwires, poutwires, discinp, keyin1)
    output_list2 = converts.circuit2bool(interwires, poutwires, discinp, keyin2)
    output_list3 = converts.circuit2bool(interwires, poutwires, discinp, keyin3)
    output_list4 = converts.circuit2bool(interwires, poutwires, discinp, keyin4)

    if list_dip:
        print("============================================= iteration: {}".format(len(list_dip)))

        output_list_temp1 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin1)
        output_list_temp2 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin2)
        output_list_temp3 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin3)
        output_list_temp4 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin4)

        for j in range(0, len(output_list_temp1)):
            outxnored_left.append(Xnor(output_list_temp1[j], list_orgcirc[len(list_dip) - 1][j]))
            outxnored_left.append(Xnor(output_list_temp2[j], list_orgcirc[len(list_dip) - 1][j]))
            outxnored_left.append(Xnor(output_list_temp3[j], list_orgcirc[len(list_dip) - 1][j]))
            outxnored_left.append(Xnor(output_list_temp4[j], list_orgcirc[len(list_dip) - 1][j]))

        for i in range(0, len(list_dip)):
            for j in range(0, len(list_dip[i])):
                if str(list_dip[i][j].value()) == "True":
                    Assert(list_dip[i][j])
                elif str(list_dip[i][j].value()) == "False":
                    Assert(Not(list_dip[i][j]))

        Assert(And(outxnored_left))

    else:
        print("============================================= iteration: {}".format(0))
        left_codition = Var(true())
        dip_assert = Var(true())

    for i in range(0, len(poutwires)):
        outxnored_right1[i] = Xnor(output_list1[i], output_list3[i]) #different outputs
        outxnored_right2[i] = Xnor(output_list2[i], output_list4[i]) #different outputs
        
        outxored_right1[i] = Xor(output_list1[i], output_list2[i]) #different outputs
        
        outxored_right2[i] = Xor(output_list1[i], output_list4[i])  # different outputs
        
        outxored_right3[i] = Xor(output_list2[i], output_list3[i])  # different outputs
        
        outxored_right4[i] = Xor(output_list3[i], output_list4[i])  # different outputs
        
    for i in range(0, len(keywires)):
        key_xored[i] = Xor(keyin1[i], keyin2[i], keyin3[i], keyin4[i])


    new_time = time.time()
    result = Solve(And(And(outxnored_right1), And(outxnored_right2), Or(outxored_right1), Or(outxored_right2), Or(outxored_right3), Or(outxored_right4), Or(key_xored)))  # Solve the instance in MonoSAT, return either True if the instance is SAT, and False if it is UNSAT
    new_time = time.time() - new_time

    if result:
        #print("SAT")
        return 1, discinp, new_time+exe_time
    else:
        #print("UNSAT")
        return -1, discinp, new_time+exe_time


def findkey(keyin_wires, interwires, poutwires, list_dip, list_orgcirc, keyinc):

    keyin = [None] * len(keyin_wires)

    outxnored = []

    for i in range(0, len(keyin_wires)):
        keyin[i] = Var()
        keyin[i].symbol = keyinc[i].symbol

    for i in range(0, len(list_dip)):

        output_list_temp = converts.circuit2bool(interwires, poutwires, list_dip[i], keyin)

        for j in range(0, len(poutwires)):
            outxnored.append(Xnor(output_list_temp[j], list_orgcirc[i][j]))

    keyfinding = And(outxnored)

    # result, intr = Solve(keyfinding)  # Solve the instance in MonoSAT, return either True if the instance is SAT, and False if it is UNSAT
    result = Solve(keyfinding)
    
    for i in range(0, len(keyin_wires)):
        keyin[i].symbol = keyinc[i].symbol

    if result:
        #print("SAT")
        return 1,keyin
    else:
        #print("UNSAT")
        return 0,None

def int2var(int_val,len_val):
    var_list=[]
    bin_val = converts.int2bin(int_val,len_val)
    for bit in bin_val:
        if bit == "0":
            var_list.append(Var(false()))
        else:
            var_list.append(Var(true()))
    return var_list


def findkey_list(keyin_wires, interwires, poutwires, list_dip, list_orgcirc, keyinc, list_keys):

    keyin = [None] * len(keyin_wires)
    loop_len = int(math.pow(2,len(keyin)))
    for i in range(loop_len):
        bin_val = converts.int2bin(i,len(keyin))
        outxnored = []
        for i in range(0, len(keyin)):
            if bin_val[i] == "0":
                keyin[i] = Var(false())
            else:
                keyin[i] = Var(true())
            keyin[i].symbol = keyinc[i].symbol

        for i in range(0, len(list_dip)):

            output_list_temp = converts.circuit2bool(interwires, poutwires, list_dip[i], keyin)

            for j in range(0, len(poutwires)):
                outxnored.append(Xnor(output_list_temp[j], list_orgcirc[i][j]))

        keyfinding = And(outxnored)

        # result, intr = Solve(keyfinding)  # Solve the instance in MonoSAT, return either True if the instance is SAT, and False if it is UNSAT
        result = Solve(keyfinding)
        
        for i in range(0, len(keyin_wires)):
            keyin[i].symbol = keyinc[i].symbol

        if result:
            #print("SAT")
            return keyin

    return None
        


def finddipham(pinwires, keywires, interwires, poutwires, list_dip, list_orgcirc, keyin1, keyin2, exe_time, interval, timeout_array, const_solve):

    discinp = [None] * len(pinwires)

    outxored_right = [None] * len(poutwires)

    bit_intval = [None] * len(poutwires)
    minham_conditions = [None] * 2 * len(poutwires)

    hamming_threshold_low = BitVector(len(poutwires))
    hamming_threshold_up = BitVector(len(poutwires))
    hammming_val = BitVector(len(poutwires))

    for i in range(0, len(poutwires)):
        bit_intval[i] = BitVector(len(poutwires))

    Assert(hamming_threshold_low < interval + 1)
    Assert(hamming_threshold_low > interval - 1)

    Assert(hamming_threshold_up < len(poutwires) + 1)
    Assert(hamming_threshold_up > len(poutwires) - 1)

    if list_dip:
        iter = len(list_dip)
    else:
        iter = 0

    outxnored_left = []

    dip_list = []

    for i in range(0, len(pinwires)):
        discinp[i] = Var()
        discinp[i].symbol = pinwires[i].name + "_" + str(iter)

    output_list1 = converts.circuit2bool(interwires, poutwires, discinp, keyin1)
    output_list2 = converts.circuit2bool(interwires, poutwires, discinp, keyin2)

    if list_dip:
        print("============================================= iteration: {}".format(len(list_dip)))

        output_list_temp1 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin1)
        output_list_temp2 = converts.circuit2bool(interwires, poutwires, list_dip[len(list_dip) - 1], keyin2)

        for j in range(0, len(output_list_temp1)):
            outxnored_left.append(Xnor(output_list_temp1[j], list_orgcirc[len(list_dip) - 1][j]))
            outxnored_left.append(Xnor(output_list_temp2[j], list_orgcirc[len(list_dip) - 1][j]))

        for i in range(0, len(list_dip)):
            for j in range(0, len(list_dip[i])):
                if str(list_dip[i][j].value()) == "True":
                    Assert(list_dip[i][j])
                elif str(list_dip[i][j].value()) == "False":
                    Assert(Not(list_dip[i][j]))

        Assert(And(outxnored_left))
        

    else:
        print("============================================= iteration: {}".format(0))
        left_codition = Var(true())
        dip_assert = Var(true())



    for i in range(0, len(poutwires)):
        outxored_right[i] = Xor(output_list1[i], output_list2[i]) #different outputs
        minham_conditions[2*i] = Implies(outxored_right[i], bit_intval[i] == 1)
        minham_conditions[2*i+1] = Implies(Not(outxored_right[i]), bit_intval[i] == 0)
    for i in range(0, len(poutwires)):
        if i == 0:
            hammming_val = bit_intval[i]
        else:
            hammming_val += bit_intval[i]

    upper_condition = (hammming_val >= hamming_threshold_low)
    lower_condition = (hammming_val <= hamming_threshold_up)

    current_timeout = int(math.ceil(sum(list(timeout_array)) / len(list(timeout_array))))
    
    new_time = time.time()
    result = Solve(And(Or(outxored_right), upper_condition, lower_condition, And(minham_conditions)),
                        time_limit_seconds=5,
                        conflict_limit=50000) 
    new_time = time.time() - new_time

    if result:

        if const_solve:
            if int(hammming_val.value()) == const_solve[0]:
                const_solve.append(int(hammming_val.value()))
            else:
                const_solve = []
        else:
            const_solve.append(int(hammming_val.value()))

        #print("SAT")
        return 1, discinp, new_time+exe_time, interval, timeout_array, const_solve
    else:
        #print("UNSAT")
        return -1, discinp, new_time+exe_time, interval, timeout_array, const_solve






