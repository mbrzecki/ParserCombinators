import unittest
import src.Monads.Result as res
import src.Parsers.StandardParsers as stp


class TestStandardParsers(unittest.TestCase):
    def test_parse_string(self):
        # Arrange
        txt = 'lorem ipsum'
        parser_succ = stp.parse_string('lorem')
        parser_fail = stp.parse_string('ipsum')
        # Act
        result_succ = parser_succ(txt)
        result_fail = parser_fail(txt)
        expected_succ = res.Success(('lorem', ' ipsum'))
        expected_fail = res.Failure('error')
        # Assert
        self.assertEqual(result_succ, expected_succ)
        self.assertEqual(result_fail, expected_fail)

    def test_parse_character(self):
        # Arrange
        txt1 = 'aaa'
        txt2 = 'bbb'
        txt3 = 'ccc'
        parser = stp.parse_character('a', 'b')
        # Act
        result_succ1 = parser(txt1)
        result_succ2 = parser(txt2)
        result_fail = parser(txt3)
        expected_succ1 = res.Success(('a', 'aa'))
        expected_succ2 = res.Success(('b', 'bb'))
        expected_fail = res.Failure('error')
        # Assert
        self.assertEqual(result_succ1, expected_succ1)
        self.assertEqual(result_succ2, expected_succ2)
        self.assertEqual(result_fail, expected_fail)

    def test_parse_digit(self):
        pass
        # Arrange
        txt_succ = '1abc'
        txt_fail = 'abc'
        parser = stp.parse_digit()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("1", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_digits(self):
        # Arrange
        txt_succ = '1234abc'
        txt_fail = 'abc'
        parser = stp.parse_digits()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("1234", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_uppercase(self):
        # Arrange
        txt_succ = 'ABCabc'
        txt_fail = 'abc'
        parser = stp.parse_uppercase()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("A", "BCabc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_lowercase(self):
        # Arrange
        txt_succ = 'abcABC'
        txt_fail = 'ABC'
        parser = stp.parse_lowercase()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("a", "bcABC"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_uppercases(self):
        # Arrange
        txt_succ = 'ABCabc'
        txt_fail = 'abc'
        parser = stp.parse_uppercases()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("ABC", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_lowercases(self):
        # Arrange
        txt_succ = 'abcABC'
        txt_fail = 'ABC'
        parser = stp.parse_lowercases()
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("abc", "ABC"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_letter(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_fail = '123'
        parser = stp.parse_letter()
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_fail = parser(txt_fail)
        exp_succ1 = res.Success.unit(("a", "bcd"))
        exp_succ2 = res.Success.unit(("A", "BCabc123"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_letters(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_fail = '123'
        parser = stp.parse_letters()
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_fail = parser(txt_fail)
        exp_succ1 = res.Success.unit(("abcd", ""))
        exp_succ2 = res.Success.unit(("ABCabc", "123"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_alphanumeric(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_succ3 = '123'
        txt_fail = '#abc'
        parser = stp.parse_alphanumeric()
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_succ3 = parser(txt_succ3)
        res_fail = parser(txt_fail)
        exp_succ1 = res.Success.unit(("a", "bcd"))
        exp_succ2 = res.Success.unit(("A", "BCabc123"))
        exp_succ3 = res.Success.unit(("1", "23"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_succ3, exp_succ3)
        self.assertEqual(res_fail, exp_fail)

    def test_parse_alphanumerics(self):
        # Arrange
        txt_succ1 = 'abcd#123'
        txt_succ2 = 'ABCabc123'
        txt_succ3 = '12#3'
        txt_fail = '#abc'
        parser = stp.parse_alphanumerics()
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_succ3 = parser(txt_succ3)
        res_fail = parser(txt_fail)
        exp_succ1 = res.Success.unit(("abcd", "#123"))
        exp_succ2 = res.Success.unit(("ABCabc123", ""))
        exp_succ3 = res.Success.unit(("12", "#3"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_succ3, exp_succ3)
        self.assertEqual(res_fail, exp_fail)
