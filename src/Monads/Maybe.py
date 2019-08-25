from abc import ABC
import src.Monads.Monad as mnd


class Maybe(mnd.Monad, ABC):
    def __init__(self, value):
        super().__init__(value)

    def __eq__(self, other):
        if not isinstance(other, Maybe):
            return False
        if type(self) == type(other):
            return self.value == other.value
        else:
            return False

    def isSomething(self):
        raise NotImplementedError

    def isNothing(self):
        raise NotImplementedError

    @classmethod
    def lift(cls, func):
        if not callable(func):
            raise Exception("Expected callable")

        def lifted_func(x):
            if x.isSomething:
                try:
                    return Something(func(x.value))
                except Exception:
                    return Nothing()
            elif x.isNothing:
                return x
            else:
                raise Exception("Expected Maybe type, but received " + str(type(x)))

        return lifted_func

    @classmethod
    def liftn(cls, func):
        if not callable(func):
            raise Exception("Expected callable")

        def lifted_func(*args):
            if not all([isinstance(arg, Maybe) for arg in args]):
                raise Exception("Expected Maybe type")

            if all([arg.isSomething for arg in args]):
                try:
                    return Something(func(*[arg.value for arg in args]))
                except Exception:
                    return Nothing()

            elif any([arg.isNothing for arg in args]):
                return Nothing()

        return lifted_func

    @classmethod
    def apply(cls, elevated_func):
        """ Unpacks a function wrapped inside a elevated value into a lifted function
        Signature: E<(a->b)> -> E<a> -> E<b>
        Alternative names: ap"""
        if elevated_func.value is None:
            return cls.lift(lambda x: Nothing(x))
        else:
            return cls.lift(elevated_func.value)

    def __str__(self):
        return str(self._value)


class Something(Maybe):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return 'Something<' + str(self._value) + '>'

    @property
    def isSomething(self):
        return True

    @property
    def isNothing(self):
        return False

    @classmethod
    def unit(cls, x):
        return Something(x)


class Nothing(Maybe):
    def __init__(self, value=None):
        super(Maybe, self).__init__(value)

    def __str__(self):
        return 'Nothing'

    @property
    def isSomething(self):
        return False

    @property
    def isNothing(self):
        return True

    @classmethod
    def unit(cls, x):
        return Nothing()
