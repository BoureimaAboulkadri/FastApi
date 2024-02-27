from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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
        return {"expression": expression.expression, "resultat": resultat}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
