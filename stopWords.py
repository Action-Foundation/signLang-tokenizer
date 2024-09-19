import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Function to remove stopwords and categorize words
def process_sentence(sentence):
    # Tokenize the sentence
    tokens = word_tokenize(sentence)
    
    # Load the list of stopwords from nltk
    stop_words = set(stopwords.words('english'))
    # print(stop_words)
    
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Tag each word with its part of speech (POS)
    pos_tags = nltk.pos_tag(filtered_tokens)
    
    # Categorize tokens into nouns and other parts
    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]  # Noun POS starts with 'NN'
    others = [(word, pos) for word, pos in pos_tags if not pos.startswith('NN')]  # Everything else

    return {
        "filtered_tokens": filtered_tokens,
        "nouns": nouns,
        "others": others
    }

# Example sentence
sentence = "The quick brown fox jumps over the lazy dog."

# Process the sentence
result = process_sentence(sentence)

# Output the results
print("Filtered Tokens (No Stopwords):", result["filtered_tokens"])
print("Nouns:", result["nouns"])
print("Other Parts of Speech:", result["others"])
