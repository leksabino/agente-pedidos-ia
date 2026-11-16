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
    from app.tools import formatar_cardapio_bonito, formatar_carrinho_bonito
    from app.database import CARDAPIO
    import re

    texto = mensagem.lower().strip()
    texto = texto.replace("marguerita", "margherita")

    # Se é número 1-4
    if texto in ["1", "2", "3", "4"]:
        numero = int(texto)
        for item in CARDAPIO:
            if item["id"] == numero:
                resultado = adicionar_item(item["nome"], 1)
                return {"resposta": f"{resultado}\n{formatar_carrinho_bonito()}"}

    if "cardapio" in texto or "cardápio" in texto or "menu" in texto:
        return {"resposta": formatar_cardapio_bonito()}

    # Quero pagar / confirmar / fechar = pede o SIM, não confirma direto
    if "pagar" in texto or "confirmar" in texto or "fechar" in texto or "finalizar" in texto:
        return {"resposta": "Pra confirmar, digite SIM. Sem SIM eu não fecho o pedido, é uma trava de segurança."}

    if texto == "sim":
        resultado = confirmar_pedido(cliente, True)
        return {"resposta": str(resultado)}

    # Procura quantidade: "99 pizzas" ou "2 batata"
    # Pega o número do começo
    match = re.match(r"(\d+)\s*(.*)", texto)
    qtd = 1
    texto_busca = texto
    if match:
        possivel_qtd = int(match.group(1))
        # Se tem número, usa ele como quantidade
        if possivel_qtd != 0:
            qtd = possivel_qtd
            texto_busca = match.group(2)

    # Procura qualquer item, até só "margherita"
    for item in CARDAPIO:
        nome_item = item["nome"].lower()
        # Aceita apelido: "margherita" sozinha = pizza margherita
        apelido = nome_item.split()[-1]  # última palavra, ex: margherita, frita
        if nome_item in texto_busca or apelido in texto_busca:
            resultado = adicionar_item(item["nome"], qtd)
            return {"resposta": f"{resultado}\n{formatar_carrinho_bonito()}"}

    return {"resposta": "Desculpe, não entendi. Digite o número (1 a 4), o nome do prato ou SIM."}