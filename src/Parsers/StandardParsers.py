import string
import src.Parsers.BasicParsers as bp
import src.Parsers.Combinators as cmb


def parse_string(txt):
    if not isinstance(txt, str):
        raise Exception('Expected string')
    return cmb.and_then(*[bp.CharParser(char) for char in txt])


def parse_character(*chars):
    return cmb.or_else(*[bp.CharParser(char) for char in chars])


def parse_digit():
    return cmb.or_else(*[bp.CharParser(char) for char in string.digits])


def parse_digits():
    return cmb.many1(*[bp.CharParser(char) for char in string.digits])


def parse_uppercase():
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_uppercase])


def parse_uppercases():
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_uppercase])


def parse_lowercase():
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_lowercase])


def parse_lowercases():
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_lowercase])


def parse_letter():
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_letters])


def parse_letters():
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_letters])


def parse_alphanumeric():
    return cmb.or_else(*[bp.CharParser(char) for char in (string.ascii_letters + string.digits)])


def parse_alphanumerics():
    return cmb.many1(*[bp.CharParser(char) for char in (string.ascii_letters + string.digits)])
