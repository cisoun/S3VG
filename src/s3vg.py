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

svg = None
fillColor = "#000"
page_width = 10
page_height = 10
page_color = "#fff"
strokeColor = "#ff"
strokeWidth = 1


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
	
	#if len(args) == 1:
	#	args.insert(0, 0)

	# Allow strings concatenation.
	if isinstance(args[0], str) or isinstance(args[1], str):
		return str(args[0]) + str(args[1])

	return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
	assign(self.children[0], self.children[1])

@addToClass(AST.ForNode)
def execute(self):
	assign(self.children[0], self.children[1])

	i = self.children[0].execute()
	first = self.children[1].execute()
	last = self.children[2].execute() + 1 # +1 otherwise ignore last iteration.

	for i in range(int(first), int(last)):
		self.children[3].execute() # Routine.
		assign(self.children[0], AST.TokenNode(float(i + 1))) # Next iteration.
		#print(self.children[0])

@addToClass(AST.PrintNode)
def execute(self):
	print (self.children[0].execute())


@addToClass(AST.CircleNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())

@addToClass(AST.FillColorNode)
def execute(self):
	global fillColor
	args = getArgs(self)
	fillColor = self.children[0].execute()

@addToClass(AST.LineNode)
def execute(self):
	global strokeColor
	global strokeWidth

	args = getArgs(self)

	x1 = args[0].execute()
	y1 = args[1].execute()
	x2 = args[2].execute()
	y2 = args[3].execute()
	print("STROKE", strokeColor)
	svg.add(
		svg.line(start=(x1, y1), end=(x2, y2), stroke=strokeColor, stroke_width=strokeWidth)
	)


@addToClass(AST.PgoneNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.PlineNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.RectNode)
def execute(self):
	args = getArgs(self)

	x = args[0].execute()
	y = args[1].execute()
	width = args[2].execute()
	height = args[3].execute()

	svg.add(
		svg.rect(
			size=(width, height),
			rx=x,
			ry=y,
			style=currentStyle()
			)
		)

@addToClass(AST.TextNode)
def execute(self):
	print (self.children[0].execute())
	print (self.children[1].execute())
	print (self.children[2].execute())

@addToClass(AST.SetPageNode)
def execute(self):
	global svg
	args = getArgs(self)
	svg['width'] = args[0].execute()
	svg['height'] = args[1].execute()
	svg['style'] = 'background-color:' + args[2].execute()

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

@addToClass(AST.StrokeColorNode)
def execute(self):
	global strokeColor
	args = getArgs(self)
	strokeColor = args[0].execute()
	

@addToClass(AST.StrokeWidthNode)
def execute(self):
	global strokeWidth
	args = getArgs(self)
	strokeWidth = args[0].execute()

# Assigne une variable à une valeur..
def assign(variable, value):
	vars[variable.tok] = value.execute()

def currentStyle():
	global fillColor
	global strokeColor
	global strokeWidth
	
	return 'fill:' + fillColor + ';stroke-width:' + str(strokeWidth) + ';stroke' + strokeColor

def getArgs(arguments):
	return arguments.children[0].children

if __name__ == "__main__":
	from parser import parse
	import sys
	import svgwrite
	
	svg = svgwrite.Drawing(filename="./test.svg")

	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	ast.execute()
	
	#svg = svgwrite.Drawing(filename="./test.svg", size=(page_width, page_width), style="background-color:#fff")
	svg.save()
