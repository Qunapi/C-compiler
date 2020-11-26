import re


class TokenType:
    openBrace = "{"
    closeBrace = "}"
    openParenthesis = "\\("
    closeParenthesis = "\\)"
    semiColon = ";"
    intKeyword = "int"
    returnKeyword = "return"
    identifier = "[a-zA-Z]\\w*"
    integerLiteral = "\\d+"
    negation = "-"
    bitwiseComplement = "~"
    logicalNegation = "!"
    addition = "\\+"
    multiplication = "\\*"
    division = "/"


class Token:
    value: str
    tokenType: TokenType

    def __init__(self, value, tokenType):
        self.value = value
        self.tokenType = tokenType


def createTokens(text):


    stringTokens = re.findall(
        f"{TokenType.openBrace}|{TokenType.closeBrace}|{TokenType.openParenthesis}"
        f"|{TokenType.closeParenthesis}|{TokenType.semiColon}|{TokenType.intKeyword}|{TokenType.returnKeyword}"
        f"|{TokenType.integerLiteral}|{TokenType.identifier}|{TokenType.negation}|{TokenType.bitwiseComplement}"
        f"|{TokenType.logicalNegation}|{TokenType.addition}|{TokenType.multiplication}|{TokenType.division}", text)

    def mapTokenToType(token):
        if (re.match(TokenType.openBrace, token)):
            return Token(token, TokenType.openBrace)
        elif (re.match(TokenType.closeBrace, token)):
            return Token(token, TokenType.closeBrace)
        elif (re.match(TokenType.openParenthesis, token)):
            return Token(token, TokenType.openParenthesis)
        elif (re.match(TokenType.closeParenthesis, token)):
            return Token(token, TokenType.closeParenthesis)
        elif (re.match(TokenType.semiColon, token)):
            return Token(token, TokenType.semiColon)
        elif (re.match(TokenType.intKeyword, token)):
            return Token(token, TokenType.intKeyword)
        elif (re.match(TokenType.returnKeyword, token)):
            return Token(token, TokenType.returnKeyword)
        elif (re.match(TokenType.identifier, token)):
            return Token(token, TokenType.identifier)
        elif (re.match(TokenType.integerLiteral, token)):
            return Token(token, TokenType.integerLiteral)
        elif (re.match(TokenType.negation, token)):
            return Token(token, TokenType.negation)
        elif (re.match(TokenType.bitwiseComplement, token)):
            return Token(token, TokenType.bitwiseComplement)
        elif (re.match(TokenType.logicalNegation, token)):
            return Token(token, TokenType.logicalNegation)
        elif (re.match(TokenType.addition, token)):
            return Token(token, TokenType.addition)
        elif (re.match(TokenType.multiplication, token)):
            return Token(token, TokenType.multiplication)
        elif (re.match(TokenType.division, token)):
            return Token(token, TokenType.division)
        else:
            raise "invalid token"
    tokens = []
    for token in stringTokens:
        tokens.append(mapTokenToType(token))

    return tokens
