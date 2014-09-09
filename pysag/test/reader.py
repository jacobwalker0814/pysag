import unittest
from pysag import Reader


class ReaderTest(unittest.TestCase):
    def setup(self):
        self.reader = Reader()

    def test_read_simple_single(self):
        expected = {
            "users": [
                {
                    "id": 1,
                    "name": "Kell"
                }
            ]
        }
        result = self.reader.read('./fixtures/simple_single')
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
