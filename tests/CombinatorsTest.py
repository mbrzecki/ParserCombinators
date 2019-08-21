import unittest

import sys
sys.path.append("../")
import src.Monads.Result as res
import src.Parsers.BasicParsers as bpr
import src.Parsers.Combinators as cmb
import src.Parsers.StandardParsers as stp


class TestAndThen(unittest.TestCase):
    def test_WhenFirstLettersAreCorrect_ReturnSuccess(self):
        # Arrange
        txt = 'lorem ipsum'
        parser1 = bpr.CharParser('l')
        parser2 = bpr.CharParser('o')
        parser3 = bpr.CharParser('r')
        parser = cmb.and_then(parser1, parser2, parser3)
        # Act
        result = parser(txt)
        expected = res.Success(('lor', 'em ipsum'))
        # Assert
        self.assertEqual(result, expected)

    def test_WhenFirstLettersAreIncorrect_ReturnFailure(self):
        # Arrange
        txt = 'lorem ipsum'
        parser1 = bpr.CharParser('l')
        parser2 = bpr.CharParser('x')
        parser3 = bpr.CharParser('r')
        parser = cmb.and_then(parser1, parser2, parser3)
        # Act
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments(self):
        # Arrange
        txt = 'lorem ipsum'
        parser_l = bpr.CharParser('l')
        parser_o = bpr.CharParser('o')
        parser_r = bpr.CharParser('r')
        parser_e = bpr.CharParser('e')

        parser1 = cmb.and_then(parser_l)
        parser2 = cmb.and_then(parser_l, parser_o)
        parser3 = cmb.and_then(parser_l, parser_o, parser_r)
        parser4 = cmb.and_then(parser_l, parser_o, parser_r, parser_e)
        # Act
        result1 = parser1(txt)
        result2 = parser2(txt)
        result3 = parser3(txt)
        result4 = parser4(txt)
        expected1 = res.Success(('l', 'orem ipsum'))
        expected2 = res.Success(('lo', 'rem ipsum'))
        expected3 = res.Success(('lor', 'em ipsum'))
        expected4 = res.Success(('lore', 'm ipsum'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        self.assertEqual(result4, expected4)


class TestOrElse(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = 'Lorem'
        txt2 = 'ipsum'
        parser1 = bpr.CharParser('L')
        parser2 = bpr.CharParser('x')
        parser3 = bpr.CharParser('i')
        # Act
        parser = cmb.or_else(parser1, parser2, parser3)
        result1 = parser(txt1)
        result2 = parser(txt2)
        expected1 = res.Success(('L', 'orem'))
        expected2 = res.Success(('i', 'psum'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_FailureCase(self):
        # Arrange
        txt = 'Lorem'
        parser1 = bpr.CharParser('l')
        parser2 = bpr.CharParser('x')
        parser3 = bpr.CharParser('i')
        # Act
        parser = cmb.or_else(parser1, parser2, parser3)
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments(self):
        # Arrange
        txt1 = 'lorem ipsum dolor sit amet'
        txt2 = 'ipsum dolor sit amet'
        txt3 = 'dolor sit amet'
        txt4 = 'sit amet'
        parser_l = bpr.CharParser('l')
        parser_o = bpr.CharParser('i')
        parser_r = bpr.CharParser('d')
        parser_e = bpr.CharParser('s')

        parser = cmb.or_else(parser_l, parser_o, parser_r, parser_e)
        # Act
        result1 = parser(txt1)
        result2 = parser(txt2)
        result3 = parser(txt3)
        result4 = parser(txt4)
        expected1 = res.Success(('l', 'orem ipsum dolor sit amet'))
        expected2 = res.Success(('i', 'psum dolor sit amet'))
        expected3 = res.Success(('d', 'olor sit amet'))
        expected4 = res.Success(('s', 'it amet'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        self.assertEqual(result4, expected4)


class TestMany(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt = 'aabbaccca1234'
        parser1 = bpr.CharParser('a')
        parser2 = bpr.CharParser('b')
        parser3 = bpr.CharParser('c')
        # Act
        parser = cmb.many(parser1, parser2, parser3)
        result = parser(txt)
        expected = res.Success(('aabbaccca', '1234'))
        # Assert
        self.assertEqual(result, expected)

    def test_NoMatch(self):
        # Arrange
        txt = 'aabbaccca1234'
        parser1 = bpr.CharParser('x')
        parser2 = bpr.CharParser('y')
        # Act
        parser = cmb.many(parser1, parser2)
        result = parser(txt)
        expected = res.Success(('', 'aabbaccca1234'))
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments(self):
        # Arrange
        txt = 'aabbacccadd1234'
        parser_a = bpr.CharParser('a')
        parser_b = bpr.CharParser('b')
        parser_c = bpr.CharParser('c')
        parser_d = bpr.CharParser('d')
        # Act
        parser1 = cmb.many(parser_a)
        parser2 = cmb.many(parser_a, parser_b)
        parser3 = cmb.many(parser_a, parser_b, parser_c)
        parser4 = cmb.many(parser_a, parser_b, parser_c, parser_d)
        result1 = parser1(txt)
        result2 = parser2(txt)
        result3 = parser3(txt)
        result4 = parser4(txt)
        expected1 = res.Success(('aa', 'bbacccadd1234'))
        expected2 = res.Success(('aabba', 'cccadd1234'))
        expected3 = res.Success(('aabbaccca', 'dd1234'))
        expected4 = res.Success(('aabbacccadd', '1234'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        self.assertEqual(result4, expected4)

    def test_ParserParseEverything_ReturnsSuccess(self):
        # Arrange
        txt = 'aabbaccca'
        parser_a = bpr.CharParser('a')
        parser_b = bpr.CharParser('b')
        parser_c = bpr.CharParser('c')
        parser_d = bpr.CharParser('d')
        # Act
        parser = cmb.many(parser_a, parser_b, parser_c, parser_d)
        result = parser(txt)
        expected = res.Success(('aabbaccca', ''))
        # Assert
        self.assertEqual(result, expected)

    def test_WhenNoParserGivenRaisesException(self):
        # Act
        with self.assertRaises(Exception) as context:
            cmb.many()
        # Assert
        self.assertEqual('Expected parser', str(context.exception))


class TestMany1(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt = 'aabbaccca1234'
        parser1 = bpr.CharParser('a')
        parser2 = bpr.CharParser('b')
        parser3 = bpr.CharParser('c')
        # Act
        parser = cmb.many1(parser1, parser2, parser3)
        result = parser(txt)
        expected = res.Success(('aabbaccca', '1234'))
        # Assert
        self.assertEqual(result, expected)

    def test_Failure(self):
        # Arrange
        txt = 'aabbaccca1234'
        parser1 = bpr.CharParser('x')
        parser2 = bpr.CharParser('y')
        # Act
        parser = cmb.many1(parser1, parser2)
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments(self):
        # Arrange
        txt = 'aabbacccadd1234'
        parser_a = bpr.CharParser('a')
        parser_b = bpr.CharParser('b')
        parser_c = bpr.CharParser('c')
        parser_d = bpr.CharParser('d')
        # Act
        parser1 = cmb.many1(parser_a)
        parser2 = cmb.many1(parser_a, parser_b)
        parser3 = cmb.many1(parser_a, parser_b, parser_c)
        parser4 = cmb.many1(parser_a, parser_b, parser_c, parser_d)
        result1 = parser1(txt)
        result2 = parser2(txt)
        result3 = parser3(txt)
        result4 = parser4(txt)
        expected1 = res.Success(('aa', 'bbacccadd1234'))
        expected2 = res.Success(('aabba', 'cccadd1234'))
        expected3 = res.Success(('aabbaccca', 'dd1234'))
        expected4 = res.Success(('aabbacccadd', '1234'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        self.assertEqual(result4, expected4)

    def test_ParserParseEverything_ReturnsSuccess(self):
        # Arrange
        txt = 'aabbaccca'
        parser_a = bpr.CharParser('a')
        parser_b = bpr.CharParser('b')
        parser_c = bpr.CharParser('c')
        parser_d = bpr.CharParser('d')
        # Act
        parser = cmb.many1(parser_a, parser_b, parser_c, parser_d)
        result = parser(txt)
        expected = res.Success(('aabbaccca', ''))
        # Assert
        self.assertEqual(result, expected)

    def test_WhenNoParserGivenRaisesException(self):
        with self.assertRaises(Exception) as context:
            cmb.many1()
        # Assert
        self.assertEqual('Expected parser', str(context.exception))


class TestOpt(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = '2345'
        txt2 = '12345'
        parser = bpr.CharParser('1')
        # Act
        parser = cmb.opt(parser)
        result1 = parser(txt1)
        result2 = parser(txt2)
        expected1 = res.Success(('', '2345'))
        expected2 = res.Success(('1', '2345'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_Failure(self):
        # Arrange
        txt = '112345'
        parser = bpr.CharParser('1')
        # Act
        parser = cmb.opt(parser)
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments_Success(self):
        # Arrange
        txt1 = '1789'
        txt2 = '789'
        parser_1 = bpr.CharParser('1')
        parser_2 = bpr.CharParser('2')
        parser_3 = bpr.CharParser('3')
        parser_4 = bpr.CharParser('4')
        # Act
        parser = cmb.opt(parser_1, parser_2, parser_3, parser_4)
        result1 = parser(txt1)
        result2 = parser(txt2)
        expected1 = res.Success(('1', '789'))
        expected2 = res.Success(('', '789'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_CorrectlyHandlesDifferentNumberOfArguments_Failure(self):
        # Arrange
        txt1 = '11789'
        txt2 = '123789'
        parser_1 = bpr.CharParser('1')
        parser_2 = bpr.CharParser('2')
        parser_3 = bpr.CharParser('3')
        parser_4 = bpr.CharParser('4')
        # Act
        parser = cmb.opt(parser_1, parser_2, parser_3, parser_4)
        result1 = parser(txt1)
        result2 = parser(txt2)
        expected1 = res.Failure('error')
        expected2 = res.Failure('error')
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)


class TestAny(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = '1'
        txt2 = 'a'
        txt3 = '$'
        parser = cmb.parse_any()
        # Act
        result1 = parser(txt1)
        result2 = parser(txt2)
        result3 = parser(txt3)
        expected1 = res.Success((txt1, ''))
        expected2 = res.Success((txt2, ''))
        expected3 = res.Success((txt3, ''))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    def test_FailureCase(self):
        # Arrange
        txt = ''
        parser = cmb.parse_any()
        # Act
        result = parser(txt)
        expected = res.Failure('No more input')
        # Assert
        self.assertEqual(result, expected)


class TestUntil(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = 'Lorem1'
        txt2 = 'Lorem#ipsum'
        parser_1 = bpr.CharParser('1')
        parser_sharp = bpr.CharParser('#')

        # Act
        parser = cmb.until(parser_1, parser_sharp)
        result1 = parser(txt1)
        result2 = parser(txt2)
        expected1 = res.Success(('Lorem', '1'))
        expected2 = res.Success(('Lorem', '#ipsum'))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_FailureCase(self):
        # Arrange
        txt = 'Lorem'
        parser_1 = bpr.CharParser('1')

        # Act
        parser = cmb.until(parser_1)
        result = parser(txt)
        expected = res.Failure('No more input')
        # Assert
        self.assertEqual(result, expected)

    def test_CorrectlyHandlesDifferentNumberOfArguments_Success(self):
        # Arrange
        txt1 = 'Lorem1'
        txt2 = 'Lorem2asdas'
        txt3 = 'Lorem31as'
        parser_1 = bpr.CharParser('1')
        parser_2 = bpr.CharParser('2')
        parser_3 = bpr.CharParser('3')

        # Act
        parser = cmb.until(parser_1, parser_2, parser_3)
        result1 = parser(txt1)
        result2 = parser(txt2)
        result3 = parser(txt3)
        expected1 = res.Success.unit(('Lorem', '1'))
        expected2 = res.Success.unit(('Lorem', '2asdas'))
        expected3 = res.Success.unit(('Lorem', '31as'))

        # # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    def test_CorrectlyHandlesDifferentNumberOfArguments_Failure(self):
        # Arrange
        txt = 'Lorem'
        parser_1 = bpr.CharParser('1')
        parser_2 = bpr.CharParser('2')
        parser_3 = bpr.CharParser('3')
        parser = cmb.until(parser_1, parser_2, parser_3)
        # Act
        result = parser(txt)
        expected = res.Failure.unit('No more input')
        # Arrange
        self.assertEqual(result, expected)


class TestLeftParser(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt = 'abc123 lorem ipsum'
        parser_l = stp.parse_lowercases()
        parser_r = stp.parse_digits()
        parser = cmb.leftparser(parser_l, parser_r)

        # Act
        result = parser(txt)
        expected = res.Success(('abc', ' lorem ipsum'))

        # Assert
        self.assertEqual(result, expected)

    def test_FailureCase(self):
        # Arrange
        txt = '123abc lorem ipsum'
        parser_l = stp.parse_lowercases()
        parser_r = stp.parse_digits()
        parser = cmb.leftparser(parser_l, parser_r)

        # Act
        result = parser(txt)
        expected = res.Failure('error')

        # Assert
        self.assertEqual(result, expected)


class TestRightParser(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt = 'abc123 lorem ipsum'
        parser_l = stp.parse_lowercases()
        parser_r = stp.parse_digits()
        parser = cmb.rightparser(parser_l, parser_r)

        # Act
        result = parser(txt)
        expected = res.Success(('123', ' lorem ipsum'))

        # Assert
        self.assertEqual(result, expected)

    def test_FailureCase(self):
        # Arrange
        txt = '123abc lorem ipsum'
        parser_l = stp.parse_lowercases()
        parser_r = stp.parse_digits()
        parser = cmb.rightparser(parser_l, parser_r)

        # Act
        result = parser(txt)
        expected = res.Failure('error')

        # Assert
        self.assertEqual(result, expected)


class TestBetweenParser(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt = 'ABCabc123 lorem ipsum'
        parser_l = stp.parse_uppercases()
        parser_m = stp.parse_lowercases()
        parser_r = stp.parse_digits()

        parser = cmb.betweenparsers(parser_l, parser_m, parser_r)

        # Act
        result = parser(txt)
        expected = res.Success(('abc', ' lorem ipsum'))

        # Assert
        self.assertEqual(result, expected)

    def test_FailureCase(self):
        # Arrange
        txt = 'ABCabc123 lorem ipsum'
        parser_l = stp.parse_uppercases()
        parser_m = stp.parse_digits()
        parser_r = stp.parse_lowercases()

        parser = cmb.betweenparsers(parser_l, parser_m, parser_r)

        # Act
        result = parser(txt)
        expected = res.Failure('error')

        # Assert
        self.assertEqual(result, expected)


class TestSepBy(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = 'abc,def,ghi'
        txt2 = 'abc'
        txt3 = ''
        sep = bpr.CharParser(",")
        item = stp.parse_lowercases()
        parser = cmb.sep_by(item, sep)

        # Act
        result1 = parser(txt1)
        expected1 = res.Success((['abc', 'def', 'ghi'], ''))
        result2 = parser(txt2)
        expected2 = res.Success((['abc'], ''))
        result3 = parser(txt3)
        expected3 = res.Success(('', ''))

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    def test_FailureCase(self):
        # Arrange
        txt1 = 'abc,123,ghi'
        txt2 = 'abc#def#ghi'
        sep = bpr.CharParser(",")
        item = stp.parse_lowercases()
        parser = cmb.sep_by(item, sep)

        # Act
        result1 = parser(txt1)
        expected1 = res.Failure('error')
        result2 = parser(txt2)
        expected2 = res.Failure('error')

        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)


class TestSepBy1(unittest.TestCase):
    def test_SuccessCase(self):
        # Arrange
        txt1 = 'abc,def,ghi'
        txt2 = 'abc'
        sep = bpr.CharParser(",")
        item = stp.parse_lowercases()
        parser = cmb.sep_by1(item, sep)
        # Act
        result1 = parser(txt1)
        expected1 = res.Success((['abc', 'def', 'ghi'], ''))
        result2 = parser(txt2)
        expected2 = res.Success((['abc'], ''))
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_FailureCase(self):
        # Arrange
        txt1 = 'abc,123,ghi'
        txt2 = 'abc#def#ghi'
        txt3 = ''
        sep = bpr.CharParser(",")
        item = stp.parse_lowercases()
        parser = cmb.sep_by1(item, sep)
        # Act
        result1 = parser(txt1)
        expected1 = res.Failure('error')
        result2 = parser(txt2)
        expected2 = res.Failure('error')
        result3 = parser(txt3)
        expected3 = res.Failure('error')
        # Assert
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
