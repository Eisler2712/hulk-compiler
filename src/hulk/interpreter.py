import subprocess
from .lexer import hulk_lexer_build
from .parser import hulk_parser_build, hulk_parse, hulk_to_grammar
from compiler.lexer import Lexer
from .grammar import hulk_grammar
from .code_generator import code_generator
from hulk.semanticCheck import hulk_semantic_check

def build() -> bool:
    hulk_lexer_build()
    return hulk_parser_build()

def compiler(program: str) -> bool:
    hulk_lexer = Lexer()
    hulk_lexer.load('hulk')

    result = hulk_lexer.run(program)
    tokens = result.tokens

    if not result.ok:
        print(f'Error: {result.error}')
        return False

    result = hulk_parse([hulk_to_grammar(t) for t in tokens])

    if not result.ok:
        print(f'Error: {result.error}')
        return False

    ast = hulk_grammar.evaluate(result.derivation_tree,tokens)
    result = hulk_semantic_check(ast)

    if not result.ok:
        print(f'Error: {result.errors}')
        return False
    
    code_generator(ast, result.context)

    try:
        result = subprocess.run(
            ["gcc", "-o", "cache/main", "cache/main.c", "-lm"])
        result = subprocess.run(
            ["./cache/main"], text=True, check=True)
    except:
        print('Runtime error')

    return True


