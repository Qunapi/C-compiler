from lexer import createTokens, Token, TokenType
from typing import Iterable
from ATS_nodes import ProgramNode, FunctionNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node


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
        raise "expression expected"

    tree.data = ConstantNode(token.value)


def parseTokens(tokens: Iterable[Token]):
    tree = parseProgram(tokens)
    return tree
