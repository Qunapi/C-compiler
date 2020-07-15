from lexer import createTokens, Token, TokenType
from parser import parseTokens
from ATS_nodes import ProgramNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node


def generate(tree):
    result = ''
    result = processNode(tree, result)
    result += '\n'
    return result


def processNode(node, result):
    if isinstance(node.data, ProgramNode):
        result += '    .globl	main\n'
        result = processNode(node.left, result)
    elif isinstance(node.data, FunctionNode):
        funcName = node.data.name
        result += f"{funcName}:\n"
        result = processNode(node.left, result)
    elif isinstance(node.data, UnaryOperatorNode):
        if node.data.name == 'return':
            returnValue = processExpression(node.left)
            result += f"    movl ${returnValue}, %eax\n"
            result += f"    ret"

    return result


def processExpression(node):
    if isinstance(node.data, ConstantNode):
        return node.data.value
