class Stmt:
   class Visitor:
       def visitBlockStmt(Block):
           raise NotImplementedError()

       def visitClassStmt(Class):
           raise NotImplementedError()

       def visitExpressionStmt(Expression):
           raise NotImplementedError()

       def visitFunctionStmt(Function):
           raise NotImplementedError()

       def visitIfStmt(If):
           raise NotImplementedError()

       def visitPrintStmt(Print):
           raise NotImplementedError()

       def visitReturnStmt(Return):
           raise NotImplementedError()

       def visitVarStmt(Var):
           raise NotImplementedError()

       def visitWhileStmt(While):
           raise NotImplementedError()

   class Block:
       def __init__(self, statements):
           self.statements = statements

       def accept(self, visitor):
           return visitor.visitBlockStmt(self)

   class Class:
       def __init__(self, name, superclass, methods):
           self.name = name
           self.superclass = superclass
           self.methods = methods

       def accept(self, visitor):
           return visitor.visitClassStmt(self)

   class Expression:
       def __init__(self, expression):
           self.expression = expression

       def accept(self, visitor):
           return visitor.visitExpressionStmt(self)

   class Function:
       def __init__(self, name, params, body):
           self.name = name
           self.params = params
           self.body = body

       def accept(self, visitor):
           return visitor.visitFunctionStmt(self)

   class If:
       def __init__(self, condition, thenBranch, elseBranch):
           self.condition = condition
           self.thenBranch = thenBranch
           self.elseBranch = elseBranch

       def accept(self, visitor):
           return visitor.visitIfStmt(self)

   class Print:
       def __init__(self, expression):
           self.expression = expression

       def accept(self, visitor):
           return visitor.visitPrintStmt(self)

   class Return:
       def __init__(self, keyword, value):
           self.keyword = keyword
           self.value = value

       def accept(self, visitor):
           return visitor.visitReturnStmt(self)

   class Var:
       def __init__(self, name, initializer):
           self.name = name
           self.initializer = initializer

       def accept(self, visitor):
           return visitor.visitVarStmt(self)

   class While:
       def __init__(self, condition, body):
           self.condition = condition
           self.body = body

       def accept(self, visitor):
           return visitor.visitWhileStmt(self)


   def accept(self, visitor):
       raise NotImplementedError()

   @classmethod
   def all_inner_class(cls):
       if hasattr(cls, "_results"):
           return cls._results
       results = []
       for attrname in dir(cls):
           obj = getattr(cls, attrname)
           if isinstance(obj, type):
               results.append(obj)
       cls._results = results
       return cls._results
