from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tokenizer import *
from gemini import *
import requests
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI(title="Video Tokens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Define a model for video tokens
class VideoToken(BaseModel):
    video_id: str
    token: str
    expiration: Optional[str] = None

# video tokens
@app.post("/video_tokens")
def read_video_tokens(video_caption:str):
    video_links = tokenize_sentence(video_caption)

    return {"tokens":  video_links}


# Root route
@app.post("/text_to_ksl")
def text_to_ksl(video_caption: str):
    tokens = tokenize_sentence(video_caption)

    # Check the number of tokens
    if len(tokens) == 1:
        video_url = tokens[0]
    else:
        video_url = getCombinedVideo(tokens)  
    
    return video_url



# This is using Gemini for the conversitions
@app.post("/story_to_ksl")
def text_to_ksl(video_caption:str):
    tokens = convert_sentence_ksl(video_caption)
        # Check the number of tokens
    if len(tokens) == 1:
        video_url = tokens[0]
    else:
        video_url = getCombinedVideo(tokens)  
    
    return video_url
 

def getCombinedVideo(tokens):
    api_url = "https://someshavideoapi.azurewebsites.net/combine_videos"
    tokens = {"urls": tokens}
    x = requests.post(api_url, json = tokens)

    return x.json()
    

