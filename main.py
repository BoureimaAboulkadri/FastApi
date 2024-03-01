from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from pymongo import MongoClient
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO


# Configuration FastAPI
app = FastAPI()

origins = [
    "http://localhost:3000",  # Port standard pour le développement React
    "http://127.0.0.1:3000",  # Autre forme d'adresse locale
    "http://0.0.0.0:8000/",  # Adresse locale pour le serveur FastAPI
    "http://127.0.0.1:8000/calculer/", # adresse locale pour le postman
    "http://localhost:8000/export/", # adresse export
    # Ajoutez d'autres origines au besoin
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes
    allow_headers=["*"],  # Autoriser tous les headers
)
# Configuration MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NPI']
collection = db['expressions']

class Expression(BaseModel):
    expression: str

def calculer_npi(expression):
    pile = []
    for token in expression.split():
        if token in "+-*/":
            b = pile.pop()
            a = pile.pop()
            if token == '+': pile.append(a + b)
            elif token == '-': pile.append(a - b)
            elif token == '*': pile.append(a * b)
            elif token == '/': pile.append(a / b)
        else:
            pile.append(float(token))
    return pile.pop()

@app.post("/calculer/")
def calculer(expression: Expression):
    try:
        resultat = calculer_npi(expression.expression)
        # Sauvegarder dans MongoDB
        insertion_result = collection.insert_one({"expression": expression.expression, "resultat": resultat})
        return {"_id": str(insertion_result.inserted_id), "expression": expression.expression, "resultat": resultat}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Exporter les résultats dans un fichier CSV
@app.get("/export/")
def export_csv():
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    del df['_id']
    csv_string = df.to_csv(index=False)
    return Response(content=csv_string, media_type="text/csv")