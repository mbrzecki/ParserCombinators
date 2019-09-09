class Monoid:
    def __init__(self):
        pass

    def add(self, other):
        raise NotImplementedError

    @staticmethod
    def zero(self, other):
        raise NotImplementedError

    @classmethod
    def checkMonoidLaws(cls):
        pass
