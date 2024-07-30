import os
import sys
import unittest
from unittest.mock import Mock

# Get the directory containing this test file
test_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (which should contain loader.py)
parent_dir = os.path.dirname(test_dir)
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# Now we can import the loader module
import loader as Loader

class TestLoader(unittest.TestCase):
    def test_is_tool(self):
        result = Loader.is_tool('bash')
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
