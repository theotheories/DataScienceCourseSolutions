# Collect user's string to be turned into an AlTeRnAtE ChArAcTeR- and ALTERNATE word-cased output
sentence = input("Give me a word or sentence:\n")

# Save a words list before manipulating the string. Use str() to get a copy without linking the variables to change simultaneously
words_list = str(sentence).split(" ")

# Need an iterable list of characters which also supports item assignment (unlike inbuilt string functionality)
char_list = list(sentence)

# Manipulate the string to alternate the case character by character:
for i in range(len(char_list)):
    if i % 2 == 0:
        char_list[i] = char_list[i].upper()
    else:
        char_list[i] = char_list[i].lower()

# Alternate the case word by word:
for i in range(len(words_list)):
    if i % 2 == 0:
        words_list[i] = words_list[i].lower()
    else:
        words_list[i] = words_list[i].upper()

# Join back into output strings
alternate_characters = "".join(char_list)
alternate_words = " ".join(words_list)

# Output
print(alternate_characters)
print(alternate_words)
