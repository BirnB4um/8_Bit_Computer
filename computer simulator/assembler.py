import os
os.system("cls")

def error(msg, tags):
    if len(tags) > 0:
        print(f"Error occured in this line:\n" + " ".join(tags))
    print("ERROR: " + msg)
    exit(1)

file = "code.txt"

#read code
ls = []
try:
    with open(file, "r") as f:
        ls = f.read().splitlines()
except:
    error("couldnt find file!", [])


variables = {} #variable addresses
jump_points = {} #jump addresses for labeled addresses
jump_points_for_conditions = []

#clean up code lines & set variables
#TODO: if more than one spaces -> replace all with only one
lines = []
for line in ls:
    line = line.split("#")[0]#strip comment
    if not (line.replace("\t", "").replace(" ", "") == ""):#if no empty line

        if line.strip("\t").split(" ")[0] == "var":#variable definition
            if line.split(" ")[1] in variables.keys():
                error(f"variable '" + str(line.split(" ")[1]) + "' already exits!", line.split(" "))
            try:
                variables[line.split(" ")[1]] = int(line.split(" ")[2])
            except:
                error("dont use '=' to assign a variable a value. use this instead: 'var x 12'", line.split(" "))

        elif line.strip("\t").strip(" ")[0] == ":":#jump-point definition
            jump_points[line.strip("\t").strip(" ").split(" ")[0][1:]] = len(lines)

        else:#code line
            lines.append(line.strip(" "))



#first iteration to set jump-points
for line_i in range(len(lines)):
    line = lines[line_i]

    #if condition
    if line.strip("\t").split(" ")[0] == "if":

        cur_scope = 0
        for c in line:
            if c == '\t':
                cur_scope += 1
            else:
                break
        
        i = line_i+1
        while True:
            if i >= len(lines):
                jump_points_for_conditions.append(i)
                break

            next_scope = 0
            for c in lines[i]:
                if c == '\t':
                    next_scope += 1
                else:
                    break

            if next_scope <= cur_scope:
                jump_points_for_conditions.append(i)
                break
            else:
                i += 1

with open("reduced_code.txt", "w") as f:
    f.write("\n".join(line for line in lines))

print("=== REDUCED CODE: ===")
print("\n".join(line for line in lines)) #print reduced code to console
print("==== END OF CODE ====\n")

#op codes for all commands
commands = {
    "END" : [0, 0, 0, 0, 0],
    "JUMP" : [0, 0, 0, 0, 1],
    "SWAP" : [0, 0, 0, 1, 0],
    "SHOW" : [0, 0, 0, 1, 1],
    "DEBUG" : [0, 0, 1, 0, 0],
    "IDT" : [0, 0, 1, 0, 1],
    "NOT" : [0, 0, 1, 1, 0],
    "OR" : [0, 0, 1, 1, 1],
    "NOR" : [0, 1, 0, 0, 0],
    "XOR" : [0, 1, 0, 0, 1],
    "XNOR" : [0, 1, 0, 1, 0],
    "AND" : [0, 1, 0, 1, 1],
    "NAND" : [0, 1, 1, 0, 0],
    "ADD" : [0, 1, 1, 0, 1],
    "SUB" : [0, 1, 1, 1, 0],
    "MUL" : [0, 1, 1, 1, 1],
    "DIV" : [1, 0, 0, 0, 0],
    "MOD" : [1, 0, 0, 0, 1],
    "SHR" : [1, 0, 0, 1, 0],
    "SHL" : [1, 0, 0, 1, 1],
    "EQL" : [1, 0, 1, 0, 0],
    "NEQ" : [1, 0, 1, 0, 1],
    "LES" : [1, 0, 1, 1, 0],
    "LOE" : [1, 0, 1, 1, 1],
    "GRT" : [1, 1, 0, 0, 0],
    "GOE" : [1, 1, 0, 0, 1],
    "USER_IN" : [1, 1, 0, 1, 0],
    "POPCNT" : [1, 1, 0, 1, 1]
}

#convert a number to a list of 8 bits
def num_to_bin_list(num):
    l = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(-1, -9, -1):
        if bin(num)[i] == '1':
            l[i] = 1
        elif bin(num)[i] == 'b':
            break
    return l

compiled_program = [[0 for n in range(35)] for i in range(256)]


def get_variable(x):
    num = [0, 0]

    if x[0] == '&':
        num[0] = 1
        x = x[1:]
    elif x[0] == '*':
        num[0] = 2
        x = x[1:]

    try:
        num[1] = int(x)
    except:
        if x in variables.keys():
            num[1] = variables[x]
        else:
            error(f"variable '{x}' not defined!", [])
    return num


def set_operator(code_line, var, op_index):
    global compiled_program

    if var[0] == 1:
        compiled_program[code_line][5 + op_index * 10 + 1] = 1
    if var[0] == 2:
        compiled_program[code_line][5 + op_index * 10] = 1
        compiled_program[code_line][5 + op_index * 10 + 1] = 1

    for i in range(len(num_to_bin_list(var[1]))):
        compiled_program[code_line][7 + op_index * 10 + i] = num_to_bin_list(var[1])[i]


def set_op_code(code_line, op):
    global compiled_program

    for i in range(len(commands[op])):
        compiled_program[code_line][i] = commands[op][i]


#compile iteration
cur_line_i = 0
for line in lines:
    line = line.replace("\t", "")
    
    #split line into tags
    tags = line.split(" ")

    if cur_line_i >= 256:
        error("code has more than 256 lines!", [])

    if tags[0] in ["END", "DEBUG", "SWAP"]:
        set_op_code(cur_line_i, tags[0])
        cur_line_i += 1

    elif tags[0] == "JUMP":
        set_op_code(cur_line_i, "JUMP")

        if len(tags) < 2:
            error("JUMP needs a argument!")

        if not (tags[1] in jump_points.keys()):
            error(f"unknown jump address: '{tags[1]}'", tags)

        set_operator(cur_line_i, [0, jump_points[tags[1]]], 0)
        cur_line_i += 1

    elif tags[0] == "SHOW":
        set_op_code(cur_line_i, "SHOW")

        if len(tags) > 2:
            error("too many arguments", tags)
        if len(tags) < 2:
            error("too few arguments", tags)

        set_operator(cur_line_i, get_variable(tags[1]), 1)
        cur_line_i += 1

    elif tags[1] == "=":#zuweisung
        set_operator(cur_line_i, get_variable(tags[0]), 2)

        if len(tags) > 5:
            error("assignment has too many arguments", tags)

        if len(tags) < 3:
            error("assignment has too few arguments!", tags)

        if len(tags) == 3:#IDT
            set_op_code(cur_line_i, "IDT")
            set_operator(cur_line_i, get_variable(tags[2]), 0)

        elif len(tags) == 4:

            if tags[2] == "not": #NOT
                set_op_code(cur_line_i, "NOT")
                set_operator(cur_line_i, get_variable(tags[3]), 0)
            elif tags[2] == "popcnt": #POPCNT
                set_op_code(cur_line_i, "POPCNT")
                set_operator(cur_line_i, get_variable(tags[3]), 0)

        elif tags[3] == "|":#OR
            set_op_code(cur_line_i, "OR")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "!|":#NOR
            set_op_code(cur_line_i, "NOR")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "^":#XOR
            set_op_code(cur_line_i, "XOR")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "!^":#XNOR
            set_op_code(cur_line_i, "XNOR")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "&":#AND
            set_op_code(cur_line_i, "AND")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "!&":#NAND
            set_op_code(cur_line_i, "NAND")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "+":#ADD
            set_op_code(cur_line_i, "ADD")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "-":#SUB
            set_op_code(cur_line_i, "SUB")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "*":#MUL
            set_op_code(cur_line_i, "MUL")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "/":#DIV
            set_op_code(cur_line_i, "DIV")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "%":#MOD
            set_op_code(cur_line_i, "MOD")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == ">>":#SHR
            set_op_code(cur_line_i, "SHR")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)
        
        elif tags[3] == "<<":#SHL
            set_op_code(cur_line_i, "SHL")
            set_operator(cur_line_i, get_variable(tags[2]), 0)
            set_operator(cur_line_i, get_variable(tags[4]), 1)

        else:
            error(f"assignment with unknown operator: '{tags[3] if len(tags) > 4 else tags[2]}'", tags)

        cur_line_i += 1

    elif tags[0] == "if":#condition


        if len(tags) > 4:
            error("too many arguments for condition", tags)
        if len(tags) < 4:
            error("too few arguments for condition", tags)

        set_operator(cur_line_i, [0,jump_points_for_conditions.pop(0)], 0)

        if tags[2] == "==":
            if tags[1] == "USER_IN":
                set_op_code(cur_line_i, "USER_IN")
                set_operator(cur_line_i, [0,0], 2)

                if tags[3] == "UP":
                    set_operator(cur_line_i, [0,1], 1)
                elif tags[3] == "DOWN":
                    set_operator(cur_line_i, [0,2], 1)
                elif tags[3] == "LEFT":
                    set_operator(cur_line_i, [0,4], 1)
                elif tags[3] == "RIGHT":
                    set_operator(cur_line_i, [0,8], 1)
                elif tags[3] == "A":
                    set_operator(cur_line_i, [0,16], 1)
                elif tags[3] == "B":
                    set_operator(cur_line_i, [0,32], 1)

            else:
                set_op_code(cur_line_i, "EQL")
                set_operator(cur_line_i, get_variable(tags[1]), 1)
                set_operator(cur_line_i, get_variable(tags[3]), 2)

        elif tags[2] == "!=":
            set_op_code(cur_line_i, "NEQ")
            set_operator(cur_line_i, get_variable(tags[1]), 1)
            set_operator(cur_line_i, get_variable(tags[3]), 2)
        elif tags[2] == "<":
            set_op_code(cur_line_i, "LES")
            set_operator(cur_line_i, get_variable(tags[1]), 1)
            set_operator(cur_line_i, get_variable(tags[3]), 2)
        elif tags[2] == "<=":
            set_op_code(cur_line_i, "LOE")
            set_operator(cur_line_i, get_variable(tags[1]), 1)
            set_operator(cur_line_i, get_variable(tags[3]), 2)
        elif tags[2] == ">":
            set_op_code(cur_line_i, "GRT")
            set_operator(cur_line_i, get_variable(tags[1]), 1)
            set_operator(cur_line_i, get_variable(tags[3]), 2)
        elif tags[2] == ">=":
            set_op_code(cur_line_i, "GOE")
            set_operator(cur_line_i, get_variable(tags[1]), 1)
            set_operator(cur_line_i, get_variable(tags[3]), 2)
        else:
            error(f"condition with unknown operator: {tags[2]}", tags)

        cur_line_i += 1

    else:
        error("unknown command", tags)

#only flag relevant bits of compiled program (for printing it to the console)
show_compiled_program_lines = [True for i in compiled_program]
if compiled_program[255] == [0 for i in range(35)]:
    for i_ in range(254, -1, -1):
        if compiled_program[i_] == [0 for i in range(35)]:
            show_compiled_program_lines[i_ + 1] = False
        else:
            break

#print compiled program to console
for line_i in range(len(compiled_program)):
    if show_compiled_program_lines[line_i]:
        line = compiled_program[line_i]
        m = "".join(str(l) for l in line[:5]) + " " + "".join(str(l) for l in line[5:7])+ " " + "".join(str(l) for l in line[7:15])+ " " + "".join(str(l) for l in line[15:17])+ " " + "".join(str(l) for l in line[17:25])+ " " + "".join(str(l) for l in line[25:27])+ " " + "".join(str(l) for l in line[27:])
        print(m)


print("Compiled Successfully!")

aaa = []
for line in compiled_program:
    for bit in line:
        aaa.append(bit)
# print(bytes(aaa))

with open("compiled_program.bin", "wb") as file:
    file.write(bytes(aaa))

exit(0)