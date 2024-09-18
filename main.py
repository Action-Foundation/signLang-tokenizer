from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tokenizer import *


# Create a FastAPI instance
app = FastAPI(title="Video Tokens API")

# Define a model for video tokens
class VideoToken(BaseModel):
    video_id: str
    token: str
    expiration: Optional[str] = None



# Root route
@app.post("/video_tokens")
def read_video_tokens(video_caption:str):
    tokens = tokenize_sentence(video_caption)

    return {"tokens": tokens}


    

