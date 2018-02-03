import tamil

ACROSS=0
DOWN=1

width, height = 11, 11

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

will_fit = {ACROSS: lambda x, y, l: x>=0 and y>=0 and width > y + l - 1,
            DOWN: lambda x, y, l: x>=0 and y>=0 and height > x + l - 1}


def print_matrix(puzzle_matrix, width):
    for i in range(width):
        print("------------------------------------------------------------------------------------")
        print("{}) ".format(i) + " | ".join(puzzle_matrix[i]))

def find_all_char_pos(s, ch, lang):
    if lang == "english":
        return [i for i, ltr in enumerate(s) if ltr == ch]
    elif lang == "tamil":
        print("letters={}".format(tamil.utf8.get_letters(s)))
        return [i for i, ltr in enumerate(tamil.utf8.get_letters(s)) if ltr == ch]

def find_intersection(word1, word2, lang):
    if lang == "english":
        intersect = set.intersection(set(word1), set(word2))
    elif lang == "tamil":
        letters1 = get_letters(word1, lang)
        letters2 = get_letters(word2, lang)
        intersect = [a for a in letters1 if a in letters2]
    return intersect

def get_letters(str, lang):
    if lang == "english":
        return [a for a in str]
    elif lang == "tamil":
        return tamil.utf8.get_letters(str)
    raise NotImplementedError

def length(str, lang="tamil"):
    if lang == "english":
        return len(str)
    if lang == "tamil":
        return len(tamil.utf8.get_letters(str))
    raise NotImplementedError

def calculate_free_rows(puzzle_matrix, height):
    print("dipoza")
    i,j = 0,0
    free_blocks_across = {}

    for i in range(height):
        temp = puzzle_matrix[i]
        # find continous chunk of free memory in this row
        before = 0
        max_count = 0
        start_j = 0
        temp_count = 0
        for j,c in enumerate(temp):
            if c == ' ':
                temp_count += 1
            else:
                if temp_count > max_count:
                    max_count = temp_count
                    start_j = j - max_count
                    print("max_count={} i={} j={}".format(max_count, i, start_j))
                start_j = j + 1
                temp_count = 0
        if temp_count > max_count:
            # End of row or if entire block is free is gets missed
            max_count = temp_count

        if free_blocks_across.get(max_count):
            free_blocks_across[max_count].append((i,start_j))
        else:
            free_blocks_across[max_count] = [(i, start_j)]

    return free_blocks_across

