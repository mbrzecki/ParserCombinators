import unittest
import src.Monads.Result as res
import src.BasicParsers.StandardParsers as stp


class TestStandardParsers(unittest.TestCase):
    def test_parse_string(self):
        # Arrange
        txt = 'lorem ipsum'
        parser_succ = stp.parse_string('lorem')
        parser_fail = stp.parse_string('ipsum', label='FAIL')
        # Act
        result_succ = parser_succ(txt)
        result_fail = parser_fail(txt)
        expected_succ = res.Success(('lorem', ' ipsum'))
        expected_fail = res.Failure('error')
        # Assert
        self.assertEqual(result_succ, expected_succ)
        self.assertEqual(result_fail, expected_fail)
        self.assertEqual(parser_succ.label, 'lorem')
        self.assertEqual(parser_fail.label, 'FAIL')

    def test_parse_string(self):
        # Arrange
        txt1 = 'lorem ipsum dolor sit amet'
        txt2 = 'ipsum dolor sit amet'
        txt3 = 'dolor sit amet'
        parser_succ = stp.parse_one_of_strings('lorem', 'ipsum', 'dolor')
        parser_fail = stp.parse_one_of_strings('xxx', label='FAIL')
        # Act
        result_succ1 = parser_succ(txt1)
        result_succ2 = parser_succ(txt2)
        result_fail = parser_fail(txt3)
        expected_succ1 = res.Success(('lorem', ' ipsum dolor sit amet'))
        expected_succ2 = res.Success(('ipsum', ' dolor sit amet'))
        expected_fail = res.Failure('error')
        # Assert
        self.assertEqual(result_succ1, expected_succ1)
        self.assertEqual(result_succ2, expected_succ2)
        self.assertEqual(result_fail, expected_fail)
        self.assertEqual(parser_succ.label, '(lorem|ipsum|dolor)')
        self.assertEqual(parser_fail.label, 'FAIL')

    def test_parse_character(self):
        # Arrange
        txt1 = 'aaa'
        txt2 = 'bbb'
        txt3 = 'ccc'
        parser = stp.parse_character('a', 'b')
        parser_label = stp.parse_character('ab', label='spam')
        # Act
        result_succ1 = parser(txt1)
        result_succ2 = parser_label(txt2)
        result_fail = parser(txt3)
        expected_succ1 = res.Success(('a', 'aa'))
        expected_succ2 = res.Success(('b', 'bb'))
        expected_fail = res.Failure('error')
        # Assert
        self.assertEqual(result_succ1, expected_succ1)
        self.assertEqual(result_succ2, expected_succ2)
        self.assertEqual(result_fail, expected_fail)
        self.assertEqual(parser.label, '[ab]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_digit(self):
        # Arrange
        txt_succ = '1abc'
        txt_fail = 'abc'
        parser = stp.parse_digit()
        parser_label = stp.parse_digit('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("1", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[0-9]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_digits(self):
        # Arrange
        txt_succ = '1234abc'
        txt_fail = 'abc'
        parser = stp.parse_digits()
        parser_label = stp.parse_digits('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("1234", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[0-9]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_uppercase(self):
        # Arrange
        txt_succ = 'ABCabc'
        txt_fail = 'abc'
        parser = stp.parse_uppercase()
        parser_label = stp.parse_uppercase('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("A", "BCabc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[A-Z]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_uppercases(self):
        # Arrange
        txt_succ = 'ABCabc'
        txt_fail = 'abc'
        parser = stp.parse_uppercases()
        parser_label = stp.parse_uppercases('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("ABC", "abc"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[A-Z]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_lowercase(self):
        # Arrange
        txt_succ = 'abcABC'
        txt_fail = 'ABC'
        parser = stp.parse_lowercase()
        parser_label = stp.parse_lowercase('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("a", "bcABC"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[a-z]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_lowercases(self):
        # Arrange
        txt_succ = 'abcABC'
        txt_fail = 'ABC'
        parser = stp.parse_lowercases()
        parser_label = stp.parse_lowercases('spam')
        # Act
        res_succ = parser(txt_succ)
        res_fail = parser(txt_fail)
        exp_succ = res.Success.unit(("abc", "ABC"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ, exp_succ)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[a-z]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_letter(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_fail = '123'
        parser = stp.parse_letter()
        parser_label = stp.parse_letter('spam')
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
        self.assertEqual(parser.label, '[A-Za-z]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_letters(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_fail = '123'
        parser = stp.parse_letters()
        parser_label = stp.parse_letters('spam')
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
        self.assertEqual(parser.label, '[A-Za-z]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_alphanumeric(self):
        # Arrange
        txt_succ1 = 'abcd'
        txt_succ2 = 'ABCabc123'
        txt_succ3 = '123'
        txt_fail = '#abc'
        parser = stp.parse_alphanumeric()
        parser_label = stp.parse_alphanumeric('spam')
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
        self.assertEqual(parser.label, '[A-Za-z0-9]')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_alphanumerics(self):
        # Arrange
        txt_succ1 = 'abcd#123'
        txt_succ2 = 'ABCabc123'
        txt_succ3 = '12#3'
        txt_fail = '#abc'
        parser = stp.parse_alphanumerics()
        parser_label = stp.parse_alphanumerics('spam')
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
        self.assertEqual(parser.label, '[A-Za-z0-9]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_word(self):
        # Arrange
        txt_succ1 = 'abc__d#123'
        txt_succ2 = 'ABCabc_123'
        txt_succ3 = '12_#3'
        txt_fail = '#abc'
        parser = stp.parse_word()
        parser_label = stp.parse_word('spam')
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_succ3 = parser(txt_succ3)
        res_fail = parser(txt_fail)
        exp_succ1 = res.Success.unit(("abc__d", "#123"))
        exp_succ2 = res.Success.unit(("ABCabc_123", ""))
        exp_succ3 = res.Success.unit(("12_", "#3"))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_succ3, exp_succ3)
        self.assertEqual(res_fail, exp_fail)
        self.assertEqual(parser.label, '[A-Za-z0-9_]+')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_integer(self):
        # Arrange
        txt_succ1 = '1'
        txt_succ2 = '1231###'
        txt_succ3 = '-423vcxv'
        txt_succ4 = '0'
        txt_fail1 = '01564'
        txt_fail2 = '--1242'
        parser = stp.parse_integer()
        parser_label = stp.parse_integer('spam')
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_succ3 = parser(txt_succ3)
        res_succ4 = parser(txt_succ4)
        res_fail1 = parser(txt_fail1)
        res_fail2 = parser(txt_fail2)
        exp_succ1 = res.Success.unit(("1", ""))
        exp_succ2 = res.Success.unit(("1231", "###"))
        exp_succ3 = res.Success.unit(("-423", "vcxv"))
        exp_succ4 = res.Success.unit(("0", ""))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_succ3, exp_succ3)
        self.assertEqual(res_succ4, exp_succ4)
        self.assertEqual(res_fail1, exp_fail)
        self.assertEqual(res_fail2, exp_fail)
        self.assertEqual(parser.label, 'INTEGER')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_unsignedinteger(self):
        # Arrange
        txt_succ1 = '1'
        txt_succ2 = '1231###'
        txt_succ3 = '0'
        txt_fail1 = '-423vcxv'
        txt_fail2 = '01564'
        parser = stp.parse_unsignedinteger()
        parser_label = stp.parse_unsignedinteger('spam')
        # Act
        res_succ1 = parser(txt_succ1)
        res_succ2 = parser(txt_succ2)
        res_succ3 = parser(txt_succ3)
        res_fail1 = parser(txt_fail1)
        res_fail2 = parser(txt_fail2)
        exp_succ1 = res.Success.unit(("1", ""))
        exp_succ2 = res.Success.unit(("1231", "###"))
        exp_succ3 = res.Success.unit(("0", ""))
        exp_fail = res.Failure.unit("error")
        # Assert
        self.assertEqual(res_succ1, exp_succ1)
        self.assertEqual(res_succ2, exp_succ2)
        self.assertEqual(res_succ3, exp_succ3)
        self.assertEqual(res_fail1, exp_fail)
        self.assertEqual(res_fail2, exp_fail)
        self.assertEqual(parser.label, 'UINTEGER')
        self.assertEqual(parser_label.label, 'spam')

    def test_parse_float(self):
        # Arrange
        txt_succs = ['0.125',  '3.125',  '-3.125', '126543.125',  '126543.125e9',
                     '32.125E9',  '32.125E-9', '123.0e-10',  '123.0E15', '123.0',
                     '.3124', '.3124E12']
        txt_fails = ['00.312', '312.', '0012.0']
        parser = stp.parse_float()
        parser_label = stp.parse_float('spam')
        # Act
        res_succs = [parser(txt_succ) for txt_succ in txt_succs]
        exp_succs = [res.Success((txt_succ, '')) for txt_succ in txt_succs]
        res_fails = [parser(txt_fail) for txt_fail in txt_fails]
        fail = res.Failure.unit("error")
        # Assert
        for e, r in zip(res_succs, exp_succs):
            self.assertEqual(e, r)
        for r in res_fails:
            self.assertEqual(fail, r)

        self.assertEqual(parser.label, 'FLOAT')
        self.assertEqual(parser_label.label, 'spam')

    def test_lstrip(self):
        # Arrange
        txt1 = ' \n\tLorem Ipsum'
        txt2 = ' \n12312'
        txt3 = 'aaaLorem Ipsum'
        exp1 = res.Success(('Lorem', ' Ipsum'))
        exp2 = res.Success(('12312', ''))
        exp3 = res.Success(('Lorem', ' Ipsum'))
        parser1 = stp.lstrip(stp.parse_string("Lorem"))
        parser2 = stp.lstrip(stp.parse_digits(), ignored_lst=[' ', '\n'])
        parser3 = stp.lstrip(stp.parse_string("Lorem"), ignored_lst=['a'])
        # Act
        res1 = parser1(txt1)
        res2 = parser2(txt2)
        res3 = parser3(txt3)
        # Assert
        self.assertEqual(res1, exp1)
        self.assertEqual(res2, exp2)
        self.assertEqual(res3, exp3)
        self.assertEqual(parser1.label, "Lorem")
        self.assertEqual(parser2.label, "[0-9]+")
        self.assertEqual(parser3.label, "Lorem")

    def test_rstrip(self):
        # Arrange
        txt1 = 'Lorem \n\tIpsum'
        txt2 = '12312 \nXYZ'
        txt3 = 'LoremaaaIpsum'
        exp1 = res.Success(('Lorem', 'Ipsum'))
        exp2 = res.Success(('12312', 'XYZ'))
        exp3 = res.Success(('Lorem', 'Ipsum'))
        parser1 = stp.rstrip(stp.parse_string("Lorem"))
        parser2 = stp.rstrip(stp.parse_digits(), ignored_lst=[' ', '\n'])
        parser3 = stp.rstrip(stp.parse_string("Lorem"), ignored_lst=['a'])
        # Act
        res1 = parser1(txt1)
        res2 = parser2(txt2)
        res3 = parser3(txt3)
        # Assert
        self.assertEqual(res1, exp1)
        self.assertEqual(res2, exp2)
        self.assertEqual(res3, exp3)
        self.assertEqual(parser1.label, "Lorem")
        self.assertEqual(parser2.label, "[0-9]+")
        self.assertEqual(parser3.label, "Lorem")

    def test_strip(self):
        # Arrange
        txt1 = ' \n\tLorem \n\tIpsum'
        txt2 = '  12312 \nXYZ'
        txt3 = '11Lorem111Ipsum'
        exp1 = res.Success(('Lorem', 'Ipsum'))
        exp2 = res.Success(('12312', 'XYZ'))
        exp3 = res.Success(('Lorem', 'Ipsum'))
        parser1 = stp.strip(stp.parse_string("Lorem"))
        parser2 = stp.strip(stp.parse_digits(), ignored_lst=[' ', '\n'])
        parser3 = stp.strip(stp.parse_string("Lorem"), ignored_lst=['1'])
        # Act
        res1 = parser1(txt1)
        res2 = parser2(txt2)
        res3 = parser3(txt3)
        # Assert
        self.assertEqual(res1, exp1)
        self.assertEqual(res2, exp2)
        self.assertEqual(res3, exp3)
        self.assertEqual(parser1.label, "Lorem")
        self.assertEqual(parser2.label, "[0-9]+")
        self.assertEqual(parser3.label, "Lorem")
