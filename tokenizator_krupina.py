"""This tokenizer is meant to find tokens in the text given.

Token is a word which in this case means a sequence of alphabetical symbols.
"""

class Token(object):
    """Define a class Token which is going to contain all the tokens we are about to find."""
    
    def __init__(self, position, word):
        """ Initializes tokens
        :param position: position of the first letter of a word in a sequence given.
        :param word: a sequence of alphabetical symbols forming a word itself.
        """
        self.position = position
        self.word = word
        
class Tokenizer(object):
    """Create a class which contains a function of tokenizing."""
    
    def tokenize(self, given):
        """The function "tokenize" searches for words(tokens) in our sequence.

        :param given: a sequence of alphabetical and non-alphabetical symbols.
    
        :return: a list of tokens.
        """
        
        if not isinstance(given,str):
            raise ValueError('Value error')

        if not given:
            return []
        
        tokens = []   # Create an empty list of tokens which it to be fulfilled later
        # The index can assume either a value of -1 or the value of the position of the symbol 
        index = -1
          
        for i, s in enumerate(given):
            # Check if the symbol in question is the end of a word
            if index > -1 and not s.isalpha():
                # If so, add the token to the list of tokens
                tokens.append(Token(index, given[index:i]))  
                index = -1
            # Check whether the symbol in question is the beginning of a word
            if index == -1 and s.isalpha(): 
                index = i
        # Check the last symbol of the sequence to see whether it is the end of a word
        # If so, add this word to our list of tokens
        if s.isalpha():
            tokens.append(Token(index, given[index:i+1]))
        return tokens

    def generator_tokenizer(self, given):
        """The function "tokenize" searches for words(tokens) in our sequence.

        :param given: a sequence of alphabetical and non-alphabetical symbols.
    
        :yield: a list of tokens.
        """
        
        if not isinstance(given,str):
            raise ValueError('Value error')

        if not given:
            return

        # The index can assume either a value of -1 or the value of the position of the symbol
        index = -1
          
        for i, s in enumerate(given):
            # Check if the symbol in question is the end of a word
            if index > -1 and not s.isalpha():
                token = (Token(index, given[index:i]))  
                index = -1
                yield token
            # Check whether the symbol in question is the beginning of a word
            if index == -1 and s.isalpha(): 
                index = i
        # Check the last symbol of the sequence to see whether it is the end of a word
        if s.isalpha():
            token = (Token(index, given[index:i+1]))
        yield token

if __name__ == '__main__':

    given = "cew r 2r 2 2 rwr44f4fyuvyk"

    words = Tokenizer().tokenize(given)  # Apply our function of tokenizing to a text given

    for token in words:
        print(token.word, token.position)  # Print each token found and its position

    generator_words = Tokenizer().generator_tokenizer(given)  # Apply our function of generating to a text given

    for token in generator_words:
        print(token.word, token.position) # Print each element found and its position
