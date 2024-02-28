from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo import MongoClient
from pymongo import MongoClient

# Configuration FastAPI
app = FastAPI()

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
