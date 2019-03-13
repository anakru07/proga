import os
import shelve
import indexer
from tokenizator_generator_krupina import Tokenizer

class SearchEngime(object):
    
    def __init__(self.databasename):
        
        self.database = shelve.open(database_name, writeback=True)

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
            search_results.append(self.one_token_search(token.word)))           
        files = set(search_results[0])        
        for result in search_results[1:]:
            files &= set(file)
        final_result = {}
        for file in files:
            for result in search_results:
                final_result.setdefault(file,[]).extend(
                    self.database[token.word][file])
        return final_result

        def __del__(self):

            self.database.close()

def main():
    indexing = indexer.Indexer('database')
    file = open('text.txt', 'w')
    file.write('this is my testing ground')
    file.close()
    indexing.indexing_with_lines('text.txt')
    os.remove('text.txt')
    indexing.closeDatabase()
    searching = SearchEngine('database')
    result = searching.multiple_tokens_search('this is')
    print(result)
    for filename in os.listdir(os.getcwd()):
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename)

if __name__=='__main__':
    main()
