from lexer import createTokens, Token, TokenType
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode

variables = {}


def parseProgram(tokens):
    tree = ProgramNode()
    tree.left = parseFunction(tokens)
    # print2DUtil(tree)
    return tree


def parseFunction(tokens):
    typeKeyword = next(tokens)

    if (typeKeyword.tokenType != TokenType.intKeyword):
        raise "type expected"

    functionIdentifier = next(tokens)
    if (functionIdentifier.tokenType != TokenType.identifier):
        raise "identifier expected"

    node = FunctionNode(functionIdentifier.value)

    openParenthesis = next(tokens)
    if (openParenthesis.tokenType != TokenType.openParenthesis):
        raise "( expected"

    closeParenthesis = next(tokens)
    if (closeParenthesis.tokenType != TokenType.closeParenthesis):
        raise ") expected"

    openBraceToken = next(tokens)
    if (openBraceToken.tokenType != TokenType.openBrace):
        raise "{ expected"

    nextToken = tokens.peek()
    node.statements = []

    while nextToken.tokenType != TokenType.closeBrace:
        node.statements.append(parseStatement(tokens))
        nextToken = tokens.peek()

    closeBraceToken = next(tokens)
    if (closeBraceToken.tokenType != TokenType.closeBrace):
        raise "} expected"

    return node


def parseStatement(tokens):
    nextToken = tokens.peek()

    if (nextToken.tokenType == TokenType.returnKeyword):
        token = next(tokens)
        node = ReturnNode(token.value)

        node.left = parseExpression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semiColon):
            raise "; expected after returnKeyword"
    elif (nextToken.tokenType == TokenType.intKeyword):
        token = next(tokens)  # int
        token = next(tokens)  # id
        node = DeclarationNode(token.value)
        nextToken = tokens.peek()
        variables[token.value] = token.value
        if (nextToken.tokenType == TokenType.assignment):
            token = next(tokens)
            node.left = parseExpression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semiColon):
            raise "; expected after int"
    else:
        node = parseExpression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semiColon):
            raise "; expected after assignment"

    return node


def parseExpression(tokens):
    variable = next(tokens)
    nextToken = tokens.peek()
    if (variable.tokenType == TokenType.identifier and nextToken.tokenType == TokenType.assignment):
        node = AssignNode(variable.value)
        next(tokens)
        node.left = parseExpression(tokens)
        return node
    else:
        tokens.prepend(variable)
        term = parseLogicalAndExpression(tokens)
        nextToken = tokens.peek()

        while nextToken.tokenType == TokenType.logicalOr:
            op = next(tokens).tokenType
            nextTerm = parseLogicalAndExpression(tokens)
            term = parseBinaryOperator(op, term, nextTerm)
            nextToken = tokens.peek()
    return term


def parseLogicalAndExpression(tokens):
    term = parseEqualityExpression(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.logicalAnd:
        op = next(tokens).tokenType
        nextTerm = parseEqualityExpression(tokens)
        term = parseBinaryOperator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parseEqualityExpression(tokens):
    term = parseRelationalExpression(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.equal or nextToken.tokenType == TokenType.notEqual:
        op = next(tokens).tokenType
        nextTerm = parseRelationalExpression(tokens)
        term = parseBinaryOperator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parseRelationalExpression(tokens):
    term = parseAdditiveExpression(tokens)
    nextToken = tokens.peek()

    while (nextToken.tokenType == TokenType.lessThan or nextToken.tokenType == TokenType.lessThanEqual or
           nextToken.tokenType == TokenType.greaterThen or nextToken.tokenType == TokenType.greaterThanOrEqual):

        op = next(tokens).tokenType
        nextTerm = parseAdditiveExpression(tokens)
        term = parseBinaryOperator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parseAdditiveExpression(tokens):
    term = parseTerm(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.addition or nextToken.tokenType == TokenType.negation:
        op = next(tokens).tokenType
        nextTerm = parseTerm(tokens)
        term = parseBinaryOperator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parseBinaryOperator(op, term, nextTerm):
    node = BinaryOperatorNode(op)
    node.left = term
    node.right = nextTerm
    return node


def parseUnaryOperator(op, term):
    node = UnaryOperatorNode(op.tokenType)
    node.left = term
    return node


def parseIntegerLiteral(literal):
    node = ConstantNode(literal.value)
    return node


def parseTerm(tokens):
    term = parseFactor(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.multiplication or nextToken.tokenType == TokenType.division:
        op = next(tokens).tokenType
        nextTerm = parseFactor(tokens)
        term = parseBinaryOperator(op, term, nextTerm)
        nextToken = tokens.peek()

    return term


def parseFactor(tokens):
    token = next(tokens)
    if token.tokenType == TokenType.openParenthesis:
        # <factor> ::= "(" <exp> ")"
        exp = parseExpression(tokens)  # parse expression inside parens
        if next(tokens).tokenType != TokenType.closeParenthesis:  # make sure parens are balanced
            raise ') expected'
        return exp
    elif isUnaryOperator(token):
        # <factor> ::= <unary_op> <factor>
        factor = parseFactor(tokens)
        return parseUnaryOperator(token, factor)
    elif token.tokenType == TokenType.integerLiteral:
        # <factor> ::= <int>
        return parseIntegerLiteral(token)
    elif token.tokenType == TokenType.identifier:
        # <factor> ::= <int>
        return parseVariable(token)
    else:
        raise '??????????'


def parseVariable(variable):
    node = VariableNode(variable.value)
    return node


def isUnaryOperator(token):
    return token.tokenType == TokenType.negation or token.tokenType == TokenType.bitwiseComplement or token.tokenType == TokenType.logicalNegation


def isBinaryOperator(token):
    return token.tokenType == TokenType.addition or token.tokenType == TokenType.multiplication or token.tokenType == TokenType.division


def parseTokens(tokens):
    tree = parseProgram(tokens)
    return  (tree, variables)


COUNT = [10]


def print2DUtil(root, space=0):
    # Base case
    if (root == None):
        return

    # Increase distance between levels
    space += COUNT[0]

    # Process right child first
    if (hasattr(root, 'right')):
        print2DUtil(root.right, space)

    # Print current node after space
    # count
    print()
    for i in range(COUNT[0], space):
        print(end=" ")

    if (hasattr(root, 'name')):
        print(root.name)

    if (hasattr(root, 'value')):
        print(root.value)

    if (hasattr(root, 'statements')):
        for statement in root.statements:
            print2DUtil(statement, space)

    # Process left child
    if (hasattr(root, 'left')):
        print2DUtil(root.left, space)
