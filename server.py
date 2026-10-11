
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

positive_words = {
    "love", "great", "good", "excellent", "amazing",
    "happy", "wonderful", "best", "awesome", "fantastic",
    "like", "enjoy", "perfect", "beautiful", "helpful",
    "delicious", "success", "pleased", "recommend"
}

negative_words = {
    "terrible", "bad", "hate", "awful", "sad",
    "horrible", "worst", "angry", "poor", "disappointed",
    "annoying", "broken", "useless", "fail", "failure",
    "dislike", "disappointing", "ugly", "problem"
}

def analyze_sentiment(sentence: str) -> str:
    words = re.findall(r"\b[\w']+\b", sentence.lower())

    positive = sum(word in positive_words for word in words)
    negative = sum(word in negative_words for word in words)

    if positive > negative:
        return "happy"
    elif negative > positive:
        return "sad"
    return "neutral"

@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": analyze_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
