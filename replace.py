# Save the sentence: “The!quick!brown!fox!jumps!over!the!lazy!dog.” as a single string.

sentence = "The!quick!brown!fox!jumps!over!the!lazy!dog."

#  Reprint this sentence as “The quick brown fox jumps over the lazy dog.” using the replace() function to replace every “!” exclamation mark with a blank space.

sentence = sentence.replace("!", " ")
print(sentence)

# Reprint that sentence as: “THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.” using the upper() function

sentence = sentence.upper()
print(sentence)

# Print the sentence in reverse. (Hint: review what you learned about slicing!

sentence = sentence[::-1]
print(sentence)
