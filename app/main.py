# app/main.py - API FastAPI, porta de entrada do agente

from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import processar_mensagem

app = FastAPI(title="Agente de Pedidos IA")

class Mensagem(BaseModel):
    mensagem: str
    cliente: str = "Cliente"

@app.get("/")
def home():
    return {"status": "Agente online"}

@app.post("/chat")
def chat(dados: Mensagem):
    resultado = processar_mensagem(dados.mensagem, dados.cliente)
    return resultado