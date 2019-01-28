import shelve
import os
from tokenizator_generator_krupina import Tokenizer

class Position(object):

    def __init__(self, beginning, end):
        self.beginning = beginning
        self.end = end

    def __eq__(self, obj):
        return (self.beginning == obj.beginning and self.end == obj.end)

    def __repr__(self):
        return '(' + str(self.beginning) + ',' + ' ' + str(self.end) + ')'

class Position_with_lines(object):

    def __init__(self, beginning, end, line):
        self.beginning = beginning
        self.end = end
        self.line = line

    def __eq__(self,obj):
        return (self.beginning == obj.beginning and self.end == obj.end and
                self.line == obj.line)

    def __repr__(self):
        return '(' + str(self.beginning) + ',' + ' ' + str(self.end) + \
             ',' + ' ' + str(self.line) + ')'

class Indexer(object):

    def __init__(self, database_name):
        self.database = shelve.open(database_name, writeback=True)

    def indexing(self, filename):

        tokenizer = Tokenizer()

        if not isinstance(filename, str):
            raise ValueError

        try:
            file = open(filename)
        except IOError:
            raise FileNotFoundError

        for token in tokenizer.generator_with_types(file.read()):
            i = token.position + len(token.string)
            self.database.setdefault(token.string, {}).setdefault(filename, []).append(
                Position(token.position, i)
            )
        file.close()
        self.database.sync()

    def indexing_with_lines(self, filename):
        
        tokenizer = Tokenizer()

        if not isinstance(filename, str):
            raise ValueError

        try:
            file = open(filename)
        except IOError:
            raise FileNotFoundError

        for linenumber, line in enumerate(file):
            for token in tokenizer.generator_with_types(file.read()):
                i = token.position + len(token.string)
                self.database.setdefault(token.string, {}).setdefault(filename, []).append(
                    Position_with_lines(token.position, i, line)
                )
        file.close()
        self.database.sync()

    def __del__(self):
        self.database.close()

def main():
    indexator = Indexer('database')
    file = open('text.txt', 'w')
    file.write('this is my testing ground')
    file.close()
    indexator.indexing_with_lines('text.txt')
    del indexator
    os.remove('text.txt')
    print(dict(shelve.open('database')))
    for filename in os.listdir(os.getcwd()):            
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename)   


if __name__=='__main__':
    main()







        
