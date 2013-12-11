import ply.yacc as yacc

from lexer import tokens
import AST

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
}

precedence = (
    ('left', 'ADD_OP', 'MIN_OP'),
    ('left', 'MUL_OP', 'DIV_OP'),
)

vars = {}

def p_program_statement(p):
	''' program : statement SEMICOLON '''
	p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
	''' program : statement SEMICOLON program '''
	p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_assignment(p):
	''' assignation : VAR IDENTIFIER EQUALS expression '''
	p[0] = AST.AssignNode((AST.TokenNode(p[2]), p[4]))

def p_expression(p):
	''' expression : expression COMMA '''
	#p[0] = AST.TokenNode([p[1]] + p[3].children)
	p[0] = AST.TokenNode(p[1])

def p_statement(p):
	''' statement : assignation '''
	p[0] = p[1]

def p_argument(p):
	'''
	argument : IDENTIFIER
		| STRING
		| NUMBER
	'''
	p[0] = AST.TokenNode(p[1])

def p_argument_recursive(p):
	''' arguments : argument COMMA arguments
		| argument '''
	if len(p) > 2:
		p[0] = AST.ArgumentsNode([p[1]] + p[3].children)
	else:
		p[0] = AST.ArgumentsNode(p[1])

def p_parameters(p):
	''' parameters : '(' arguments ')' '''
	p[0] = AST.ParametersNode(p[2])

def p_statement_circle(p):
    ''' statement : CIRCLE parameters '''
    p[0] = AST.CircleNode(p[2])

def p_statement_line(p):
    ''' statement : LINE parameters '''
    p[0] = AST.LineNode(p[2])

def p_statement_pgone(p):
    ''' statement : PGONE parameters '''
    p[0] = AST.PgoneNode(p[2])

def p_statement_pline(p):
    ''' statement : PLINE parameters '''
    p[0] = AST.PlineNode(p[2])

def p_statement_rect(p):
    ''' statement : RECT parameters '''
    p[0] = AST.RectNode(p[2])
    
def p_statement_text(p):
    ''' statement : TEXT parameters '''
    p[0] = AST.TextNode(p[2])

def p_statement_setpage(p):
    ''' statement : SETPAGE parameters '''
    p[0] = AST.SetPageNode(p[2])

def p_statement_setunit(p):
    ''' statement : SETUNIT parameters '''
    p[0] = AST.SetUnitNode(p[2])

def p_statement_setfont(p):
    ''' statement : SETFONT parameters '''
    p[0] = AST.SetFontNode(p[2])

def p_statement_setopacity(p):
    ''' statement : SETOPACITY parameters '''
    p[0] = AST.setOpacityNode(p[2])

def p_statement_fillcolor(p):
    ''' statement : FILLCOLOR parameters '''
    p[0] = AST.FillColorNode(p[2])

def p_statement_strokecolor(p):
    ''' statement : STROKECOLOR parameters '''
    p[0] = AST.StrokeColorNode(p[2])

def p_statement_strokewidth(p):
    ''' statement : STROKEWIDTH parameters '''
    p[0] = AST.StrokeWidthNode(p[2])

def p_expression_identifier(p):
	'''
		expression : NUMBER
		| STRING
	'''
	p[0] = AST.TokenNode(p[1])

def p_expression_parenthesis(p):
    ''' expression : '(' expression ')' '''
    p[0] = p[2]

#def p_expression_op(p):
#	'''expression : expression ADD_OP expression
#			| expression MUL_OP expression '''
#	p[0] = AST.OpNode(p[2], [p[1], p[3]])







def p_error(p):
	print("Syntax error in line %d" % p.lineno)
	yacc.errok()

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
