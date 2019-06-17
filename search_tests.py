import unittest
from indexer import Position_with_lines
from search_engine import SearchEngine


database = {'this': {'test1.txt': [Position_with_lines(0, 4, 0)]},
            'is': {'test1.txt': [Position_with_lines(5, 7, 0)]},
            'my': {'test1.txt': [Position_with_lines(8, 10, 0)]},
            'testing': {'test1.txt': [Position_with_lines(11, 18, 0)],
                        'test2.txt': [Position_with_lines(0, 7, 0)]},
            'ground': {'test1.txt': [Position_with_lines(19, 24, 0)],
                       'test2.txt': [Position_with_lines(8,14,0)]},
            'for': {'test2.txt': [(15, 18)]},
            'search': {'test2.txt': [(19, 25)]},
            'engine': {'test2.txt': [(26, 32)]}
            }


test1 = 'this is my testing ground'
test2 = "testing ground for search engine"


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SearchEngine('database')
        self.engine.database.update(database)
        test = open("test1.txt", 'w')
        test.write(test1)
        test.close()
        test = open("test2.txt", 'w')
        test.write(test2)
        test.close()

    def test_empty(self):
        result = self.engine.single_token_search('')
        self.assertEqual(result, {})

    def test_search_one(self):
        result = self.engine.single_token_search('for')
        self.assertEqual(result, {'test2.txt': [(15, 18)]})

    def test_search_many_one(self):
        result = self.engine.multiple_tokens_search('testing')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(11, 18, 0)],
                                  'test2.txt': [Position_with_lines(0, 7, 0)]})

    def test_search_many_two(self):
        result = self.engine.multiple_tokens_search('testing ground')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(11, 18, 0), Position_with_lines(19, 24, 0)],
                                  'test2.txt': [Position_with_lines(0, 7, 0), Position_with_lines(8, 14, 0)]})


if __name__ == '__main__':
    unittest.main()