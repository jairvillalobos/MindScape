from transformers import pipeline
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class Texto(BaseModel):
    texto: str

router = APIRouter()

# Cargar el pipeline de análisis de sentimientos
nlp = pipeline('sentiment-analysis')

@router.post("/analizar_sentimiento")
async def analizar_sentimiento_endpoint(texto: Texto):
    if not texto.texto:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")
    
    # Usar BERT para analizar el sentimiento
    result = nlp(texto.texto)[0]
    sentiment = result['label']
    score = result['score']
    
    # Definir un umbral para la neutralidad
    umbral_neutral = 0.05
    
    if score < umbral_neutral:
        return {"sentiment": "El texto parece ser neutral.", "score": score}
    elif sentiment == 'POSITIVE':
        return {"sentiment": "El texto expresa una emoción positiva.", "score": score}
    else:
        return {"sentiment": "El texto expresa una emoción negativa.", "score": score}
