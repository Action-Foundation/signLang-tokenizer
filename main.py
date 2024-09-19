from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tokenizer import *
import requests

# Create a FastAPI instance
app = FastAPI(title="Video Tokens API")

# Define a model for video tokens
class VideoToken(BaseModel):
    video_id: str
    token: str
    expiration: Optional[str] = None

# video tokens
@app.post("/video_tokens")
def read_video_tokens(video_caption:str):
    tokens = tokenize_sentence(video_caption)

    return {"tokens": tokens}


# Root route
@app.post("/text_to_ksl")
def text_to_ksl(video_caption:str):
    tokens = tokenize_sentence(video_caption)
    video_url = getCombinedVideo(tokens)
    return video_url

def getCombinedVideo(tokens):
    api_url = "https://someshavideoapi.azurewebsites.net/combine_videos"
    tokens = {"urls": tokens}
    x = requests.post(api_url, json = tokens)

    return x.json()
    

