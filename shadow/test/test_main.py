import unittest
from unittest.mock import MagicMock, call

from shadow import ShaDow


class TestEvaluate(unittest.TestCase):
    def test_evaluate_return_number(self):
        self.assertEqual(ShaDow.evaluate(1), 1)
        self.assertEqual(ShaDow.evaluate(4), 4)
        self.assertEqual(ShaDow.evaluate(352), 352)

    def test_evaluate_return_Sha(self):
        self.assertEqual(ShaDow.evaluate(3), 'Sha')
        self.assertEqual(ShaDow.evaluate(9), 'Sha')
        self.assertEqual(ShaDow.evaluate(3 * 2343443), 'Sha')

    def test_evaluate_return_Dow(self):
        self.assertEqual(ShaDow.evaluate(5), 'Dow')
        self.assertEqual(ShaDow.evaluate(10), 'Dow')
        self.assertEqual(ShaDow.evaluate(5000), 'Dow')
        self.assertEqual(ShaDow.evaluate(5 * 1323211), 'Dow')

    def test_evaluate_return_Shadow(self):
        self.assertEqual(ShaDow.evaluate(15), 'ShaDow')
        self.assertEqual(ShaDow.evaluate(30), 'ShaDow')
        self.assertEqual(ShaDow.evaluate(30), 'ShaDow')
        self.assertEqual(ShaDow.evaluate(230145), 'ShaDow')
        self.assertEqual(ShaDow.evaluate(15 * 9983643), 'ShaDow')


class TestWorker(unittest.TestCase):
    def test_worker(self):
        shadow = ShaDow()
        shadow.evaluate = MagicMock()

        shadow.worker(2)
        shadow.evaluate.assert_called_with(2)


class TestGenerator(unittest.TestCase):
    def test_numbers_1_to_20(self):
        expected = [1, 2, 'Sha', 4, 'Dow', 'Sha', 7, 8, 'Sha', 'Dow',
                    11, 'Sha', 13, 14, 'ShaDow', 16, 17, 'Sha', 19, 'Dow']
        with unittest.mock.patch('builtins.print') as mocked_print:
            ShaDow().generator(20)
            self.assertEqual(20, len(mocked_print.mock_calls))
            self.assertEqual([call(e) for e in expected], mocked_print.mock_calls)


if __name__ == '__main__':
    unittest.main()
