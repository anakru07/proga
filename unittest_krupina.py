import unittest
from tokenizator_generator_krupina import Tokenizer

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_only_alpha(self):
        result = self.tokenizer.tokenize('This is my testing ground')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_begin_with_non_alpha(self):
        result = self.tokenizer.tokenize('/This is my testing ground')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 20)

    def test_end_with_non_alpha(self):
        result = self.tokenizer.tokenize('This is my testing ground/')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_begin_with_multiple_non_alpha(self):
        result = self.tokenizer.tokenize('/.!This is my testing ground')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 3)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 22)

    def test_end_with_multiple_non_alpha(self):
        result = self.tokenizer.tokenize('This is my testing ground!./')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_non_alpha_middle(self):
        result = self.tokenizer.tokenize('This is my! testing ground')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 20)

    def test_multiple_non_alpha_middle(self):
        result = self.tokenizer.tokenize('This is my(!) testing ground')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 22)

    def test_empty_string(self):
        result = self.tokenizer.tokenize('')
        self.assertEqual(len(result), 0)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize([679])

        
    def test_gen_only_alpha(self):
        result = list(self.tokenizer.generator_tokenizer('This is my testing ground'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_gen_begin_with_non_alpha(self):
        result = list(self.tokenizer.generator_tokenizer('/This is my testing ground'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 20)

    def test_gen_end_with_non_alpha(self):
        result = list(self.tokenizer.generator_tokenizer('This is my testing ground/'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_gen_begin_with_multiple_non_alpha(self):
        result = list(self.tokenizer.generator_tokenizer('/.!This is my testing ground'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 3)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 22)

    def test_gen_end_with_multiple_non_alpha(self):
        result = list(self.tokenizer.generator_tokenizer('This is my testing ground!./'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 19)

    def test_gen_non_alpha_middle(self):
        result = list(self.tokenizer.generator_tokenizer('This is my! testing ground'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 20)

    def test_gen_multiple_non_alpha_middle(self):
        result = list(self.tokenizer.generator_tokenizer('This is my(!) testing ground'))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].word, 'This')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].word, 'ground')
        self.assertEqual(result[4].position, 22)

    def test_gen_empty_string(self):
        result = list(self.tokenizer.generator_tokenizer(''))
        self.assertEqual(len(result), 0)

    def test_gen_value_error(self):
        with self.assertRaises(ValueError):
            list(self.tokenizer.generator_tokenizer([679]))


    def test_gt_empty_string(self):
        result = list(self.tokenizer.generator_with_types(''))
        self.assertEqual(len(result), 0)

    def test_gt_a(self):
        result = list(self.tokenizer.generator_with_types('T'))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, 'T')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 'a')

    def test_gt_d(self):
        result = list(self.tokenizer.generator_with_types('4'))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, '4')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 'd')

    def test_gt_s(self):
        result = list(self.tokenizer.generator_with_types(' '))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, ' ')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 's')

    def test_gt_p(self):
        result = list(self.tokenizer.generator_with_types('.'))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, '.')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 'p')

    def test_gt_o(self):
        result = list(self.tokenizer.generator_with_types('⏰'))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].word, '⏰')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 'o')

    def test_gt_type_change(self):
        result = list(self.tokenizer.generator_with_types('Ух!'))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].word, 'Ух')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[0].typ, 'a')
        self.assertEqual(result[1].word, '!')
        self.assertEqual(result[1].position, 2)
        self.assertEqual(result[1].typ, 'p')
        
if __name__ == '__main__':
    unittest.main()
