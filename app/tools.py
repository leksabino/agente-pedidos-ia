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

def confirmar_pedido(cliente: str, confirmacao_explicita: bool):
    # Trava 1: sem SIM, não confirma
    if not confirmacao_explicita:
        return {"erro": "Preciso da sua confirmação explícita. Digite SIM para confirmar."}
    # Trava 2: carrinho vazio não confirma
    if not carrinho:
        return {"erro": "Carrinho vazio."}
    # Calcula total
    total = 0
    for item in carrinho:
        total += item["preco"] * item["qtd"]
    # Limpa o carrinho depois de confirmar
    carrinho.clear()
    return {"sucesso": f"Pedido confirmado para {cliente}", "total": formatar_preco(total)}

def formatar_cardapio_bonito():
    linhas = ["🍕 Cardápio:"]
    for item in CARDAPIO:
        linhas.append(f"{item['id']}. {item['nome']} - {formatar_preco(item['preco'])}")
    return "\n".join(linhas)

def formatar_carrinho_bonito():
    if not carrinho:
        return "Carrinho vazio."
    # Agrupa: soma quantidade do mesmo item
    agrupado = {}
    for item in carrinho:
        nome = item["nome"]
        if nome not in agrupado:
            agrupado[nome] = {"preco": item["preco"], "qtd": 0}
        agrupado[nome]["qtd"] += item["qtd"]
    linhas = ["🛒 Seu pedido:"]
    total = 0
    for nome, dados in agrupado.items():
        subtotal = dados["preco"] * dados["qtd"]
        total += subtotal
        linhas.append(f"{dados['qtd']}x {nome} - {formatar_preco(subtotal)}")
    linhas.append(f"Total: {formatar_preco(total)}")
    return "\n".join(linhas)