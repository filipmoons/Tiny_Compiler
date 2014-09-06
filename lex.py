# ------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - The defintions to generate the lexer through lex
# ------------------------------------------------------------



import ply.lex as lex
#Handle reserved words
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'write' : 'WRITE',
   'read' : 'READ',
   'length' : 'LENGTH',
   'while' : 'WHILE',
   'char' : 'CHAR',
   'return' : 'RETURN',
   'int' : 'INT',
   'write' : 'WRITE'
}

# List of token names.
tokens = [
   'NAME', 
   'NUMBER',
   'QCHAR',
   'COMMENT',   
   'NEQUAL',
   'LPAR',
   'RPAR',
   'LBRACE',
   'RBRACE',
   'LBRACK',
   'RBRACK',
   'ASSIGN',
   'SEMICOLON',
   'COMMA',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'EQUAL',
   'GREATER',
   'LESS',
   'NOT'] + list(reserved.values())


def t_IGNORE_comment(t):
    r'///*.*\n'
    t.lexer.lineno += t.value.count('\n')


# Regular expression rules for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAR      = r'\('
t_RPAR      = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACK    = r'\['
t_RBRACK    = r'\]'
t_EQUAL     = r'=='
t_ASSIGN    = r'='
t_SEMICOLON = r';'
t_COMMA     = r'\,'
t_GREATER   = r'>'
t_LESS      = r'<'
t_NEQUAL    = r'!='
t_NOT       = r'!'
t_QCHAR     = r'\'[a-zA-Z0-9_]\''


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()



