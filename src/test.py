"""import algo_methods
algo = "sar"
org1 = "bench_ckt/c432.bench"
obfs1 = f"obfuscated/c432_{algo}.bench"
key1 = "10011000111110101001100011111010"
org2 = "bench_ckt/c3540.bench"
obfs2 = f"obfuscated/c3540_{algo}.bench"
key2 = "000011111110101001000111000011111110101001000111"

#algo_methods.sarlock(org1,obfs1,key1)
#algo_methods.asob("bench_ckt/c432.bench","obfuscated/c432_sar_libar.bench", "sarlock", "00001111","10101010111100101010",.3)
#algo_methods.asob("bench_ckt/c432.bench","obfuscated/c432_asob.bench","101111011001100",7)
#algo_methods.RLL("bench_ckt/c432.bench","obfuscated/c432_rll.bench","10011000111110101001100011111010")
#algo_methods.RLL("bench_ckt/c3540.bench","obfuscated/c3540_rll.bench","000011111110101001000111000011111110101001000111")

libar_prcnt=[1,2,3,4,5,7,10]

for prcnt in libar_prcnt:
    algo_methods.libar("c432/c432_rll_32k.bench",f"c432/c432_libar_bolINPclk_{prcnt}.bench","10011000111110101001100011111010",prcnt,True)
"""
import random

def int2bin(value, size):
    string_val = list("0" * size)
    temp_value = list(reversed(list("{0:b}".format(value))))
    for i in range(0, len(temp_value)):
        string_val[i] = temp_value[i]
    string_val = "".join(list(reversed(string_val)))
    return string_val


def get_random_boolean_list(length):
    return [random.choice([True, False]) for _ in range(length)]

str2bool = {"0":False,"1":True}

for i in range(16):
    print("___________________________")
    key = int2bin(i,4)
    for j in range(4):
        inp = int2bin(j,2)
        y=((str2bool[key[0]]^str2bool[inp[0]])&(str2bool[key[1]]^str2bool[inp[1]])) & \
        (not((str2bool[key[2]]^str2bool[inp[0]])&(str2bool[key[3]]^str2bool[inp[1]])))
        print(key, inp, y)
 


import re

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


def forward_propagation(as_cone_wires, src_gate, prev_gate_index, gate_visited, gate_lines, input_vars, output_vars, assigned_vars):
    if src_gate in output_vars:
        return None
    else:
        for j in range(prev_gate_index,len(gate_lines)):
            if not(gate_visited[j]):
                if src_gate in gate_lines[j]:
                    gate_visited[j]=True
                    gate_match = re.findall(r'\b\w+\b', gate_lines[j])
                    as_cone_wires.append(gate_match[0])
                    forward_propagation(as_cone_wires, gate_match[0], j, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)
                    for wire in gate_match[2:]:
                        backward_propagation(as_cone_wires, wire, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)
                    break
        
        return None


with open("c6288/c6288_sarlock_32k.bench", 'r') as file:
        lines = file.readlines()
input_vars, output_vars, output_vars_pos, assigned_vars, io_lines, gate_lines = get_wire_io(lines)

#create cone
as_cone_wires=[]
gate_visited = [False]*len(gate_lines)
for i in range(len(gate_lines)):
    gate = gate_lines[i]
    if "keyinput" in gate:
        gate_visited[i]=True
        gate_match = re.findall(r'\b\w+\b', gate)
        as_cone_wires.append(gate_match[0])
        forward_propagation(as_cone_wires, gate_match[0], i, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)
        for wire in gate_match[2:]:
            backward_propagation(as_cone_wires, wire, gate_visited, gate_lines, input_vars, output_vars, assigned_vars)


logic_cone=[]
for gate in gate_lines:
    gate_match = re.findall(r'\b\w+\b', gate)
    if gate_match[0] in as_cone_wires:
        logic_cone.append(gate)

io_lines=[]
for wire in as_cone_wires:
    if wire in input_vars:
        io_lines.append(f"INPUT({wire})")
    elif wire in output_vars:
        io_lines.append(f"OUTPUT({wire})")


with open("obfuscated/sarlock.bench", 'w') as file:
    file.write("\n".join(io_lines)+"\n\n"+"\n".join(logic_cone))
    print("AntiSAT bench file created")

#python3 src/smt_tool.py --algorithm sarlock_enc --original /home/mahmudul-hasan/Downloads/SMTAttack-master/benchmarks/originals/c432.bench --obfuscated /home/mahmudul-hasan/Research/BUET_SAT_SIMULATOR/obfuscated/c432_sar_smt.bench --design_name c432 --key_str 111101010101010111000000000001101010
