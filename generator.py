import random

# https://simple.wikipedia.org/wiki/Leet
letters_nums = {"b": "8", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}

# Based on dividing the keyboard into two halfs.. -1 for left side and 1 for right side.
letters_map = {'a': -1, 'c': -1, 'd': -1, 'e': -1, 'f': -1, 'q': -1, 'r': -1, 's': -1, 'v': -1, 'w': -1, 'x': -1, 'z': -1, "1": -1, "2": -1, "3": -1, "4": -1, "5": -
               1, "!": -1, 'b': 1, 'g': 0, 'h': 1, 'i': 1, 'j': 1, 'k': 1, 'l': 1, 'm': 1, 'n': 1, 'o': 1, 'p': 1, 't': 0, 'u': 1, 'y': 1, "6": 1, "7": 1, "8": 1, "9": 1, "0": 1}


def read(lang_file):
    # Openning the language's words file and loading it into a list
    with open(lang_file, "r") as file:
        words_lst = list(file)

    # Randomizing the words list
    random.shuffle(words_lst)

    # Words dictionary with length and whether easy typing or not
    words = {}

    # Deciding the word's length and calculating a score for easy tpying
    for word in words_lst:
        word = word.strip("\n")

        if word not in words:
            words[word] = {"len": len(word), "easy": False}
            easy_score = 0
            for letter in word:
                if letter in letters_map:
                    easy_score += letters_map[letter]

            # If the words divide almost equally between the two sides of the keyboard, congrats, it is an easy word!
            if easy_score in [-1, 0, 1]:
                words[word]["easy"] = True

    return words


def generate(words, min_len, max_len, min_word_len, max_word_len, words_per_pwd=4):
    # Filtering words based on length
    filtered_words = {}
    for word in words:
        if min_word_len <= words[word]["len"] <= max_word_len:
            filtered_words[word] = len(word)

    used = {}
    passwords = []

    # Generating passwords to fit the chosen criteria
    total = 0
    while total < 10:
        password = ""
        password_lst = []
        current_word_size = max_len
        for word in filtered_words:
            if ((word not in used and len(password_lst) < words_per_pwd) and ((len(password)+filtered_words[word] < min_len) or (filtered_words[word] < current_word_size))):
                password += word
                password_lst.append(word.lower())
                used[word] = "USED"
                current_word_size = current_word_size - filtered_words[word]

        if (len(password_lst) == 4) and (min_len <= len("".join(password_lst)) <= max_len):
            passwords.append(password_lst)
            password = ""
            current_word_size = max_len
            total += 1

    return passwords


def easy(words):
    # Filtering based on easy typing
    easy = {}
    for word in words:
        if words[word]["easy"] == True and word not in easy:
            easy[word] = {"len": words[word]["len"]}

    return easy


def numbers(passwords):
    # Doing letter/number substitutions
    for i in range(len(passwords)):
        for j in range(len(passwords[i])):
            passwords[i][j] = list(passwords[i][j])
            for k in range(len(passwords[i][j])):
                if passwords[i][j][k] in letters_nums:
                    passwords[i][j][k] = letters_nums[passwords[i][j][k]]
            passwords[i][j] = "".join(passwords[i][j])

    return passwords
