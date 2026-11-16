# app/agent.py - cérebro do agente, usa Gemini + tools com fallback

import os
from dotenv import load_dotenv
from app.tools import listar_cardapio, adicionar_item, ver_carrinho, confirmar_pedido

load_dotenv()
chave = os.getenv("GEMINI_API_KEY")

# Tenta ligar o Gemini novo
modelo = None
cliente_gemini = None
try:
    from google import genai
    if chave:
        cliente_gemini = genai.Client(api_key=chave)
        modelo = "gemini-2.0-flash"
        print("Gemini conectado")
    else:
        print("Sem chave, usando fallback")
except Exception as e:
    print(f"Gemini falhou, usando fallback: {e}")

def processar_mensagem(mensagem: str, cliente: str = "Cliente"):
    texto = mensagem.lower()

    # Se o Gemini estiver ligado, tenta usar ele só pra entender
    if cliente_gemini:
        try:
            resposta = cliente_gemini.models.generate_content(
                model=modelo,
                contents=f"Você é atendente. Cliente disse: '{mensagem}'. Responda curto."
            )
            # A gente ainda usa sua lógica com guardrail, o Gemini só ajuda a entender
            if "cardapio" in texto or "cardápio" in texto:
                return {"resposta": f"Gemini: {resposta.text} | Cardápio: {listar_cardapio()}"}
        except Exception:
            pass

    # Fallback que você já fez
    if "cardapio" in texto or "cardápio" in texto or "menu" in texto:
        return {"resposta": f"Nosso cardápio: {listar_cardapio()}"}
    if texto.strip() == "sim":
        resultado = confirmar_pedido(cliente, True)
        return {"resposta": str(resultado)}
    if "pizza margherita" in texto:
        resultado = adicionar_item("Pizza Margherita", 1)
        return {"resposta": str(resultado) + f" | {ver_carrinho()}"}
    return {"resposta": "Desculpe, não entendi. Você quer ver o cardápio, pedir Pizza Margherita ou confirmar com SIM?"}