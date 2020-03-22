import unittest
import loader as Loader
from unittest.mock import Mock


class TestLoader(unittest.TestCase):
    def test_is_tool(self):
        result = Loader.is_tool('bash')
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
