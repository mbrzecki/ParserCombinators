import unittest

import sys
sys.path.append("../")
import src.Monads.Result as res
import src.Monads.Maybe as mbe
from src.Monads.MonadLaws import MonadLaws


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
        success_res = MonadLaws.apply_and_unit_reproduces_lift(res.Success)
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


class TestMaybe(unittest.TestCase):
    def test_eq(self):
        # Arrange
        s1 = mbe.Something(10)
        s2 = mbe.Something(10)
        s3 = mbe.Something(11)
        n1 = mbe.Nothing(10)
        # Act
        # Assert
        self.assertTrue(s1 == s2)
        self.assertFalse(s1 == s3)
        self.assertFalse(s1 == n1)

    def test_lift_WhenLiftedFunctionCalledOnSomething_SomethingIsReturned(self):
        # Arrange
        def triple(x): return 3*x
        lifted_f = mbe.Maybe.lift(triple)
        arg = mbe.Something(5)
        expected = mbe.Something(15)
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_lift_WhenNotCallableIsGiven_ExceptionIsRaised(self):
        # Act
        with self.assertRaises(Exception) as context:
            mbe.Maybe.lift(123)
        # Assert
        self.assertEqual('Expected callable', str(context.exception))

    def test_lift_WhenLiftedFunctionCalledOnNothing_FailureIsNothing(self):
        # Arrange
        def triple(x): return 3*x
        lifted_f = mbe.Maybe.lift(triple)
        arg = mbe.Nothing()
        expected = mbe.Nothing()
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_lift_WhenLiftedFunctionRaisesException_NothingIsReturn(self):
        # Arrange
        def triple(x): return 3 / x
        lifted_f = mbe.Maybe.lift(triple)
        arg = mbe.Something(0)
        expected = mbe.Nothing()
        # Act
        result = lifted_f(arg)
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionCalledOnSomething_SomethingIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = mbe.Maybe.liftn(sumThree)
        arg1 = mbe.Something(1)
        arg2 = mbe.Something(2)
        arg3 = mbe.Something(3)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = mbe.Something(6)
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionCalledOnNothing_NothingIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = mbe.Maybe.liftn(sumThree)
        arg1 = mbe.Something(1)
        arg2 = mbe.Nothing(4)
        arg3 = mbe.Something(3)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = mbe.Nothing()
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenLiftedFunctionRaisesException_NothingIsReturn(self):
        # Arrange
        def sumThree(x, y, z): return x + y / z
        lifted_f = mbe.Maybe.liftn(sumThree)
        arg1 = mbe.Something(1)
        arg2 = mbe.Something(2)
        arg3 = mbe.Something(0)
        # Act
        result = lifted_f(arg1, arg2, arg3)
        expected = mbe.Nothing()
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenNotCallableIsGiven_NothingIsReturned(self):
        # Arrange
        def sumThree(x, y, z): return x + y / z
        lifted_f = mbe.Maybe.liftn(sumThree)
        arg1 = mbe.Something(1)
        arg2 = mbe.Something(2)
        # Act
        result = lifted_f(arg1, arg2)
        expected = mbe.Nothing()
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenImproperNumberOfArgumentsGiven_NothingIsReturned(self):
        # Arrange
        def sumThree(x, y, z): return x + y + z
        lifted_f = mbe.Maybe.liftn(sumThree)
        arg1 = mbe.Something(1)
        arg2 = mbe.Something(2)
        # Act
        result = lifted_f(arg1, arg2)
        expected = mbe.Nothing()
        # Assert
        self.assertEqual(result, expected)

    def test_liftn_WhenOneArgumentFunctionIsGiven_liftIsReproduced(self):
        # Arrange
        def double(x): return 2 * x
        lifted_fn = mbe.Maybe.liftn(double)
        lifted_f = mbe.Maybe.lift(double)
        arg = mbe.Something(5)
        # Act
        result_f = lifted_f(arg)
        result_fn = lifted_fn(arg)
        # Assert
        self.assertEqual(result_f, result_fn)


class TestSomething(unittest.TestCase):
    def test_MonadLaws_PreservingIdentity(self):
        some_res = MonadLaws.functor_preserving_identity(mbe.Something)
        self.assertTrue(some_res)

    def test_MonadLaws_PreservingComposition(self):
        some_res = MonadLaws.functor_preserving_composition(mbe.Something)
        self.assertTrue(some_res)

    def test_MonadLaws_apply_and_unit_reproduces_lift(self):
        some_res = MonadLaws.apply_and_unit_reproduces_lift(mbe.Something)
        self.assertTrue(some_res)

    def test_unit(self):
        # Arrange
        expected = mbe.Something(123)
        # Act
        result = mbe.Something.unit(123)
        # Assert
        self.assertEqual(result, expected)

    def test_isSomething_isNothing(self):
        something = mbe.Something(123)
        self.assertTrue(something.isSomething)
        self.assertFalse(something.isNothing)


class TestNothing(unittest.TestCase):
    def test_MonadLaws_PreservingIdentity(self):
        nothing_res = MonadLaws.functor_preserving_identity(mbe.Nothing)
        self.assertTrue(nothing_res)

    def test_MonadLaws_PreservingComposition(self):
        nothing_res = MonadLaws.functor_preserving_composition(mbe.Nothing)
        self.assertTrue(nothing_res)

    def test_MonadLaws_apply_and_unit_reproduces_lift(self):
        nothing_res = MonadLaws.apply_and_unit_reproduces_lift(mbe.Nothing)
        self.assertTrue(nothing_res)

    def test_unit(self):
        # Arrange
        expected = mbe.Nothing()
        # Act
        result = mbe.Nothing.unit("error")
        # Assert
        self.assertEqual(result, expected)

    def test_isSomething_isNothing(self):
        nothing = mbe.Nothing()
        self.assertFalse(nothing.isSomething)
        self.assertTrue(nothing.isNothing)
