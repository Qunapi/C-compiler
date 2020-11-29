from lexer import create_tokens, Token, TokenType
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode, IfNode, ConditionalNode, CompoundNode, NullNode,  ForNode, ForDeclarationNode, WhileNode, DoWhileNode, BreakNode, ContinueNode


def parse_program(tokens):
    tree = ProgramNode()
    tree.left = parse_function(tokens)
    # print2DUtil(tree)
    return tree


def parse_function(tokens):
    type_keyword = next(tokens)

    if (type_keyword.token_type != TokenType.int_keyword):
        raise "type expected"

    function_identifier = next(tokens)
    if (function_identifier.token_type != TokenType.identifier):
        raise "identifier expected"

    node = FunctionNode(function_identifier.value)

    open_parenthesis = next(tokens)
    if (open_parenthesis.token_type != TokenType.open_parenthesis):
        raise "( expected"

    close_parenthesis = next(tokens)
    if (close_parenthesis.token_type != TokenType.close_parenthesis):
        raise ") expected"

    open_brace_token = next(tokens)
    if (open_brace_token.token_type != TokenType.open_brace):
        raise "{ expected"

    next_token = tokens.peek()
    node.statements = []

    while next_token.token_type != TokenType.close_brace:
        node.statements.append(parse_block_item(tokens))
        next_token = tokens.peek()

    close_brace_token = next(tokens)
    if (close_brace_token.token_type != TokenType.close_brace):
        raise "} expected"

    return node


def parse_statement(tokens):
    next_token = tokens.peek()

    if (next_token.token_type == TokenType.return_keyword):
        token = next(tokens)
        node = ReturnNode(token.value)

        node.left = parse_option_expression(tokens)

        token = next(tokens)
        if (token.token_type != TokenType.semi_colon):
            raise "; expected after returnKeyword"
        return node

    elif (next_token.token_type == TokenType.if_keyword):
        node = IfNode()
        next(tokens)
        token = next(tokens)
        if (token.token_type != TokenType.open_parenthesis):
            raise '( expected'

        node.condition = parse_expression(tokens)

        token = next(tokens)
        if (token.token_type != TokenType.close_parenthesis):
            raise ') expected'

        true_branch = parse_statement(tokens)

        node.true_branch = true_branch

        next_token = tokens.peek()
        if (next_token.token_type == TokenType.else_keyword):
            next(tokens)
            node.false_branch = parse_statement(tokens)
        return node

    elif (next_token.token_type == TokenType.open_brace):
        node = parse_compound_block(tokens)
        return node

    elif (next_token.token_type == TokenType.for_keyword):
        for_token = next(tokens)
        parenthesis_token = next(tokens)
        next_token = tokens.peek()
        if (next_token.token_type == TokenType.int_keyword):
            tokens.prepend(parenthesis_token)
            tokens.prepend(for_token)
            node = parse_for_declaration(tokens)
            return node
        tokens.prepend(parenthesis_token)
        tokens.prepend(for_token)
        next_token = tokens.peek()

    if (next_token.token_type == TokenType.for_keyword):
        node = parse_for(tokens)

    elif (next_token.token_type == TokenType.while_keyword):
        node = parse_while(tokens)

    elif (next_token.token_type == TokenType.do_keyword):
        node = parse_do_while(tokens)

    elif (next_token.token_type == TokenType.break_keyword):
        node = parse_break(tokens)

    elif (next_token.token_type == TokenType.continue_keyword):
        node = parse_continue(tokens)

    else:
        node = parse_option_expression(tokens)

        token = next(tokens)
        if (token.token_type != TokenType.semi_colon):
            raise "; expected after assignment"

    return node


def parse_for(tokens):
    node = ForNode()
    token = next(tokens)
    if (token.token_type != TokenType.for_keyword):
        raise "for expected"
    token = next(tokens)
    if (token.token_type != TokenType.open_parenthesis):
        raise "( expected"

    node.initial_expression = parse_option_expression(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.semi_colon):
        raise "; expected after assignment"

    node.condition = parse_option_expression(tokens)
    token = next(tokens)
    if (token.token_type != TokenType.semi_colon):
        raise "; expected after expression"

    node.post_expression = parse_option_expression(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.close_parenthesis):
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_for_declaration(tokens):
    node = ForDeclarationNode()
    token = next(tokens)
    if (token.token_type != TokenType.for_keyword):
        raise "for expected"
    token = next(tokens)
    if (token.token_type != TokenType.open_parenthesis):
        raise "( expected"

    node.initial_expression = parse_declaration(tokens)
    node.condition = parse_option_expression(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.semi_colon):
        raise "; expected after expression"

    node.post_expression = parse_option_expression(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.close_parenthesis):
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_while(tokens):
    node = WhileNode()
    token = next(tokens)
    if (token.token_type != TokenType.while_keyword):
        raise "while expected"
    token = next(tokens)
    if (token.token_type != TokenType.open_parenthesis):
        raise "( expected"

    node.condition = parse_expression(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.close_parenthesis):
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_do_while(tokens):
    node = DoWhileNode()
    token = next(tokens)

    if (token.token_type != TokenType.do_keyword):
        raise "do expected"

    node.body = parse_statement(tokens)

    token = next(tokens)
    if (token.token_type != TokenType.while_keyword):
        raise "while expected"

    node.condition = parse_expression(tokens)

    return node


def parse_break(tokens):
    token = next(tokens)
    if (token.token_type != TokenType.break_keyword):
        raise "break expected"

    node = BreakNode()

    token = next(tokens)
    if (token.token_type != TokenType.semi_colon):
        raise "; expected after break"

    return node


def parse_continue(tokens):
    token = next(tokens)
    if (token.token_type != TokenType.continue_keyword):
        raise "continue expected"

    node = ContinueNode()

    token = next(tokens)
    if (token.token_type != TokenType.semi_colon):
        raise "; expected after continue"

    return node


def parse_compound_block(tokens):
    node = CompoundNode()

    open_brace_token = next(tokens)
    if (open_brace_token.token_type != TokenType.open_brace):
        raise "{ expected"

    next_token = tokens.peek()
    node.statements = []

    while next_token.token_type != TokenType.close_brace:
        node.statements.append(parse_block_item(tokens))
        next_token = tokens.peek()

    close_brace_token = next(tokens)
    if (close_brace_token.token_type != TokenType.close_brace):
        raise "} expected"

    return node


def parse_block_item(tokens):
    next_token = tokens.peek()
    if (next_token.token_type == TokenType.int_keyword):
        node = parse_declaration(tokens)
    else:
        node = parse_statement(tokens)

    return node


def parse_declaration(tokens):
    next_token = tokens.peek()
    if (next_token.token_type == TokenType.int_keyword):
        token = next(tokens)  # int
        token = next(tokens)  # id
        node = DeclarationNode(token.value)
        next_token = tokens.peek()
        if (next_token.token_type == TokenType.assignment):
            token = next(tokens)
            node.left = parse_expression(tokens)

        token = next(tokens)
        if (token.token_type != TokenType.semi_colon):
            raise "; expected after int"
    else:
        raise 'wrong declaraion'

    return node


def parse_option_expression(tokens):
    next_token = tokens.peek()
    if (next_token.token_type == TokenType.semi_colon or next_token.token_type == TokenType.close_parenthesis):
        return NullNode()
    else:
        return parse_expression(tokens)


def parse_expression(tokens):
    variable = next(tokens)
    next_token = tokens.peek()
    if (variable.token_type == TokenType.identifier and next_token.token_type == TokenType.assignment):
        node = AssignNode(variable.value)
        next(tokens)
        node.left = parse_expression(tokens)
        return node
    else:
        tokens.prepend(variable)
        node = parse_conditional_expression(tokens)

    return node


def parse_conditional_expression(tokens):
    node = parse_logical_or_expression(tokens)
    next_token = tokens.peek()

    if (next_token.token_type == TokenType.question_mark):
        next(tokens)
        conditional_node = ConditionalNode()
        conditional_node.condition = node
        node = conditional_node
        node.true_branch = parse_expression(tokens)
        token = next(tokens)
        if (token.token_type != TokenType.colon):
            raise ': expected'
        node.false_branch = parse_conditional_expression(tokens)

    return node


def parse_logical_or_expression(tokens):
    term = parse_logical_and_expression(tokens)
    next_token = tokens.peek()

    while next_token.token_type == TokenType.logical_or:
        op = next(tokens).token_type
        nextTerm = parse_logical_and_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()

    return term


def parse_logical_and_expression(tokens):
    term = parse_equality_expression(tokens)
    nextToken = tokens.peek()

    while nextToken.token_type == TokenType.logical_and:
        op = next(tokens).token_type
        nextTerm = parse_equality_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parse_equality_expression(tokens):
    term = parse_relational_expression(tokens)
    next_token = tokens.peek()

    while next_token.token_type == TokenType.equal or next_token.token_type == TokenType.not_equal:
        op = next(tokens).token_type
        nextTerm = parse_relational_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_relational_expression(tokens):
    term = parse_additive_expression(tokens)
    next_token = tokens.peek()

    while (next_token.token_type == TokenType.less_than or next_token.token_type == TokenType.less_than_equal or
           next_token.token_type == TokenType.greater_then or next_token.token_type == TokenType.greater_than_or_equal):

        op = next(tokens).token_type
        nextTerm = parse_additive_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_additive_expression(tokens):
    term = parse_term(tokens)
    next_token = tokens.peek()

    while next_token.token_type == TokenType.addition or next_token.token_type == TokenType.negation or next_token.token_type == TokenType.mod:
        op = next(tokens).token_type
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
    node = UnaryOperatorNode(op.token_type)
    node.left = term
    return node


def parseIntegerLiteral(literal):
    node = ConstantNode(literal.value)
    return node


def parse_term(tokens):
    term = parse_factor(tokens)
    nextToken = tokens.peek()

    while nextToken.token_type == TokenType.multiplication or nextToken.token_type == TokenType.division:
        op = next(tokens).token_type
        nextTerm = parse_factor(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()

    return term


def parse_factor(tokens):
    token = next(tokens)
    if token.token_type == TokenType.open_parenthesis:
        exp = parse_expression(tokens)
        if next(tokens).token_type != TokenType.close_parenthesis:
            raise ') expected'
        return exp
    elif is_unary_operator(token):
        factor = parse_factor(tokens)
        return parse_unary_operator(token, factor)
    elif token.token_type == TokenType.integer_literal:
        return parseIntegerLiteral(token)
    elif token.token_type == TokenType.identifier:
        return parse_variable(token)
    else:
        raise '??????????'


def parse_variable(variable):
    node = VariableNode(variable.value)
    return node


def is_unary_operator(token):
    return token.token_type == TokenType.negation or token.token_type == TokenType.bitwise_complement or token.token_type == TokenType.logical_negation


def is_binary_operator(token):
    return token.token_type == TokenType.addition or token.token_type == TokenType.multiplication or token.token_type == TokenType.division or token.token_type == TokenType.mod


def parse_tokens(tokens):
    tree = parse_program(tokens)
    return tree


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

    if (hasattr(root, 'condition')):
        print('if')
        print2DUtil(root.condition, space)

    if (hasattr(root, 'true_branch')):
        print2DUtil(root.true_branch, space)

    if (hasattr(root, 'false_branch')):
        print2DUtil(root.false_branch, space)

    if (hasattr(root, 'left')):
        print2DUtil(root.left, space)
