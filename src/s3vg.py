import AST
from AST import addToClass
from functools import reduce
operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

vars ={}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

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
    print (self.children[0].execute())
    print (self.children[1].execute())
    print (self.children[2].execute())

@addToClass(AST.SetUnit)
def execute(self):
    print (self.children[0].execute())

@addToClass(AST.SetFont)
def execute(self):
    print (self.children[0].execute())
    print (self.children[1].execute())
    print (self.children[2].execute())
    print (self.children[3].execute())

@addToClass(AST.SetOpacity)
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
    
#@addToClass(AST.WhileNode)
#def execute(self):
#    while self.children[0].execute():
#        self.children[1].execute()

if __name__ == "__main__":
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    
    ast.execute()
