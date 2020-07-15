from os import listdir, system
from lexer import createTokens
from parser import parseTokens
from generator import generate
from pathlib import Path


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
    tokensIterator = iter(tokens)
    tree = parseTokens(tokensIterator)

    result = generate(tree)

    resultFile = open(f"./results/{fileName}.s", "w")

    resultFile.write(result)
    resultFile.close()

    system(f'gcc ./results/{fileName}.s -o ./compiled/{fileName}')
    system(f'gcc ./tests/{file} -o ./compiledWithGCC/{file}')

system('echo "" > ./results.txt; for file in $(ls ./compiled); do ./compiled/$file; echo "$? $file">> ./results.txt; done')
system('echo "" > ./results_real.txt; for file in $(ls ./tests); do ./compiledWithGCC/$file; echo "$? $file">> ./results_real.txt; done')
