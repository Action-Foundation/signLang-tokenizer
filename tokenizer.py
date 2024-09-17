from nltk.tokenize import MWETokenizer
import re

import json

# Initialize the multi-word expression tokenizer
tokenizer = MWETokenizer(separator='_')

videos_dict = {'.': 'stop'}
# Function to split phrases into tuples, convert to lowercase, and add them to the tokenizer
def add_phrases_as_tuples(data):
    phrases = list()
    videos = {}
    for video_data in data:
        # Split each phrase by spaces, convert to lowercase, and create a tuple
        phrase_tuple = tuple(video_data['title'].lower().split())
        phrase = '_'.join(phrase_tuple)
    
        phrases.append(phrase_tuple)
        videos[phrase]= video_data['video']
    return [phrases, videos]

def init_tokenizer(): 
    # Open and load the JSON file
    with open('videos.json', 'r') as file:
        data = json.load(file)

    # Add phrases as tuples to the tokenizer
    phrases, videos = add_phrases_as_tuples(data)
    #print(f"Phases, {phrases}")

    for  phrase in phrases:
        tokenizer.add_mwe(phrase)
    return [phrases, videos]

phrases, videos = init_tokenizer()
videos_dict = videos

# Function to tokenize a sentence using the added phrases
def tokenize_sentence(sentence):
    video_link=[]
    # Preprocess the sentence: remove punctuation and convert to lowercase
    clean_sentence = re.sub(r'[^\w\s]', '', sentence).lower()
    
    # Tokenize the sentence
    tokens = tokenizer.tokenize(clean_sentence.split())
    
    for token in tokens:
        print(f"Tokeensssssssssssssssssssssssssss {token}")
        print(f"Videos {videos_dict}")
        token

        video_url = videos_dict.get(token, "fakeurl.mp4")

        video_link.append(video_url)

    # Print out the tokens
    return video_link
