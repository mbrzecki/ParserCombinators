
class MonadLaws:
    """See https://en.wikibooks.org/wiki/Haskell/Applicative_functors"""
    @classmethod
    def functor_preserving_identity(cls, functor):
        """ 1st Functor law
            Functor (lift) preserves identity
            F id = lifted_id """
        lifted_id = functor.lift(cls.id)
        arg = 42
        lifted_arg = functor.unit(arg)
        precondition = cls.id(arg) == arg
        condition = lifted_id(lifted_arg) == lifted_arg
        return precondition and condition

    @classmethod
    def functor_preserving_composition(cls, functor):
        """ 2nd Functor law
            Functor (lift) preserves composition
            F (f . g)  ==  F f . F g """
        lifted_f1 = functor.lift(cls.f1)
        lifted_f2 = functor.lift(cls.f2)
        lifted_f12 = functor.lift(cls.f12)
        arg = functor.unit(123)
        return lifted_f12(arg) == lifted_f1(lifted_f2(arg))

    @classmethod
    def appfunctor_preserving_identity(cls, applicative_functor):
        """ 1st Applicative Functor law:
            Applicative functor (apply) preserves identity
            apply unit id = lifted_id """
        pass

    @classmethod
    def appfunctor_homomorphism(cls, applicative_functor):
        """ 2nd Applicative Functor law:
            Applicative functor (apply)  preserves identity
            apply unit f (unit x) = unit f(x) """
        pass

    @classmethod
    def appfunctor_interchange(cls, applicative_functor):
        """ 3rd Applicative Functor law: """
        pass

    @classmethod
    def appfunctor_composition(cls, applicative_functor):
        """ 4th Applicative Functor law: """
        pass

    @classmethod
    def apply_and_unit_reproduces_lift(cls, applicative_functor):
        """ f: a->b
            1) unit f = unit a->b = E<a->b>
            2) apply E<a->b> = E<a>->E<b> = lift a->b = lift f
            3) apply unit <-> lift """
        elevated_f = applicative_functor.unit(cls.f1)
        apply_elevated_f = applicative_functor.apply(elevated_f)
        lifted = applicative_functor.lift(cls.f1)
        arg = applicative_functor.unit(123)
        return lifted(arg) == apply_elevated_f(arg)

    @classmethod
    def id(cls, x):
        return x

    @classmethod
    def f1(cls, x):
        return x + 3

    @classmethod
    def f2(cls, x):
        return 2 * x

    @classmethod
    def f12(cls, x):
        return cls.f1(cls.f2(x))