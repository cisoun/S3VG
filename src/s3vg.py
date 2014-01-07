import svgwrite
import AST
from AST import addToClass
from functools import reduce

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
	'%' : lambda x,y: x%y
}

constants = {
	'BLACK'			: '#000',
	'BLUE'			: '#314e6c',
	'BROWN'			: '#663822',
	'CM'			: 'cm',
	'GREEN'			: '#267726',
	'NULL'			: 0,
	'ORANGE'		: '#df421e',
	'PINK'			: '#c4757e',
	'PURPLE'		: '#8700a8',
	'PX'			: 'px',
	'RED'			: '#ed0000',
	'TRANSPARENT'	: '#00000000',
	'YELLOW'		: '#ebb13d',
	'WHITE'			: '#fff'
}

vars = {}

svg = None
fillColor = '#000'
page_width = 10
page_height = 10
page_color = '#fff'
strokeColor = '#ff'
strokeWidth = 1


@addToClass(AST.ProgramNode)
def execute(self):
	for c in self.children:
		c.execute()
	
@addToClass(AST.TokenNode)
def execute(self):
	if isinstance(self.tok, str):
		try:
			if self.tok in constants:
				return constants[self.tok]
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
	iterator = self.children[0].tok
	first = self.children[1].execute()
	last = self.children[2].execute()
	program = self.children[3]

	vars[iterator] = 0
	for i in range(int(first), int(last) + 1): # +1 otherwise ignore last iteration.
		program.execute() # Routine.
		vars[iterator] = i + 1

@addToClass(AST.PrintNode)
def execute(self):
	print(self.children[0].execute())


@addToClass(AST.CircleNode)
def execute(self):
	global fillColor
	global strokeColor
	global strokeWidth

	args = getArgs(self)

	x = getArg(args, 0)
	y = getArg(args, 1)
	radius = getArg(args, 2)

	svg.add(
		svg.circle(
			center=(x, y),
			r=radius,
			fill=fillColor,
			stroke=strokeColor,
			stroke_width=strokeWidth
			)
		)


@addToClass(AST.FillColorNode)
def execute(self):
	global fillColor
	args = getArgs(self)
	fillColor = getArg(args, 0)

@addToClass(AST.LineNode)
def execute(self):
	global strokeColor
	global strokeWidth

	args = getArgs(self)

	x1 = getArg(args, 0)
	y1 = getArg(args, 1)
	x2 = getArg(args, 2)
	y2 = getArg(args, 3)

	svg.add(
		svg.line(
			start=(x1, y1),
			end=(x2, y2),
			stroke=strokeColor,
			stroke_width=strokeWidth
			)
		)


@addToClass(AST.PgoneNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.PlineNode)
def execute(self):
	print (self.children[0].execute())

@addToClass(AST.RectNode)
def execute(self):
	global fillColor
	global strokeColor
	global strokeWidth

	args = getArgs(self)

	x = getArg(args, 0)
	y = getArg(args, 1)
	width = getArg(args, 2)
	height = getArg(args, 3)
	radius = getArg(args, 4)

	svg.add(
		svg.rect(
			insert=(x, y),
			size=(width, height),
			rx=radius,
			ry=radius,
			fill=fillColor
			stroke=strokeColor,
			stroke_width=strokeWidth
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
	
	svg['width'] = getArg(args, 0)
	svg['height'] = getArg(args, 1)
	svg['style'] = 'background-color:' + getArg(args, 2)

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
	strokeColor = getArg(args, 0)
	

@addToClass(AST.StrokeWidthNode)
def execute(self):
	global strokeWidth
	args = getArgs(self)
	strokeWidth = getArg(args, 0)

# Assigne une variable à une valeur..
def assign(variable, value):
	vars[variable.tok] = value.execute()

def currentStyle():
	global fillColor
	global strokeColor
	global strokeWidth
	
	return 'fill:' + fillColor + ';stroke-width:' + str(strokeWidth) + ';stroke' + strokeColor

def getArgs(context):
	return context.children[0].children

def getArg(args, index):
	if len(args) == 0:
		return 0
	return args[index].execute()

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
