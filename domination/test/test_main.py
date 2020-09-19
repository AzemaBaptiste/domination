import unittest
from unittest.mock import patch

from domination import __main__


class TestMain(unittest.TestCase):
    def test_main_called(self):
        with patch('faust.App.main') as mocked_faust_app:
            __main__.main()
            mocked_faust_app.assert_called_once()


if __name__ == '__main__':
    unittest.main()
