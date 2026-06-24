import time
import torch
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# 1. Initialisation de l'API
app = FastAPI(
    title="AI Intern Inference Service",
    description="API de prédiction NLP pour le stage de 2e année ESIEE"
)

# 2. Configuration CORS requis par les livrables
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à n'importe quel site web de requêter ton IA
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Loading model
print("Loading IMDb model...")
classifier = pipeline(
    "text-classification",
    model="./my_imdb_model",
    tokenizer="./my_imdb_model"
)
print("IMDb model ready !")

# 4. Déclaration du contrat de données (Pydantic Schema)
class PredictionRequest(BaseModel):
    text: str

# 5. Middleware de Logging pour mesurer la latence demandée
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Ajoute le temps de calcul dans les headers de la réponse
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"Route {request.url.path} exécutée en {process_time:.4f} secondes")
    return response

# 6. Route /healthz requise
@app.get("/healthz")
def health_check():
    return {"status": "healthy", "model_loaded": True}

# 7. Route /predict requise avec le schéma Pydantic
@app.post("/predict")
def predict_sentiment(payload: PredictionRequest):
    # On extrait le texte validé automatiquement par Pydantic
    text_to_analyze = payload.text

    # Inférence avec ton modèle
    model_output = classifier(text_to_analyze)[0]

    # Ton modèle renvoie "LABEL_0" ou "LABEL_1", on le convertit en texte lisible
    raw_label = model_output["label"]
    friendly_label = "POSITIVE" if raw_label == "LABEL_1" else "NEGATIVE"

    return {
        "text": text_to_analyze,
        "label": friendly_label,
        "score": round(model_output["score"], 4)
    }