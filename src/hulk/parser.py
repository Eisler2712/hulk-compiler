from typing import List

from compiler.automatonLR1 import AutomatonLR1
from compiler.grammar import GrammarToken
from compiler.lexer import LexerToken
from compiler.parser import Parser, ParseResult
from compiler.tableLR import TableLR
from hulk.constants import *
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
