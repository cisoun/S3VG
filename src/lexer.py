import ply.lex as lex

reserved_words = (
	'var',
	'for'
)

methods = (
	'circle',
	'line',
	'pgone',
	'pline',
	'rect',
	'text',
	'setPage',
	'setUnit',
	'setFont',
	'setOpacity',
	'fillColor',
	'strokeColor',
	'strokeWidth'
)

tokens = (
	'IDENTIFIER',
	'METHOD',
	'NUMBER',
	'STRING',
	'EQUALS',
	'SEMICOLON',
	'COMMA',
	'ADD_OP',
	'MIN_OP',
	'MUL_OP',
	'DIV_OP',
	'MOD_OP'
) + tuple(map(lambda s:s.upper(), methods)) + tuple(map(lambda s:s.upper(), reserved_words))

literals = '();={}'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_COMMA = r','
t_ignore  = ' \t'

def t_ADD_OP(t):
	r'\+'
	return t

def t_MIN_OP(t):
	r'\-'
	return t
	
def t_MUL_OP(t):
	r'\*'
	return t

def t_DIV_OP(t):
	r'\/'
	return t

def t_MOD_OP(t):
	r'%'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_STRING(t):
	r'"[^"]*"'
	t.value = t.value[1:-1]
	return t

#def t_METHOD(t):
#	r'[A-Za-z0-9_]+'
#	if t.value in methods:
#		t.type = t.value.upper()
#	return t

def t_IDENTIFIER(t):
	r'[A-Za-z0-9_]+'
	if t.value in reserved_words + methods:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
