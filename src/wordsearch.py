from pprint import pprint
from wordgen import WordSearchGen
import random
import string

class WordSearchmaker:

    def is_placeable(self, word, path):
        return not any((step != ' ' and step != char) for (char, step) in zip(word, path))

    def place_word(self, orientation, word, row, col):
        if orientation == "HORIZONTAL":
            for i in range(0, self.length):
                self.grid[row][i] = word[i]
        elif orientation == "VERTICAL":
            for i in range(0, self.length):
                self.grid[i][col] = word[i]
        elif orientation == "DIAGONAL":
            for i in range(0, self.length):
                self.grid[row + i][col+ i] = word[i]

    def _get_new_positions(self, orientation):
        if orientation == "HORIZONTAL":
            max_row_randint_range = self.dim - 1
            max_col_randint_range = abs(self.dim - self.length)
        elif orientation == "VERTICAL":
            max_row_randint_range = abs(self.dim - self.length)
            max_col_randint_range = self.dim - 1
        elif orientation == "DIAGONAL":
            max_row_randint_range = abs(self.dim - self.length)
            max_col_randint_range = abs(self.dim - self.length)

        row = random.randint(0, max_row_randint_range)
        col = random.randint(0, max_col_randint_range)
        return row, col

    def _get_path(self, orientation, row, col):
        if orientation == "HORIZONTAL":
            return [self.grid[row][i] for i in range(self.length)]
        elif orientation == "VERTICAL":
            return [self.grid[i][col] for i in range(self.length)]
        elif orientation == "DIAGONAL":
            return [self.grid[row + i][col + i] for i in range(self.length)]

    def _fill_remaining_spaces(self):
        self.grid = (
            [[string.ascii_lowercase[(random.randint(0,25))] 
            if y == ' ' else y for y in x] for x in self.grid]
        )

    def make_wordsearch(self):
        for word in self.words:
            placement_attempts = 0
            word_key = (word['word'])[::-1] if word['reversed'] else word['word']
            self.length = len(word_key)
            row_spot, col_spot = self._get_new_positions(word['orientation'])
            path = self._get_path(word['orientation'], row_spot, col_spot)

            while not self.is_placeable(word_key, path):
                row_spot, col_spot = self._get_new_positions(word['orientation'])
                path = self._get_path(word['orientation'], row_spot, col_spot)
                placement_attempts += 1
                if placement_attempts == self.max_attempts:
                    self.words = [words for words in self.words if words.get('word') != word['word']]
                    break
            else:
                print("Successfully placed word: ", word, " with path: ", path)
                self.place_word(word['orientation'], word_key, row_spot, col_spot)
        
        self._fill_remaining_spaces()

    def __init__(self, dim, words):
        self.dim = dim
        self.grid  = [[' ' for y in range(x * dim, x * dim + dim)] for x in range(dim)]
        self.wg = WordSearchGen(dim)
        self.words = self.wg.get_wordbank() if not len(words) else words
        self.max_attempts = 10
        self.length = 0
        self.make_wordsearch()


def main():
    ws = WordSearchmaker(5, words = [])

    for row in ws.grid:
        print(" ".join(row))
    pprint([word['word'] for word in ws.words])

if __name__ == '__main__':
    main()