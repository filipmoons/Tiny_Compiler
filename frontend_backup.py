# ------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - Function definitions for intermediate code generation to TAC (Three
#   adress code). The syntax three is traversed to (1) build a symbol
#   table and (2) to generate recursively TAC-code. This method is called
#   Syntax Directed Translation (SDT).
#
# - Operations to traverse the syntax three easily, are defined in the
#   yacc.py source file.
# ------------------------------------------------------------


from yacc import *
import collections #To use OrderedDict (ordered directionaries)
    


class SymbolTable_Entry:
    def __init__(self, name, typi):
        self.name = name
        self.type = typi

class SymbolTable_Var_Entry(SymbolTable_Entry):
    def __init__(self, name, typi, num_of_elements = 0):
        self.name = name
        self.type = typi
        self.num_of_elements = num_of_elements + 1 #We assume as an array is declared, by example int[6], we get as num_of_elements 6, but in fact, there are 7 elements (we start counting from zero).
    def offset(self):
        if self.type == "int":
            return self.num_of_elements*4
        elif self.type == "char":
            return self.num_of_elements*1
    def width(self):
        if self.type == "int":
            return 4
        elif self.type == "char":
            return 1

class SymbolTable_Function_Entry(SymbolTable_Entry):
    def __init__(self, name, typi):
        self.name = name
        self.type = typi
        self.FormalParams = collections.OrderedDict() #Symbol table is implemented as an ordered dictionary of SymbolTable_Entry-objects
        self.subtable = collections.OrderedDict() #Symbol table is implemented as an ordered dictionary of SymbolTable_Entry-objects. You might expect here an instance of the SymbolTable-class, but this would be a bit exaggerated because you can only have 1 level of subscoping.
        self.current_FormalParams = False #state to check if we have to add var declarations to the formal params or not

    def StartFormalParamsDeclarations(self):
        self.current_FormalParams = True

    def StopFormalParamsDeclarations(self):
        self.current_FormalParams = False

    def AddEntry(self, name, typi, num_of_elements):
        if self.current_FormalParams:
            self.FormalParams[name] = SymbolTable_Var_Entry(name, typi, num_of_elements)
        else:
            self.subtable[name] = SymbolTable_Var_Entry(name, typi, num_of_elements)

    def FormalParams_offset(self):
        offset = 0
        for key in self.FormalParams:
            offset = offset + self.FormalParams[key].offset()
        return offset
    
    def Function_offset(self):
        offset = 0
        for key in self.subtable:
            offset = offset + self.subtable[key].offset()
        return offset

    def Return_offset(self):
        if self.type == "int":
            return 4
        elif self.type == "char":
            return 1
        else:
            return 0
    
    def __getitem__(self, index):
        return self.subtable[index]
        

        
class SymbolTable:
    #-----------------------------------
    #Subclasses for SymbolTable-entries
    #-----------------------------------

    #-----------------------------------
    #'Head' class definition
    #-----------OrderedDic------------------------      
    def __init__(self):
        self.table = collections.OrderedDict() #Symbol table is implemented as a as an ordered dictionary directory of SymbolTable_Entry-objects. We use an ordered dictionary instead of a regular dictionary, because we must be able to traverse the entries in the order in which they are added. A regular dictionary doesn't keep trac of this.
        self.CurrentSubScope = None #State to known if the syntax tree traversal is within a subscope (only one subscope can occur in our language),when CurrentSubScope isn't equal to 'None', we are currently adding entries to a subscope.
        self.offset = 0
        
    def NewSubScope(self, name, typi):
        self.CurrentSubScope = name #We change the state of the symbol table to know that the next entries must be added to the current sub scope (i.e. the current symboltable_function_entry)
        self.table[name] = SymbolTable_Function_Entry(name, typi)

    def AddEntry(self, name, typi, num_of_elements = 0): #Actually, we know for sure this method will only be called for var declarations, function declarations would always use the NewSubScope().
        if self.CurrentSubScope:
            self.table[self.CurrentSubScope].AddEntry(name, typi, num_of_elements)
        else:
            self.table[name] = SymbolTable_Var_Entry(name, typi, num_of_elements)
    
    def StopSubScope(self):
        self.CurrentSubScope = None

    def VariableExists(self, variable): #This function checks if a variable is declared in the symbol table in the proper scope. Useful for a semantic check.
        if self.CurrentSubScope:
            if (variable in self.table[self.CurrentSubScope].subtable) or (variable in self.table[self.CurrentSubScope].FormalParams):
                return True
        else:
            if variable in self.table:
                return True
        return False
    
    def __getitem__(self, index):
        if index in self.table:
            return self.table[index] #Check if the asked entry is in the main table, if true, return it
        else:
            return self.table[self.CurrentSubScope].subtable[index]
        
        


symboltable = SymbolTable()

tempVariableCount = -1
tempLabelCount = -1

def newtemp(type):
    global symboltable
    global tempVariableCount
    tempVariableCount = tempVariableCount + 1
    tempVar = "_t" + str(tempVariableCount)
    symboltable.AddEntry(tempVar, type)
    return tempVar
    
def newlabel():
    global tempLabelCount
    tempLabelCount = tempLabelCount + 1
    return "_L" + str(tempLabelCount)


class Quadruple:
    def __init__(self, op, arg1, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result


def codeGenerator(code, op, arg1=None, arg2=None, result=None):
    code.append(Quadruple(op,arg1,arg2,result))

def codeAdd(code, string):
    code.append(string)


def traversal(tree,code):
    global tempVariableCount
    global symboltable
    global tempLabelCount
        
        
    def ExactTwoChildren():
        MaxTwoChildren(2)
         
    def MaxTwoChildren(NumberOfChildren):
        print NumberOfChildren
        if NumberOfChildren == 1:
            traversal(tree.children[0],code)
        elif NumberOfChildren <> 0:
            traversal(tree.children[0],code)
            traversal(tree.children[1],code)
       
    def program():
        print("Program")
        #Two possible types: Node("program", [p[1]]) or Node("program", [p[1],p[2]])
        MaxTwoChildren(NumberOfChildren(tree))        

    def declaration():
        print("Declaratie!")
        #Two possible types: Node("declaration", [p[1]]) or Node("declaration", [p[1],p[2]])
        MaxTwoChildren(NumberOfChildren(tree))

    def pars():
        MaxTwoChildren(NumberOfChildren(tree))

    def block():
        print("Block!")
        #Two possible types: Node("block", [Node("var_declarations", None, None), p[2]]), Node("block", [p[2], p[3]]), which actually results in just one type. This function is not responsible of solving the no var_declarations issue.
        ExactTwoChildren()
    
    def var_declarations():
        print("Var declarations!")
        #Three possible types: Node("var_declarations", [p[1]]), Node("var_declarations", [p[1],p[2]]) or Node("var_declarations", None, None)
        if(tree.children):
                MaxTwoChildren(NumberOfChildren(tree)) #We ommit the Node("var_declarations", None, None) type
    
    def var_declaration():
        print("Var declaration!")
        #One possible type: p[0] = Node("var_declaration", [], [p[1],p[2]])
        #We suppose here that a var of type 'int' has an offset of 4 byte and a var of type 'char has an offset of 1 byte
        #An array has an offset of number_of_elements*offset_of_type
        if tree.leaf[0] == 'int' or tree.leaf[0] == 'char':
            symboltable.AddEntry(tree.leaf[1], tree.leaf[0])
        elif tree.leaf[0].type == 'array_type':
            print("We hebben een array vast!")
            #One possible type: Node("array_type", p[3], p[1])
            symboltable.AddEntry(tree.leaf[1], tree.leaf[0].leaf, tree.leaf[0].children)
            
        
    def assign():
        #One possible type:Node("assign", [p[1],p[3]])
        #We can actually do a type check here, if we would like
        what_to_assign = traversal(tree.children[1], code)
        assign_to = traversal(tree.children[0], code)
        codeGenerator(code, "=", what_to_assign, None, assign_to)

    def var():
        #One possible type: Node("var", None, p[1])
        #Here we do also a little semantic check: is this variable already declared?
        if(symboltable.VariableExists(tree.leaf)):
            return tree.leaf
        else:
            raise Exception("The variable " + tree.leaf + " wasn't declared in the function " + symboltable.CurrentSubScope)


    def array():
        print("Array!")
        #One type: lexp : lexp LBRACK exp RBRACK -> Node("array", [p[3]], [p[1]])
        index = traversal(tree.children[0],code)
        print index
        which_array = traversal(tree.leaf[0],code)
        print which_array
        tempVar = newtemp('int')
        width_one_array_element = symboltable[which_array].width()
        codeGenerator(code, 'assign', width_one_array_element, None, tempVar)
        tempVar2 = newtemp('int')
        codeGenerator(code, '*', tempVar, index, tempVar2)
        tempVar3 = newtemp('int')
        codeGenerator(code, '+', which_array, tempVar2, tempVar3)
        tempVar4 = newtemp('int')
        codeGenerator(code, 'assign', '*(' + tempVar3 + ')', None, tempVar4)
        return tempVar4


    def statement_list():
        print("Statement list")
        #Two possible types: Node("statement_list", [p[1],p[3]]), Node("statement_list", [p[1]])
        MaxTwoChildren(NumberOfChildren(tree))

    def return_node():
        #Node("return", [p[2]])
        what_to_return = traversal(tree.children[0],code)
        codeGenerator(code, "Return", what_to_return)

    def write():
        print("Write!")
        #One possible type: Node("write", [p[2]])
        what_to_write = traversal(tree.children[0],code)
        what_to_write_type = symboltable[what_to_write].type
        codeGenerator(code, "PushParam", what_to_write)
        if what_to_write_type == "int":
            codeGenerator(code, "LCall", "_PrintInt")
            codeGenerator(code, "PopParams", 4)
        else:
            codeGenerator(code, "LCall", "_PrintChar")
            codeGenerator(code, "PopParams", 1)

    def binop():
        print("Binop!")
        #One possible type: Node("binop", [p[1], p[3]], p[2])
        op = tree.leaf
        arg1 = traversal(tree.children[0],code)
        arg2 = traversal(tree.children[1],code)
        tempVar = newtemp('int')
        print arg1
        print arg2
        codeGenerator(code, op, arg1, arg2, tempVar)
        return tempVar

    def unop():
        #One possible type: Node("unup", [p[2]], p[1])
        op = 'uminus'
        arg1 = traversal(tree.children[0],code)
        tempVar = newtemp('int')

        codeGenerator(code, op, arg1, None, tempVar)
        return tempVar

    def number():
        print("Number!")
        #One possible type: Node("number", None, p[1])
        op = 'assign'
        arg1 = tree.leaf
        arg2 = None
        tempVar = newtemp('int')
        print tempVar
        codeGenerator(code, op, tree.leaf, None, tempVar)
        return tempVar

    def qchar():
        #One possible type: Node("qchar", None, p[1])
        op = 'assign'
        arg1 = tree.leaf
        arg2 = None
        tempVar = newtemp('char')
        print tempVar
        codeGenerator(code, op, tree.leaf, None, tempVar)
        return tempVar

    def if_node():
        #Only type: If_Node(exp, if_statement)
        predicate = traversal(tree.exp, code)
        newLabel = newlabel()
        codeGenerator(code, "IfNode", predicate, None, newLabel)
        traversal(tree.if_statement,code)
        codeGenerator(code, "Label", None, None, newLabel)

    def if_else_node():
        #Only type: If_Else_Node(exp, if_statement,else_statement):
        predicate = traversal(tree.exp, code)
        falseLabel = newlabel()
        returnLabel = newlabel()
        codeGenerator(code, "IfNode", predicate, None, falseLabel)
        traversal(tree.if_statement,code)
        codeGenerator(code, "Goto", None, None, returnLabel)
        codeGenerator(code, "Label", None, None, falseLabel)
        traversal(tree.else_statement,code)
        codeGenerator(code, "Label", None, None, returnLabel)

    def while_node():
        #only type: While_Node(exp, statement)
        predicateLabel = newlabel()
        codeGenerator(code, "Label", None, None, predicateLabel)
        predicate = traversal(tree.exp, code)
        returnLabel = newlabel()
        codeGenerator(code, "IfNode", predicate, None, returnLabel)
        traversal(tree.statement,code)
        codeGenerator(code, "Goto", None, None, predicateLabel)
        codeGenerator(code, "Label", None, None, returnLabel)

    def length():
        #Node("length", p[2])
        length_var = symboltable[tree.children[0].leaf].num_of_elements
        tempVar = newtemp('int')
        codeGenerator(code, 'assign', length_var, None, tempVar)
        return tempVar

    def call_function():
        #FunctionCall_Node(function_name,pars)
        tempVar = newtemp(symboltable[tree.function_name].type)
        #The params must be declared in a reversed order following the LIFO-principle, so we temporarily use an array with the subcode for the pars. We will use an iteration in reversed order on this subcode to push the parameters in this right order.  
        subcode = []
        traversal(tree.pars,subcode)
        code.extend(subcode)
        check_offset = 0 #This variable is used to do a little type check, this type check verifies if the number of actual params is equal to the number of formal params. The sum of the offsets of the actual params must eventually equal the offset of the formal params of the function. 
        for item in reversed(subcode): #Push the actual params in reversed order (LIFO-principle)
            codeGenerator(code, "PushParam", item.result)
            check_offset = check_offset + symboltable[item.result].offset()
        codeGenerator(code, "= LCall", tree.function_name, None, tempVar)
        codeGenerator(code, "TO_CHECK_FormalParamsOffset", "PopParams", tree.function_name, check_offset) #We CAN'T be sure that the offset of the formal parameters is already known, because we don't know whether the called function is already defined or not. So, we add to the code a "labeled" (with "TO_CHECK") quadruple to be replaced by the then surely known information in a next iteration. In this iteration, we also do the type check.
        return tempVar
           
    def function():
        print("Function")
        #Only possible type: Function_Node(self, return_type, name, formal_pars, block)
        symboltable.NewSubScope(tree.name, tree.return_type)
        #Start declaration of formal paramaters
        symboltable[tree.name].StartFormalParamsDeclarations()
        formalparamscode = [] #Normally, this array will stay empty: var declarations don't create any real code, it only adds entries to the symbol table. Anyway, we will not use this 'code array'.  
        traversal(tree.formal_pars,code)
        symboltable[tree.name].StopFormalParamsDeclarations()
        #Start real code for the function body
        codeGenerator(code,tree.name)
        codeGenerator(code,"TO_CHECK_FunctionOffset", "BeginFunc", tree.name) #We don't know the offset of the function yet, because the code of the function body has yet to be generated. This information will be added in an iteration of the code after the complete tree traversal.
        traversal(tree.block,code)
        symboltable.StopSubScope()
        codeGenerator(code,"EndFunc")
        
        
    options = {'declaration' : declaration,
               'program': program,
               'function': function,
               'block': block,
               'var_declarations' : var_declarations,
               'var_declaration' : var_declaration,
               'function' : function,
               'number' : number,
               'binop': binop,
               'write': write,
               'statement_list' : statement_list,
               'unop' : unop,
               'assign' : assign,
               'var' : var,
               'qchar' : qchar,
               'array' : array,
               'if' : if_node,
               'if_else' : if_else_node,
               'while': while_node,
               'length' : length,
               'return' : return_node,
               'formal_pars': pars,
               'call_function': call_function,
               'pars' : pars
               }
  
    print tree
    
    return options[tree.type]()


def generateTAC(tree):
    code = []
    global tempVariableCount
    global symboltable
    global tempLabelCount
    tempVariableCount = -1
    tempLabelcount = -1
    symboltable = SymbolTable()
    traversal(tree,code)
    #this iteration of the quadruples is needed to replace the labeled quadruples (with "TO_CHECK") by normal quadruples containig information of the symbol table. This information can only be added now, because we couldn't know whether this information was available or not during the tree traversal.
    i = 0
    for item in code:
        if item.op == "TO_CHECK_FormalParamsOffset":
            FormalParamsOffset = symboltable[item.arg2].FormalParams_offset()
            if FormalParamsOffset == item.result: #item.result contains the check_offset-value
                code[i] = Quadruple(item.arg1, FormalParamsOffset)
            else:
                raise Exception("A function call of " + item.arg2 + " is illegal. Check if the number of actual parameters equals the number of formal parameters.")
            
        elif item.op == "TO_CHECK_FunctionOffset":
            code[i] = Quadruple(item.arg1, symboltable[item.arg2].Function_offset())
        i += 1
    return code

def show_code(code):
    return_string = ''
    for item in code:
        op = str(item.op)
        arg1 = str(item.arg1)
        arg2 = str(item.arg2)
        result = str(item.result)
        if item.op and item.arg1 and item.arg2 and item.result:
            return_string = return_string + "\t" +  result + " = " + arg1 + " " + op + " " + arg2 + ";\n"

        elif item.op == "IfNode":
            return_string = return_string + "\t" + "IfZ " + arg1 + " Goto " + result + ";\n"

        elif item.op and item.arg1 and item.result:
            return_string = return_string + "\t" +  result + " = "
            if op == "uminus":
                return_string = return_string + "-" + arg1 + ";\n"
            else:
                return_string = return_string +  arg1 + ";\n"
        elif item.op and item.arg1:
            return_string = return_string + "\t" + op + " "+ arg1 + ";\n"
        elif item.op:
            if op == "EndFunc":
                return_string = return_string + "\t" + "EndFunc" + ";\n"
            elif op == "Label":
                return_string = return_string + result + ":"
            elif op == "Goto":
                return_string = return_string + "\t" +  "Goto " + result + ";\n"
            else:
                return_string = return_string + op + ":\n"
    return return_string


