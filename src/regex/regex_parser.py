from typing import List

from src.compiler.automatonSLR1 import AutomatonSLR1
from src.compiler.grammar import GrammarToken
from src.compiler.parser import Parser
from src.compiler.parser_out import ParseResult
from src.compiler.tableLR import TableLR
from .regex_core import RegexToken
from .regex_grammar import regex_grammar


def regex_build() -> bool:
    a = AutomatonSLR1('regex', regex_grammar)
    return a.ok


def regex_parser(l: List[GrammarToken]) -> ParseResult:
    t = TableLR(regex_grammar)
    t.load('regex')
    return Parser(regex_grammar, t).parse(l)


def regex_to_grammar(token: RegexToken) -> GrammarToken:
    if token.is_special:
        return [t for t in regex_grammar.terminals if t.value == token.value][0]

    return [t for t in regex_grammar.terminals if t.value == 'ch'][0]
