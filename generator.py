from lexer import createTokens, Token, TokenType
from parser import parseTokens, ProgramNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node


def generate(tree):
    result = ''
    node = tree
    stack = []
    while node != None:
        if isinstance(node.data, ProgramNode):
            result += '    .globl	main\n'
            node = node.left
        elif isinstance(node.data, FunctionNode):
            funcName = node.data.name
            result += f"{funcName}:\n"
            stack.append(node)
            node = node.left
        elif isinstance(node.data, UnaryOperatorNode):
            if node.data.name == 'return':
                returnValue = createExpression(node.left)
                result += f"    movl ${returnValue}, %eax\n"
                result += f"    ret"
                node = None  # stack.pop()
    result += "\n"
    return result


def createExpression(node):
    if isinstance(node.data, ConstantNode):
        return node.data.value


tokens = createTokens()
tokensIterator = iter(tokens)
tree = parseTokens(tokensIterator)


result = generate(tree)


file1 = open("result.s", "w")

file1.write(result)
file1.close()
