# ------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
# 
# ------------------------------------------------------------
import ply.yacc as yacc
import lex
import re

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = None
        self.leaf = leaf
    def __str__(self):
        string_children = []
        if self.children and (type(self.children) is list): 
            for child in self.children:
                string_children.append(str(child))
          
        else:
            string_children = self.children

        string_leaf = []
        if self.leaf and (type(self.leaf) is list):
            for leaf in self.leaf:
                string_leaf.append(str(leaf))
        else:
            string_leaf = self.leaf
        return_string = str([self.type,string_children, string_leaf])
        return_string = re.sub('[\\\']', '', return_string)
        return return_string

class Function_Node(Node):
    def __init__(self, return_type, name, formal_pars, block):
        self.type = 'function'
        self.return_type = return_type
        self.name = name
        self.formal_pars = formal_pars
        self.block = block
        self.children = [return_type, name, formal_pars, block]
        self.leaf = None

class If_Node(Node):
    def __init__(self, exp, if_statement):
        self.type = 'if'
        self.exp = exp
        self.if_statement = if_statement
        self.children = [exp, if_statement]
        self.leaf = None

class If_Else_Node(Node):
    def __init__(self, exp, if_statement,else_statement):
        self.type = 'if_else'
        self.exp = exp
        self.if_statement = if_statement
        self.else_statement = else_statement
        self.children = [exp, if_statement,else_statement]
        self.leaf = None

class While_Node(Node):
    def __init__(self, exp, statement):
        self.type = 'while'
        self.exp = exp
        self.statement = statement
        self.children = [exp, statement]
        self.leaf = None
    


tokens = lex.tokens



precedence = (
    ('nonassoc', 'EQUAL', 'NEQUAL', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'), 
)
def p_program_declaration_declarationSTAR(p):
    'program : declaration declarationSTAR'
    p[0]= Node("program", [p[1],p[2]])

def p_program_declaration(p):
    'program : declaration'
    p[0]= Node("program", [p[1]])

def p_declarationSTAR_declaration(p):
    'declarationSTAR : declaration'
    p[0] = Node("declaration", [p[1]])

def p_declarationSTAR_declaration_derclarationSTAR(p):
    'declarationSTAR : declaration declarationSTAR'
    p[0] = Node("declaration", [p[1], p[2]])


def p_declaration(p):
    '''declaration : var_declaration
                   | fun_declaration'''
    p[0] = Node("declaration",[p[1]])

def p_var_declaration(p):
    'var_declaration	: type NAME SEMICOLON'
    p[0] = Node("var_declaration", [], [p[1],p[2]])

def p_fun_declaration(p):
    'fun_declaration : type NAME LPAR formal_pars RPAR block'
    p[0] = Function_Node(p[1], p[2], p[4], p[6])

def p_fun_declaration_noformal(p):
    'fun_declaration : type NAME LPAR RPAR block'
    p[0] = Function_Node(p[1], p[2], Node("formal_pars", None, None) , p[5])

def p_formal_pars_formal_par_formal_parsSTAR(p):
    'formal_pars : formal_par COMMA formal_parsSTAR'
    p[0] = Node("formal_pars", [p[1],p[3]])

def p_formal_pars_formal_par(p):
    'formal_pars : formal_par'
    p[0] = Node("formal_pars", [p[1]])

def p_formal_parsSTAR_formal_par(p):
    'formal_parsSTAR : formal_par'
    p[0] = Node("formal_pars", [p[1]])

def p_formal_parsSTAR_formal_par_formal_parSTAR(p):
    'formal_parsSTAR : formal_par COMMA formal_parsSTAR'
    p[0] = Node("formal_pars", [p[1],p[3]])

def p_formal_par(p):
    'formal_par : type NAME'
    p[0] = Node("formal_par", [], [p[1],p[2]])

def p_block(p):
    'block : LBRACE var_declarationSTAR statements RBRACE'
    p[0] = Node("block", [p[2], p[3]])

def p_block_withoutVarDeclaration(p):
    'block : LBRACE statements RBRACE'
    p[0] = Node("block", [Node("var_declarations", None, None), p[2]])
    
def p_var_declarationSTAR_var_declaration(p):
    'var_declarationSTAR : var_declaration'
    p[0] = Node("var_declarations", [p[1]])

def p_var_declarationSTAR_var_declaration_var_derclarationSTAR(p):
    'var_declarationSTAR : var_declaration var_declarationSTAR'
    p[0] = Node("var_declarations", [p[1], p[2]])


def p_statements_statement_statementsSTAR(p):
    'statements : statement SEMICOLON statementsSTAR'
    p[0] = Node("statement_list", [p[1],p[3]])

def p_statements_statement(p):
    'statements : statement SEMICOLON'
    p[0] = Node("statement_list", [p[1]])

def p_statementsSTAR_statement(p):
    'statementsSTAR : statement SEMICOLON'
    p[0] = Node("statement_list", [p[1]])

def p_statementsSTAR_statement_statementsSTAR(p):
    'statementsSTAR : statement SEMICOLON statementsSTAR'
    p[0] = Node("statement_list", [p[1],p[3]])

def p_statement_IF(p):
    'statement : IF LPAR exp RPAR statement'
    p[0] = If_Node(p[3], p[5])

def p_statement_IF_ELSE(p):
    'statement : IF LPAR exp RPAR statement ELSE statement'
    p[0] = If_Else_Node(p[3], p[5], p[7])

def p_statement_WHILE(p):
    'statement : WHILE LPAR exp RPAR statement'
    p[0] = While_Node(p[3], p[5])

def p_statement_WRITE(p):
    'statement : WRITE exp'
    p[0] = Node("write", [p[2]])

def p_statement_READ(p):
    'statement : READ exp'
    p[0] = Node("read", [p[2]])

def p_statement_lexp_ASSIGN_exp(p):
    'statement : lexp ASSIGN exp'
    p[0] = Node("assign", [p[1],p[3]])

def p_statement_RETURN_exp(p):
    'statement : RETURN exp'
    p[0] = Node("return", [p[2]])

def p_statement_NAME_LPAR_pas_RPAR(p):
    'statement : NAME LPAR pars RPAR'
    p[0] = Node("call_function", [p[1],p[3]])
    
def p_exp_NUMBER(p):
    'exp : NUMBER'
    p[0] = Node("number", None, p[1])

def p_exp_QCHAR(p):
    'exp : QCHAR'
    p[0] = Node("qchar", None, p[1])


def p_exp_binop_exp(p):
    'exp : exp binop exp'
    p[0] = Node("binop", [p[1], p[3]], p[2])

def p_exp_unup(p):
    'exp : unop exp'
    p[0] = Node("unup", [p[2]], p[1])

def p_exp_lexp(p):
    'exp : lexp'
    p[0] = p[1]

def p_unup(p):
    '''unop	: MINUS
		| NOT'''
    p[0] = p[1]

def p_LPAR_exp_RPAR(p):
    'exp : LPAR exp RPAR'
    p[0] = p[2] #Voorrangsregels checken!

def p_exp_NAME_LPAR_pas_RPAR(p):
    'exp : NAME LPAR pars RPAR'
    p[0] = Node("call_function", [p[1],p[3]])

    
def p_binop(p):
    '''binop : MINUS
	     | PLUS
	     | TIMES
	     | DIVIDE
	     | EQUAL
	     | NEQUAL
	     | GREATER
	     | LESS'''
    p[0] = p[1]

def p_pars_par_parsSTAR(p):
    'pars : exp COMMA parsSTAR'
    p[0] = Node("pars", [p[1],p[3]])

def p_pars_par(p):
    'pars : exp'
    p[0] = Node("pars", [p[1]])

def p_parsSTAR_par(p):
    'parsSTAR : exp'
    p[0] = Node("pars", [p[1]])

def p_parsSTAR_par_parSTAR(p):
    'parsSTAR : exp COMMA parsSTAR'
    p[0] = Node("pars", [p[1],p[3]])

    
def p_type(p):
    '''type : INT
            | CHAR'''
    p[0] = p[1]

def p_lexp(p):
    'lexp : var'
    p[0] = Node("var", None, p[1])

def p_var(p):
    'var : NAME'
    p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc(debug=1)

def parse(data,debug=0):
    parser.error = 0
    p = parser.parse(data,debug=debug)
    if parser.error: return None
    return p
