import string
import src.Parsers.BasicParsers as bp
import src.Parsers.Combinators as cmb
#TODO: add Labels


def parse_string(txt, label=None):
    if not isinstance(txt, str):
        raise Exception('Expected string')
    return cmb.and_then(*[bp.CharParser(char) for char in txt], label=label)


def parse_one_of_strings(*strings, **kwargs):
    label = kwargs.get('label', '(' + '|'.join(strings) + ')')
    return cmb.or_else(*[parse_string(s) for s in strings], label=label)


def parse_character(*chars, **kwargs):
    label = kwargs.get('label', None)
    return cmb.or_else(*[bp.CharParser(char) for char in chars], label=label)


def parse_digit(label='[0-9]'):
    return cmb.or_else(*[bp.CharParser(char) for char in string.digits], label=label)


def parse_digits(label='[0-9]+'):
    return cmb.many1(*[bp.CharParser(char) for char in string.digits], label=label)


def parse_uppercase(label='[A-Z]'):
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_uppercase], label=label)


def parse_uppercases(label='[A-Z]+'):
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_uppercase], label=label)


def parse_lowercase(label='[a-z]'):
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_lowercase], label=label)


def parse_lowercases(label='[a-z]+'):
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_lowercase], label=label)


def parse_letter(label='[A-Za-z]'):
    return cmb.or_else(*[bp.CharParser(char) for char in string.ascii_letters], label=label)


def parse_letters(label='[A-Za-z]+'):
    return cmb.many1(*[bp.CharParser(char) for char in string.ascii_letters], label=label)


def parse_alphanumeric(label='[A-Za-z0-9]'):
    return cmb.or_else(*[bp.CharParser(char) for char in (string.ascii_letters + string.digits)], label=label)


def parse_alphanumerics(label='[A-Za-z0-9]+'):
    return cmb.many1(*[bp.CharParser(char) for char in (string.ascii_letters + string.digits)], label=label)


def parse_word(label='[A-Za-z0-9_]+'):
    return cmb.many1(*[bp.CharParser(char) for char in (string.ascii_letters + string.digits + '_')], label=label)


def parse_integer(label='INTEGER'):
    sign = cmb.opt(bp.CharParser('-'))
    digits1to9 = cmb.or_else(*[bp.CharParser(char) for char in '123456789'])
    digits0to9 = cmb.many1(*[bp.CharParser(char) for char in string.digits])
    return cmb.and_then(sign, digits1to9, cmb.opt(digits0to9), label=label)


def parse_unsignedinteger(label='UINTEGER'):
    digits1to9 = cmb.or_else(*[bp.CharParser(char) for char in '123456789'])
    digits0to9 = cmb.many1(*[bp.CharParser(char) for char in string.digits])
    return cmb.and_then(digits1to9, cmb.opt(digits0to9), label=label)
