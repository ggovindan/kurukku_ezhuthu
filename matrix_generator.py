import random
import tamil
from utils import ACROSS, DOWN, calculate_next_pos, will_fit, length, find_all_char_pos, calculate_free_rows, get_letters
from utils import print_matrix, find_intersection

class CrosswordGen(object):
    def __init__(self, dimension=(11,11), lang="tamil"):
        self.lang = lang
        self.width = dimension[0]
        self.height = dimension[1]
        self.filled_pos = {}
        self.puzzle_matrix = [[" " for i in range(self.width)] for j in range(self.height)]

    def generate_puzzle(self, words_clues = None):
        if not words_clues:
            print("generate puzzle needs a list of words and clues in"
            "the following format [{'answer': 'வணக்கம்', 'clue': 'hello in tamil'}]")
            return None
        result = []
        across = 1
        down = 1
        num_puzzle = len(words_clues) - 1
        while num_puzzle >= 0:
            rand_num = random.randint(0, num_puzzle)
            p = words_clues.pop(rand_num)
            num_puzzle -= 1
            if len(p['answer']) >= self.width:
                continue
            x = self._find_best_fit(p)
            x['startx'], x['starty'] = x['starty'], x['startx']
            if x['orientation'] == 'across':
                x['position'] = across
                across += 1
            else:
                x['position'] = down
                down += 1
            result.append(x)
            print_matrix(self.puzzle_matrix, self.width)
        print(result)


    def _fill_word_in_matrix(self, word, orientation=ACROSS, start_elem=(0, 0)):
        i, j = start_elem
        self.filled_pos[word] = {'position': (i, j), 'orientation': orientation}
        if orientation == ACROSS:
            for l in get_letters(word, self.lang):
                self.puzzle_matrix[i][j] = l
                j += 1
        else:
            for l in get_letters(word, self.lang):
                self.puzzle_matrix[i][j] = l
                i += 1

    def _check_overlap(self, word, orientation, x, y):
        i, j = x, y
        next_pos = calculate_next_pos[orientation](i, j, length(word, self.lang))
        for a in get_letters(word, self.lang):
            try:
                (i, j) = next(next_pos)
                print("i={} j={}".format(i, j))
            except StopIteration as e:
                print("stop iteration received after will fit word={} i, j={}".format(word, (i, j)))

            if self.puzzle_matrix[i][j] != " ":
                if self.puzzle_matrix[i][j] == a:
                    continue
                else:
                    print("Overlap of letter {} with {} at {}".format(a, self.puzzle_matrix[i][j], (i, j)))
                    return True
        return False

    def _find_best_fit(self, puzzle):
        """
        calculate the best fit for a given word.
        Prefer words with intersections over non intersecting spaces
        :return: position (x, y) in the puzzle_matrix
        """

        word = puzzle['answer']

        # if first word
        print(len(self.filled_pos))
        if len(self.filled_pos) == 0:
            x = random.randint(0,4)
            y = random.randint(0,4)
            print("first_word: {} x:{} y:{}".format(word, x, y))
            print("will_fit: {}".format(will_fit[ACROSS](x, y, length(word, self.lang))))
            if will_fit[ACROSS](x, y, length(word, self.lang)):
                puzzle['orientation'] = "across"
                # puzzle['position'] = t + 1
                puzzle['startx'] = x + 1
                puzzle['starty'] = y + 1
                self._fill_word_in_matrix(word, ACROSS, (x,y))
                return puzzle

        # first find the location where it overlaps.. then move to the other ones to keep it interesting
        for key in self.filled_pos:
            #the orientation for this word should be perpendicular to the one we are trying to match
            pos = int(not self.filled_pos[key]['orientation'])
            # find the intersecting letters between the two words
            intersect = find_intersection(key, word, self.lang)
            print("trying to intersect filled_word={} with word={}".format(key, word))
            if len(intersect) == 0:
                # no letters matched.. lets find the next
                continue
            else:
                a = [-10, -10]
                print("intersecting letters={}".format(intersect))
                for letter in intersect:
                    indexes1 = find_all_char_pos(key, letter, self.lang)
                    for index in indexes1:
                        # index = filled_pos[key]['word'].find(letter)
                        print("location of the letter={} in word={} is {}".format(letter, key, index))
                        filled_word_pos = self.filled_pos[key]['position']
                        a[pos] = filled_word_pos[pos] + index
                        indexes2 = find_all_char_pos(word, letter, self.lang)
                        for index2 in indexes2:
                            # index2 = word.find(letter)
                            print("location of the letter={} in word={} is {}".format(letter, word, index2))
                            a[self.filled_pos[key]['orientation']] = filled_word_pos[int(not pos)]  - index2
                            print("looking for match in location={}".format(a))
                            print("will_fit={}".format(will_fit[pos](a[0], a[1], length(word, self.lang))))
                            if will_fit[pos](a[0], a[1], length(word, self.lang)):
                                if not self._check_overlap(word, pos, a[0], a[1]):
                                    self._fill_word_in_matrix(word, pos, (a[0], a[1]))
                                    calculate_free_rows(self.puzzle_matrix, self.height)
                                    puzzle['orientation'] = "down" if pos else "across"
                                    # puzzle['position'] = t + 1
                                    puzzle['startx'] = a[0] + 1
                                    puzzle['starty'] = a[1] + 1
                                    return puzzle
        # if we are still here then we havent found a place for this word
        # fill it in an empty space
        free_blocks_across = calculate_free_rows(self.puzzle_matrix, self.height)
        print("@@@@@@filling a random across free_blocks_across={}".format(free_blocks_across))
        for key, val in sorted(free_blocks_across.items()):
            print("key={} val={}".format(key, val))
            if key >= length(word, self.lang):
                pos = val.pop(random.randint(0, len(val)-1 ))
                if will_fit[ACROSS](pos[0], pos[1], length(word, self.lang)) and not self._check_overlap(word, ACROSS, pos[0], pos[1]):
                    self._fill_word_in_matrix(word, ACROSS, (pos))
                    puzzle['orientation'] = "across"
                    # puzzle['position'] = t + 1
                    puzzle['startx'] = pos[0] + 1
                    puzzle['starty'] = pos[1] + 1
                    return puzzle

x = CrosswordGen()
x.generate_puzzle([{'answer': 'வணக்கம்', 'clue': 'hello in tamil'},
                   {'answer': 'கருமாரி', 'clue': 'my goddess'},
                   {'answer': 'குருநாதன்', 'clue': 'my name'},
                   {'answer': 'ரிக்க்ஷா', 'clue': 'thing used to pull people'}])