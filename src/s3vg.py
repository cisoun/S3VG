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
	# Colors taken from the Oxygen palette.
	'BLACK'			: '#000',
	'BLUE'			: '#0057AE',
	'BROWN'			: '#75511A',
	'CM'			: 'cm',
	'GRAY'			: '#888A85',
	'GREEN'			: '#37A42C',
	'NULL'			: 0,
	'ORANGE'		: '#EC7331',
	'PINK'			: '#E20071',
	'PURPLE'		: '#A02786',
	'PX'			: 'px',
	'RED'			: '#E20800',
	'TRANSPARENT'	: '#00000000',
	'YELLOW'		: '#FFDD00',
	'WHITE'			: '#fff'
}

svg = None

fillColor = '#000'
fontBold = False
fontFamily = 'sans'
fontItalic = False
fontSize = 10
opacity = 1.0
page_width = 10
page_height = 10
page_color = '#fff'
strokeColor = '#fff'
strokeWidth = 1

vars = {}
coords = {}


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
	global opacity
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
			**style()
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
			**style()
			)
		)

@addToClass(AST.PgonNode)
def execute(self):
	args = getArgs(self)
	points = []

	for i in range(0, len(args) - 1):
		coords = getArg(args, i)
		points.append(coords.split(','))

	svg.add(
		svg.polygon(
			points=points,
			**style()
			)
		)
	

@addToClass(AST.PlineNode)
def execute(self):
	args = getArgs(self)
	points = []

	for i in range(0, len(args) - 1):
		coords = getArg(args, i)
		points.append(coords.split(','))

	svg.add(
		svg.polyline(
			points=points,
			**style()
			)
		)

@addToClass(AST.RectNode)
def execute(self):
	global fillColor
	global opacity
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
			**style()
			)
		)

@addToClass(AST.TextNode)
def execute(self):
	args = getArgs(self)

	x = getArg(args, 0)
	y = getArg(args, 1)
	text = getArg(args, 2)

	svg.add(
		svg.text(
			text=text,
			insert=(x, y),
			style=styleFont(),
			**style()
			)
		)

@addToClass(AST.SetPageNode)
def execute(self):
	global svg
	args = getArgs(self)
	
	svg['width'] = getArg(args, 0)
	svg['height'] = getArg(args, 1)
	svg['style'] = 'background-color:' + getArg(args, 2)

@addToClass(AST.SetFontNode)
def execute(self):
	global fontBold
	global fontFamily
	global fontItalic
	global fontSize
	
	args = getArgs(self)
	
	fontFamily = getArg(args, 0)
	fontSize = getArg(args, 1)
	fontBold = getArg(args, 2)
	fontItalic = getArg(args, 3)
	
@addToClass(AST.SetOpacityNode)
def execute(self):
	global opacity
	opacity = getArg(getArgs(self), 0)

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

@addToClass(AST.ToRGBNode)
def execute(self):
	args = getArgs(self)

	red = checkRGB(getArg(args, 0))
	green = checkRGB(getArg(args, 1))
	blue = checkRGB(getArg(args, 2))

	return ("#%.2x%.2x%.2x" % (red, green, blue))

def checkRGB(value):
	v = abs(int(value))
	if v > 255:
		v = 255
	return v

# Assigne une variable à une valeur..
def assign(variable, value):
	vars[variable.tok] = value.execute()

def style():
	global fillColor
	global opacity
	global strokeColor
	global strokeWidth

	style = {}
	style['fill'] = fillColor
	style['stroke'] = strokeColor
	style['stroke_width'] = strokeWidth

	# By default, every object has an opacity of 1.
	# Bypass if opacity is at 1 so the output code will be lighter.
	if opacity < 1.0:
		style['fill_opacity'] = opacity
		style['stroke_opacity'] = opacity

	return style

def styleFont():
	global fontBold
	global fontFamily
	global fontItalic
	global fontSize
	
	styles = {}
	styles['font-family'] = fontFamily
	styles['font-size'] = fontSize
	if fontBold: styles['font-weight'] = 'bold'
	if fontItalic: styles['font-style'] = 'italic'

	return styleFactory(**styles)

def styleFactory(**styles):
	result = ''
	for s in styles:
		result += str(s) + ':' + str(styles[s]) + ';'
	return result

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
