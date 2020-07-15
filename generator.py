from lexer import createTokens, Token, TokenType
from parser import parseTokens
from ATS_nodes import ProgramNode, KeywordNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node


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
    elif isinstance(node.data, KeywordNode):
        if node.data.name == TokenType.returnKeyword:
            result = processExpression(node.left, result)
            result += f"    ret"

    return result


def processExpression(node, result):
    if isinstance(node.data, ConstantNode):
        result += f"    movl ${node.data.value}, %eax\n"
    elif isinstance(node.data, UnaryOperatorNode):
        if node.data.name == TokenType.negation:
            result = processExpression(node.left, result)
            result += f"    neg %eax\n"
        elif node.data.name == TokenType.bitwiseComplement:
            result = processExpression(node.left, result)
            result += f"    not %eax\n"
        elif node.data.name == TokenType.logicalNegation:
            result = processExpression(node.left, result)
            result += f"    cmpl $0, %eax\n"
            result += f"    movl $0, %eax\n"
            result += f"    sete %al\n"
    return result
