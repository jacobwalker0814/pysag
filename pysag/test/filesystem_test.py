import unittest
import os
from .. import Reader
from .. import DataNode


class DataNodeTest(unittest.TestCase):
    def test_getting_what_you_give(self):
        data = {"foo": "bar", "num": 1, "list": [4, 2]}
        node = DataNode()
        node.populate(data)
        self.assertEqual(data, node.export())


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()
        self.fixture_base = os.path.dirname(__file__)

    def test_read_simple_single(self):
        # Parse the fixture
        fixture_path = self.fixture_base + '/fixtures/simple_single'
        result = self.reader.read(fixture_path)

        # See what we got
        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 1, 'There should only be 1 entry in the list')
        self.assertIsInstance(result['users'][0], DataNode, 'The entry in the list should be a DataNode')
        self.assertEqual(result['users'][0].export(), {'id': '1', 'name': 'Kell'}, 'The DataNode should match my data')

    # TODO read only yml
    # TODO read multiple
    # TODO test failure cases

if __name__ == '__main__':
    unittest.main()
