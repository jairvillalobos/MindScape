"""
from fastapi import APIRouter, HTTPException
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pydantic import BaseModel
import nltk

nltk.download('vader_lexicon')

class Texto(BaseModel):
    texto: str

router = APIRouter()

@router.post("/analizar_sentimiento")
async def analizar_sentimiento(texto: Texto):
    if not texto.texto:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")
    
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(texto.texto)
    polaridad = sentiment['compound']
    
    if polaridad > 0:
        return {"sentiment": "El texto expresa una emoción positiva."}
    elif polaridad < 0:
        return {"sentiment": "El texto expresa una emoción negativa."}
    else:
        return {"sentiment": "El texto parece ser neutral."}
"""
