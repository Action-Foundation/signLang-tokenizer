import google.generativeai as genai
import os
import nltk
import json
from tokenizer import *


# Configure Google Generative AI API
genai.configure(api_key=os.environ['API_KEY'])


# Example complex sentence
complex_se = """
Once a day the big blue bus stops in Bubu's village to pick up people to go to town. Bubu has never seen such a big bus. He counts 9 passenger windows and a window for the driver. "There must be 9 rows of passenger seats with at least 6 seats in a row," Bubu thinks.
If Bubu is right, how many passengers can the big blue bus carry?

Tomorrow, Bubu's mother will take him to town to buy a new school uniform. She sells eggs for R15 a dozen. Most weeks she makes R450. How many dozen eggs does she need to sell to make R450? For the last 4 weeks, she has been able to save half her money to pay for Bubu's new uniform.
Can you work out how much money she saved in 4 weeks?

It's almost three months since Bubu's last bus trip. He cannot wait!
Tomorrow is the big day. By seven o'clock, he is in bed, but he can't fall asleep. His mind is racing. He can't stop thinking about the trip to town. It's already half past nine, but Bubu is still wide awake.

Every morning, Bubu's mother wakes him at seven o'clock. But today he is already wide awake by six o'clock, even though he only went to sleep at eleven o'clock last night.
By seven o'clock he is washed and dressed and ready to go. How long did Bubu sleep last night?

At quarter to eight Bubu and his mother get to the bus stop. The big blue bus is supposed to arrive by eight o'clock.
Bubu's mother checks her watch. The big blue bus is already fifteen minutes late. "But the bus is always on time. I wonder what the problem is?" she says.

Soon more people join them at the bus stop. They also look at their watches and ask why the bus is late. "It is already nine o'clock. I am going to be late for work!" says the bald man in the blue suit.
Bubu and his mother have been waiting the longest. To Bubu, it feels like hours and hours. But it isn't really. How long have they been waiting?

Bubu is worried. "Will I ever get my uniform?" he asks his mother.
Bubu works out that the trip to town and back will take about 4 hours. An hour to get there, 2 hours to shop and 1 hour to get back. "I have a soccer game with my friends at two o'clock. I hope the bus comes soon or we won't make it home in time."

"""
def convert_sentence_ksl(complex_sentence):
    # Create the meta prompt to guide the model's behavior
    meta_prompt = """
    Please simplify the following sentence for Kenya Sign Language interpretation. Follow these rules:
    1. Capitalize persons or country  names that appear in the sentence names are like Jonh.
    2. Remove these stop words: ['is', 'too', 'been', 'does', 'shouldnt', 'dont', 'shan't', 'while', 'haven't', 'so', 'until', 'it's', 'during', 'nor', 'of', 'had', 'whom', 'any', 'they'].
    3. Replace certain words with their specific values:
    - 'into' with 'in'
    - 'haven't', 'won't', 'wouldn't', 'didn't' with 'bado', 'no', 'zero', 'nothing'
    - 'until' with 'time what'
    - 'when' with 'time what'
    - 'through' with 'finish'
    - 'most' with 'a lot'
    - 'during' with 'time which'
    - 'you'd' with 'you'
    - 'further' with 'far'
    - 'are' with 'time'

    4. If a sentence is continuous (e.g., 'I am going'), change it to present form (e.g., 'I go').
    5. Identify if the sentence is a question, listing, or statement.
    6. If the sentence is in the past, prepend 'past /'. If it’s in the present or future, prepend 'present/'. Remove tense markers in the final output and only retain the present tense form.
    7. Exclude occupations or titles like 'Miss,' 'Mrs.,' 'President' from the final output.
    8. If the sentence contains a name of place, city, country, village, i.e., the name of places will always start with a capital letter, so keep it capitalized.
    9. Ensure the sentence follows a subject-object-verb order.

    Sentence: {}
    """.format(complex_sentence)

    # Generate content using the model
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(meta_prompt)

    # Output the result
    # print(response.text)
    video_link=[]

    # Extract the simplified sentence starting with "present/" or "past /"
    simplified_sentence = None
    tense_prefix = None


    simplified_sentence = ""
    tense_prefix = ""
    video_link = []

    response_text = response.text

    if "present/" in response_text:
        start_index = response_text.index("present/")
        simplified_sentence = response_text[start_index:].strip()
        tense_prefix = "present/"
    elif "past /" in response_text:
        start_index = response_text.index("past /")
        simplified_sentence = response_text[start_index:].strip()
        tense_prefix = "past /"

    if simplified_sentence:
        # Tokenization using NLTK
        words = nltk.word_tokenize(simplified_sentence)
        tokens = []

        # Add tense prefix as a token
        if tense_prefix:
            tokens.append(tense_prefix)

        # Check if the simplified sentence is a question
        is_question = "?" in simplified_sentence

        # Add 'type' if it's a question
        if is_question:
            tokens.append('type')

        for word in words:
            if word.isupper():
                tokens.extend(list(word))
            else:
                tokens.append(word)

        # Prepare output in JSON format
        output_json = {
            "simplified_sentence": simplified_sentence,
            "tokens": tokens
        }

        # Convert to JSON string
        output_json_str = json.dumps(output_json)

        # Generate video links
        for char in output_json["tokens"]:
            if char in videos_dict:
                char_video_url = videos_dict[char]
                video_link.append(char_video_url)

        return video_link

    return None, None





