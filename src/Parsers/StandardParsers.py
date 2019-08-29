import string
import src.Monads.Result as res
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
    return cmb.and_then(sign, parse_unsignedinteger(), label=label)


def parse_unsignedinteger(label='UINTEGER'):
    digits_09 = parse_digit('0123456789')
    digits_19 = parse_character('1', '2', '3', '4', '5', '6', '7', '8', '9')
    nonzero = cmb.and_then(digits_19, cmb.many(digits_09))
    zero = bp.CharParser('0')

    def internal(txt):
        fst_digit = zero(txt)
        if fst_digit.isSuccess:
            snd = digits_09(fst_digit.value[1])
            if snd.isSuccess:
                return res.Failure('error')
            else:
                return fst_digit
        return nonzero(txt)

    return bp.CharParser(internal, label)


def parse_float(label='FLOAT'):
    sign = cmb.opt(bp.CharParser('-'))
    coma = bp.CharParser('.')
    e = cmb.or_else(bp.CharParser('e'), bp.CharParser('E'))
    exponent = cmb.opt(cmb.and_then(e, parse_integer()))
    integer = parse_integer()
    return cmb.and_then(sign, cmb.opt(integer), coma, parse_digits(), exponent, label=label)
