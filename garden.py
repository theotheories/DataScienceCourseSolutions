# A garden-path sentence is a grammatically correct sentence that starts in such a way that a reader's most likely interpretation will be incorrect; the reader is lured into a parse that turns out to be a dead end or yields a clearly unintended meaning. "Garden path" refers to the saying "to be led down [or up] the garden path", meaning to be deceived, tricked, or seduced. In A Dictionary of Modern English Usage (1926), Fowler describes such sentences as unwittingly laying a "false scent". https://en.wikipedia.org/wiki/Garden-path_sentence

# Ambiguity inherent in these types of sentences makes for interesting challenges for NLP algorithms to parse the parts of speech, etc. and to ultimately understand the sentences' meaning

# Import spaCy for NLP: tokenisation, lemmatisation, named entity recognition. Ensure English model en_core_web_sm is installed.

# A named entity is a “real-world object” that’s assigned a name – for example, a person, a country, a product or a book title. It is possible that a sentence contains zero named entities.

import spacy 
nlp = spacy.load('en_core_web_sm')

garden_path_sentences = [
    "The old man the boats.",
    "The horse raced past the barn fell.",
    "The man whistling tunes pianos.",
    "The girl told the story cried.",
    "The man who hunts ducks out on weekends.",
    "Fat people eat accumulates.",
    "Apple that the farmer grows is delicious.",
    "May that we all love is sunny.",
    "The Amazon that explorers discovered is vast.",
    "The Jaguar that lives in the zoo is fast.",
    "The man the professor the student has studies Rome 101AD.",
    "Mary gave the child a Band-Aid.",
    "That Jill is never here hurts.",
    "The cotton clothing is made of grows in Mississippi."
]

# Initialise a list variable, which will provide a reference glossary of the named entities found in the sample, at the end of the output. 
explanatory_array = []

# For each sentence in the list, feed it to the spaCy nlp model to make "doc", display tokens, stop words, and lemmas, using spaCy methods. 
# Printed statements explain to the user what each method is doing
# Perform named entity recognition, and append the entity codes found to the explanatory array which will form a glossary at the end of the output.

for sentence in garden_path_sentences:
    doc = nlp(sentence)
    print(f"Original: {sentence}")
    
    print("Tokenised view of the sentence, ignoring spaces and punctuation:")
    print([token.orth_ for token in doc if not token.is_punct | token.is_space])
    
    print("Stop words in original sentence, which will be ignored for the purpose of NLP:")
    print([token.orth_ for token in doc if token.is_stop])
    
    print("Lemmas (root meaning) of each meaningful word in the sentence:")
    print([token.lemma_ for token in doc if not token.is_punct | token.is_space | token.is_stop])
    
    print("Named entity recognition classifies real-world objects referenced in the sentence into categories:")
    print([(entity, entity.label_) for entity in doc.ents])
    
    # Add entity label codes to eventually produce a glossary of what they represent
    for entity in doc.ents:
        explanatory_array.append(entity.label_)
    
    # Space out the results by printing a newline
    print()


# Create the glossary by calling the spacy.explain() method on the entity codes found in the text
# Use set to list conversion with sorted() to make the glossary alphabetical and non-repetitive

print(f"{'GLOSSARY: NAMED ENTITY CODE EXPLANATION':-^80}")
for entity_code in sorted(list(set(explanatory_array))):
    named_entity_explanation = spacy.explain(entity_code)
    print(f"{entity_code:_<20}{named_entity_explanation:_>60}")
    print()

# I purposefully used a couple of confounding terms in the sentences:
# None of the following classifications made sense. Otherwise, spaCy did a good job of extracting named entities correctly. 
# Amazon and Jaguar are classified as ORG - Companies, agencies, institutions etc, but in the sentences they instead mean the rainforest and the animal respectively.
# Rome 101AD is supposed to refer to a university class code, and I included it to try to make the model think it was a place name plus a date. But instead, strangely, it classified Rome 101AD as a FAC - building or highway, etc!
