# https://exercism.org/tracks/python/exercises/little-sisters-vocab


def add_prefix_un(word: str) -> str:
    """
    This function takes a word and adds the prefix "un" to it.

    Parameters:
    - word (str): The word to which the prefix "un" is to be added.

    Returns:
    - str: The new word with the prefix "un".
    """
    return "un" + word


def make_word_groups(vocab_words: list[str]) -> str:
    """
    This function takes a list of vocabulary words and applies the prefix (first element of the list) to each word.

    Parameters:
    - vocab_words (list[str]): A list where the first element is the prefix and the rest are words to which the prefix is to be applied.

    Returns:
    - str: A string with the prefix applied to each word, separated by " :: ".
    """
    prefix = vocab_words[0]
    # Prefix is first member of the list
    # [prefix + word for word in vocab_words[1:]] is a list comprehension that will add prefix to every word except the prefix itself (which is the first member of the list, so skip it with a slice from index 1 to the end of the list)
    # prefix needs to be in the final list, so prepend the comprehension with [prefix]
    # Join all the members of the new list with " :: "
    return " :: ".join([prefix] + [prefix + word for word in vocab_words[1:]])


def remove_suffix_ness(word: str) -> str:
    """
    This function removes the suffix "ness" from a word. If the word ends with "iness", it replaces "i" with "y".

    Parameters:
    - word (str): The word from which the suffix "ness" is to be removed.

    Returns:
    - str: The word without the suffix "ness".
    """
    if word.endswith("iness"):
        return word[:-5] + "y"
    else:
        return word[:-4]


def adjective_to_verb(sentence: str, index: int) -> str:
    """
    This function extracts an adjective from a sentence and turns it into a verb by adding the suffix "en".

    Parameters:
    - sentence (str): The sentence from which the adjective is to be extracted.
    - index (int): The index of the adjective in the sentence when the sentence is split into words.

    Returns:
    - str: The verb form of the extracted adjective.
    """
    words = sentence.split()
    return words[index].rstrip(".") + "en"


# Debugging, using f-string self-documenting expressions
print(f'{add_prefix_un("happy")=}')
print(f'{add_prefix_un("manageable")=}')
print(f'{make_word_groups(["en", "close", "joy", "lighten"])=}')
print(f'{make_word_groups(["pre", "serve", "dispose", "position"])=}')
print(f'{make_word_groups(["auto", "didactic", "graph", "mate"])=}')
print(f'{make_word_groups(["inter", "twine", "connected", "dependent"])=}')
print(f'{remove_suffix_ness("heaviness")=}')
print(f'{remove_suffix_ness("sadness")=}')
print(f'{adjective_to_verb("I need to make that bright.", -1)=}')
print(f'{adjective_to_verb("It got dark as the sun set.", 2)=}')


# Tests
assert add_prefix_un("happy") == "unhappy"
assert add_prefix_un("manageable") == "unmanageable"


assert (
    make_word_groups(["en", "close", "joy", "lighten"])
    == "en :: enclose :: enjoy :: enlighten"
)
assert (
    make_word_groups(["pre", "serve", "dispose", "position"])
    == "pre :: preserve :: predispose :: preposition"
)
assert (
    make_word_groups(["auto", "didactic", "graph", "mate"])
    == "auto :: autodidactic :: autograph :: automate"
)
assert (
    make_word_groups(["inter", "twine", "connected", "dependent"])
    == "inter :: intertwine :: interconnected :: interdependent"
)


assert remove_suffix_ness("heaviness") == "heavy"
assert remove_suffix_ness("sadness") == "sad"


assert adjective_to_verb("I need to make that bright.", -1) == "brighten"
assert adjective_to_verb("It got dark as the sun set.", 2) == "darken"
