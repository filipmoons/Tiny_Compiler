# -------------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - A function to optimize the TAC code using constant folding.
# - A function to optimize the TAC code using dead code elimination.
#   This function checks for each local variable of a function if
#   something more happens with the variable than just declaring
#   it and assigning a value to the variable. If not, the complete
#   variable disappears from the TAC-code. This dead code elimination
#   is easily implemented by traversing the entire symbol table.
# -------------------------------------------------------------------

from frontend import *


#--------------------------------------------
# Helper functions
#--------------------------------------------     



class constant_variable:
    def __init__(self, name, value, line, scope):
        self.name = name
        self.value = value
        self.line = line #'line' (= index) where the constant variable is found. This is important to know, otherwise we could replace values in previous lines of code, which should be avoided at all time. This scenario would change the semantics of the program.
        self.scope = scope #We have to know in which function the local variable is declared. We may not change a variable with the same name in other scope!
    def __eq__(self, other): #for testing if the variable is an element of the constant variables list
        if self.name == other:
            return True
        return False

#Predicate to check if a variable is a tempVar
def is_tempVar(item):
    if "_t" in str(item):
        return True
    return False
    
#Cleanup the temp variables (they must again be re-numbered after an optimalization)
def cleanup_tempVars(code,symboltable):
    def change_tempVar(item, tempCount, tempVars, replaceVars):
    #check if we have tempVar
        if is_tempVar(item) and not(item in tempVars):
            tempVars.append(item)
            newtempVar = "_t" + str(tempCount)
            tempCount += 1
            replaceVars.append(newtempVar)
            symboltable.ChangeName(item, newtempVar)
            return newtempVar, tempCount, tempVars, replaceVars
        elif item in tempVars:
            return replaceVars[tempVars.index(item)], tempCount, tempVars, replaceVars
        else:
            return item, tempCount, tempVars, replaceVars
    
    i = 0
    tempCount = 0
    tempVars = [] #Save the temporary variables that are used in the program (they may not be replaced when they occur)
    replaceVars = [] #List with the replacements of the temporary variables. They share the same indices with tempVars
    for item in code:
        code[i].arg1, tempCount, tempVars, replaceVars  = change_tempVar(item.arg1, tempCount, tempVars, replaceVars)
        code[i].arg2, tempCount, tempVars, replaceVars = change_tempVar(item.arg2, tempCount, tempVars, replaceVars)
        code[i].result, tempCount, tempVars, replaceVars = change_tempVar(item.result, tempCount, tempVars, replaceVars)
        i += 1
    return code,symboltable


#--------------------------------------------
# Optimalizations
#--------------------------------------------     


def constant_folding(code, symboltable):      
    global is_tempVar
    def loop(code, previous_code, symboltable):
        #Find the constant variables
        constant_variables = [] #type to save the constant_variables
        sub_symboltable = None
        binop = ['+', '*', '/', '-'] #A list of the used binary operations, this is handy for if-test
        changed = False #state to indicate if the code was changed
        scope = None        

        for item in code:
            if item.op == "assign" and not item.arg2:
                if is_tempVar(item.result) and isinstance(item.arg1, int): #This kind of code line has to consider the place where it is defined
                    sub_symboltable.var_delete(item.result) #Delete variable in the symboltable. Important for calculating the offsets.
                    constant_variables.append(constant_variable(item.result, item.arg1, code.index(item), scope)) #Here we say line = 0, because this replacement must be preformed everywhere in the scope.
                    code.remove(item) #Delete the quadruple in the code

                elif is_tempVar(item.result): #consant_folding doesn't delete assignments to non-temporary variables, that's left to the  dead code elimination-optimalization
                    sub_symboltable.var_delete(item.result) #Delete variable in the symboltable. Important for calculating the offsets.
                    constant_variables.append(constant_variable(item.result, item.arg1, 0, scope)) #Here we say line = 0, because this replacement must be preformed everywhere in the scope.
                    code.remove(item) #Delete the quadruple in the code

                elif is_tempVar(item.arg1) and not is_tempVar(item.result): #Delete statements of the type a = _t1. _t1 will be replaced by a everywhere
                    sub_symboltable.var_delete(item.arg1)
                    constant_variables.append(constant_variable(item.arg1, item.result,0, scope)) #Here we say line = 0, because this replacement must be preformed everywhere in the scope.
                    code.remove(item)

                else:
                    constant_variables.append(constant_variable(item.result, item.arg1, code.index(item), scope)) #Here we say line = 0, because this replacement must be preformed everywhere in the scope.



                
            if item.op in binop:
                if isinstance(item.arg1, int) and isinstance(item.arg2, int):
                    if item.op == '+':
                        value = item.arg1 + item.arg2
                    elif item.op == "*":
                        value = item.arg1 * item.arg2
                    elif item.op == "/":
                        value = item.arg1 / item.arg2 #This is ok because Python returns an int when dividing two ints.
                    elif item.op == "-":
                        value = item.arg1 - item.arg2
                    code[code.index(item)] = Quadruple('assign', value, None, item.result)
                    changed = True
            
            if item.op == "function":
                sub_symboltable = symboltable[item.result] #The 'local' symboltable to delete variables right
                scope = item.result
            if item.op == "EndFunc":
                sub_symboltable = None
                scope = None
        
        #We loop the entire code to get the offsets straight and to replace to constant variable with his value
        i = 0
    
        for item in code:
            if item.op == "function":
                sub_symboltable = symboltable[item.result] #The 'local' symboltable to calculate the offsets right
                scope = item.result
            if item.op == "EndFunc":
                sub_symboltable = None
                scope = None
            if item.op == "BeginFunc":
                if item.arg1 <> sub_symboltable.Function_size():
                    code[i].arg1 = sub_symboltable.Function_size() #Set the the size of the function right
                    changed = True 
            for var in constant_variables:
                if item.arg1 == var.name and scope == var.scope and code.index(item)>=var.line:
                    code[i].arg1 = var.value
                    changed = True 
                if item.arg2 == var.name and scope == var.scope and code.index(item)>=var.line:
                    code[i].arg2 = var.value
                    changed = True 
                if item.result == var.name and is_tempVar(item.result) and scope == var.scope and code.index(item)>=var.line:
                    code[i].result = var.value
                    changed = True 
            i += 1
            
        #Check if the current code equals the previous code, if so, we stop iterating
        if not changed:
            return code, symboltable
        else:
            return loop(code, code, symboltable) #We keep on iterating our code until no constant variables are left.
    print show_TAC(code)    
    code, symboltable = loop(code, code, symboltable)

    #cleanup
    code,symboltable = cleanup_tempVars(code,symboltable)

    return code, symboltable
    
    

def dead_code_elimination(code, symboltable):
    changed = False
    for function in symboltable.table:
        for var in symboltable[function].subtable:
            #looping on the code:
            happening_more = False #does something exciting happen with the variable (= something else than just declaring and assigning to it?)
            for item in code:
                if item.arg1 == var or item.arg2 == var or (item.result == var and item.op !=  'assign'):
                    happening_more = True
              
            if not happening_more: #the variable does only occur in an assign statement (and a declaration, otherwise it wouldn't be in the symbol table and an error would have been thrown).
                print "ik verwijder" + var
                symboltable[function].var_delete(var) #Delete variable in the symboltable. Important for calculating the offsets.
                i = 0
                scope = None
                for item in code:
                    if item.op == "function":
                        scope = item.result
                    if item.op == "EndFunc":
                        scope = None
                    if item.op == "BeginFunc" and scope == function:
                        if item.arg1 <> symboltable[function].Function_size():
                            code[i].arg1 = symboltable[function].Function_size() #Set the the size of the function right
                            changed = True
                    if item.op == "assign" and str(item.result) == str(var) and scope == function:
                        del code[i] #Delete the quadruples in the code that assign things to our annoying variable.
                        changed = True
                    i += 1
    #cleanup    
    code,symboltable = cleanup_tempVars(code,symboltable)
    print show_TAC(code)
    #Check if the current code equals the previous code, if so, we stop iterating
    if not changed:
        return code, symboltable
    else:
        return dead_code_elimination(code, symboltable)
    
