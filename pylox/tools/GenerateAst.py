import sys


class GenerateAst:
    def main(self, args: list) -> None:
        if len(args) != 1:
            print("Usage: generate_ast <output directory>")
            sys.exit(64)

        outputDir = args[0]
        expr = [
            "Assign     : Token name, Expr value",
            "Binary     : Expr left, Token operator, Expr right",
            "Call       : Expr callee, Token paren, list[Expr] arguments",
            "Get        : Expr object, Token name",
            "Grouping   : Expr expression",
            "Literal    : Object value",
            "Logical    : Expr left, Token operator, Expr right",
            "Set        : Expr object, Token name, Expr value",
            "Super      : Token keyword, Token method",
            "This       : Token keyword",
            "Unary      : Token operator, Expr right",
            "Variable   : Token name",
        ]
        self.defineAst(outputDir, "Expr", expr)

        stmt = [
            "Block      : list[Stmt] statements",
            "Class      : Token name, Expr.Variable superclass, list[Stmt] methods",
            "Expression : Expr expression",
            "Function   : Token name, list[Token] params, list[Stmt] body",
			"If			: Expr condition, Stmt thenBranch, Stmt elseBranch",
            "Print      : Expr expression",
            "Return     : Token keyword, Expr value",
            "Var        : Token name, Expr initializer",
            "While      : Expr condition, Stmt body",
        ]
        self.defineAst(outputDir, "Stmt", stmt)

    def defineAst(self, outputDir: str, baseName: str, types: list) -> None:
        path = outputDir + "/" + baseName + ".py"

        with open(path, "w") as f:
            f.write("class " + baseName + ":")
            f.write("\n")

        self.defineVisitor(path, baseName, types)

        # The Ast classes
        for type in types:
            className = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            self.defineType(path, baseName, className, fields)

        # base Accpept method
        with open(path, "a") as f:
            f.write("\n")
            f.write("   def accept(self, visitor):")
            f.write("\n")
            f.write("       raise NotImplementedError()")
            f.write("\n")

            # Function to return all inner classes
            f.write("\n")
            f.write("   @classmethod")
            f.write("\n")
            f.write("   def all_inner_class(cls):")
            f.write("\n")
            f.write('       if hasattr(cls, "_results"):')
            f.write("\n")
            f.write('           return cls._results')
            f.write("\n")
            f.write('       results = []')
            f.write("\n")
            f.write('       for attrname in dir(cls):')
            f.write("\n")
            f.write('           obj = getattr(cls, attrname)')
            f.write("\n")
            f.write('           if isinstance(obj, type):')
            f.write("\n")
            f.write('               results.append(obj)')
            f.write("\n")
            f.write('       cls._results = results')
            f.write("\n")
            f.write('       return cls._results')
            f.write("\n")

    def defineVisitor(self, path, baseName, types) -> None:
        with open(path, "a") as f:
            f.write("   class Visitor:")
            f.write("\n")

            for type in types:
                typeName = type.split(":")[0].strip()
                f.write("       def visit" + typeName + baseName + "(" + typeName + "):")
                f.write("\n")
                f.write("           raise NotImplementedError()")
                f.write("\n\n")

    def defineType(self, path: str, baseName: str, className: str, fieldList: str) -> None:
        with open(path, "a") as f:
            f.write("   class " + className + ":")
            f.write("\n")

            # Constructor
            fields = fieldList.split(", ")
            newFieldListList = []
            for field in fields:
                newField = field.strip()
                fieldType = newField.split(" ")[0]
                fieldName = newField.split(" ")[1]
                newFieldListList.append(fieldName)
            newFieldList = ", ".join(newFieldListList)

            f.write("       def __init__(self, " + newFieldList + "):")
            f.write("\n")
            for field in fields:
                fieldName = field.split(" ")[1]
                f.write("           self." + fieldName + " = " + fieldName)
                f.write("\n")

            f.write("\n")

            # Visitor
            f.write("       def accept(self, visitor):")
            f.write("\n")
            f.write("           return visitor.visit" + className + baseName + "(self)")
            f.write("\n\n")


def parseArgs():
    args = sys.argv
    return args[1:]

if __name__ == "__main__":
    args = parseArgs()
    app = GenerateAst()
    app.main(args)
