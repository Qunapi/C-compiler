class ProgramNode:
    pass


class FunctionNode:
    def __init__(self, name):
        self.name = name


class ConstantNode:
    def __init__(self, value):
        self.value = value


class UnaryOperatorNode:
    def __init__(self, name):
        self.name = name


class BinaryOperatorNode:
    def __init__(self, name):
        self.name = name


class KeywordNode:
    def __init__(self, name):
        self.name = name


class Node:
    def __init__(self):
        self.left = None
        self.right = None
