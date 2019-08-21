import src.Monads.Result as res


class CharParser:
    def __init__(self, val):
        if isinstance(val, str):
            self._val = val
            self._f = self._inner
        elif callable(val):
            self._val = None
            self._f = val

    def _inner(self, txt):
        if txt == "":
            return res.Failure("No more input")
        if txt.startswith(self._val):
            return res.Success((self._val, txt[1:]))
        return res.Failure("error")

    def __call__(self, txt):
        return self._f(txt)
