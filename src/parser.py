import ply.yacc as yacc

from lexer import tokens
import AST
from AST import addToClass

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
	'%' : lambda x,y: x%y
}

precedence = (
    ('left', 'ADD_OP', 'SUB_OP'),
    ('left', 'MUL_OP', 'DIV_OP'),
)

def p_program_statement(p):
	''' 
		program : statement SEMICOLON
		| structure
	'''
	p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
	'''
		program : statement SEMICOLON program
		| structure program
	'''
	if len(p) > 3:
		p[0] = AST.ProgramNode([p[1]] + p[3].children)
	else:
		p[0] = AST.ProgramNode([p[1]] + p[2].children)

def p_for(p):
	''' structure : FOR IDENTIFIER EQUALS NUMBER TO NUMBER '{' program '}' '''
	p[0] = AST.ForNode((AST.TokenNode(p[2]), AST.TokenNode(p[4]), AST.TokenNode(p[6]), p[8]))


def p_assignment(p):
	'''
		assignation : VAR IDENTIFIER EQUALS expression
		| IDENTIFIER EQUALS expression
	'''
	if len(p) > 4:
		p[0] = AST.AssignNode((AST.TokenNode(p[2]), p[4]))
	else:
		p[0] = AST.AssignNode((AST.TokenNode(p[1]), p[3]))

def p_assignment_coords(p):
	'''	assignation : COORDS IDENTIFIER '''
	p[0] = AST.CoordsNode(p[2])


def p_expression(p):
	''' expression : expression COMMA '''
	p[0] = AST.TokenNode(p[1])

def p_expression_identifier(p):
	'''
		expression : IDENTIFIER
		| NUMBER
		| STRING
	'''
	p[0] = AST.TokenNode(p[1])

def p_expression_statement(p):
	'''
		expression : statement
	'''
	p[0] = p[1]

def p_expression_parenthesis(p):
    ''' expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_op(p):
	'''
		expression : expression ADD_OP expression
		| expression SUB_OP expression
		| expression MUL_OP expression
		| expression DIV_OP expression
		| expression MOD_OP expression
	'''
	p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_arguments(p):
	''' arguments : '(' arguments ')' '''
	p[0] = p[2]

def p_argument_recursive(p):
	''' arguments : expression COMMA arguments
		| expression '''
	if len(p) > 2:
		p[0] = AST.ArgumentsNode([p[1]] + p[3].children)
	else:
		p[0] = AST.ArgumentsNode(p[1])

def p_statement(p):
	''' 
		statement : assignation
		| structure
	'''
	p[0] = p[1]

def p_statement_coordscallback(p):
	''' statement : IDENTIFIER DOT IDENTIFIER arguments '''
	p[0] = AST.CoordsCallbackNode((AST.CoordsNode(p[1]), AST.TokenNode(p[3]), p[4]))
	

#
# S3VG objects
#



#
# S3VG methods
#

def p_statement_fillcolor(p):
    ''' statement : FILLCOLOR arguments '''
    p[0] = AST.FillColorNode(p[2])

def p_statement_circle(p):
    ''' statement : CIRCLE arguments '''
    p[0] = AST.CircleNode(p[2])

def p_statement_line(p):
    ''' statement : LINE arguments '''
    p[0] = AST.LineNode(p[2])

def p_statement_pgon(p):
    ''' statement : PGON arguments '''
    p[0] = AST.PgonNode(p[2])

def p_statement_pline(p):
    ''' statement : PLINE arguments '''
    p[0] = AST.PlineNode(p[2])

def p_statement_text(p):
    ''' statement : TEXT arguments '''
    p[0] = AST.TextNode(p[2])

def p_statement_rect(p):
    ''' statement : RECT arguments '''
    p[0] = AST.RectNode(p[2])

def p_statement_setpage(p):
    ''' statement : SETPAGE arguments '''
    p[0] = AST.SetPageNode(p[2])

def p_statement_setfont(p):
    ''' statement : SETFONT arguments '''
    p[0] = AST.SetFontNode(p[2])

def p_statement_setopacity(p):
    ''' statement : SETOPACITY arguments '''
    p[0] = AST.SetOpacityNode(p[2])

def p_statement_strokecolor(p):
    ''' statement : STROKECOLOR arguments '''
    p[0] = AST.StrokeColorNode(p[2])

def p_statement_strokewidth(p):
    ''' statement : STROKEWIDTH arguments '''
    p[0] = AST.StrokeWidthNode(p[2])

def p_statement_torbg(p):
	''' statement : TORGB arguments '''
	p[0] = AST.ToRGBNode(p[2])


def p_statement_print(p):
    ''' statement : PRINT arguments '''
    p[0] = AST.PrintNode(p[2])

def p_error(p):
	print("Syntax error at '%s'" % p.value)
	yacc.errok()

def parse(program):
    return yacc.parse(program)

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

#@addToClass(AST.ForNode)
#def thread(self, lastNode):
#    beforeCond = lastNode
#    exitCond = self.children[0].thread(lastNode)
#    exitCond.addNext(self)
#    exitBody = self.children[1].thread(self)
#    exitBody.addNext(beforeCond.next[-1])
#    return self

def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys, os

	prog = open(sys.argv[1]).read()
	result = yacc.parse(prog)
	if result:
		print (result)

		ast = parse(prog)
		entry = thread(ast)
		graph = ast.makegraphicaltree()
		entry.threadTree(graph)

		name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
		graph.write_pdf(name) 
		print ("wrote ast to", name)
	else:
		print ("Parsing returned no result!")
