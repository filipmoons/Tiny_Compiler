# -------------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - This file compiles the defined 'data'-variable. The compiling process
# can be followed in the terminal, every intermediate step will be outputted
# (output of the lexer, syntax tree, TAC & assembly). The only difference
# from the main.py-file is that all the output is printed in the terminal
# and no GUI is used. Therefore, this source file is particularly handy
# to test compiler output during the development stage of this compiler.
#
# NOTE: The generated assembly x86 code is completely based on the
# book 'Principles of Compiler Design' by Tata McGraw-Hill Education,
# 2010
# -------------------------------------------------------------------


#Import compiler elements
from lex import *
from yacc import *
import frontend as frontend
import frontend_optimalizations as optimalization
import backend as backend

data4 = '''
int tiny(){
int x;
int y;
x = 1 + 2;
y = 3 + 4;
return x + y;
x = 10;
x = 3;
y = 4;
}'''


dataf = '''int go(int b){
int a;
a = 4;
b = a + 3;
}

int main(){
int c;
int x;
c = go(5);
x = 5;
}'''

datax = '''int factorial(int f)
{
int min;
int value;
int volgend;
min = f - 1;
volgend = factorial(min);
value = f*volgend;
if(f==0) return 0 else return value;
}

int tiny()
{
int input;
read input;
write factorial(input);
}'''

data = '''int fib(n){
	int vorig;
	int vorigvorig;
	int uitkomst
	if n < 2 return n;
	vorig = fib(n-1);
	vorigvorig = fib(n-2);
	uitkomst = vorig + vorigvorig;
	return uitkomst;
}

int tiny(){
	int input;
	int output;
	read input;
	output = fib(input);
	write output;
}'''


data1 = '''int go(){
int a;
int[4] b;
a = length b;
if(a > 3) a = 5 else write 5;
write a;
while(a > 99) a = 66;
}'''

data2 = '''
int go(){
char[2] a;
write 'c';
}
int main() {
write 4;
write 25*-25; 
}'''



# Give the lexer some input
lexer.input(data)

# Tokenize
print("Output Lexer")
print("============")
print("")
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok

#Build parse tree
tree = yacc.parse(data, 0)
print("")
print("Syntax tree")
print("===========")
print("")
print tree
#Traverse tree for TAC-generation
code, symboltable = frontend.generateTAC(tree)
print("")
print("Tree address code")
print("=================")
print("")
print frontend.show_TAC(code)
#Constant folding optimalization
code, symboltable = optimalization.constant_folding(code, symboltable)
print("")
print("Constant folding optimalization")
print("===============================")
print("")
print frontend.show_TAC(code)
#Dead code elimination
code, symboltable = optimalization.dead_code_elimination(code, symboltable)
print("")
print("Dead code elimination")
print("=====================")
print("")
print frontend.show_TAC(code)
#Generate assembly code
print("")
print("Assembly code")
print("=============")
print("")
assembly = backend.generateAssembly(code,symboltable)
print backend.show_assembly(assembly)
