from pymongo import MongoClient
import json
import random

client = MongoClient('mongodb://localhost:27017/')

width, height = 20, 20

puzzle_matrix = [[" " for i in range(width)] for j in range(height)]

filled_pos = {}

ACROSS=0
DOWN=1

def get_word(type='cities', length=None, level=0):
    db = client.tamil_puzzle
    collection = db['tamil_puzzle']
    words = collection.find({'length':length, 'type': type, 'level': level})
    try:
        return words.next()
    except StopIteration as e:
        return None

will_fit = {ACROSS: lambda x, y, l: x>=0 and y>=0 and width > y + l - 1,
            DOWN: lambda x, y, l: x>=0 and y>=0 and height > x + l - 1}

def next_pos_across(x, y, l):
    while (y) < width:
        yield (x, y)
        y += 1


def next_pos_down(x, y, l):
    while (x) < height:
        yield (x, y)
        x += 1



calculate_next_pos = {ACROSS: next_pos_across,
            DOWN: next_pos_down}


def print_matrix():
    for i in range(width):
        print("------------------------------------------------------------------------------------")
        print("{}) ".format(i) + " | ".join(puzzle_matrix[i]))


def fill_word_in_matrix(word, orientation=ACROSS, start_elem=(0,0)):
    i, j = start_elem
    filled_pos[word] = {'position': (i, j), 'orientation': orientation}
    if orientation == ACROSS:
        for l in word:
            puzzle_matrix[i][j] = l
            j += 1
    else:
        for l in word:
            puzzle_matrix[i][j] = l
            i +=1

def check_overlap(word, orientation, x, y):
    i, j = x, y
    next_pos = calculate_next_pos[orientation](i, j, len(word))
    for a in word:
        try:
            (i, j) = next(next_pos)
            print("i={} j={}".format(i,j))
        except StopIteration as e:
            print("stop iteration received after will fit word={} i, j={}".format(word, (i, j)))

        if puzzle_matrix[i][j] != " ":
            if puzzle_matrix[i][j] == a:
                continue
            else:
                print("Overlap of letter {} with {} at {}".format(a,puzzle_matrix[i][j], (i,j)))
                return True
    return False

def find_all_char_pos(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


# An efficient way to calculate blocks of available memory in puzzle_matrix
def calculate_free_memory():
    # 1. Get all the starting positions of words filled in so far.
    # 2. start with (0,0) and increment i,j to the value where the first word is written.
    # 3. this will become the first rectangle of unwritten memory.
    # 4. then increment i to the one found in the first list of filled words
    # 5. 

def find_best_fit(word):
    """
    calculate the best fit for a given word.
    Prefer words with intersections over non intersecting spaces
    :return: position (x, y) in the puzzle_matrix
    """

    # if first word
    print(len(filled_pos))
    if len(filled_pos) == 0:
        x = random.randint(0,4)
        y = random.randint(0,4)
        print("first_word: {} x:{} y:{}".format(word, x, y))
        print("will_fit: {}".format(will_fit[ACROSS](x, y, len(word))))
        if will_fit[ACROSS](x, y, len(word)):
            fill_word_in_matrix(word, ACROSS, (x,y))
            return

    # first find the location where it overlaps.. then move to the other ones to keep it interesting
    for key in filled_pos:
        #the orientation for this word should be perpendicular to the one we are trying to match
        pos = int(not filled_pos[key]['orientation'])
        # find the intersecting letters between the two words
        intersect = set.intersection(set(key), set(word))
        print("trying to intersect filled_word={} with word={}".format(key, word))
        if len(intersect) == 0:
            # no letters matched.. lets find the next
            continue
        else:
            a = [-10, -10]
            print("intersecting letters={}".format(intersect))
            for letter in intersect:
                indexes1 = find_all_char_pos(key, letter)
                for index in indexes1:
                    # index = filled_pos[key]['word'].find(letter)
                    print("location of the letter={} in word={} is {}".format(letter, key, index))
                    filled_word_pos = filled_pos[key]['position']
                    a[pos] = filled_word_pos[pos] + index
                    indexes2 = find_all_char_pos(word, letter)
                    for index2 in indexes2:
                        # index2 = word.find(letter)
                        print("location of the letter={} in word={} is {}".format(letter, word, index2))
                        a[filled_pos[key]['orientation']] = filled_word_pos[int(not pos)]  - index2
                        print("looking for match in location={}".format(a))
                        print("will_fit={}".format(will_fit[pos](a[0], a[1], len(word))))
                        if will_fit[pos](a[0], a[1], len(word)):
                            if not check_overlap(word, pos, a[0], a[1]):
                                fill_word_in_matrix(word, pos, (a[0], a[1]))
                                return


def generate_puzzle(type, level):
    # first_word = get_word(type='cities', length=8, level=level)
    print("****************************************")
    second_word = "KANCHIPURAN"
    find_best_fit(second_word)
    print_matrix()

    print("****************************************")
    second_word = "THIRUVANNAMALAI"
    find_best_fit(second_word)
    print_matrix()

    print("****************************************")
    first_word = "THANJAVUR"
    find_best_fit(first_word)
    print_matrix()

    # for the biggest word pick the corners across/down
    print("****************************************")
    third_word = "MADURAI"
    find_best_fit(third_word)
    print_matrix()

    print("****************************************")
    third_word = "KANYAKUMARI"
    find_best_fit(third_word)
    print_matrix()

    print("****************************************")
    third_word = "KUMBAKONAM"
    find_best_fit(third_word)
    print_matrix()

    print("****************************************")
    third_word = "KAILASH"
    find_best_fit(third_word)
    print_matrix()

    print("****************************************")
    third_word = "AGNI"
    find_best_fit(third_word)
    print_matrix()

    print("****************************************")
    third_word = "PARVATHY"
    find_best_fit(third_word)
    print_matrix()

generate_puzzle("type", 0)