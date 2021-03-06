import unittest
import os
from indexer import Position_with_lines
from search_engine import SearchEngine
from search_engine import ContextWindow

database = {'this': {'test1.txt': [Position_with_lines(0, 4, 0)]},
            'is': {'test1.txt': [Position_with_lines(5, 7, 0)]},
            'my': {'test1.txt': [Position_with_lines(8, 10, 0)]},
            'testing': {'test1.txt': [Position_with_lines(11, 18, 0)],
                        'test2.txt': [Position_with_lines(0, 7, 0)]},
            'ground': {'test1.txt': [Position_with_lines(19, 24, 0)],
                       'test2.txt': [Position_with_lines(8, 14, 0)]},
            'for': {'test2.txt': [(15, 18)]},
            'search': {'test2.txt': [(19, 25)]},
            'Engine': {'test2.txt': [(27, 33)]}
            }

test1 = 'this is my testing ground'
test2 = 'testing ground for search. Engine'

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
   
    def tearDown(self):
        if 'test1.txt' in os.listdir(os.getcwd()):
            os.remove('test1.txt')
        if 'test2.txt' in os.listdir(os.getcwd()):
            os.remove('test2.txt')    

class TestContextWindow(unittest.TestCase):

    def setUp(self):
        self.engine = SearchEngine('database')
        self.engine.database.update(database)
        test = open("test1.txt", 'w')
        test.write(test1)
        test.close()
        test = open("test2.txt", 'w')
        test.write(test2)
        test.close()
        
    def test_input(self):
        with self.assertRaises(ValueError):
            ContextWindow.get_from_file(9, 'арбуз', 7)

    def test_simple(self):
        result = ContextWindow.get_from_file("test1.txt", Position_with_lines(8, 10, 0), 1)
        self.assertEqual(result.positions, [Position_with_lines(8, 10, 0)])
        self.assertEqual(result.beginning, 4)
        self.assertEqual(result.end, 19)
        self.assertEqual(result.line, test1)

    def test_cross_sentence_boundary(self):
        result = ContextWindow.get_from_file("test1.txt", Position_with_lines(5, 7, 0), 2)
        self.assertEqual(result.positions, [Position_with_lines(5, 7, 0)])
        self.assertEqual(result.beginning, 0)
        self.assertEqual(result.end, 19)
        self.assertEqual(result.line, test1)

    def test_join_contexts(self):    
        result1 = ContextWindow.get_from_file("test1.txt", Position_with_lines(5, 7, 0), 2)
        result2 = ContextWindow.get_from_file("test1.txt", Position_with_lines(8, 10, 0), 2)
        self.con = ContextWindow([Position_with_lines(5, 7, 0), Position_with_lines(8, 10, 0)], 'this is my testing ground', 0, 25)
        self.assertEqual(result1.beginning, self.con.beginning)
        self.assertEqual(result2.end, self.con.end)
        self.assertEqual(result1.line, self.con.line)
        os.remove('test1.txt')
    
    def test_join_contexts_sent_bound(self):
        result1 = ContextWindow.get_from_file("test2.txt", Position_with_lines(15, 18, 0), 1)
        result2 = ContextWindow.get_from_file("test2.txt", Position_with_lines(27, 33, 0), 1)
        self.con = ContextWindow([Position_with_lines(15, 18, 0), Position_with_lines(27, 33, 0)], 'testing ground for search. Engine blah bla', 7, 39)
        self.assertEqual(result1.beginning, self.con.beginning)
        self.assertEqual(result2.end, self.con.end)
        self.assertEqual(result1.line, self.con.line)
        os.remove('test2.txt')

    def test_join_contexts_sent_bound2(self):
        result1 = ContextWindow.get_from_file("test2.txt", Position_with_lines(15, 18, 0), 1)
        result2 = ContextWindow.get_from_file("test2.txt", Position_with_lines(34, 38, 0), 1)
        self.con = ContextWindow([Position_with_lines(15, 18, 0), Position_with_lines(34, 38, 0)], 'testing ground for search. Engine blah bla', 7, 42)
        self.assertEqual(result1.beginning, self.con.beginning)
        self.assertEqual(result2.end, self.con.end)
        self.assertEqual(result1.line, self.con.line)
        os.remove('test2.txt')

    def test_expand_context(self):
        query = ContextWindow.get_from_file("test2.txt", Position_with_lines(0, 7, 0), 2)
        query.expand_context()
        text = 'testing ground for search.'
        self.assertEqual(str(query), text)
            
    def test_expand_contexts_sent_bound1(self):
        result = ContextWindow.get_from_file("test2.txt", Position_with_lines(19, 25, 0), 2)
        result.expand_context()
        text = 'testing ground for search.'
        self.assertEqual(str(result), text)

    def test_highlight(self):
        query = ContextWindow.get_from_file("test1.txt", Position_with_lines(5, 7, 0), 1)
        query = query.highlight()
        text = 'this <B>is</B> my '
        self.assertEqual(str(query), text)

    def tearDown(self):
        if 'test1.txt' in os.listdir(os.getcwd()):
            os.remove('test1.txt')
        if 'test2.txt' in os.listdir(os.getcwd()):
            os.remove('test2.txt')    

if __name__ == '__main__':
    unittest.main()
