import unittest
import src.Monads.Result as res
import src.Parsers.BasicParsers as bp


class TestCharParsers(unittest.TestCase):
    def test_WhenFirstLetterIsCorrect_ReturnsSuccess(self):
        # Arrange
        txt = 'Lorem ipsum'
        parser = bp.CharParser('L')
        # Act
        result = parser(txt)
        expected = res.Success(('L', 'orem ipsum'))
        # Assert
        self.assertEqual(result, expected)

    def test_WhenFirstLetterIsIncorrect_ReturnsFailure(self):
        # Arrange
        txt = 'Lorem Ipsum'
        parser = bp.CharParser('X')
        # Act
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)
