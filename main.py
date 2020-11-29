from os import listdir, system
from lexer import create_tokens
from parser import parse_tokens
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

    file_name = Path(file).with_suffix('')

    print(f"Processing {file}")
    tokens = create_tokens(text)
    tokens_iterator = peekable(tokens)
    tree = parse_tokens(tokens_iterator)

    result = generate(tree)

    result_file = open(f"./results/{file_name}.s", "w")

    result_file.write(result)
    result_file.close()

    system(f'gcc ./results/{file_name}.s -o ./compiled/{file_name}.c')
    system(f'gcc -w ./tests/{file}  -o ./compiledWithGCC/{file}')


print ("GCC start")
subprocess.call(['sh', './scripts/echoGCCresults.sh']) 

print ("self-compiled start")
subprocess.call(['sh', './scripts/echoResults.sh']) 

compare()
