import unittest
import os
import shelve
from indexer import Indexer, Position, Position_with_lines

class IndexerTest(unittest.TestCase):
    def setUp(self):
        self.indexer = Indexer("database")

    def tearDown(self):
        del self.indexer
        for filename in os.listdir(os.getcwd()):
            if (filename == "database" or filename.startswith("database.")):
                os.remove(filename)
            if "text.txt" in os.listdir(os.getcwd()):
                os.remove("text.txt")

    def test_wrong_input(self):
        with self.assertRaises(FileNotFoundError):
            self.indexer.indexing("i am not a document")

    def test_error_wrong_input_wrong_path(self):
        with self.assertRaises(FileNotFoundError): 
            self.indexer.indexingw("текст.txt")
            
    def test_one_word(self):
        test = open("text.txt", 'w' )
        test.write("programming")
        test.close()
        self.indexer.indexing("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "programming":{"text.txt": [Position(0, 10)]
        }}
        self.assertEqual(words1, words2)

    def test_two_words(self):
        test = open("text.txt", 'w' )
        test.write("my test")
        test.close()
        self.indexer.indexing("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "my":{"text.txt": [Position(0, 2)]},
            "test":{"text.txt": [Position(3, 7)]
        }}
        self.assertEqual(words1, words2)

    def test_two_identical_words(self):
        test = open("text.txt", 'w' )
        test.write("my my")
        test.close()
        self.indexer.index("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "my":{"text.txt": [Position(0, 2),
                               Position(3, 5)]
        }}
        self.assertEqual(words1, words2)
                  
    def test_two_files(self):
        test = open("text.txt", 'w' )
        test.write("test")
        test.close()
        test = open("text1.txt", 'w' )
        test.write("my my")
        test.close()
        self.indexer.indexing("text.txt")
        self.indexer = Indexer('database')
        self.indexer.indexing("text1.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "my":{"text.txt": [Position(0, 2),
                               Position(3, 5)]},
            "test":{"text.txt": [Position(0, 4)]
        }}
        self.assertEqual(words1, words2)

    def test_multiple_lines(self):
        test = open("text.txt", 'w' )
        test.write("testing\nground")
        test.close()
        self.indexer.indexing_with_lines("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "testing":{"text.txt": [Position(0, 7, 0)},
            "ground":{"text.txt": [Position(0, 6, 1)]
        }}
        self.assertEqual(words1, words2)

if __name__ == '__main__':
    unittest.main()
