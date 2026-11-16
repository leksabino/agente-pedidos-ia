# app/guardrails.py - travas de segurança

from app.database import CARDAPIO, formatar_preco

def item_existe(nome_item: str) -> bool:
    for item in CARDAPIO:
        if item["nome"].lower() == nome_item.lower():
            return True
    return False

def validar_quantidade(qtd: int) -> bool:
    return 1 <= qtd <= 10

def checar_guardrails(item: str, qtd: int):
    if not item_existe(item):
        return False, f"Desculpe, '{item}' não está no cardápio."
    if not validar_quantidade(qtd):
        return False, "Quantidade precisa ser entre 1 e 10."
    return True, "OK"