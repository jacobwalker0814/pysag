import unittest
import os
import mockfs
import json
import datetime

from .. import Reader
from .. import Writer


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()

    # Helper function for defining path to a fixture dir
    def fixture_dir(self, dir):
        return '%s/fixtures/%s' % (os.path.dirname(__file__), dir)

    def test_read_simple_single(self):
        result = self.reader.read(self.fixture_dir('simple_single'))

        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 1, 'There should only be 1 entry in the list')
        self.assertEqual(result['users'][0], {'_id': '1', 'name': 'Kell'}, 'The node should match my data')

    def test_read_simple_multiple(self):
        result = self.reader.read(self.fixture_dir('simple_multiple'))

        self.assertTrue('people' in result, '\'people\' key must be in result')
        self.assertIs(type(result['people']), list, '\'people\' must be a list')
        self.assertEqual(len(result['people']), 3, 'There should be 3 entries in the list')

    def test_read_only_yaml(self):
        # Parse the fixture which contains yml and other files
        result = self.reader.read(self.fixture_dir('read_only_yaml'))

        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 1, 'There should only be 1 entry in the list')

    def test_ignore_invalid_yaml(self):
        result = self.reader.read(self.fixture_dir('ignore_invalid_yaml'))

        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 1, 'There should only be 1 entry in the list')

    def test_make_empty_list_for_empty_dirs(self):
        result = self.reader.read(self.fixture_dir('empty_dirs'))

        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 0, 'The list should be empty')

        self.assertTrue('projects' in result, '\'projects\' key must be in result')
        self.assertIs(type(result['projects']), list, '\'projects\' must be a list')
        self.assertEqual(len(result['projects']), 1, 'There should only be 1 entry in the list')

    def test_properties_with_markdown(self):
        result = self.reader.read(self.fixture_dir('markdown_property'))

        self.assertTrue('users' in result, '\'users\' key must be in result')
        self.assertIs(type(result['users']), list, '\'users\' must be a list')
        self.assertEqual(len(result['users']), 1, 'There should be one entry')

        expected = {
            '_id': '1',
            'name': 'Jacob',
            'profile': '<p>This guy <strong>really</strong> likes markdown</p>'
        }
        self.assertEqual(result['users'][0], expected)


class Writertest(unittest.TestCase):
    # TODO test failure when directory already exists
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
        data = {
            'users': [{'_id': '1', 'name': 'Kell'}]
        }

        self.mfs.makedirs('/site/api')
        output_dir = '/site/api'
        self.writer.write_api(data, output_dir)

        # A file should have been made for all of our users
        self.assertFileExists(output_dir + '/users.json')
        expected = {
            'result': [
                {'_id': '1', 'name': 'Kell'}
            ]
        }
        content = self.parse_json_file(output_dir + '/users.json')
        self.assertEqual(content, expected)

        # A directory should have been made to hold individual users
        self.assertDirExists(output_dir + '/users')
        self.assertFileExists(output_dir + '/users/1.json')
        expected = {
            'result': {
                '_id': '1',
                'name': 'Kell'
            }
        }
        content = self.parse_json_file(output_dir + '/users/1.json')
        self.assertEqual(content, expected)

    def test_writing_datetimes(self):
        """
        Test that datetime objects can be serialized to JSON. The yaml reader
        will have converted strings like "2014-10-09" into datetimes and we
        want to simply convert it back.
        """
        data = {
            'posts': [{'_id': '1', 'date': datetime.date(2014, 10, 9)}]
        }

        self.mfs.makedirs('/site/api')
        output_dir = '/site/api'
        self.writer.write_api(data, output_dir)

        expected = {
            'result': {
                '_id': '1',
                'date': '2014-10-09'
            }
        }
        content = self.parse_json_file(output_dir + '/posts/1.json')
        self.assertEqual(content, expected)
