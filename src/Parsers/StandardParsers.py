import string
import src.Monads.Result as res
import src.Parsers.BasicParsers as bp
import src.Parsers.Combinators as cmb


def parse_string(string, label=None):
    """
    returns parser of a given string
    """
    if not isinstance(string, str):
        raise Exception('Expected string')
    return cmb.and_then(*[bp.LParser(char) for char in string], label=label)


def parse_one_of_strings(*strings, **kwargs):
    """
    returns parser that match one of the strings given
    """
    label = kwargs.get('label', '(' + '|'.join(strings) + ')')
    return cmb.or_else(*[parse_string(s) for s in strings], label=label)


def parse_character(*chars, **kwargs):
    """
    returns parser that match one of the strings given
    """
    label = kwargs.get('label', None)
    if len(chars) == 1 and len(chars[0]) > 1:
        return cmb.or_else(*[bp.LParser(char) for char in chars[0]], label=label)
    return cmb.or_else(*[bp.LParser(char) for char in chars], label=label)


def parse_digit(label='[0-9]'):
    """
    returns parser parsing single digit: [0-9]
    """
    return cmb.or_else(*[bp.LParser(char) for char in string.digits], label=label)


def parse_digits(label='[0-9]+'):
    """
    returns parser parsing at least one digit: [0-9]+
    """
    return cmb.many1(*[bp.LParser(char) for char in string.digits], label=label)


def parse_uppercase(label='[A-Z]'):
    """
    returns parser parsing single capital letter: [A-Z]
    """
    return cmb.or_else(*[bp.LParser(char) for char in string.ascii_uppercase], label=label)


def parse_uppercases(label='[A-Z]+'):
    """
    returns parser parsing at least one capital letter: [A-Z]+
    """
    return cmb.many1(*[bp.LParser(char) for char in string.ascii_uppercase], label=label)


def parse_lowercase(label='[a-z]'):
    """
    returns parser parsing single small latter: [a-z]
    """
    return cmb.or_else(*[bp.LParser(char) for char in string.ascii_lowercase], label=label)


def parse_lowercases(label='[a-z]+'):
    """
    returns parser parsing at least one small latter: [a-z]+
    """
    return cmb.many1(*[bp.LParser(char) for char in string.ascii_lowercase], label=label)


def parse_letter(label='[A-Za-z]'):
    """
    returns parser parsing single latter: [A-Za-z]
    """
    return cmb.or_else(*[bp.LParser(char) for char in string.ascii_letters], label=label)


def parse_letters(label='[A-Za-z]+'):
    """
    returns parser parsing at least one latter: [A-Za-z]+
    """
    return cmb.many1(*[bp.LParser(char) for char in string.ascii_letters], label=label)


def parse_alphanumeric(label='[A-Za-z0-9]'):
    """
    returns parser parsing single letter or digit: [A-Za-z0-9]
    """
    return cmb.or_else(*[bp.LParser(char) for char in (string.ascii_letters + string.digits)], label=label)


def parse_alphanumerics(label='[A-Za-z0-9]+'):
    """
    returns parser parsing at least one letter or digit: [A-Za-z0-9]+
    """
    return cmb.many1(*[bp.LParser(char) for char in (string.ascii_letters + string.digits)], label=label)


def parse_word(label='[A-Za-z0-9_]+'):
    """
    returns parser parsing at least one letter or digit or underscore: [A-Za-z0-9_]+
    """
    return cmb.many1(*[bp.LParser(char) for char in (string.ascii_letters + string.digits + '_')], label=label)


def parse_integer(label='INTEGER'):
    """
    returns parser for integer
    """
    sign = cmb.opt(bp.LParser('-'))
    return cmb.and_then(sign, parse_unsignedinteger(), label=label)


def parse_unsignedinteger(label='UINTEGER'):
    """
    returns parser for unsigned integer
    """
    digits_09 = parse_digit('0123456789')
    digits_19 = parse_character('123456789')
    nonzero = cmb.and_then(digits_19, cmb.many(digits_09))
    zero = bp.LParser('0')

    def internal(txt):
        fst_digit = zero(txt)
        if fst_digit.isSuccess:
            snd = digits_09(fst_digit.value[1])
            if snd.isSuccess:
                return res.Failure('error')
            else:
                return fst_digit
        return nonzero(txt)

    return bp.LParser(internal, label)


def parse_float(label='FLOAT'):
    """
    returns parser for floating point number
    """
    sign = cmb.opt(bp.LParser('-'))
    coma = bp.LParser('.')
    e = cmb.or_else(bp.LParser('e'), bp.LParser('E'))
    exponent = cmb.opt(cmb.and_then(e, parse_integer()))
    integer = parse_integer()
    return cmb.and_then(sign, cmb.opt(integer), coma, parse_digits(), exponent, label=label)


def lstrip(parser, ignored_lst=None):
    """
    Strips ignored characters from left side
    """
    if ignored_lst is None:
        ignored_lst = [' ', '\t', '\n']
    ignored_parser = cmb.many(parse_one_of_strings(*ignored_lst))

    def internal(txt):
        stripping = ignored_parser(txt)
        return parser(stripping.value[1])

    return bp.LParser(internal, parser.label)


def rstrip(parser, ignored_lst=None):
    """
    Strips ignored characters from right side
    """
    if ignored_lst is None:
        ignored_lst = [' ', '\t', '\n']
    ignored_parser = cmb.many(parse_one_of_strings(*ignored_lst))

    def internal(txt):
        result = parser(txt)
        if result.isFailure:
            return result

        _, remaining = ignored_parser(result.value[1]).value
        return res.Success((result.value[0], remaining))

    return bp.LParser(internal, parser.label)


def strip(parser, ignored_lst=None):
    """
    Strips ignored characters from both sides
    """
    if ignored_lst is None:
        ignored_lst = [' ', '\t', '\n']
    return lstrip(rstrip(parser, ignored_lst), ignored_lst)