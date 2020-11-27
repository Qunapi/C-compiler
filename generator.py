from lexer import createTokens, Token, TokenType
from parser import parseTokens
from ATS_nodes import ProgramNode, KeywordNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node
from helpers import createClauseLabel, createEndLabel


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
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif isinstance(node, BinaryOperatorNode):

        if node.name == TokenType.logicalOr:
            clauseLabel = createClauseLabel()
            endLabel = createEndLabel()

            result = processExpression(node.left, result)
            result += f"    cmp $0, %rax\n"
            result += f"    je {clauseLabel}\n"
            result += f"    movq $1, %rax\n"
            result += f"    jmp {endLabel}\n"
            result += f"{clauseLabel}:\n"
            result = processExpression(node.right, result)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{endLabel}:\n"

        elif node.name == TokenType.logicalAnd:
            clauseLabel = createClauseLabel()
            endLabel = createEndLabel()

            result = processExpression(node.left, result)
            result += f"    cmp $0, %rax\n"
            result += f"    jne {clauseLabel}\n"
            result += f"    jmp {endLabel}\n"
            result += f"{clauseLabel}:\n"
            result = processExpression(node.right, result)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{endLabel}:\n"

        else:
            result = processExpression(node.right, result)
            result += f"    push %rax\n"
            result = processExpression(node.left, result)
            result += f"    pop %rbx\n"

            if node.name == TokenType.negation:
                result += f"    sub %rbx, %rax\n"

            elif node.name == TokenType.addition:
                result += f"    add %rbx, %rax\n"

            elif node.name == TokenType.multiplication:
                result += f"    imul %rbx, %rax\n"

            elif node.name == TokenType.division:
                result += f"    movq $0, %rdx\n"
                result += f"    cqo\n"
                result += f"    idiv %rbx\n"

            elif node.name == TokenType.equal:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    sete %al\n"

            elif node.name == TokenType.notEqual:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setne %al\n"

            elif node.name == TokenType.greaterThen:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setg %al\n"

            elif node.name == TokenType.greaterThanOrEqual:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setge %al\n"

            elif node.name == TokenType.lessThan:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setl %al\n"

            elif node.name == TokenType.lessThanEqual:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setle %al\n"

    return result
