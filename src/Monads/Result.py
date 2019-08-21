from abc import ABC
import src.Monads.Monad as mnd


class Result(mnd.Monad, ABC):
    def __init__(self, value):
        super().__init__(value)

    def __eq__(self, other):
        if not isinstance(other, Result):
            return False
        if type(self) == type(other):
            return self.value == other.value
        else:
            return False

    def isSuccess(self):
        raise NotImplementedError

    def isFailure(self):
        raise NotImplementedError

    @classmethod
    def lift(cls, func):
        if not callable(func):
            raise Exception("Expected callable")

        def lifted_func(x):
            if isinstance(x, Success):
                try:
                    return Success(func(x.value))
                except Exception as e:
                    if hasattr(e, 'message'):
                        return Failure(str(e.message))
                    else:
                        return Failure(str(e))
            elif isinstance(x, Failure):
                return x
            else:
                raise Failure("Expected Result type, but received " + str(type(x)))

        return lifted_func

    @classmethod
    def liftn(cls, func):
        if not callable(func):
            raise Exception("Expected callable")

        def lifted_func(*args):
            if not all([isinstance(arg, Result) for arg in args]):
                raise Exception("Expected Result type")

            if all([isinstance(arg, Success) for arg in args]):
                try:
                    return Success(func(*[arg.value for arg in args]))
                except Exception as e:
                    if hasattr(e, 'message'):
                        return Failure(str(e.message))
                    else:
                        return Failure(str(e))
            elif any([isinstance(arg, Failure) for arg in args]):
                return args

        return lifted_func

    @classmethod
    def apply(cls, elevated_func):
        """ Unpacks a function wrapped inside a elevated value into a lifted function
        Signature: E<(a->b)> -> E<a> -> E<b>
        Alternative names: ap"""
        return cls.lift(elevated_func.value)

    def __str__(self):
        return str(self._value)


class Success(Result):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return 'Success<' + str(self._value) + '>'

    @property
    def isSuccess(self):
        return True

    @property
    def isFailure(self):
        return False

    @classmethod
    def unit(cls, x):
        return Success(x)


class Failure(Result):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return 'Failure<' + str(self._value) + '>'

    @property
    def isSuccess(self):
        return False

    @property
    def isFailure(self):
        return True

    @classmethod
    def unit(cls, x):
        return Failure(x)
