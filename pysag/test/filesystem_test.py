import unittest
import os
import mockfs
import json

from .. import DataNode
from .. import Reader
from .. import Writer


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


class Writertest(unittest.TestCase):
    def setUp(self):
        self.mfs = mockfs.replace_builtins()
        self.writer = Writer()

    def tearDown(self):
        mockfs.restore_builtins()

    # A little helper for getting the contents of a JSON file
    def parse_json_file(self, path):
        with open(path) as f:
            return json.load(f)

    # Assertion helper
    def assertFileExists(self, path):
        self.assertTrue(os.path.isfile(path), "File %s does not exists" % path)

    # Assertion helper
    def assertDirExists(self, path):
        self.assertTrue(os.path.isdir(path), "Directory %s does not exists" % path)

    def test_writing_single_simple(self):
        node = DataNode()
        node.populate({'id': '1', 'name': 'Kell'})
        data = {
            'users': [node]
        }

        self.mfs.makedirs('/site/api')
        output_dir = '/site/api'
        self.writer.write(data, output_dir)

        # A file should have been made for all of our users
        self.assertFileExists(output_dir + '/users.json')
        expected = {
            'result': [
                {'id': '1', 'name': 'Kell'}
            ]
        }
        content = self.parse_json_file(output_dir + '/users.json')
        self.assertEqual(content, expected)

        # A directory should have been made to hold individual users
        self.assertDirExists(output_dir + '/users')
        self.assertFileExists(output_dir + '/users/1.json')
        expected = {
            'result': {
                'id': '1',
                'name': 'Kell'
            }
        }
        content = self.parse_json_file(output_dir + '/users/1.json')
        self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()
