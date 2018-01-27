from pymongo import MongoClient
import json
import random

client = MongoClient('mongodb://localhost:27017/')

width, height = 11, 11

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

will_fit = {ACROSS: lambda x, y, l: x>=0 and y>=0 and width >= y + l - 1,
            DOWN: lambda x, y, l: x>=0 and y>=0 and height >=x + 1 - 1}

def next_pos_across(x, y, l):
    if (y + 1) < l and (y+1) < width:
        yield (x, y+1)
    else:
        raise StopIteration

def next_pos_down(x, y, l):
    if (x + 1) < l and (x + 1) < height:
        yield (x+1, y)
    else:
        raise StopIteration


next_pos = {ACROSS: next_pos_across,
            DOWN: next_pos_down}


def print_matrix():
    for i in range(width):
        print("-------------------------------------")
        print(" | ".join(puzzle_matrix[i]))


def fill_word_in_matrix(word, orientation=ACROSS, start_elem=(0,0)):
    i, j = start_elem
    filled_pos[(i, j)] = {'word': word, 'orientation': orientation}
    if orientation == ACROSS:
        for l in word:
            puzzle_matrix[i][j] = l
            j += 1
    else:
        for l in word:
            puzzle_matrix[i][j] = l
            i +=1


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
        intersect = set.intersection(set(filled_pos[key]['word']), set(word))
        if len(intersect) == 0:
            # no letters matched.. lets find the next
            continue
        else:
            a = [-10, -10]
            print("intersecting letters={}".format(intersect))
            for letter in intersect:
                index = filled_pos[key]['word'].find(letter)
                print("location of the letter={} in word={} is {}".format(letter, filled_pos[key]['word'], index))
                a[pos] = key[pos] + index
                index2 = word.find(letter)
                print("location of the letter={} in word={} is {}".format(letter, word, index2))
                a[filled_pos[key]['orientation']] = key[int(not pos)] - index2

                print("looking for match in location={}".format(a))
                print("will_fit={}".format(will_fit[pos](a[0], a[1], len(word))))
                if will_fit[pos](a[0], a[1], len(word)):
                    fill_word_in_matrix(word, pos, (a[0], a[1]))
                    return


def generate_puzzle(type, level):
    # first_word = get_word(type='cities', length=8, level=level)
    first_word = "MURUGA"
    find_best_fit(first_word)
    print_matrix()

    second_word = "MITHILA"
    find_best_fit(second_word)
    print_matrix()
    # for the biggest word pick the corners across/down

    third_word = "LATHA"
    find_best_fit(third_word)
    print_matrix()

generate_puzzle("type", 0)