from nltk.tokenize import MWETokenizer
import re

import json

# Open and load the JSON file
with open('videos.json', 'r') as file:
    data = json.load(file)

# Access data
titles = [item['title'] for item in data]

# Print the list of titles
print(titles) 

# Initialize the multi-word expression tokenizer
tokenizer = MWETokenizer(separator='_')

# Function to split phrases into tuples, convert to lowercase, and add them to the tokenizer
def add_phrases_as_tuples(phrases):
    for phrase in phrases:
        # Split each phrase by spaces, convert to lowercase, and create a tuple
        phrase_tuple = tuple(phrase.lower().split())
        tokenizer.add_mwe(phrase_tuple)  # Add each tuple to the tokenizer

# Function to tokenize a sentence using the added phrases
def tokenize_sentence(sentence):
    # Preprocess the sentence: remove punctuation and convert to lowercase
    clean_sentence = re.sub(r'[^\w\s]', '', sentence).lower()  
    
    # Tokenize the sentence
    tokens = tokenizer.tokenize(clean_sentence.split())
    
    # Print out the tokens
    print("Tokens:", tokens)

# Example usage
phrases = titles
sentence = "Abraham, feeling abashed, decided to abandon a lot of his old methods and focus on new techniques. "
   

print(sentence)


# Add phrases as tuples to the tokenizer
add_phrases_as_tuples(phrases)

# Tokenize the sentence
tokenize_sentence(sentence)
