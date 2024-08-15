import sys 
from monosat import *
import logicwire
import baseutils
from collections import deque
from random import randint
import math 
import re ,os
import converts


def get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time):
    print("---------------- looking for key (Last SAT Call) ------------")
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

        print("key= {}".format(''.join(correct_key)))
        print("func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}".format(iter, exe_func_time, exe_non_func_time))

    else:
        print("Didn't Found Any Satisfiable Key")


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
    

def sat(orig_bench_address,obf_bench_address,max_iter=sys.maxsize):

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
    print("================ keyFind SAT call ================")
    get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time)
            

def appsat(orig_bench_address,obf_bench_address,max_iter=sys.maxsize):
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

    print("================ keyFind SAT call ================")
    get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time)
            


def hamming_sweep(orig_bench_address,obf_bench_address, max_iter=sys.maxsize):
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

    print("########## looking for DIPs (Iterative SAT Calls)  ##########")

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
            print("func_iteration= {}; func_exe_time= {}; nonfunc_exe_time= {}".format(iter-1, exe_func_time, exe_non_func_time))
            return None
        
        res, dscinp, new_func_time, interval, timeout_array, const_solve = baseutils.finddipham(obfpinwires, obfkeywires, obfinterwires, obfpoutwires, list_dip,
                                                       list_orgcirc, keyin1, keyin2,
                                                       exe_func_time, interval, timeout_array, const_solve)  # duplicate and find dip

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

    print("================ keyFind SAT call ================")
    get_key(obfkeywires, obfinterwires, obfpoutwires, list_str_dip, list_dip, list_orgcirc, keyinc,iter, exe_func_time, exe_non_func_time)
            

def get_rand(end_pt,list):
    end_pt -= 1
    rand_pos = randint(0,end_pt)
    while rand_pos in list:
        rand_pos = randint(0,end_pt)
    list.append(rand_pos)
    return rand_pos


def RLL(org_name,obfs_name,key_str):
    bench_gates = 0
    io_lines = ""
    gate_lines =[]
    io_pins = []
    gate_limit_flag = False

    bench_file = open(org_name)
    for line in bench_file:
        if " = " in line:
            bench_gates += 1
            gate_lines.append(line)
        else:
            io_lines += line
            matches = re.findall(r'\b\w+\b', line)
            if len(matches)==2:
                if (matches[0].strip() == "INPUT") | (matches[0].strip() == "OUTPUT"):
                    io_pins.append(matches[1].strip())

    bench_file.close()

    randins_number = len(key_str)
    if randins_number >= bench_gates:
        print("Number of keybits are more than the number of gates")
        return None
    obfs_gates=[]

    for i in range(randins_number):
        inserting_gate_flag = True
        io_lines += f"INPUT(keyinput{str(i)})\n"
        while inserting_gate_flag:
            if len(obfs_gates)>=bench_gates:
                gate_limit_flag = True
                break
            rand_pos = get_rand(bench_gates,obfs_gates)
            gate_match = re.findall(r'\b\w+\b', gate_lines[rand_pos])
            target_pin = ""
            while target_pin=="":
                for pin in gate_match[2:]:
                    if pin not in io_pins:
                        target_pin = pin
                        break
                if target_pin != "":
                        gate_lines[rand_pos]= gate_lines[rand_pos].replace(target_pin,f"RLL{str(i)}")
                        if key_str[i]=="1":
                            gate_lines.insert(rand_pos,f"RLL{str(i)} = XNOR({target_pin}, keyinput{str(i)})")
                        else:
                            gate_lines.insert(rand_pos,f"RLL{str(i)} = XOR({target_pin}, keyinput{str(i)})")
                        inserting_gate_flag = False
                        break
                else:
                    if len(obfs_gates)>=bench_gates:
                        gate_limit_flag = True
                        break
                    rand_pos = get_rand(bench_gates,obfs_gates)
                    gate_match = re.findall(r'\b\w+\b', gate_lines[rand_pos])
        if gate_limit_flag:
            print("Number of keybits are more than the number of non input gates")
            return None


    with open(obfs_name, 'w') as file:
        file.write(io_lines+ "\n" + "\n".join(gate_lines))

    return io_lines,gate_lines

def libar(org_name,obfs_name,key_str,libar_percent):
    wires = []
    pin_a = []
    pin_b = []

    io_lines,gate_lines = RLL(org_name,obfs_name,key_str)
    libar_number = int(math.ceil(len(key_str)*libar_percent))
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
    txt_content = converts.unroll_bench(obfs_name, int(math.ceil(len(key_str)*libar_percent)))
    obfs_name = obfs_name.replace(".bench","_unrolled.bench")
    with open(obfs_name, 'w') as file:
        file.write(txt_content)
        print("Libar bench file Unrolled!!!")


def get_wire_io(lines):
    input_vars = []
    output_vars = []
    output_vars_pos =[]
    assigned_vars = []
    assigned_vars_pos = []
    io_lines = []
    gate_lines = []
    # Regular expressions to match INPUT, OUTPUT, and gate assignments
    input_pattern = re.compile(r'^INPUT\((\w+)\)')
    output_pattern = re.compile(r'^OUTPUT\((\w+)\)')
    

    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("INPUT"):
            match = input_pattern.match(line)
            if match:
                input_vars.append(match.group(1))
        elif line.startswith("OUTPUT"):
            match = output_pattern.match(line)
            if match:
                output_vars.append(match.group(1))
                output_vars_pos.append(i)
        else:
            gate_match = re.findall(r'\b\w+\b', line)
            try:
                var_name = gate_match[0].strip()
                if var_name in output_vars:
                    index_out = output_vars.index(var_name)
                    output_vars_pos[index_out]=i
                else:    
                    assigned_vars.append(var_name)
                    assigned_vars_pos.append(i)
                
            except:
                pass

    return input_vars, output_vars, output_vars_pos, assigned_vars, assigned_vars_pos

def anti_sat(org_name,obfs_name,key_str):
    with open(org_name, 'r') as file:
        lines = file.readlines()
    
def sarlock(org_name,obfs_name,key_str,init_key_pos=0):
    with open(org_name, 'r') as file:
        lines = file.readlines()
    input_vars, output_vars, output_vars_pos, assigned_vars, assigned_vars_pos = get_wire_io(lines)

    index_out = randint(0,len(output_vars)-1)
    selected_output = output_vars[index_out]

    if len(key_str)>len(input_vars):
        print("Number of key is greater than the number of inputs")
        return [None]*6

    #sarlock building starts here 
    


    return input_vars, output_vars, output_vars_pos, assigned_vars, assigned_vars_pos, selected_output


def hybrid_libar(org_name,obfs_name,libar_key_str,libar_percent, other_algo, other_algo_str):
    if other_algo == "sarlock":
        input_vars, output_vars, output_vars_pos, assigned_vars, assigned_vars_pos, selected_output=sarlock(org_name,obfs_name,other_algo_str,selected_output = "")

    
    if input_vars == None:
        return None
    
    


def convert_bench2verilog(input_file):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    v_text = converts.bench2verilog(input_file, file_name)
    file_name += ".v"
    output_file = os.path.join("bench_verilog",file_name)
    with open(output_file, 'w') as file:
        file.write(v_text)
        print("Verilog file created. Please look at bench_verilog folder.")
    

