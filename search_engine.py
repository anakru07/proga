import os
import shelve
import indexer
from indexer import Position_with_lines
import re
from tokenizator_generator_krupina import Tokenizer

class ContextWindow(object):
    """
    This class stores information about context windows
    """
    def __init__(self, positions, line, beginning, end):
        """
        This method creates an instance of ContextWindow class
        @param position: list of positions of the words we search for
        @param line: text of the line with the word
        @param start: position of the first character of the context window
        @param end: position after the last character of the context window
        """
        self.positions = positions
        self.line = line
        self.beginning = beginning
        self.end = end
        
    @classmethod
    def get_from_file(cls, filename, position, context_size):
        t = Tokenizer()
        if not (isinstance(filename, str)
                and isinstance(position, Position_with_lines)
                and isinstance(context_size, int)):
            raise ValueError (filename, position, context_size)

        with open(filename) as f:
            for i, line in enumerate(f):
                if i == position.line:
                    break
        if i != position.line:
            raise ValueError('Wrong line number')
        
        line = line.strip("\n")
        positions = [position]        
        right = line[position.end:]
        left = line[:position.beginning]
        sum_len_left, sum_len_right = 0, 0
        for i in range(context_size):
            try:
                sum_len_left += len(left.split()[-context_size:][i]) + 1
            except IndexError:
                pass
            try:
                sum_len_right += len(right.split()[:context_size][i]) + 1
            except IndexError:
                pass
        beginning = max(0, position.beginning - sum_len_left)
        end = min(len(line), position.end + sum_len_right)
        return cls(positions, line[beginning:end], beginning, end)

    def check_crossing(self, con):
        return (self.beginning <= con.end and
                self.end >= con.beginning and
                con.line == self.line)
    
    def join_contexts(self, con):
        for position in con.positions:
            if position not in self.positions:
                self.positions.append(position)
        self.beginning = min(self.beginning, con.beginning)
        self.end = max(self.end, con.end)

    def expand_context(self):
        
        first = re.compile(r'[.!?]\s[A-ZА-Яa-zа-я]')
        last = re.compile(r'[A-ZА-Яa-zа-я]\s[.!?]')

        right = self.line[self.end:]
        left = self.line[:self.beginning+1:-1]
        
        last_obj = last.match(left) 
        first_obj = first.match(right) 
        if left and last_obj: 
            self.beginning -= last_obj.start()
        if right and first_obj: 
            self.end += first_obj.start() + 1

    def __eq__(self, con):
        return ((self.positions == con.position) and
                (self.line == con.line) and
                (self.beginning == con.beginning) and
                (self.end == con.end))

    def __repr__(self):
        return self.line
        
class SearchEngine(object):
    
    def __init__(self, databasename):
        
        self.database = shelve.open(databasename, writeback=True)

    def single_token_search(self, query):
        
        if not isinstance(query, str):
            raise TypeError        
        if query not in self.database:
            return {}        
        if query == "":
            raise ValueError        
        return self.database[query]

    def multiple_tokens_search(self, query):
        
        if not isinstance(query, str):
            raise TypeError        
        if query == "":
            raise ValueError        
        tokenizer = Tokenizer()
        search_tokens = list(tokenizer.generate_alpha_and_digits(query))
        search_results = []        
        for token in search_tokens:
            if token.word not in self.database:
                return{}
            search_results.append(self.single_token_search(token.word))
        files = set(search_results[0])        
        for result in search_results[1:]:
            files &= set(result)
        final_result = {}
        for file in files:
            for result in search_results:
                final_result[file] = final_result.setdefault(file, []) + result[file]
        return final_result

    def get_window(self, input_dict, context_size=3):
        
        if not (isinstance(input_dict, dict) and
                isinstance(context_size, int)):
            raise ValueError

        contexts_dict = {}
        for f, positions in input_dict.items(): 
            for position in positions:
                context = ContextWindow.get_from_file(f, position, context_size)
                contexts_dict.setdefault(f, []).append(context)

        joined_contexts_dict = self.join_windows(contexts_dict)
        
        return joined_contexts_dict
    
    def join_windows(self, input_dict):
        
        contexts_dict = {}
        null_cont = ContextWindow([], "", 0, 0)
        for f, contexts in input_dict.items():
            previous_context = null_cont
            for context in contexts:
                if previous_context.check_crossing(context):
                    previous_context.join_contexts(context)
                else:
                    if previous_context is not null_cont:
                        contexts_dict.setdefault(f, []).append(previous_context)
                    previous_context = context
            contexts_dict.setdefault(f, []).append(previous_context)
            
        return contexts_dict

    def search_to_context(self, query, context_size):

        positions_dict = self.multiple_tokens_search(query)
        context_dict = self.get_window(positions_dict, context_size)
        return context_dict


    def search_to_sentence(self, query, context_size):

        context_dict = self.search_to_context(query, context_size)
        for contexts in context_dict.values():
            for context in contexts:
                context.to_sentence()
        sentence_dict = self.join_contexts(context_dict)
        return sentence_dict

    def closeDatabase(self):
        self.database.close()
        for filename in os.listdir(os.getcwd()):
            if (filename.startswith('database.')):
                os.remove(filename)
            if (filename.startswith('text')):
                os.remove(filename)


def main():
    indexing = indexer.Indexer('database')
    with open('text.txt', 'w') as test_file_1:
        test_file_1.write('Огромный зал на первом этаже обращен окнами на север, точно художественная студия. На дворе лето, в зале и вовсе тропически жарко, но по-зимнему холоден и водянист свет, что жадно течет в эти окна в поисках живописно драпированных манекенов или нагой натуры, пусть блеклой и зябко-пупырчатой, – и находит лишь никель, стекло, холодно блестящий фарфор лаборатории')

    indexing.indexing_with_lines('text.txt')
    searching = SearchEngine('database')
    result = searching.search_to_context('первом', 6)
    print(result)

    del searching
    for filename in os.listdir(os.getcwd()):
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename)
            
if __name__=='__main__':
    main()
