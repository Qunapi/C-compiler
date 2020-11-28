from lexer import create_tokens, Token, TokenType
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode

variables = {}


def parse_program(tokens):
    tree = ProgramNode()
    tree.left = parse_function(tokens)
    # print2DUtil(tree)
    return tree


def parse_function(tokens):
    type_keyword = next(tokens)

    if (type_keyword.tokenType != TokenType.int_keyword):
        raise "type expected"

    function_identifier = next(tokens)
    if (function_identifier.tokenType != TokenType.identifier):
        raise "identifier expected"

    node = FunctionNode(function_identifier.value)

    open_parenthesis = next(tokens)
    if (open_parenthesis.tokenType != TokenType.open_parenthesis):
        raise "( expected"

    close_parenthesis = next(tokens)
    if (close_parenthesis.tokenType != TokenType.close_parenthesis):
        raise ") expected"

    open_brace_token = next(tokens)
    if (open_brace_token.tokenType != TokenType.open_brace):
        raise "{ expected"

    next_token = tokens.peek()
    node.statements = []

    while next_token.tokenType != TokenType.close_brace:
        node.statements.append(parse_statement(tokens))
        next_token = tokens.peek()

    close_brace_token = next(tokens)
    if (close_brace_token.tokenType != TokenType.close_brace):
        raise "} expected"

    return node


def parse_statement(tokens):
    nextToken = tokens.peek()

    if (nextToken.tokenType == TokenType.return_keyword):
        token = next(tokens)
        node = ReturnNode(token.value)

        node.left = parse_expression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semi_colon):
            raise "; expected after returnKeyword"

    else:
        node = parse_expression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semi_colon):
            raise "; expected after assignment"

    return node


def parse_declaration(tokens):
    if (nextToken.tokenType == TokenType.int_keyword):
        token = next(tokens)  # int
        token = next(tokens)  # id
        node = DeclarationNode(token.value)
        nextToken = tokens.peek()
        variables[token.value] = token.value
        if (nextToken.tokenType == TokenType.assignment):
            token = next(tokens)
            node.left = parse_expression(tokens)

        token = next(tokens)
        if (token.tokenType != TokenType.semi_colon):
            raise "; expected after int"
    else:
        raise 'wrong declaraion'

    return node


def parse_expression(tokens):
    variable = next(tokens)
    next_token = tokens.peek()
    if (variable.tokenType == TokenType.identifier and next_token.tokenType == TokenType.assignment):
        node = AssignNode(variable.value)
        next(tokens)
        node.left = parse_expression(tokens)
        return node
    else:
        tokens.prepend(variable)
        term = parse_logical_and_expression(tokens)
        next_token = tokens.peek()

        while next_token.tokenType == TokenType.logical_or:
            op = next(tokens).tokenType
            nextTerm = parse_logical_and_expression(tokens)
            term = parse_binary_operator(op, term, nextTerm)
            next_token = tokens.peek()
    return term


def parse_logical_and_expression(tokens):
    term = parse_equality_expression(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.logical_and:
        op = next(tokens).tokenType
        nextTerm = parse_equality_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parse_equality_expression(tokens):
    term = parse_relational_expression(tokens)
    next_token = tokens.peek()

    while next_token.tokenType == TokenType.equal or next_token.tokenType == TokenType.not_equal:
        op = next(tokens).tokenType
        nextTerm = parse_relational_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_relational_expression(tokens):
    term = parse_additive_expression(tokens)
    next_token = tokens.peek()

    while (next_token.tokenType == TokenType.less_than or next_token.tokenType == TokenType.less_than_equal or
           next_token.tokenType == TokenType.greater_then or next_token.tokenType == TokenType.greater_than_or_equal):

        op = next(tokens).tokenType
        nextTerm = parse_additive_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_additive_expression(tokens):
    term = parse_term(tokens)
    next_token = tokens.peek()

    while next_token.tokenType == TokenType.addition or next_token.tokenType == TokenType.negation:
        op = next(tokens).tokenType
        nextTerm = parse_term(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_binary_operator(op, term, nextTerm):
    node = BinaryOperatorNode(op)
    node.left = term
    node.right = nextTerm
    return node


def parse_unary_operator(op, term):
    node = UnaryOperatorNode(op.tokenType)
    node.left = term
    return node


def parseIntegerLiteral(literal):
    node = ConstantNode(literal.value)
    return node


def parse_term(tokens):
    term = parse_factor(tokens)
    nextToken = tokens.peek()

    while nextToken.tokenType == TokenType.multiplication or nextToken.tokenType == TokenType.division:
        op = next(tokens).tokenType
        nextTerm = parse_factor(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()

    return term


def parse_factor(tokens):
    token = next(tokens)
    if token.tokenType == TokenType.open_parenthesis:
        # <factor> ::= "(" <exp> ")"
        exp = parse_expression(tokens)  # parse expression inside parens
        if next(tokens).tokenType != TokenType.close_parenthesis:  # make sure parens are balanced
            raise ') expected'
        return exp
    elif is_unary_operator(token):
        # <factor> ::= <unary_op> <factor>
        factor = parse_factor(tokens)
        return parse_unary_operator(token, factor)
    elif token.tokenType == TokenType.integer_literal:
        # <factor> ::= <int>
        return parseIntegerLiteral(token)
    elif token.tokenType == TokenType.identifier:
        # <factor> ::= <int>
        return parse_variable(token)
    else:
        raise '??????????'


def parse_variable(variable):
    node = VariableNode(variable.value)
    return node


def is_unary_operator(token):
    return token.tokenType == TokenType.negation or token.tokenType == TokenType.bitwise_complement or token.tokenType == TokenType.logical_negation


def is_binary_operator(token):
    return token.tokenType == TokenType.addition or token.tokenType == TokenType.multiplication or token.tokenType == TokenType.division


def parse_tokens(tokens):
    tree = parse_program(tokens)
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
