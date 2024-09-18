import requests
import re
from tokenizer import *

# Define the API endpoint
url = "https://theactionfoundationkenya.org/somesha-kids/mobileappfiles/ios/somesha-stories.php"

# Function to clean up the text
def clean_text(text):
    # Remove \r, \n, and escaped quotes
    return re.sub(r'[\r\n"]', '', text)

try:
    # Send a GET request to the API endpoint
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response content (assuming it's JSON)
        data = response.json()
        
        # Initialize a list to store the cleaned data
        cleaned_data = []
        
        # Loop through the response data
        for item in data:
            # Extract id, description, and long_story
            story_id = item.get('id')
            title = clean_text(item.get('title', ''))
            long_story = clean_text(item.get('long_story', ''))
            translated_text = f"{title}{long_story}"

            tokens = tokenize_sentence(translated_text)
            
            # Append the cleaned data to the list
            cleaned_data.append({
                'id': story_id,
                'title': title,
                'long_story': long_story,
                'translated_text': tokens
            })
        
        # Print the cleaned data
        print("Cleaned Data:")
        for story in cleaned_data:
            print(story)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
