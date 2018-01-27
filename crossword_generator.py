from pymongo import MongoClient
import json

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

will_fit = {ACROSS: lambda x, y, l: width >= y + l - 1,
            DOWN: lambda x, y, l: height >=x + 1 - 1}

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
        print "-------------------------------------"
        print " | ".join(puzzle_matrix[i])


def fill_word_in_matrix(word, orientation=ACROSS, start_elem=(0,0)):
    i, j = start_elem
    filled_pos[(i, j)] = {'word': word, 'orientation': orientation}
    if orientation:
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
    



def generate_puzzle(type, level):
    first_word = get_word(type='cities', length=8, level=level)
    fill_word_in_matrix(first_word)
    # for the biggest word pick the corners across/down
