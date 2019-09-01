import src.Monads.Result as res


class LParser:
    def __init__(self, val, label=None):
        if isinstance(val, str):
            self._val = val
            self._f = self._inner
            self._label = label if label else val
        elif callable(val):
            self._val = None
            self._f = val
            self._label=label if label else "Unknown parser"
        else:
            raise Exception("Incorrect initialization of parsers")

    def _inner(self, txt):
        if txt == "":
            return res.Failure("No more input")
        if txt.startswith(self._val):
            return res.Success((self._val, txt[1:]))
        return res.Failure("error")

    def __call__(self, txt):
        return self._f(txt)

    def set_label(self, label):
        self._label = label

    @property
    def label(self):
        return self._label
