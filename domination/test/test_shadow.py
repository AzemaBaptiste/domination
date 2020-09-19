import unittest
from unittest.mock import MagicMock, call

from domination.shadow import ShaDow


class TestEvaluate(unittest.TestCase):
    def test_evaluate_return_number(self):
        self.assertEqual(ShaDow.evaluate(1), 'Incompatible')
        self.assertEqual(ShaDow.evaluate(4), 'Incompatible')
        self.assertEqual(ShaDow.evaluate(352), 'Incompatible')

    def test_evaluate_return_sha(self):
        self.assertEqual(ShaDow.evaluate(3), 'Sha')
        self.assertEqual(ShaDow.evaluate(9), 'Sha')
        self.assertEqual(ShaDow.evaluate(3 * 2343443), 'Sha')

    def test_evaluate_return_dow(self):
        self.assertEqual(ShaDow.evaluate(5), 'Dow')
        self.assertEqual(ShaDow.evaluate(10), 'Dow')
        self.assertEqual(ShaDow.evaluate(5000), 'Dow')
        self.assertEqual(ShaDow.evaluate(5 * 1323211), 'Dow')

    def test_evaluate_return_shadow(self):
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
        expected = ['Incompatible', 'Incompatible', 'Sha', 'Incompatible', 'Dow', 'Sha',
                    'Incompatible', 'Incompatible', 'Sha', 'Dow', 'Incompatible', 'Sha',
                    'Incompatible', 'Incompatible', 'ShaDow', 'Incompatible', 'Incompatible',
                    'Sha', 'Incompatible', 'Dow']
        with unittest.mock.patch('logging.info') as mocked_logging_info:
            ShaDow().generator(20)
            self.assertEqual(20, len(mocked_logging_info.mock_calls))
            self.assertEqual([call(e) for e in expected], mocked_logging_info.mock_calls)


if __name__ == '__main__':
    unittest.main()
