from typing import List

from src.compiler.automatonLR1 import AutomatonLR1
from src.compiler.grammar import GrammarToken
from src.compiler.lexer import LexerToken
from src.compiler.parser import Parser, ParseResult
from src.compiler.tableLR import TableLR
from src.hulk.constants import *
from .grammar import hulk_grammar


def hulk_parser_build() -> bool:
    a = AutomatonLR1('hulk', hulk_grammar)
    return a.ok


def hulk_parse(tokens: List[GrammarToken]) -> ParseResult:
    t = TableLR(hulk_grammar)
    t.load('hulk')

    p = Parser(hulk_grammar, t)

    return p.parse(tokens)


def hulk_to_grammar(token: LexerToken) -> GrammarToken:
    if token.value in SPECIAL_TOKENS or token.value in RESERVED_WORDS:
        return GrammarToken(token.value, True)

    if token.type == STRING:
        return GrammarToken('str', True)

    if token.type == NUMBER:
        return GrammarToken('num', True)

    if token.type == IDENTIFIER:
        return GrammarToken('id', True)

    if token.type == BOOLEAN:
        return GrammarToken('bool', True)
