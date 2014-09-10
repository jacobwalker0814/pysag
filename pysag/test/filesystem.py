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
        expected = {
            'users': [
                {
                    'id': '1',
                    'name': 'Kell'
                }
            ]
        }
        fixture_path = self.fixture_base + '/fixtures/simple_single'
        result = self.reader.read(fixture_path)
        self.assertEqual(result, expected)

    # TODO read only yml
    # TODO read multiple
    # TODO test failure cases

if __name__ == '__main__':
    unittest.main()
