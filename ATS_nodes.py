class ProgramNode:
    def __init__(self):
        self.statements = []


class FunctionNode:
    def __init__(self, name):
        self.name = name
        self.variables = []
        self.stack_size = []
        self.statements = []


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


class NullNode:
    pass


class ForNode:
    def __init__(self):
        self.initial_expression = None
        self.condition = None
        self.post_expression = None
        self.body = None


class ForDeclarationNode:
    def __init__(self):
        self.initial_expression = None
        self.condition = None
        self.post_expression = None
        self.body = None


class WhileNode:
    def __init__(self):
        self.condition = None
        self.body = None


class DoWhileNode:
    def __init__(self):
        self.body = None
        self.condition = None


class BreakNode:
    pass


class ContinueNode:
    pass


class FunctionCallNode:
    def __init__(self):
        self.name = None
        self.args = []
