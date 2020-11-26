from lexer import createTokens, Token, TokenType
from parser import parseTokens
from ATS_nodes import ProgramNode, KeywordNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node


def generate(tree):
    result = ''
    result += processNode(tree, result)
    result += '\n'
    return result


def processNode(node, result):
    if isinstance(node, ProgramNode):
        result += '    .globl	_main\n'
        result = processNode(node.left, result)
    elif isinstance(node, FunctionNode):
        funcName = node.name
        result += f"_{funcName}:\n"
        result = processNode(node.left, result)
    elif isinstance(node, KeywordNode):
        if node.name == TokenType.returnKeyword:
            result = processExpression(node.left, result)
            result += f"    ret"

    return result


def processExpression(node, result):
    if isinstance(node, ConstantNode):
        result += f"    movq ${node.value}, %rax\n"
    elif isinstance(node, UnaryOperatorNode):
        if node.name == TokenType.negation:
            result = processExpression(node.left, result)
            result += f"    neg %rax\n"
        elif node.name == TokenType.bitwiseComplement:
            result = processExpression(node.left, result)
            result += f"    not %rax\n"
        elif node.name == TokenType.logicalNegation:
            result = processExpression(node.left, result)
            result += f"    cmpl $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif isinstance(node, BinaryOperatorNode):
        if node.name == TokenType.negation:
            result = processExpression(node.right, result)
            result += f"    push %rax\n"
            result = processExpression(node.left, result)
            result += f"    pop %rbx\n"
            result += f"    sub %rbx, %rax\n"
            
        elif node.name == TokenType.addition:
            result = processExpression(node.right, result)
            result += f"    push %rax\n"
            result = processExpression(node.left, result)
            result += f"    pop %rbx\n"
            result += f"    add %rbx, %rax\n"

        elif node.name == TokenType.multiplication:
            result = processExpression(node.right, result)
            result += f"    push %rax\n"
            result = processExpression(node.left, result)
            result += f"    pop %rbx\n"
            result += f"    imul %rbx, %rax\n"

        elif node.name == TokenType.division:
            result = processExpression(node.right, result)
            result += f"    push %rax\n"
            result = processExpression(node.left, result)
            result += f"    pop %rbx\n"

            result += f"    movq $0, %rdx\n"
            result += f"    cqo\n"
            result += f"    idiv %rbx\n"


    return result
