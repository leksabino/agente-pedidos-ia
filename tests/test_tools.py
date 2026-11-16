# tests/test_tools.py - garante que guardrail e tools não quebram

from app.guardrails import checar_guardrails
from app.tools import adicionar_item, ver_carrinho, carrinho

def test_guardrail_bloqueia_item_fora_cardapio():
    pode, msg = checar_guardrails("Sushi", 1)
    assert pode == False

def test_guardrail_bloqueia_quantidade_alta():
    pode, msg = checar_guardrails("Pizza Margherita", 99)
    assert pode == False

def test_adicionar_item_calcula_total():
    carrinho.clear()
    adicionar_item("Pizza Margherita", 2)
    resultado = ver_carrinho()
    assert resultado["total"] == "R$ 91.80"