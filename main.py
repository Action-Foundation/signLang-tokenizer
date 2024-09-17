from fastapi import FastAPI
from pydantic import BaseModel
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import uvicorn

# Download required NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')

class Item(BaseModel):
    sentence: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sign Language API"}

@app.post("/a2sl")
def a2sl(item: Item):
    text = item.sentence.lower()

    # Tokenize the input into words
    words = word_tokenize(text)

    # Perform part of speech tagging on the words
    tagged = nltk.pos_tag(words)

    tense = {
        "future": 0,
        "present": 0,
        "past": 0,
        "present_continuous": 0  
    }

    # Count the number of verbs in each tense
    for _, pos in tagged:
        if pos == "MD":
            tense["future"] += 1
        elif pos in ["VBP", "VBZ"]:
            tense["present"] += 1
        elif pos in ["VBD", "VBN"]:
            tense["past"] += 1
        elif pos == "VBG":
            tense["present_continuous"] += 1  # Fixed typo here

    stop_words = set([
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
        'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
        'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
    ])

    lemmatizer = WordNetLemmatizer()
    filtered_text = []

    for word, pos in tagged:
        if word.lower() not in stop_words:
            if pos.startswith('VB'):
                lemma = lemmatizer.lemmatize(word, pos='v')
            elif pos.startswith('JJ') or pos.startswith('RB'):
                lemma = lemmatizer.lemmatize(word, pos='a')
            else:
                lemma = lemmatizer.lemmatize(word)
            filtered_text.append(lemma)

    # Determine the probable tense based on the counts
    probable_tense = max(tense, key=tense.get)

    # Check the probable tense and make adjustments
    if probable_tense == "past" and tense["past"] >= 1:
        filtered_text = ["Before"] + filtered_text
    elif probable_tense == "future" and tense["future"] >= 1:
        if "will" not in filtered_text:
            filtered_text = ["Will"] + filtered_text
    elif probable_tense == "present" and tense["present_continuous"] >= 1:  
        filtered_text = ["Now"] + filtered_text

    # List of animations videos for sign language
    videos = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a",
        "after", "again", "against", "age", "all", "alone", "also", "and", "ask", "at",
        "b", "be", "beautiful", "before", "best", "better", "busy", "but", "bye",
        "c", "can", "cannot", "change", "college", "come", "computer",
        "d", "day", "distance", "do not", "does not",
        "e", "eat", "engineer",
        "f", "fight", "finish", "from", "g", "glitter", "go",
        "god", "gold", "good", "great", "h", "hand", "hands", "happy", "hello", "help",
        "her", "here", "his", "home", "homepage", "how", "i", "invent", "it", "j", "k", "keep",
        "l", "language", "laugh", "learn", "m", "me", "more", "my", "n", "name", "next", "not", "now",
        "o", "of", "on", "our", "out", "p", "pretty", "q", "right", "s", "sad", "safe", "see", "self",
        "sign", "so", "sound", "stay", "study", "t", "talk", "television", "thank you", "thank",
        "that", "they", "this", "those", "time", "to", "type", "u", "us", "v", "w", "walk", "wash",
        "way", "we", "welcome", "what", "when", "where", "which", "who", "whole", "whose", "why",
        "will", "with", "without", "words", "work", "world", "wrong", "x", "y", "your", "yourself", "z"
    ]

    result = []
    for word in filtered_text:
        if word.lower() in videos:
            result.append(word.title())
        else:
            result.extend(char.upper() for char in word)

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#openCV
# ffprob
# ffmpeg