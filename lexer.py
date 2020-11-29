import re


class TokenType:
    open_brace = "{"
    close_brace = "}"
    open_parenthesis = "\\("
    close_parenthesis = "\\)"
    semi_colon = ";"
    int_keyword = "int"
    return_keyword = "return"
    integer_literal = "\\d+"
    negation = "-"
    bitwise_complement = "~"
    addition = "\\+"
    multiplication = "\\*"
    division = "/"
    logical_and = '&&'
    logical_or = '\\|\\|'
    equal = '=='
    not_equal = '!='
    less_than_equal = '<='
    less_than = '<'
    greater_than_or_equal = '>='
    greater_then = '>'
    logical_negation = "!"
    assignment = '='
    if_keyword = 'if'
    else_keyword = 'else'
    colon = ":"
    question_mark = "\\?"
    for_keyword = "for"
    while_keyword = "while"
    do_keyword = "do"
    break_keyword = "break"
    continue_keyword = "continue"
    identifier = "[a-zA-Z]\\w*"
    mod = "%"
    comma = ","


class Token:
    value: str
    token_type: TokenType

    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type


def create_tokens(text):

    string_tokens = re.findall(
        f"{TokenType.open_brace}|{TokenType.close_brace}|{TokenType.open_parenthesis}"
        f"|{TokenType.close_parenthesis}|{TokenType.semi_colon}|{TokenType.int_keyword}|{TokenType.return_keyword}"
        f"|{TokenType.integer_literal}|{TokenType.negation}|{TokenType.bitwise_complement}"
        f"|{TokenType.addition}|{TokenType.multiplication}|{TokenType.division}"
        f"|{TokenType.logical_and}|{TokenType.logical_or}|{TokenType.equal}|{TokenType.not_equal}"
        f"|{TokenType.less_than_equal}|{TokenType.less_than}|{TokenType.greater_than_or_equal}|{TokenType.greater_then}"
        f"|{TokenType.logical_negation}|{TokenType.assignment}"
        f"|{TokenType.if_keyword}|{TokenType.else_keyword}|{TokenType.colon}|{TokenType.question_mark}"
        f"|{TokenType.for_keyword}|{TokenType.while_keyword}|{TokenType.do_keyword}|{TokenType.break_keyword}"
        f"|{TokenType.continue_keyword}|{TokenType.identifier}|{TokenType.mod}|{TokenType.comma}", text)

    def map_token_to_type(token):
        if (re.match(TokenType.open_brace, token)):
            return Token(token, TokenType.open_brace)
        elif (re.match(TokenType.close_brace, token)):
            return Token(token, TokenType.close_brace)
        elif (re.match(TokenType.open_parenthesis, token)):
            return Token(token, TokenType.open_parenthesis)
        elif (re.match(TokenType.close_parenthesis, token)):
            return Token(token, TokenType.close_parenthesis)
        elif (re.match(TokenType.semi_colon, token)):
            return Token(token, TokenType.semi_colon)
        elif (re.match(TokenType.int_keyword, token)):
            return Token(token, TokenType.int_keyword)
        elif (re.match(TokenType.return_keyword, token)):
            return Token(token, TokenType.return_keyword)
        elif (re.match(TokenType.integer_literal, token)):
            return Token(token, TokenType.integer_literal)
        elif (re.match(TokenType.negation, token)):
            return Token(token, TokenType.negation)
        elif (re.match(TokenType.bitwise_complement, token)):
            return Token(token, TokenType.bitwise_complement)
        elif (re.match(TokenType.addition, token)):
            return Token(token, TokenType.addition)
        elif (re.match(TokenType.multiplication, token)):
            return Token(token, TokenType.multiplication)
        elif (re.match(TokenType.division, token)):
            return Token(token, TokenType.division)
        elif (re.match(TokenType.logical_and, token)):
            return Token(token, TokenType.logical_and)
        elif (re.match(TokenType.logical_or, token)):
            return Token(token, TokenType.logical_or)
        elif (re.match(TokenType.equal, token)):
            return Token(token, TokenType.equal)
        elif (re.match(TokenType.not_equal, token)):
            return Token(token, TokenType.not_equal)
        elif (re.match(TokenType.less_than_equal, token)):
            return Token(token, TokenType.less_than_equal)
        elif (re.match(TokenType.less_than, token)):
            return Token(token, TokenType.less_than)
        elif (re.match(TokenType.greater_than_or_equal, token)):
            return Token(token, TokenType.greater_than_or_equal)
        elif (re.match(TokenType.greater_then, token)):
            return Token(token, TokenType.greater_then)
        elif (re.match(TokenType.logical_negation, token)):
            return Token(token, TokenType.logical_negation)
        elif (re.match(TokenType.assignment, token)):
            return Token(token, TokenType.assignment)
        elif (re.match(TokenType.if_keyword, token)):
            return Token(token, TokenType.if_keyword)
        elif (re.match(TokenType.else_keyword, token)):
            return Token(token, TokenType.else_keyword)
        elif (re.match(TokenType.colon, token)):
            return Token(token, TokenType.colon)
        elif (re.match(TokenType.question_mark, token)):
            return Token(token, TokenType.question_mark)
        elif (re.match(TokenType.for_keyword, token)):
            return Token(token, TokenType.for_keyword)
        elif (re.match(TokenType.while_keyword, token)):
            return Token(token, TokenType.while_keyword)
        elif (re.match(TokenType.do_keyword, token)):
            return Token(token, TokenType.do_keyword)
        elif (re.match(TokenType.break_keyword, token)):
            return Token(token, TokenType.break_keyword)
        elif (re.match(TokenType.continue_keyword, token)):
            return Token(token, TokenType.continue_keyword)
        elif (re.match(TokenType.identifier, token)):
            return Token(token, TokenType.identifier)
        elif (re.match(TokenType.mod, token)):
            return Token(token, TokenType.mod)
        elif (re.match(TokenType.comma, token)):
            return Token(token, TokenType.comma)

        else:
            raise "invalid token"

    tokens = []
    for token in string_tokens:
        tokens.append(map_token_to_type(token))

    return tokens
