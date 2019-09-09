import unittest
import src.Monads.Result as res
import src.Parsers.BasicParsers as bp


class TestLParsers(unittest.TestCase):
    def test_WhenFirstLetterIsCorrect_ReturnsSuccess(self):
        # Arrange
        txt = 'Lorem ipsum'
        parser = bp.LParser('L')
        # Act
        result = parser(txt)
        expected = res.Success(('L', 'orem ipsum'))
        # Assert
        self.assertEqual(result, expected)

    def test_WhenFirstLetterIsIncorrect_ReturnsFailure(self):
        # Arrange
        txt = 'Lorem Ipsum'
        parser = bp.LParser('X')
        # Act
        result = parser(txt)
        expected = res.Failure('error')
        # Assert
        self.assertEqual(result, expected)

    def test_WrongArgumentPassedToConstructor_RaisesException(self):
        # Act
        with self.assertRaises(Exception) as context:
            bp.LParser(123)
        # Assert
        self.assertEqual('Incorrect initialization of parsers',
                         str(context.exception))

    def test_WhenLabelIsGiven_ReturnsLabel(self):
        # Arrange
        parser = bp.LParser('X', 'SomeLabel')
        # Assert
        self.assertEqual(parser.label, 'SomeLabel')

    def test_WhenConstructorCalledWithStringAndNoLabel_ReturnsPredefinedLabel(self):
        # Arrange
        parser = bp.LParser('X')
        # Assert
        self.assertEqual(parser.label, 'X')

    def test_WhenConstructorCalledWithFuncAndNoLabel_ReturnsPredefinedLabel(self):
        # Arrange
        parser = bp.LParser(lambda x: x)
        # Assert
        self.assertEqual(parser.label, 'Unknown parser')
