# app/agent.py - cérebro do agente, usa Gemini + tools com fallback

import os
from app.tools import listar_cardapio, adicionar_item, ver_carrinho, confirmar_pedido

def processar_mensagem(mensagem: str, cliente: str = "Cliente"):
    texto = mensagem.lower()

    # 1. Se falar em cardápio, mostra cardápio
    if "cardapio" in texto or "cardápio" in texto or "menu" in texto:
        return {"resposta": f"Nosso cardápio: {listar_cardapio()}"}

    # 2. Se falar SIM, tenta confirmar
    if texto.strip() == "sim":
        resultado = confirmar_pedido(cliente, True)
        return {"resposta": str(resultado)}

    # 3. Se falar pizza, tenta adicionar 1 pizza
    if "pizza margherita" in texto:
        resultado = adicionar_item("Pizza Margherita", 1)
        return {"resposta": str(resultado) + f" | {ver_carrinho()}"}

    # 4. Se não entendeu, faz fallback
    return {"resposta": "Desculpe, não entendi. Você quer ver o cardápio, pedir Pizza Margherita ou confirmar com SIM?"}