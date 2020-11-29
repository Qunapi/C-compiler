class ProgramNode:
    pass


class FunctionNode:
    def __init__(self, name):
        self.name = name
        self.variables = []
        self.stack_size =[]


class ConstantNode:
    def __init__(self, value):
        self.value = value


class UnaryOperatorNode:
    def __init__(self, name):
        self.name = name


class BinaryOperatorNode:
    def __init__(self, name):
        self.name = name


class ReturnNode:
    def __init__(self, name):
        self.name = name

class DeclarationNode:
    def __init__(self, name):
        self.name = name

class VariableNode:
    def __init__(self, name):
        self.name = name

class AssignNode:
    def __init__(self, name):
        self.left = None
        self.right = None
        self.name = name

class Node:
    def __init__(self):
        self.left = None
        self.right = None

class IfNode: 
    def __init__(self):
        self.true_branch = None
        self.false_branch = None
        self.condition = None

class ConditionalNode:
    def __init__(self):
        self.true_branch = None
        self.false_branch = None
        self.condition = None

class CompoundNode:
    def __init__(self):
        self.statements = []