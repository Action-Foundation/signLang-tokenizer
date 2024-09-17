from nltk.tokenize import MWETokenizer
import re

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
    clean_sentence = re.sub(r'[^\w\s]', '', sentence).lower()  # Remove punctuation and lowercase
    
    # Tokenize the sentence
    tokens = tokenizer.tokenize(clean_sentence.split())
    
    # Print out the tokens
    print("Tokens:", tokens)

# Example usage
phrases = ['the west wing', 'new york city', 'artificial intelligence']
sentence = 'Something about the west wing in New York City related to artificial intelligence.'

# Add phrases as tuples to the tokenizer
add_phrases_as_tuples(phrases)

# Tokenize the sentence
tokenize_sentence(sentence)
