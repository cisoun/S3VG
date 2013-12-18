import svgwrite
import AST
from AST import addToClass
from functools import reduce
operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
}

vars = {}

page_width = 10
page_height = 10
page_color = "#fff"


@addToClass(AST.ProgramNode)
def execute(self):
	for c in self.children:
		c.execute()
	
@addToClass(AST.TokenNode)
def execute(self):
	if isinstance(self.tok, str):
		try:
			if self.tok in vars:
				return vars[self.tok]
			return self.tok
		except KeyError:
			print ("*** Error: variable %s undefined!" % self.tok)
	return self.tok

@addToClass(AST.ArgumentsNode)
def execute(self):
	return self.children[0].execute()

@addToClass(AST.OpNode)
def execute(self):
	args = [c.execute() for c in self.children]
	if len(args) == 1:
		args.insert(0, 0)
	return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
	assign(self.children[0], self.children[1])

@addToClass(AST.ForNode)
def execute(self):
	assign(self.children[0], self.children[1])

	i = self.children[0].execute()
	first = self.children[1].execute()
	last = self.children[2].execute() + 1 # +1 sinon ignore la dernière itération.

	for i in range(int(first), int(last)):
		self.children[3].execute()
		assign(self.children[0], AST.TokenNode(float(i + 1)))

@addToClass(AST.PrintNode)
def execute(self):
	print (self.children[0].execute())


@addToClass(AST.CircleNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())

@addToClass(AST.LineNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())
	print (self.children[3].execute())

@addToClass(AST.PgoneNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.PlineNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.RectNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())
	print (self.children[3].execute())

@addToClass(AST.TextNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())

@addToClass(AST.SetPageNode)
def execute(self):
	args = getArgs(self)
	page_width = args[0].execute()
	page_height = args[1].execute()
	page_color = args[2].execute()

@addToClass(AST.SetUnitNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.SetFontNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())
	print (self.children[3].execute())

@addToClass(AST.SetOpacityNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.FillColorNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.StrokeColorNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.StrokeWidthNode)
def execute(self):
	print (self.children[0].execute())

# Assigne une variable à une valeur..
def assign(variable, value):
	vars[variable.tok] = value.execute()

def getArgs(arguments):
	return arguments.children[0].children

if __name__ == "__main__":
	from parser import parse
	import sys
	import svgwrite

	svg = svgwrite.Drawing(filename="./test.svg", size=(page_width, page_width), style="background-color:#f00")

	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	ast.execute()
	
	svg.save()
