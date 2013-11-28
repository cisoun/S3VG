import ply.yacc as yacc

from lexer import tokens
import AST

vars = {}


def p_expression_number(p):
	'''expression : NUMBER'''
	p[0] = p[1]

def p_expression_parenthesis(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_error(p):
	print("Syntax error in line %d" % p.lineno)
	yacc.errok()

#def parse(program):
#    return yacc.parse(program)

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
