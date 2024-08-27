#Import the MonoSAT library
from monosat import *
import logging
from random import randint
import re

LOGIC_VALUE_ZERO = "0"
LOGIC_VALUE_ONE = "1"

PRIMARY_INPUT = "pin"
PRIMARY_OUTPUT = "pout"
KEY_INPUT = "kin"
INTERMEDIATE_WIRE = "inwire"


ERR_PR = 3
WAR_PR = 2
INF_PR = 1
DBG_PR = 0


def int2bin(value, size):
    string_val = list("0" * size)
    temp_value = list(reversed(list("{0:b}".format(value))))
    for i in range(0, len(temp_value)):
        string_val[i] = temp_value[i]
    string_val = "".join(list(reversed(string_val)))
    return string_val


def bin2int(value):
    return int(value, 2)

def convert_gate_line(line, gate_count):
    match = re.findall(r'\b\w+\b', line)
    gate_dict=[ "AND", "NAND", "OR", "NOR", "XOR", "XNOR", "NOT", "BUF", "DFF"]
    
    if match:
        output_var = match[0]
        gate_type = match[1]  # Convert gate type to lowercase
        inputs = match[2:]
        
        if gate_type in gate_dict:
            gate_unique_name = f"{gate_type}{len(inputs)}_{gate_count}"
            converted_line = f"{gate_type.lower()} {gate_unique_name} ({output_var}, {', '.join(inputs)});"
            return gate_type, converted_line
    
    return None, None

def bench2verilog(file_path, file_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    gate_count = 1
    input_vars = []
    output_vars = []
    assigned_vars = []
    dff_module = [
            "module DFF(Q, clk, D);",
            "input D;",
            "input clk;",
            "output Q;",
            "always @(clk)", 
            "begin",
            "  Q <= D;", 
            "end", 
            "endmodule"]
    opr_lines=[]
    gate_types=[]

    # Regular expressions to match INPUT, OUTPUT, and gate assignments
    input_pattern = re.compile(r'^INPUT\((\w+)\)')
    output_pattern = re.compile(r'^OUTPUT\((\w+)\)')
    assign_pattern = re.compile(r'^(\w+)\s*=\s*(NAND|NOR|AND|OR|XOR|XNOR|NOT|DFF|BUF)\((.*)\)')

    for line in lines:
        line = line.strip()
        if line.startswith("INPUT"):
            match = input_pattern.match(line)
            if match:
                input_vars.append(match.group(1))
        elif line.startswith("OUTPUT"):
            match = output_pattern.match(line)
            if match:
                output_vars.append(match.group(1))
        else:
            match = assign_pattern.match(line)
            if match:
                assigned_vars.append(match.group(1))
                gate_type,opr_line = convert_gate_line(line,gate_count)
                if opr_line is not None:
                    opr_lines.append(opr_line)
                    if gate_type not in gate_types:
                        gate_types.append(gate_type) 
                    gate_count += 1

    # Intermediate variables are those assigned but not inputs or outputs
    intermediate_vars = [var for var in assigned_vars if var not in input_vars and var not in output_vars]

    module_heading = f"module {file_name}({','.join(input_vars + output_vars)});"
    input_line = f"input {','.join(input_vars)};"
    output_line = f"output {','.join(output_vars)};"
    wire_line = f"wire {','.join(intermediate_vars)};"
    termination_line = "endmodule"
    main_module="\n".join([module_heading,"",input_line,output_line,wire_line,""]+opr_lines+["",termination_line])
    
    if "DFF" in gate_types:
        main_module = "\n".join(dff_module + ["\n", main_module])
    return main_module

def unroll_bench(file_path,unroll_iter_no):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    final_file = []
    execution_code = []
    input_vars = []
    output_vars = []
    one_flag = True

    input_pattern = re.compile(r'^INPUT\((\w+)\)')
    output_pattern = re.compile(r'^OUTPUT\((\w+)\)')
    assign_pattern = re.compile(r'^(\w+)\s*=\s*(NAND|AND|NOR|OR|XOR|XNOR|NOT|DFF|BUF)\((.*)\)')

    for line in lines:
        final_file.append(line)
        line = line.strip()
        if line.startswith("INPUT"):
            match = input_pattern.match(line)
            if match:
                input_vars.append(match.group(1))
        elif line.startswith("OUTPUT"):
            match = output_pattern.match(line)
            if match:
                output_vars.append(match.group(1))
        else:
            match = assign_pattern.match(line)
            if match:
                execution_code.append(line)

                dff_match = re.findall(r'\b\w+\b', line)
                if dff_match[0] in output_vars:
                    new_out =dff_match[0]+"_"+str(unroll_iter_no)+" "
                    final_file.pop()
                    final_file.append(line.replace(dff_match[0]+" ",new_out)+"\n")   
                elif "CLK" in dff_match[0]:
                    final_file.pop()          
                if "DFF" in line:
                    final_file.pop()
                    if one_flag:
                        final_file +=[f"W1_INV = NOT({input_vars[0]})\n",f"ONE = OR({input_vars[0]}, W1_INV)\n"]
                        one_flag = False
                    final_file.append(f"{dff_match[0]} = AND(ONE, {dff_match[3]})\n")


    temp = []
    for i in range(unroll_iter_no-1):
        for line in execution_code:
            gate_match = re.findall(r'\b\w+\b', line)
            in_var = gate_match[2:]
            for j in range(len(in_var)):
                if in_var[j] not in input_vars:
                    in_var[j] += "_"+str(i)

            if "DFF" in line:
                final_file.pop()
                temp.append(f"{gate_match[0]}_{i} = AND({', '.join(in_var)})")
            else:
                temp.append(f"{gate_match[0]}_{i} = {gate_match[1]}({', '.join(in_var)})")
        temp.append("\n")


    for line in execution_code:
        gate_match = re.findall(r'\b\w+\b', line)
        in_var = gate_match[2:]
        for j in range(len(in_var)):
            if in_var[j] not in input_vars:
                in_var[j] += "_"+str(unroll_iter_no)

        if gate_match[0] not in output_vars:
            gate_match[0] += "_"+str(unroll_iter_no)    
        if "DFF" in line:
            temp.append(f"{gate_match[0]} = AND({', '.join(in_var)})")
        else:
            temp.append(f"{gate_match[0]} = {gate_match[1]}({', '.join(in_var)})")
            
    return "".join(final_file)+"\n"+"\n".join(temp)



def circuit2bool(interwires, poutwires, pin, keyin): #wires are inwire + pout

    interwires_var = [None] * (len(interwires))
    poutwires_var = [None] * (len(poutwires))

    logging.debug("converts/circuit2bool: size of interwires: {}".format(len(interwires)))
    logging.debug("converts/circuit2bool: size of poutwires: {}".format(len(poutwires)))

    logging.debug("**********convert inter wires****************")
    for i in range(0, len(interwires)):
        operands_list = []

        logging.debug("----------------------------------")
        logging.debug("converts/circuit2bool: wire {} = {}:(".format(interwires[i].name, interwires[i].type))
        for j in range(0, len(interwires[i].operands)):
            if j != len(interwires[i].operands) - 1:
                logging.debug("{}, ".format(interwires[i].operands[j].name))
            else:
                logging.debug("{})".format(interwires[i].operands[j].name))

        logging.debug(" index = {}, catg = {}".format(i, interwires[i].catg))

        if interwires[i].type == "NOT" or interwires[i].type == "not":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[0].name, interwires[i].operands[0].catg))
            if interwires[i].operands[0].catg == PRIMARY_INPUT:
                logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(pin[interwires[i].operands[0].index])
            elif interwires[i].operands[0].catg == KEY_INPUT:
                logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(keyin[interwires[i].operands[0].index])
            elif interwires[i].operands[0].catg == INTERMEDIATE_WIRE:
                logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(interwires_var[interwires[i].operands[0].index])
            elif interwires[i].operands[0].catg == PRIMARY_OUTPUT:
                logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(poutwires_var[interwires[i].operands[0].index])

        elif interwires[i].type == "BUFF" or interwires[i].type == "buff" or interwires[i].type == "BUF" or interwires[i].type == "buf":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[0].name, interwires[i].operands[0].catg))
            if interwires[i].operands[0].catg == PRIMARY_INPUT:
                logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(Not(pin[interwires[i].operands[0].index]))
            elif interwires[i].operands[0].catg == KEY_INPUT:
                logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(Not(keyin[interwires[i].operands[0].index]))
            elif interwires[i].operands[0].catg == INTERMEDIATE_WIRE:
                logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(Not(interwires_var[interwires[i].operands[0].index]))
            elif interwires[i].operands[0].catg == PRIMARY_OUTPUT:
                logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[0].index))
                interwires_var[i] = Not(Not(poutwires_var[interwires[i].operands[0].index]))

        elif interwires[i].type == "AND" or interwires[i].type == "and":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = And(operands_list)

        elif interwires[i].type == "NAND" or interwires[i].type == "nand":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Nand(operands_list)

        elif interwires[i].type == "OR" or interwires[i].type == "or":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Or(operands_list)

        elif interwires[i].type == "NOR" or interwires[i].type == "nor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Nor(operands_list)

        elif interwires[i].type == "XOR" or interwires[i].type == "xor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Xor(operands_list)

        elif interwires[i].type == "XNOR" or interwires[i].type == "xnor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Xnor(operands_list)
        elif interwires[i].type == "MUX" or interwires[i].type == "mux":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(interwires[i].operands)))
            for j in range(0, len(interwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, interwires[i].operands[j].name, interwires[i].operands[j].catg))
                if interwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(pin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(keyin[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(interwires_var[interwires[i].operands[j].index])
                elif interwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(interwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            interwires_var[i] = Or(And(Not(operands_list[0]), operands_list[1]), And(operands_list[0], operands_list[2]))

        interwires_var[i].symbol = interwires[i].name

        logging.debug("**********convert out wires****************")
    for i in range(0, len(poutwires)):
        operands_list = []

        logging.debug("----------------------------------")
        logging.debug("converts/circuit2bool: wire {} = {}: ".format(poutwires[i].name, poutwires[i].type))
        for j in range(0, len(poutwires[i].operands)):
            if j != len(poutwires[i].operands) - 1:
                logging.debug("{}, ".format(poutwires[i].operands[j].name))
            else:
                logging.debug("{})".format(poutwires[i].operands[j].name))

        logging.debug("index = {}, catg = {}".format(i, poutwires[i].catg))

        if poutwires[i].type == "NOT" or poutwires[i].type == "not":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[0].name, poutwires[i].operands[0].catg))
            if poutwires[i].operands[0].catg == PRIMARY_INPUT:
                logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(pin[poutwires[i].operands[0].index])
            elif poutwires[i].operands[0].catg == KEY_INPUT:
                logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(keyin[poutwires[i].operands[0].index])
            elif poutwires[i].operands[0].catg == INTERMEDIATE_WIRE:
                logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(interwires_var[poutwires[i].operands[0].index])
            elif poutwires[i].operands[0].catg == PRIMARY_OUTPUT:
                logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(poutwires_var[poutwires[i].operands[0].index])

        elif poutwires[i].type == "BUFF" or poutwires[i].type == "buff" or poutwires[i].type == "BUF" or poutwires[i].type == "buf":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[0].name, poutwires[i].operands[0].catg))
            if poutwires[i].operands[0].catg == PRIMARY_INPUT:
                logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(Not(pin[poutwires[i].operands[0].index]))
            elif poutwires[i].operands[0].catg == KEY_INPUT:
                logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(Not(keyin[poutwires[i].operands[0].index]))
            elif poutwires[i].operands[0].catg == INTERMEDIATE_WIRE:
                logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(Not(interwires_var[poutwires[i].operands[0].index]))
            elif poutwires[i].operands[0].catg == PRIMARY_OUTPUT:
                logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[0].index))
                poutwires_var[i] = Not(Not(poutwires_var[poutwires[i].operands[0].index]))

        elif poutwires[i].type == "AND" or poutwires[i].type == "and":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = And(operands_list)

        elif poutwires[i].type == "NAND" or poutwires[i].type == "nand":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = Nand(operands_list)

        elif poutwires[i].type == "OR" or poutwires[i].type == "or":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = Or(operands_list)

        elif poutwires[i].type == "NOR" or poutwires[i].type == "nor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = Nor(operands_list)

        elif poutwires[i].type == "XOR" or poutwires[i].type == "xor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = Xor(operands_list)

        elif poutwires[i].type == "XNOR" or poutwires[i].type == "xnor":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[poutwires[i].operands[j].index])
            poutwires_var[i] = Xnor(operands_list)

        elif poutwires[i].type == "MUX" or poutwires[i].type == "mux":
            logging.debug("converts/circuit2bool: has {} operands!".format(len(poutwires[i].operands)))
            for j in range(0, len(poutwires[i].operands)):
                logging.debug("converts/circuit2bool: operand[{}] = {}: a {}".format(j, poutwires[i].operands[j].name, poutwires[i].operands[j].catg))
                if poutwires[i].operands[j].catg == PRIMARY_INPUT:
                    logging.debug(" equal with = VAR_PI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(pin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == KEY_INPUT:
                    logging.debug(" equal with = VAR_KI[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(keyin[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == INTERMEDIATE_WIRE:
                    logging.debug(" equal with = VAR_II[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(interwires_var[poutwires[i].operands[j].index])
                elif poutwires[i].operands[j].catg == PRIMARY_OUTPUT:
                    logging.debug(" equal with = VAR_PO[{}]".format(poutwires[i].operands[j].index))
                    operands_list.append(poutwires_var[interwires[i].operands[j].index])
            poutwires_var[i] = Or(And(Not(operands_list[0]), operands_list[1]), And(operands_list[0], operands_list[2]))

        poutwires_var[i].symbol = poutwires[i].name

    return poutwires_var




