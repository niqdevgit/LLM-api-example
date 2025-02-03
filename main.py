from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import requests
import os

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can limit it to specific domains later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load fine-tuned model from Hugging Face
model_name = "niklassuvitie/ft-imdb-distilbert"  # Update with your HF model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Groq Cloud API details
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

# Request body schema
class SentimentRequest(BaseModel):
    text: str
    model: str  # "custom" (DistilBERT) or "llama" (Groq Llama 3)

# Function to predict sentiment using the fine-tuned model
def predict_custom_model(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    confidence, predicted_class = torch.max(scores, dim=-1)
    sentiment = "positive" if predicted_class.item() == 1 else "negative"
    
    return {"sentiment": sentiment, "confidence": confidence.item()}

# Function to predict sentiment using Groq's Llama 3 API
def predict_llama(text):
    prompt = f"Classify the sentiment of this text as positive or negative: '{text}'"
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3-8b",  # Use the correct Llama 3 model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Groq API error")
    
    reply = response.json()["choices"][0]["message"]["content"].strip().lower()
    sentiment = "positive" if "positive" in reply else "negative"
    
    return {"sentiment": sentiment, "confidence": None}  # No confidence score from Groq

# Define the API endpoint
@app.post("/analyze/")
def analyze_sentiment(request: SentimentRequest):
    if request.model == "custom":
        return predict_custom_model(request.text)
    elif request.model == "llama":
        return predict_llama(request.text)
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")
