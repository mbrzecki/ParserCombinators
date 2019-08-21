import unittest

import sys
sys.path.append("../")
import src.Monads.Result as res

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


class TestResult(unittest.TestCase):
    def test_eq(self):
        # Arrange
        s1 = res.Success(10)
        s2 = res.Success(10)
        s3 = res.Success(11)
        f1 = res.Failure(10)
        f2 = res.Failure(10)
        f3 = res.Failure(11)
        # Act
        # Assert
        self.assertTrue(s1 == s2)
        self.assertFalse(s1 == s3)
        self.assertTrue(f1 == f2)
        self.assertFalse(f1 == f3)
        self.assertFalse(s1 == f1)
        self.assertFalse(s1 == f3)

    def test_lift_WhenLiftedFunctionCalledOnSuccess_SuccessIsReturn(self):
        # Arrange
        def triple(x): return 3*x
        lifted_f = res.Result.lift(triple)
        arg = res.Success(5)
        expected = res.Success(15)
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_lift_WhenNotCallableIsGiven_ExceptionIsRaised(self):
        # Act
        with self.assertRaises(Exception) as context:
            res.Result.lift(123)
        # Assert
        self.assertEqual('Expected callable', str(context.exception))

    def test_lift_WhenLiftedFunctionCalledOnFailure_FailureIsReturn(self):
        # Arrange
        def triple(x): return 3*x
        lifted_f = res.Result.lift(triple)
        arg = res.Failure("error")
        expected = res.Failure("error")
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_lift_WhenLiftedFunctionRaisesException_FailureIsReturn(self):
        # Arrange
        def triple(x): return 3 / x
        lifted_f = res.Result.lift(triple)
        arg = res.Success(0)
        expected = res.Failure("division by zero")
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionCalledOnSuccess_SuccessIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = res.Result.liftn(sumThree)
        arg1 = res.Success(1)
        arg2 = res.Success(2)
        arg3 = res.Success(3)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = res.Success(6)
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionCalledOnFailure_FailureIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = res.Result.liftn(sumThree)
        arg1 = res.Success(1)
        arg2 = res.Failure(4)
        arg3 = res.Success(3)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = tuple([arg1, arg2, arg3])
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionRaisesException_FailureIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y / z
        lifted_f = res.Result.liftn(sumThree)
        arg1 = res.Success(1)
        arg2 = res.Success(2)
        arg3 = res.Success(0)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = res.Failure("division by zero")
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenNotCallableIsGiven_ExceptionIsRaised(self):
        # Act
        with self.assertRaises(Exception) as context:
            res.Result.liftn(123)
        # Assert
        self.assertEqual('Expected callable', str(context.exception))

    def test_liftn_WhenInproperNumberOfArgumentsGiven_FailureIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = res.Result.liftn(sumThree)
        arg1 = res.Success(1)
        arg2 = res.Success(2)
        # Act
        result = lifted_f(arg1, arg2)
        expected = res.Failure(r"sumThree() missing 1 required positional argument: 'z'")
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenOneArgumentFunctionIsGiven_liftIsReproduced(self):
        # Arrange
        def double(x): return 2 * x
        lifted_fn = res.Result.liftn(double)
        lifted_f = res.Result.lift(double)
        arg = res.Success(5)
        # Act
        result_f = lifted_f(arg)
        result_fn = lifted_fn(arg)
        # Assert
        self.assertEqual(result_f, result_fn)


class TestSuccess(unittest.TestCase):
    def test_MonadLaws_PreservingIdentity(self):
        success_res = MonadLaws.functor_preserving_identity(res.Success)
        self.assertTrue(success_res)

    def test_MonadLaws_PreservingComposition(self):
        success_res = MonadLaws.functor_preserving_composition(res.Success)
        self.assertTrue(success_res)

    def test_MonadLaws_apply_and_unit_reproduces_lift(self):
        success_res = MonadLaws.apply_and_unit_reproduces_lift(res.Failure)
        self.assertTrue(success_res)

    def test_unit(self):
        # Arrange
        expected = res.Success(123)
        # Act
        result = res.Success.unit(123)
        # Assert
        self.assertEqual(result, expected)

    def test_isFailure_isSuccess(self):
        success = res.Success(123)
        self.assertTrue(success.isSuccess)
        self.assertFalse(success.isFailure)


class TestFailure(unittest.TestCase):
    def test_MonadLaws_PreservingIdentity(self):
        failure_res = MonadLaws.functor_preserving_identity(res.Failure)
        self.assertTrue(failure_res)

    def test_MonadLaws_PreservingComposition(self):
        failure_res = MonadLaws.functor_preserving_composition(res.Failure)
        self.assertTrue(failure_res)

    def test_MonadLaws_apply_and_unit_reproduces_lift(self):
        failure_res = MonadLaws.apply_and_unit_reproduces_lift(res.Failure)
        self.assertTrue(failure_res)

    def test_unit(self):
        # Arrange
        expected = res.Failure("error")
        # Act
        result = res.Failure.unit("error")
        # Assert
        self.assertEqual(result, expected)

    def test_isFailureisSuccess(self):
        fail = res.Failure("error")
        self.assertFalse(fail.isSuccess)
        self.assertTrue(fail.isFailure)
