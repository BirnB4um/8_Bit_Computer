# 8_Bit_Computer

Assembler and simulator for a 8 Bit Computer made in [CircuitGrid](https://github.com/BirnB4um/CircuitGrid)


## Docs:


Everything after a &#35; is a comment.  
```
# this is a comment
```
---
<br>

Operands can be constants, variables(&) or pointer(*):  
```
# Example for constant: 
x = 69  #set x to 69

# Example for variable: 
x = &y  #set x to the value in y

# Example for pointer: 
x = *y  #set x to the value in the address stored in y
```  
---

Operations can't be concatenated! 
```
x = 1 + 3 + 5 #not okay :(

x = 1 + 3 #okay :)
x = &x + 5 #okay :)

if &x + 1 == 2 #not okay :(

```

---
<br>

The Preprocessor replaces all variables with their addresses. 
So this...
```
var x 0
var y 1

x = y
&x = 2
```
...will be converted to this...
```
0 = 1
&0 = 2
```
which will set the value in address 0 to 1  
and sets the value in the address, which is stored at address 0, to 2.  
After execution address 0 has value 1 and address 1 has value 2

---
<br>

Labels can be defined with a colon 
```
:main
JUMP main
```
---
<br>

If conditions run the next indented scope if the condition is true.  
Indentations have to be Tabs!

```
if &x >= 2
    #do something
    y = 1 + 1
```
---
<br>

Checking user input:  
All USER_IN values: UP, DOWN, LEFT, RIGHT, A, B  
Example for USER_IN if condition:
```
if USER_IN == DOWN
    #do something
```

<br>
<br>

# Keywords

| Keyword | Description | Example |
| --- | --- | --- |
| var | declares a variable and its address | var x 0 |
| END | ends the program | END |
| JUMP | jump to a label | JUMP main |
| SWAP | updates the screen with the last 32 bytes in RAM | SWAP |
| SHOW | displays the given value | SHOW &x |
| DEBUG | pauses the execution (Breakpoint) | DEBUG |
| << | bitshift left | x = &y << 3 |
| >> | bitshit right | x = &y >> 3 |
| = | assigns a value | x = 42 |
| + | adds two values | x = &x + &y |
| - | subtracts two values | x = &x - &y |
| * | multiplies two values | x = &x * &y |
| / | divides two values | x = &x / &y |
| % | modulo operation | x = &x % 2 |
| not | bitwise NOT | x = not &y |
| &#124; | bitwise OR | x = 12 &#124; 6 |
| !&#124; | bitwise NOR | x = 12 !&#124; 6 |
| ^ | bitwise XOR | x = 12 ^ 6 |
| !^ | bitwise XNOR | x = 12 !^ 6 |
| & | bitwise AND | x = 12 & 6 |
| !& | bitwise NAND | x = 12 !& 6 |
| popcnt | gets the number of ones in value | x = popcnt 69 |
| if | checks a condition | if &x != 2 |
| if | checks user input | if USER_IN == UP |


Some example scripts are in *"computer simulator/code_archive"*  

Errors from compilation dont always make sense because i didn't bother to write error-handeling for every case