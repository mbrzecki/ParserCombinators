import src.Monads.Result as res
import src.BasicParsers.BasicParsers as bp


def and_then(*parsers, **kwargs):
    """
    Applies parsers one by one. All parsers must be successful to return Success
    """
    label = kwargs.get('label', None)
    if label is None:
        label = ''.join([p.label for p in parsers])

    if len(parsers) == 1:
        return bp.LParser(parsers[0], label)

    if len(parsers) == 2:
        def internal(txt):
            res1 = parsers[0](txt)
            if res1.isFailure:
                return res1
            char1, remaining1 = res1.value

            res2 = parsers[1](remaining1)
            if isinstance(res2, res.Failure):
                return res2
            char2, remaining2 = res2.value

            return res.Success((char1 + char2, remaining2))
        return bp.LParser(internal, label)

    parser_new = and_then(parsers[0], parsers[1])
    new_parsers = [parser_new] + list(parsers[2:])
    return and_then(*new_parsers, label=label)


def or_else(*parsers, **kwargs):
    """
    Applies parsers one by one. At least one parsers must be successful to return Success
    """
    label = kwargs.get('label', None)
    if label is None:
        label = '[' + ''.join([p.label for p in parsers]) + ']'

    if len(parsers) == 1:
        return bp.LParser(parsers[0], label)

    if len(parsers) == 2:
        def internal(txt):
            res1 = parsers[0](txt)
            if res1.isSuccess:
                return res1

            res2 = parsers[1](txt)
            if res2.isSuccess:
                return res2

            return res.Failure('error')
        return bp.LParser(internal, label)

    parser_new = or_else(parsers[0], parsers[1])
    new_parsers = [parser_new] + list(parsers[2:])
    return or_else(*new_parsers, label=label)


def many(*parsers, **kwargs):
    """
    matches zero or more occurrences of the specified parsers.
    """
    label = kwargs.get('label', None)
    if label is None:
        label = '(' + ''.join([p.label for p in parsers]) + ')*'

    if len(parsers) == 0:
        raise Exception("Expected parser")
    if len(parsers) == 1:
        parser = parsers[0]
    elif len(parsers) > 1:
        parser = or_else(*parsers)

    def internal(txt):
        fst_res = parser(txt)
        if fst_res.isFailure:
            return res.Success.unit(("", txt))

        parsed1, remaining1 = fst_res.value
        parsed2, remaining2 = internal(remaining1).value
        ret = (parsed1 + parsed2, remaining2)
        return res.Success.unit(ret)

    return bp.LParser(internal, label=label)


def many1(*parsers, **kwargs):
    """
    matches one or more occurrences of the specified parsers.
    """
    label = kwargs.get('label', None)
    if label is None:
        label = '(' + ''.join([p.label for p in parsers]) + ')+'
    parser = many(*parsers)

    def internal(txt):
        result = parser(txt)
        if result.value[0]:
            return result
        return res.Failure.unit("error")

    return bp.LParser(internal, label)


def opt(*parsers, **kwargs):
    """
    matches zero or one occurrence of the specified parsers.
    """
    label = kwargs.get('label', None)
    if label is None:
        label = '(' + ''.join([p.label for p in parsers]) + ')?'

    parser = or_else(*parsers)

    def internal(txt):
        fst_result = parser(txt)
        if fst_result.isFailure:
            return res.Success(("", txt))
        if fst_result.isSuccess:
            parsed, remaining = fst_result.value
            snd_result = parser(remaining)
            if snd_result.isFailure:
                return fst_result
        return res.Failure('error')

    return bp.LParser(internal, label)


def parse_any(**kwargs):
    """
    matches any pattern.
    """
    label = kwargs.get('label', None)
    if label is None:
        label = '.?'

    def internal(txt):
        if txt == "":
            return res.Failure("No more input")
        return res.Success.unit((txt[0], txt[1:]))

    return bp.LParser(internal, label)


def until(*parsers, **kwargs):
    """
    matches zero or one occurrence of the specified parsers.
    """
    parser = or_else(*parsers)
    label = kwargs.get('label', None)
    if label is None:
        label = '(.*?)[' + ''.join([p.label for p in parsers]) + ']'

    def internal(input_txt):
        ret = ""
        txt = input_txt
        anyp = parse_any()
        checker = parser(txt)
        while checker.isFailure:
            parsed, txt = anyp(txt).value
            ret = ret + parsed
            checker = parser(txt)
            if txt == "":
                break
        if checker.isSuccess:
            return res.Success.unit((ret, txt))
        return res.Failure("No more input")

    return bp.LParser(internal, label)


def leftparser(lparser, rparser, **kwargs):
    """
    Matches left parsers then right one, return result of left parser
    """
    label = kwargs.get('label', None)
    if label is None:
        label = lparser.label + rparser.label

    def internal(txt):
        fst_result = lparser(txt)
        if isinstance(fst_result, res.Failure):
            return res.Failure.unit("error")
        parsed, remaining = fst_result.value
        snd_result = rparser(remaining)
        if isinstance(snd_result, res.Failure):
            return res.Failure.unit("error")
        _, remaining = snd_result.value

        return res.Success.unit((parsed, remaining))

    return bp.LParser(internal, label)


def rightparser(lparser, rparser, **kwargs):
    """
    Matches left parsers then right one, return result of right parser
    """
    label = kwargs.get('label', None)
    if label is None:
        label = lparser.label + rparser.label

    def internal(txt):
        fst_result = lparser(txt)
        if fst_result.isFailure:
            return res.Failure.unit("error")
        _, remaining = fst_result.value
        snd_result = rparser(remaining)
        if snd_result.isFailure:
            return res.Failure.unit("error")
        parsed, remaining = snd_result.value

        return res.Success.unit((parsed, remaining))

    return bp.LParser(internal, label)


def betweenparsers(lparser, mparser, rparser, **kwargs):
    """
    Matches left parsers then mid one and finally right one, return result of middle parser
    """
    label = kwargs.get('label', None)
    if label is None:
        label = lparser.label + mparser.label + rparser.label

    def internal(txt):
        fst_result = lparser(txt)
        if fst_result.isFailure:
            return res.Failure.unit("error")
        _, remaining = fst_result.value
        snd_result = mparser(remaining)
        if snd_result.isFailure:
            return res.Failure.unit("error")
        parsed, remaining = snd_result.value
        trd_result = rparser(remaining)
        _, remaining = trd_result.value
        if trd_result.isFailure:
            return res.Failure.unit("error")

        return res.Success.unit((parsed, remaining))

    return bp.LParser(internal, label)


def sep_by(item, sep, **kwargs):
    """
    parses zero or more occurrences of a parser with a separator
    """
    label = kwargs.get('label', None)
    if label is None:
        label = item.label + '[' + sep.label + item.label + ']+'

    sep_item = and_then(sep, item)
    sep_items = many(sep_item)

    def internal(txt):
        if txt == "":
            return res.Success.unit(('', ''))
        ret = ''
        fst_element = item(txt)
        if fst_element.isSuccess:
            parsed, remaining = fst_element.value
            rest_of_elements = sep_items(remaining)
            if rest_of_elements.isSuccess:
                parsed_rest, remaining = rest_of_elements.value
                return res.Success.unit((parsed + parsed_rest, remaining))
        return res.Failure('error')

    return bp.LParser(internal, label)


def sep_by1(item, sep, **kwargs):
    """
    parses one or more occurrences of a parser with a separator
    """
    label = kwargs.get('label', None)
    if label is None:
        label = item.label + '[' + sep.label + item.label + ']+'

    sep_items = sep_by(item, sep)
    parser = and_then(item, sep, sep_items)

    def internal(txt):
        if txt == "":
            return res.Failure.unit('error')
        fst_res = item(txt)
        if fst_res.isFailure:
            return res.Failure('error')
        parsed, remaining = fst_res.value
        snd_res = sep(remaining)
        if snd_res.isFailure:
            return res.Success((parsed, remaining))

        result = parser(txt)
        if result.isSuccess:
            parsed, remaining = result.value
            return res.Success.unit((parsed, remaining))
        return res.Failure('error')

    return bp.LParser(internal, label)
