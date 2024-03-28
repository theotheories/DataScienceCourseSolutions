# python -m spacy download en_core_web_md
# python -m spacy download en_core_web_sm

# Practical Task 1 - NLP Semantic Similarity Basics

import os
import spacy

nlp_md = spacy.load('en_core_web_md')

word1 = nlp_md("cat")
word2 = nlp_md("monkey")
word3 = nlp_md("banana")

print(f"Similarity between cat and monkey: {word1.similarity(word2)}") # 0.5929930274321619
print(f"Similarity between banana and monkey: {word3.similarity(word2)}") # 0.4041501317354622
print(f"Similarity between banana and cat: {word3.similarity(word1)}") # 0.22358827466989753

print("\nObservation: The model captures logical connections - cats and monkeys are both mammals and share many features. Monkeys eat bananas so they are often words that appear in the same sentence, and they are therefore similar, but other than a dietary relationship they share very little in common. Cats don't even eat bananas so there is a low similarity between those words.")


# Vectors - two for loops to compare between all the words

tokens = nlp_md('cat apple monkey banana ')

print("\nVectors - comparing words pairwise \n")
for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))

# Comparing sentence vectors

sentence_to_compare = "Why is my cat on the car"

sentences = ["where did my dog go",
"Hello, there is my car",
"I've lost my car in my car",
"I'd like my boat back",
"I will name my dog Diana"]

model_sentence = nlp_md(sentence_to_compare)

print(f"\nThe sentence to compare is: {sentence_to_compare}\n")

for sentence in sentences:
    similarity = nlp_md(sentence).similarity(model_sentence)
    print(f"{sentence} - {similarity}")


# Using the simpler model 'en_core_web_sm'

nlp_sm = spacy.load('en_core_web_sm')

word1_sm = nlp_sm("cat")
word2_sm = nlp_sm("monkey")
word3_sm = nlp_sm("banana")

print(f"Smaller model: Similarity between cat and monkey: {word1_sm.similarity(word2_sm)}") # 0.6770566055016188
print(f"Smaller model: Similarity between banana and monkey: {word3_sm.similarity(word2_sm)}") # 0.7276309976205778
print(f"Smaller model: Similarity between banana and cat: {word3_sm.similarity(word1_sm)}") # 0.6806929905901463

# The above give the user warning: UserWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.

# The strangest thing about this smaller model is the very high similarity between bananas and cats... it seems that the small model is much worse at figuring out similar concepts. It may be to do with the lack of word vectors as spacy warns you above. 


# Practical Task 2 - Movie Recommendation System

def recommend_movie(description, movie_data):
    """
    Recommends a movie based on word vector similarity to the provided description.

    Args:
        description (str): The description of the movie the user has watched.
        movie_data (dict): A dictionary where keys are movie titles and values are their descriptions.

    Returns:
        The title of the most similar movie (str).
    """
    descriptions = {}
    for title, desc in movie_data.items():
        descriptions[title] = nlp_md(desc)  # Create doc objects for descriptions

    # Get the doc object for the user-provided description
    user_movie = nlp_md(description)

    max_similarity = 0
    recommended_movie = None
    for title, movie_doc in descriptions.items():
        similarity = user_movie.similarity(movie_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            recommended_movie = title

    return recommended_movie

# Assuming movies.txt is in the same directory as this script
with open(os.path.join(os.path.dirname(__file__), "movies.txt"), "r") as f:
    movie_data = {}  # Create an empty dictionary
    
    for line in f.readlines():
        title, desc = line.strip().split(":", 1) # Split each line into title and description
        movie_data[title] = desc # Set the keys and values per movie

# The description is of Planet Hulk, and movie_data is read from movies.txt
recommended_movie = recommend_movie(
    "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk lands on the planet Sakaar where he is sold into slavery and trained as a gladiator.",
    movie_data,
)

print(f"\nPractical Task 2")
print(f"\nRecommended movie to watch after Planet Hulk: {recommended_movie}")

