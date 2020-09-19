import unittest
from unittest.mock import patch, call

from domination import process


class TestProcessHumanRating(unittest.TestCase):
    def test_ok(self):
        human = process.HumanRating(rating=18, unique_id="unique_123")
        with patch('logging.info') as mocked_logging:
            process.process_human_rating(human)
            assert mocked_logging.mock_calls == [call('Sha')]

    def test_rating_not_integer(self):
        human = process.HumanRating(rating="18", unique_id="unique_123")
        with self.assertRaises(ValueError):
            process.process_human_rating(human)


if __name__ == '__main__':
    unittest.main()
