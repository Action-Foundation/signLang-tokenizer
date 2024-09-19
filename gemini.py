import google.generativeai as genai
import os
import nltk

# Configure Google Generative AI API
genai.configure(api_key=os.environ['API_KEY'])

# Example complex sentence
complex_sentence = "Mr. Kilonzo went to church at Nairobi every Sunday"

# Create the meta prompt to guide the model's behavior
meta_prompt = """
Please simplify the following sentence for Kenya Sign Language interpretation. Follow these rules:
1. Capitalize names that appear in the sentence.
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
print(complex_sentence)
print(response.text)

# Extract the simplified sentence starting with "present/"
simplified_sentence = None

if "present/" in response.text:
    start_index = response.text.index("present/")
    simplified_sentence = response.text[start_index:].strip()

if simplified_sentence:
    # Tokenization using NLTK
    words = nltk.word_tokenize(simplified_sentence)
    tokens = []  # Initialize the tokens list

    # Check if the simplified sentence is a question
    is_question = "?" in simplified_sentence  # Adjust this condition based on how you determine questions

    # Add 'Present' as a token
    tokens.append('Present')

    # Add 'type' if it's a question
    if is_question:
        tokens.append('type')

    for word in words:
        if word.isupper():  # If the word is fully capitalized
            tokens.extend(list(word))  # Add each letter as a separate token
        else:
            tokens.append(word)  # Add regular words to the list

    print(tokens)  # Print the list of tokens
else:
    print("No simplified sentence found.")




