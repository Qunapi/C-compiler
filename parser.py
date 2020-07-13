from lexer import createTokens, Token, TokenType
from typing import Iterable


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


class Node:
    def __init__(self):
        self.left = None
        self.right = None


def parseProgram(tokens: Iterable[Token]):
    tree = Node()
    tree.data = ProgramNode()
    tree.left = Node()
    parseFunction(tokens, tree.left)
    return tree


def parseFunction(tokens: Iterable[Token], tree: Node):
    typeKeyword = next(tokens)
    if (typeKeyword.tokenType != TokenType.intKeyword):
        raise "type expected"

    functionIdentifier = next(tokens)
    if (functionIdentifier.tokenType != TokenType.identifier):
        raise "identifier expected"

    tree.data = FunctionNode(functionIdentifier.value)

    openParenthesis = next(tokens)
    if (openParenthesis.tokenType != TokenType.openParenthesis):
        raise "( expected"

    closeParenthesis = next(tokens)
    if (closeParenthesis.tokenType != TokenType.closeParenthesis):
        raise ") expected"

    openBraceToken = next(tokens)
    if (openBraceToken.tokenType != TokenType.openBrace):
        raise "{ expected"

    tree.left = Node()
    parseStatement(tokens, tree.left)

    closeBraceToken = next(tokens)
    if (closeBraceToken.tokenType != TokenType.closeBrace):
        raise "} expected"


def parseStatement(tokens: Iterable[Token], tree: Node):
    token = next(tokens)
    if (token.tokenType != TokenType.returnKeyword):
        raise "return expected"

    tree.data = UnaryOperatorNode(token.value)
    tree.left = Node()
    parseExpression(tokens, tree.left)

    token = next(tokens)
    if (token.tokenType != TokenType.semiColon):
        raise "; expected"


def parseExpression(tokens: Iterable[Token], tree: Node):
    token = next(tokens)
    if (token.tokenType != TokenType.integerLiteral):
        raise "int literal expected"

    tree.data = ConstantNode(token.value)

    # def parseInt(tokens: List[Token]):


def parseTokens(tokens: Iterable[Token]):
    tree = parseProgram(tokens)
    return tree


tokens = createTokens()
tokensIterator = iter(tokens)
tree = parseTokens(tokensIterator)
print("")
