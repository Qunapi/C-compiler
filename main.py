from os import listdir, system
from lexer import createTokens
from parser import parseTokens
from generator import generate
from pathlib import Path
from comparison import compare
from more_itertools import peekable
import subprocess



files = listdir("./tests")

Path("./tests").mkdir(parents=True, exist_ok=True)
Path("./results").mkdir(parents=True, exist_ok=True)
Path("./compiled").mkdir(parents=True, exist_ok=True)
Path("./compiledWithGCC").mkdir(parents=True, exist_ok=True)


for file in files:
    f = open(f"./tests/{file}", "r")
    text = f.read()

    fileName = Path(file).with_suffix('')

    print(f"Processing {file}")
    tokens = createTokens(text)
    tokensIterator = peekable(tokens)
    tree = parseTokens(tokensIterator)

    result = generate(tree)

    resultFile = open(f"./results/{fileName}.s", "w")

    resultFile.write(result)
    resultFile.close()

    system(f'gcc ./results/{fileName}.s -o ./compiled/{fileName}.c')
    system(f'gcc ./tests/{file} -o ./compiledWithGCC/{file}')


print ("GCC start")
subprocess.call(['sh', './scripts/echoGCCresults.sh']) 

print ("main start")
subprocess.call(['sh', './scripts/echoResults.sh']) 

compare()
