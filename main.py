from os import listdir
from lexer import createTokens
from parser import parseTokens
from generator import generate

files = listdir("./src")

for file in files:
    f = open(f"./src/{file}", "r")
    text = f.read()
    print(f"Processing {file}")
    tokens = createTokens(text)
    tokensIterator = iter(tokens)
    tree = parseTokens(tokensIterator)

    result = generate(tree)

    resultFile = open(f"./results/{file}.s", "w")

    resultFile.write(result)
    resultFile.close()
