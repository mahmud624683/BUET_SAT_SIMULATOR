import sys 
from monosat import *
import logicwire
import baseutils
from collections import deque
import random
import math 

import re, os
import converts



def get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time,print_str):
    #print("---------------- looking for key (Last SAT Call) ------------")
    new_list_dips = Var(true())
    for i in range(0, len(list_str_dip)):
        for j in range(0, len(list_str_dip[i])):
            if list_str_dip[i][j] == "1":
                list_dip[i][j] = Var(true())
                Solve(list_dip[i][j])
            elif list_str_dip[i][j] == "0":
                list_dip[i][j] = Var(false())
                Solve(Not(list_dip[i][j]))
            new_list_dips = And(new_list_dips, list_dip[i][j])
    status, found_keys = baseutils.findkey(obfkeywires, obfinterwires, obfpoutwires, list_dip, list_orgcirc, keyinc)

    if status==1:
        combined_key = [None] * len(found_keys)
        for i in range(0, len(found_keys)):
            key_name = found_keys[i].getSymbol()
            key_index = int(key_name[key_name.find("keyinput") + 8: key_name.find("c")])
            combined_key[key_index] = str(found_keys[i].value())

        correct_key = [None] * len(combined_key)
        for i in range(0, len(combined_key)):
            if combined_key[i] == "True":
                correct_key[i] = "1"
            else:
                correct_key[i] = "0"
        return print_str+"key= {}; func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}\n".format(''.join(correct_key),iter, exe_func_time, exe_non_func_time)

    else:
        return print_str +"Didn't Found Any Satisfiable Key\n"


def init_attack(orig_bench_address,obf_bench_address):
    orgwires, orgpinwires, orgkeywires, orginterwires, orgpoutwires = logicwire.wire_dep(orig_bench_address)
    obfwires, obfpinwires, obfkeywires, obfinterwires, obfpoutwires = logicwire.wire_dep(obf_bench_address)

    str_dip = [None] * len(obfpinwires)
    keyin1 = [None] * len(obfkeywires)
    keyin2 = [None] * len(obfkeywires)
    keyin3 = [None] * len(obfkeywires)
    keyin4 = [None] * len(obfkeywires)
    keyinc = [None] * len(obfkeywires)

    for i in range(0, len(obfkeywires)):
        keyin1[i] = Var()
        keyin1[i].symbol = obfkeywires[i].name + "_1" + str(iter)

        keyin2[i] = Var()
        keyin2[i].symbol = obfkeywires[i].name + "_2" + str(iter)

        keyin3[i] = Var()
        keyin3[i].symbol = obfkeywires[i].name + "_3" + str(iter)

        keyin4[i] = Var()
        keyin4[i].symbol = obfkeywires[i].name + "_4" + str(iter)

        keyinc[i] = Var()
        keyinc[i].symbol = obfkeywires[i].name + "c"

    return obfpinwires, obfkeywires, obfinterwires, obfpoutwires, orgpoutwires, orgwires, str_dip, keyin1, keyin2, keyin3, keyin4, keyinc
    

def sat(orig_bench_address,obf_bench_address,max_iter=sys.maxsize, print_str = ""):

    exe_func_time = 0
    exe_non_func_time = 0
    res = 1
    iter = 0
    
    list_dip = []
    list_str_dip = []
    list_orgcirc = []

    obfpinwires, obfkeywires, obfinterwires, obfpoutwires, orgpoutwires, orgwires, str_dip, keyin1, keyin2, keyin3, keyin4, keyinc=init_attack(orig_bench_address,obf_bench_address)


    while res == 1:
        if iter>max_iter:
            print("MAX ITERATION LIMIT EXCEEDED!!!")
            print("func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}".format(iter-1, exe_func_time, exe_non_func_time))
            return None
        res, dscinp, new_func_time = baseutils.finddip(obfpinwires, obfkeywires, obfinterwires, obfpoutwires, list_dip,
                                                       list_orgcirc, keyin1, keyin2, exe_func_time)

        if res == 1:
            orgcirc = logicwire.var_log_sim(dscinp, orgwires, iter)
            iter += 1
            list_dip.append(dscinp)

            for i in range(0, len(dscinp)):
                if str(dscinp[i].value()) == "True":
                    str_dip[i] = "1"
                else:
                    str_dip[i] = "0"
            list_str_dip.append(str_dip)
            str_dip = [None] * len(obfpinwires)
            list_orgcirc.append(orgcirc)

            exe_func_time = new_func_time
        else:
            Monosat().newSolver()
    #print("================ keyFind SAT call ================")
    return get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, 
            list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time, print_str)
            

def appsat(orig_bench_address,obf_bench_address,max_iter=sys.maxsize, print_str = ""):
    exe_func_time = 0
    exe_non_func_time = 0
    res = 1
    iter = 0
    
    list_dip = []
    list_str_dip = []
    list_orgcirc = []

    obfpinwires, obfkeywires, obfinterwires, obfpoutwires, orgpoutwires, orgwires, str_dip, keyin1, keyin2, keyin3, keyin4, keyinc=init_attack(orig_bench_address,obf_bench_address)

    while res == 1:
        if iter>max_iter:
            print("MAX ITERATION LIMIT EXCEEDED!!!")
            print(print_str+"func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}".format(iter-1, exe_func_time, exe_non_func_time))
            return None
        res, dscinp, new_func_time = baseutils.double_dip(obfpinwires, obfkeywires, obfinterwires, obfpoutwires, list_dip,
                                                       list_orgcirc, keyin1, keyin2, keyin3, keyin4, exe_func_time)

        if res == 1:
            orgcirc = logicwire.var_log_sim(dscinp, orgwires, iter)
            iter += 1
            list_dip.append(dscinp)

            for i in range(0, len(dscinp)):
                if str(dscinp[i].value()) == "True":
                    str_dip[i] = "1"
                else:
                    str_dip[i] = "0"
            list_str_dip.append(str_dip)
            str_dip = [None] * len(obfpinwires)
            list_orgcirc.append(orgcirc)

            exe_func_time = new_func_time
        else:
            Monosat().newSolver()

    #print("================ keyFind SAT call ================")
    return get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip,
             list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time, print_str)
            


def hamming_sweep(orig_bench_address,obf_bench_address, max_iter=sys.maxsize,print_str = ""):
    exe_func_time = 0
    exe_non_func_time = 0

    orgwires, orgpinwires, orgkeywires, orginterwires, orgpoutwires = logicwire.wire_dep(orig_bench_address)
    obfwires, obfpinwires, obfkeywires, obfinterwires, obfpoutwires = logicwire.wire_dep(obf_bench_address)

    list_dip = []
    orgcirc = [None] * len(orgpoutwires)
    str_dip = [None] * len(obfpinwires)
    list_str_dip = []
    list_orgcirc = []
    list_cpy_dip = []
    res = 1

    timeout_array = deque([20] * 10)
    const_solve = []

    #print("########## looking for DIPs (Iterative SAT Calls)  ##########")

    iter = 0
    keyin1 = [None] * len(obfkeywires)
    keyin2 = [None] * len(obfkeywires)
    keyinc = [None] * len(obfkeywires)

    interval = len(orgpoutwires)
    approx = 0
    for i in range(0, len(obfkeywires)):
        keyin1[i] = Var()
        keyin1[i].symbol = obfkeywires[i].name + "_1" + str(iter)
        keyin2[i] = Var()
        keyin2[i].symbol = obfkeywires[i].name + "_2" + str(iter)
        keyinc[i] = Var()
        keyinc[i].symbol = obfkeywires[i].name + "c"
        
    while res != -1 and interval != 0:
        if(iter>max_iter):
            print("MAX ITERATION LIMIT EXCEEDED!!!")
            print(print_str +"func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}".format(iter-1, exe_func_time, exe_non_func_time))
            return None
        
        res, dscinp, new_func_time, interval, timeout_array, const_solve = baseutils.finddipham(obfpinwires, obfkeywires, obfinterwires, obfpoutwires, list_dip,
                                                       list_orgcirc, keyin1, keyin2, exe_func_time, interval, timeout_array, const_solve)  # duplicate and find dip

        if len(const_solve) > 50:
            interval = 0
            res = -1
            approx = 1

        if res == 1:
            orgcirc = logicwire.var_log_sim(dscinp, orgwires, iter)
            iter += 1
            list_dip.append(dscinp)
            for i in range(0, len(dscinp)):
                if str(dscinp[i].value()) == "True":
                    str_dip[i] = "1"
                else:
                    str_dip[i] = "0"
            list_str_dip.append(str_dip)
            str_dip = [None] * len(obfpinwires)
            list_orgcirc.append(orgcirc)

            exe_func_time = new_func_time
        elif res == -2:
            interval -= 1
            if interval == 0:
                res = -1
        elif res == -1 and interval != 0:
            interval -= 1
            res = 1
        else:
            
            Monosat().newSolver()

    #print("================ keyFind SAT call ================")
    return get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip,
             list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time, print_str)
            


def RLL(org_name,obfs_name,key_str, write_file = True):

    with open(org_name, 'r') as file:
        lines = file.readlines()
    input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines = get_wire_io(lines)

    bench_gates = len(gate_lines)
    randins_number = len(key_str)
    if randins_number >= bench_gates:
        print("Number of keybits are more than the number of gates")
        return None
    
    inserted = 0
    line_no=0
    while inserted<randins_number:
        gate_match = re.findall(r'\b\w+\b', gate_lines[line_no])
        rand_val = random.random()
        if line_no==bench_gates-1:
            print("Number of gates are less than the key length")
            return None 
        elif gate_match[0] not in output_vars:
            gate_out = gate_match[0]
            if rand_val > 0.5 and key_str[inserted]=="1":
                io_lines += f"INPUT(keyinput{str(inserted)})\n"
                gate_lines[line_no] = gate_lines[line_no].replace(" = ", "_enc = ")
                gate_lines.insert(line_no+1,gate_out + " = XNOR(keyinput" + str(inserted) + ", " + gate_out + "_enc)")
                inserted +=1
                line_no += 1
            elif key_str[inserted]=="0":
                io_lines += f"INPUT(keyinput{str(inserted)})\n"
                gate_lines[line_no] = gate_lines[line_no].replace(" = ", "_enc = ")
                gate_lines.insert(line_no+1,gate_out + " = XOR(keyinput" + str(inserted) + ", " + gate_out + "_enc)")
                inserted +=1
                line_no += 1
        line_no += 1

    if write_file:
        with open(obfs_name, 'w') as file:
            file.write(io_lines+ "\n" + "\n".join(gate_lines))
            print("RLL bench file created")
    else:
        return io_lines,gate_lines

def libar(org_name,obfs_name,key_str,libar_bit_no,rll_file=False,clk_inp_overlap="1"):
    wires = []
    pin_a = []
    pin_b = []
    if rll_file:
        io_lines = ""
        gate_lines =[]
        bench_file = open(org_name)
        for line in bench_file:
            if " = " in line:
                gate_lines.append(line)
            elif len(line)>5:
                io_lines += line
        bench_file.close()
    else:
        io_lines,gate_lines = RLL(org_name,obfs_name,key_str, write_file= False)

    libar_number = libar_bit_no
    i=0
    gate_num=len(gate_lines)
    while i<gate_num:
        gate = gate_lines[i]
        wire = gate.split("=")[0].strip()
        if libar_number == 0:
            break
        if "keyinput" in gate:
            if (len(wires)+len(pin_a))>=2:
                gate_match = re.findall(r'\b\w+\b', gate)
                key_pin = ""
                for pin in gate_match[2:]:
                    if "keyinput" in pin:
                        key_pin = pin

                if clk_inp_overlap == 2: #bothpin overlap
                    if len(pin_a)==0:
                        clk_pin_a = wires.pop()
                        pin_a.append(clk_pin_a)
                    else:
                        clk_pin_a = pin_a.pop()
                    if len(pin_b)==0:
                        clk_pin_b = wires.pop()
                        pin_b.append(clk_pin_b)
                    else:
                        clk_pin_b = pin_b.pop()
                elif clk_inp_overlap == 1: # one pin overlap
                    if len(pin_a)==0:
                        clk_pin_a = wires.pop()
                        pin_a.append(clk_pin_a)
                    else:
                        clk_pin_a = pin_a.pop()

                    clk_pin_b = wires.pop()
                    while clk_pin_b in pin_b:
                        if len(wires)==0:
                            print("Insufficient intermediate wires are available in the circuit for required number of libar block")
                            return None
                        clk_pin_b = wires.pop()
                    pin_b.append(clk_pin_b)

                else: #no overlap
                    clk_pin_a = wires.pop()
                    while clk_pin_a in pin_a:
                        if len(wires)==0:
                            print("Insufficient intermediate wires are available in the circuit for required number of libar block")
                            return None
                        clk_pin_a = wires.pop()
                    pin_a.append(clk_pin_a) 

                    clk_pin_b = wires.pop()
                    while clk_pin_b in pin_b:
                        if len(wires)==0:
                            print("Insufficient intermediate wires are available in the circuit for required number of libar block")
                            return None
                        clk_pin_b = wires.pop()
                    pin_b.append(clk_pin_b)

                gate_lines[i]= gate_lines[i].replace(key_pin,f"LIBAR{str(libar_number)}")
                gate_lines.insert(i,f"LIBAR{str(libar_number)} = DFF(CLK{str(libar_number)}, {key_pin})")
                gate_lines.insert(i,f"CLK{str(libar_number)} = NOR({clk_pin_a}, {clk_pin_b})")
                libar_number -= 1
                gate_num += 2
                i += 2        
        wires.append(wire)
        i += 1
    
    with open(obfs_name, 'w') as file:
        file.write(io_lines+ "\n" + "\n".join(gate_lines))
        print("Libar bench file created")
    
    if libar_bit_no>0:
        txt_content = converts.unroll_bench(obfs_name, libar_bit_no)
        obfs_name = obfs_name.replace(".bench","_unrolled.bench")
        with open(obfs_name, 'w') as file:
            file.write(txt_content)
            print("Libar bench file Unrolled!!!")


def get_wire_io(lines):
    input_vars = []
    output_vars = []
    outvarpos_in_gatelines =[]
    assigned_vars = [] #wire list
    io_lines = ""
    gate_lines = []
    # Regular expressions to match INPUT, OUTPUT, and gate assignments
    input_pattern = re.compile(r'^INPUT\((\w+)\)')
    output_pattern = re.compile(r'^OUTPUT\((\w+)\)')
    
    gate_count = 0
    for line in lines:
        line = line.strip()
        if "=" in line:
            gate_lines.append(line)
            gate_match = re.findall(r'\b\w+\b', line)
            var_name = gate_match[0].strip()
            if var_name in output_vars:
                outvarpos_in_gatelines.append(gate_count)

            assigned_vars.append(var_name)
            gate_count += 1

        elif len(line)>3:
            io_lines += line+"\n"
            if line.startswith("INPUT"):
                match = input_pattern.match(line)
                if match:
                    input_vars.append(match.group(1))
            elif line.startswith("OUTPUT"):
                match = output_pattern.match(line)
                if match:
                    output_vars.append(match.group(1))
            
    return input_vars, output_vars, outvarpos_in_gatelines, assigned_vars, io_lines, gate_lines

def backward_propagation(as_cone_wires, wire, gate_visited, gate_lines, input_vars, output_vars, assigned_vars):
    if wire in input_vars:
        if wire not in as_cone_wires:
            as_cone_wires.append(wire)
        return None
    gate_index = assigned_vars.index(wire)
    if gate_visited[gate_index]:
        return None
    else:
        as_cone_wires.append(wire)
        gate_visited[gate_index] = True
        gate_match = re.findall(r'\b\w+\b', gate_lines[gate_index])
        for wire in gate_match[2:]:
            backward_propagation(as_cone_wires, wire, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)
        return None


def anti_sat(org_name,obfs_name,key_str,init_key_pos=0, write_file = True):
    loop_len = int(len(key_str)/2)
    if len(key_str)%2 == 1:
        print("In anti-sat key bit must be in even length. last bit will be omitted")
    if key_str[:loop_len] != key_str[loop_len:(2*loop_len)]:
        print(f"The key bit should be equal if half splitted. but here your key: {key_str} is not.")
        return [None]*7
        
    with open(org_name, 'r') as file:
        lines = file.readlines()
    input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines = get_wire_io(lines)
    if loop_len>=len(input_vars):
        print("Number of key is greater than the number of inputs")
        return [None]*7
    index_out = random.randint(0,len(output_vars)-1)
    sig_ins_index = output_vars_pos[index_out]
    out_line = gate_lines[sig_ins_index]
    gate_match = re.findall(r'\b\w+\b', out_line)
    target_index = assigned_vars.index(gate_match[2])
    selected_output = gate_match[2].strip()
    sig_bit_index = random.randint(0,len(key_str)-1)
    

    #antisat building starts here 
    main_bit_inps = []
    cmplmnt_bit_inps = []
    key_str = key_str.strip()

    for i in range(loop_len):
        io_lines += f"INPUT(keyinput{i+init_key_pos})\n"
        io_lines += f"INPUT(keyinput{i+loop_len+init_key_pos})\n"
        input_vars += [f"keyinput{i+init_key_pos}", f"keyinput{i+loop_len+init_key_pos}"]
        gate_lines.append(f"CMP1_{i} = XOR(keyinput{i+init_key_pos}, {input_vars[i]})")
        gate_lines.append(f"CMP2_{i} = XOR(keyinput{i+loop_len+init_key_pos}, {input_vars[i]})")
        assigned_vars += [f"CMP1_{i}",f"CMP2_{i}"]
        main_bit_inps.append(f"CMP1_{i}")
        cmplmnt_bit_inps.append(f"CMP2_{i}")
        i += 1

    gate_lines.append("MAIN_BIT = AND(" + ", ".join(main_bit_inps)+")")
    gate_lines.append("CMPLMNT_BIT = NAND(" + ", ".join(cmplmnt_bit_inps)+")")
    gate_lines.append("SIG_BIT_0 = AND(MAIN_BIT, CMPLMNT_BIT)")
    assigned_vars += ["MAIN_BIT", "CMPLMNT_BIT", "SIG_BIT_0"]

    
    gate_lines[target_index] = gate_lines[target_index].replace(selected_output,selected_output+"_enc")
    assigned_vars[target_index] = selected_output+"_enc"
    
    if key_str[sig_bit_index]=="0":
        gate_lines.append(f"{selected_output} = XOR(SIG_BIT_0, {selected_output}_enc)")
        assigned_vars.append(selected_output)
    else:
        gate_lines.append("SIG_BIT_1 = NOT(SIG_BIT_0)")
        assigned_vars.append(f"SIG_BIT_1")
        gate_lines.append(f"{selected_output} = XNOR(SIG_BIT_1, {selected_output}_enc)")
        assigned_vars.append(selected_output)
        
    if write_file:
        with open(obfs_name, 'w') as file:
            file.write(io_lines+ "\n" + "\n".join(gate_lines))
            print("AntiSAT bench file created")
    else:
        return input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines, selected_output
    
def sarlock(org_name,obfs_name,key_str,init_key_pos=0, write_file = True):
    with open(org_name, 'r') as file:
        lines = file.readlines()
    input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines = get_wire_io(lines)

    if len(key_str)>len(input_vars):
        print("Number of key is greater than the number of inputs")
        return [None]*7

    #sarlock building starts here
    xor_gates =[]
    not_key_list=[]
    for i in range(0,len(key_str)):
        io_lines += f"INPUT(keyinput{i+init_key_pos})\n"
        input_vars.append(f"keyinput{i+init_key_pos}")
        xor_gates.append(f"nXOR{i} = XOR({input_vars[i]}, keyinput{i+init_key_pos})")
        not_key_list.append(f"not_keyinp{str(i+init_key_pos)} = NOT(keyinput{i+init_key_pos})")
        assigned_vars += [f"nXOR{i}",f"not_keyinp{str(i+init_key_pos)}"]

    xor_gates += not_key_list

    flip_sig_list = []
    mask_sig_list = []
    for i in range(0, int(len(key_str)/10)):
        flip_sig = []
        mask_sig = []
        for j in range(0, 10):
            flip_sig.append(f"nXOR{str(i*10 + j)}")
            if j==9 and j==0:
                if key_str[j] == "0":
                    mask_sig.append(f"not_keyinp{str(i*10 + j + init_key_pos)}")
                elif key_str[i] == "1":
                    mask_sig.append(f"keyinput{str(i*10 + j + init_key_pos)}")
            else:
                if key_str[j] == "0":
                    mask_sig.append(f"not_keyinp{str(i*10 + j + init_key_pos)}")
                elif key_str[i] == "1":
                    mask_sig.append(f"keyinput{str(i*10 + j + init_key_pos)}")

        xor_gates.append(f"flipSig{i} = OR("+", ".join(flip_sig)+")")
        xor_gates.append(f"maskSig{i} = AND("+", ".join(mask_sig)+")")        
        flip_sig_list.append(f"flipSig{i}")
        mask_sig_list.append(f"maskSig{i}")
        assigned_vars += [f"flipSig{i}",f"maskSig{i}"]
        
    flip_sig = []
    mask_sig = []
    for i in range(int(len(key_str)/10)*10, len(key_str)):
        flip_sig.append(f"nXOR{str(i)}")
        if key_str[i] == "0":
            mask_sig.append(f"not_keyinp{str(i+ init_key_pos)}")
        elif key_str[i] == "1":
            mask_sig.append(f"keyinput{str(i+ init_key_pos)}")

    if len(flip_sig)>1:
        flip_sig_list.append(f"flipSig{int(len(key_str)/10)}")
        mask_sig_list.append(f"maskSig{int(len(key_str)/10)}")
        xor_gates.append(f"flipSig{int(len(key_str)/10)} = OR("+", ".join(flip_sig)+")")
        xor_gates.append(f"maskSig{int(len(key_str)/10)} = AND("+", ".join(mask_sig)+")")
        assigned_vars += [f"flipSig{int(len(key_str)/10)}"f"maskSig{int(len(key_str)/10)}"]
    elif len(flip_sig)==1: 
        flip_sig_list.append(flip_sig[0])
        mask_sig_list.append(mask_sig[0])
        
    
    if len(flip_sig_list)>1:
        xor_gates.append(f"flipSig = NOR("+", ".join(flip_sig_list)+")")
        xor_gates.append(f"maskSig = AND("+", ".join(mask_sig_list)+")")
        assigned_vars += [f"flipSig", f"maskSig"]
    elif len(flip_sig_list)==1:
        xor_gates[-1] = xor_gates[-1].replace("maskSig0","maskSig")
        xor_gates[-2] = xor_gates[-2].replace("flipSig0 = OR","flipSig = NOR")
        assigned_vars[-1] = assigned_vars[-1].replace("maskSig0","maskSig")
        assigned_vars[-2] = assigned_vars[-2].replace("flipSig0","flipSig")
    else:
        xor_gates.append(f"flipSig = NOR("+", ".join(flip_sig)+")") 
        xor_gates.append(f"maskSig = AND("+", ".join(mask_sig)+")")
        assigned_vars += [f"flipSig", f"maskSig"]

    xor_gates.append("not_mask = NOT(maskSig)")
    xor_gates.append("flip_mask = AND(flipSig, not_mask)")
    assigned_vars += ["not_mask", "flip_mask"]

    gate_lines += xor_gates
    sig_ins_index = output_vars_pos[-1]
    selected_output = output_vars[-1].strip()
    gate_lines[sig_ins_index] = gate_lines[sig_ins_index].replace(selected_output,selected_output+"_enc")
    assigned_vars[sig_ins_index] = selected_output+"_enc"
    gate_lines.append(f"{selected_output} = XOR(flip_mask, {selected_output}_enc)")
    assigned_vars.append(selected_output)    
    if write_file:
        with open(obfs_name, 'w') as file:
            file.write(io_lines+ "\n" + "\n".join(gate_lines))
            print("SARLock bench file created")
    else:
        return input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines, selected_output


def bench2list(org_file, add_out=True):
    with open(org_file, 'r') as file:
            lines = file.readlines()
        
    output_vars=[]
    input_vars=[]
    io_lines = []
    gate_lines = []
    wires = []
    input_pattern = re.compile(r'^INPUT\((\w+)\)')
    output_pattern = re.compile(r'^OUTPUT\((\w+)\)')
    
    for line in lines:
        line = line.strip()
        
        if "=" in line:
            gate_lines.append(line)
            gate_match = re.findall(r'\b\w+\b', line)
            var_name = gate_match[0].strip()
            wires.append(var_name)

        elif len(line)>3:
            if line.startswith("INPUT"):
                match = input_pattern.match(line)
                if match:
                    input_vars.append(match.group(1))
                    io_lines.append(line)
            elif line.startswith("OUTPUT"):
                match = output_pattern.match(line)
                if match:
                    if add_out:
                        io_lines.append(line)
                    output_vars.append(match.group(1))
                    
    
    return gate_lines,io_lines,input_vars,output_vars,wires

def cac(org_name,obfs_name,cac_file,key_bit_no):
    org_gates, org_io, org_inputs, org_outputs, org_wires = bench2list(org_name)
    lock_gates, lock_io, lock_inputs, lock_outputs, lock_wires = bench2list(cac_file, False)

    bench = org_io
    for i in range(key_bit_no):
        bench.append(f"INPUT(keyinput{i})")

    gate_index = org_wires.index(org_outputs[-1])
    org_gates[gate_index] = org_gates[gate_index].replace(org_outputs[-1],org_outputs[-1]+"_enc")
    lock_gates[-1] = lock_gates[-1].replace(lock_outputs[0],org_outputs[-1])
    lock_gates[-3] = lock_gates[-3].replace("OPO",org_outputs[-1]+"_enc")

    wirex=[]
    for i in range(len(lock_gates)):
        if "in_" in lock_gates[i]:
            gate_match = re.findall(r'\b\w+\b', lock_gates[i])
            for inp in gate_match[2:]:
                if "in_" in inp:
                    inp_index = int(inp.split("_")[-1].strip())
                    lock_gates[i] = lock_gates[i].replace(inp,org_inputs[inp_index])
        

    bench += org_gates+lock_gates
    with open(obfs_name, 'w') as file:
        file.write("\n".join(bench))
        print(obfs_name+" bench file created")



def hybrid_libar(org_name,obfs_name, other_algo, other_algo_str,libar_key_str,libar_percent):
    if other_algo == "sarlock":
        input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines, selected_output=sarlock(org_name,obfs_name,other_algo_str,init_key_pos=len(libar_key_str),write_file=False)
    elif other_algo == "antisat":
        input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines, selected_output=anti_sat(org_name,obfs_name,other_algo_str,init_key_pos=len(libar_key_str),write_file=False)
    else:
        print("The entered method don't match with anything")
        return None
    
    if input_vars == None:
        return None
    
    gate_visited = [False]*len(gate_lines)
    as_cone_wires = []
    backward_propagation(as_cone_wires, selected_output, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)
    as_cone_wires = list(set(as_cone_wires))
    cone_len = len(as_cone_wires)
    gate_num = len(gate_lines)-1
    libar_no = math.ceil(len(libar_key_str)*libar_percent)
    if (gate_num-cone_len+len(input_vars))<1:
        print("Not enough gate exist outside the antisat locked cone")
        return None
    
    i=0
    for key in libar_key_str:
        target_pin =""
        rand_pos = -1
        while rand_pos<0:
            wire_index = random.randint(0,gate_num)
            target_pin = assigned_vars[wire_index]
            if target_pin not in as_cone_wires:
                rand_pos = wire_index
                gate_match = re.findall(r'\b\w+\b', gate_lines[wire_index])
                target_pin = gate_match[2].strip()
                break
        if f"INPUT(keyinput{i})" not in io_lines:
            io_lines += f"INPUT(keyinput{i})\n"
        gate_lines[rand_pos]= gate_lines[rand_pos].replace(target_pin,f"RLL{str(i)}")
        if key=="1":
            gate_lines.insert(rand_pos,f"RLL{str(i)} = XNOR({target_pin}, keyinput{str(i)})")
        else:
            gate_lines.insert(rand_pos,f"RLL{str(i)} = XOR({target_pin}, keyinput{str(i)})")
        i += 1

    with open(obfs_name, 'w') as file:
        file.write(io_lines+ "\n" + "\n".join(gate_lines))
        print(f"Libar, {other_algo} hybrid bench file created")

    txt_content = converts.unroll_bench(obfs_name,  math.ceil(len(libar_key_str)*libar_percent))
    obfs_name = obfs_name.replace(".bench","_unrolled.bench")
    with open(obfs_name, 'w') as file:
        file.write(txt_content)
        print("Libar bench file Unrolled!!!")
    
    
def convert_bench2verilog(input_file):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    v_text = converts.bench2verilog(input_file, file_name)
    file_name += ".v"
    output_file = os.path.join("bench_verilog",file_name)
    with open(output_file, 'w') as file:
        file.write(v_text)
        print("Verilog file created. Please look at bench_verilog folder.")
    