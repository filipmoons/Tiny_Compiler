# -------------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - Function definitions for assembly code generation, starting from
#   an array with quadruples containing TAC-statements
#
# NOTE: The generated assembly x86 code is completely based on the
# book 'Principles of Compiler Design' by Tata McGraw-Hill Education,
# 2010
# -------------------------------------------------------------------

from frontend import *

class LineOfCode:
    def __init__(self, indent, *arg):
        self.indent = indent
        count = 0
        for item in arg:
            if not count:
                self.line = str(item)
                count = 1
            else:
                self.line = self.line + " " + str(item)
        
    def __str__(self):
        if self.indent:
            return "\t" + self.line
        else:
            return self.line

assembly_code = []
indent = False #global variable to keep track of a added line of assembly code must be indented or not
sub_symboltable = None

def generateAssembly(code,symboltable):
    global sub_symboltable
    global assembly_code 
    global indent
    assembly_code = []
    indent = False #global variable to keep track of a added line of assembly code must be indented or not

     #Easy function to add a string element to the assembly_code
    def addline(*arg):
        global assembly_code
        assembly_code.append(LineOfCode(indent,*arg))


    def addfile(filename):
        assemblyfile = open(filename,'r')
        for line in assemblyfile:
            addline(line.rstrip())
        assemblyfile.close()

    def use(item):
        if isinstance(item, int):
            return '$' + str(item)#Automatically add $-signs to numeric values
        else:
            offset = sub_symboltable.var_offset(item) #Replace variables with their offsets
            return str(offset)+'(%ebp)'
                
     
       
    def startIndent():
        global indent
        indent = True

    def stopIndent():
        global indent
        indent = False

    #Loop on the quadruples in code!
    #-------------------------------
    def function(item):
        global sub_symboltable
        addline(".global", item.result)
        addline(".type " + item.result + ", @function")
        addline(item.result + ":")
        startIndent()
        sub_symboltable = symboltable[item.result] #The 'local' symboltable
        addline("push %ebp")
        addline("movl %esp, %ebp")

    def EndFunc(item):
        global sub_symboltable
        addline("movl %ebp, %esp")
        addline("popl %ebp")
        addline("ret")
        sub_symboltable = []
        stopIndent()
     
    def BeginFunc(item):
        addline("subl", use(item.arg1) + ", %esp")
        
    def PushParam(item):
        addline("pushl", use(item.arg1))

    def Goto(item):
        addline("jmp", item.result)

    def Label(item):
        stopIndent()
        addline(item.result, ":")
        startIndent()
        

    def assign(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("movl %eax,", use(item.result))

    def plus(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("addl_", use(item.arg2)+',%eax')
        addline("movl %eax,", use(item.result))

    def substraction(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("subl_", use(item.arg2)+',%eax')
        addline("movl %eax,", item.result)

    def uminus(item):
        addline("movl", use(item.arg1)+',%eax')
        addline('negl %eax')
        addline("movl %eax,", item.result)

    def multiplication(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("imull", item.arg2)
        addline("movl %eax,", item.result)

    def division(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("cltd")
        addline("idivl", item.arg2)
        addline("movl %eax,", item.result)
  
    def assign_address(item):
        addline("leal", use(item.arg1)+',%eax')
        addline("movl %eax,", item.result)

    def LCall_return(item):
        addline("call", item.arg1)
        addline("movl %eax,", item.result)

    def LCall_noreturn(item):
        addline("call", item.arg1)

    def PopParams(item):
        addline("addl", use(item.arg1)+',%esp')
        
    def Return(item):
        addline("movl", use(item.arg1)+',%eax')

    def less(item):
        addline("movl", use(item.arg2)+',%eax')
        addline("cmp %eax,", item.arg1)
        #We jump as the result is zero
        addline("movl $1, %eax")
        addline("movl %eax,", item.result)
        addline("movl $0, %eax")
        addline("cmovl $eax,", item.result)   
    
    def greater(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("cmp %eax,", item.arg2)
        #We jump as the result is zero
        addline("movl $1, %eax")
        addline("movl %eax,", item.result)
        addline("movl $0, %eax")
        addline("cmovl $eax,", item.result)   

    def equal(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("cmp %eax,", item.arg2)
        #We jump as the result is zero
        addline("movl $1, %eax")
        addline("movl %eax,", item.result)
        addline("movl $0, %eax")
        addline("cmove $eax,", item.result)   
        

    def nequal(item):
        addline("movl", use(item.arg1)+',%eax')
        addline("cmp %eax,", item.arg2)
        #We jump as the result is zero
        addline("movl $1, %eax")
        addline("movl %eax,", item.result)
        addline("movl $0, %eax")
        addline("cmovne $eax,", item.result)  

    def not_op(item):
        addline("movl", use(item.arg1)+',%eax') #item.arg1 is a predicate that equals 0 or 1. This function must flip these values.
        addline("cmp %eax,", 0) 
        #We jump as the result is zero
        addline("movl $0, %eax")
        addline("movl %eax,", item.result)
        addline("movl $1, %eax")
        addline("cmove $eax,", item.result)
        

    def IfNode(item):
        addline("movl", use(item.arg1)+',%eax') #item.arg1 is a predicate that equals 0 or 1. This function must flip these values.
        addline("cmp %eax,", 0)
        addline("jz", item.result)
        
    options = {'EndFunc' : EndFunc,
               'BeginFunc' : BeginFunc,
               'PushParam': PushParam,
               'Goto': Goto,
               'Label' : Label,
               'IfNode': IfNode,
               'assign': assign,
               '= LCall': LCall_return,
               'LCall' : LCall_noreturn,
               'Return' : Return,
               '+' : plus,
               '-' : substraction,
               'uminus' : uminus,
               '*' : multiplication,
               '/' : division,
               'assign_address': assign_address,
               'PopParams': PopParams,
               '<' : less,
               '>' : greater,
               '==' : equal,
               '!=' : nequal,
               'not' : not_op,
               'function' : function} 


    #Generating everything
    #-------------------------------
    addline(".section .text")
    addline(".globl _start")
    addline("_start:")
    startIndent()
    addline("call tiny")
    addline("jmp exit")
    stopIndent()
    #We do some conditional includes now:
    print_int = False #avoid to add a function several times
    print_char = False
    read_char = False
    read_int = False
    for item in code:
        if item.arg1 == "print_int" and not print_int:
            addfile("print_int.s")
            print_int = True
            
        elif item.arg1 == "print_char" and not print_char:
            addfile("print_char.s")
            print_char = True

        elif item.arg1 == "read_char" and not read_char:
            addfile("read_char.s")
            read_char = True

        elif item.arg1 == "read_int" and not read_int:
            addfile("read_int.s")
            read_int = True
        
    
    #Here we start looping our code
    for item in code:
        options[item.op](item)
        
    
    addline(".type exit, @function")
    addline("exit:")
    startIndent()
    addline("movl $0, %ebx")
    addline("movl $1, %eax")
    stopIndent()
    final_code = assembly_code
    return final_code

def show_assembly(assembly):
    code_string = ''
    for line in assembly:
        code_string = code_string + str(line) + "\n"
    return code_string
