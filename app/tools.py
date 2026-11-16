# app/tools.py - ferramentas que o agente pode chamar

from app.database import CARDAPIO, formatar_preco
from app.guardrails import checar_guardrails

carrinho = []

def listar_cardapio():
    return CARDAPIO

def adicionar_item(nome: str, quantidade: int):
    pode, msg = checar_guardrails(nome, quantidade)
    if not pode:
        return {"erro": msg}
    # Acha o item no cardápio real
    for item in CARDAPIO:
        if item["nome"].lower() == nome.lower():
            carrinho.append({"nome": item["nome"], "preco": item["preco"], "qtd": quantidade})
            return {"sucesso": f"{quantidade}x {nome} adicionado"}
    return {"erro": "Item não encontrado"}

def ver_carrinho():
    total = 0
    for item in carrinho:
        total += item["preco"] * item["qtd"]
    return {"itens": carrinho, "total": formatar_preco(total)}