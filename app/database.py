# app/database.py

CARDAPIO = [
    {"id": 1, "nome": "Pizza Margherita", "preco": 45.90},
    {"id": 2, "nome": "Hambúrguer Artesanal", "preco": 32.50},
    {"id": 3, "nome": "Refrigerante", "preco": 7.00},
    {"id": 4, "nome": "Batata Frita", "preco": 18.00},
]

def formatar_preco(preco: float) -> str:
    # :.2f significa "sempre 2 casas depois da vírgula"
    return f"R$ {preco:.2f}"