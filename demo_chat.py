# demo - chat.py - só pra testar no terminal digitando
# Não é a API oficial. Pra usar a API: uvicorn app.main:app --reload

from app.agent import processar_mensagem

print("=== Agente de Pedidos IA - Demo no Terminal ===")
print("Digite 'sair' para parar")
print("Você pode digitar:")
print("  - cardapio")
print("  - 1, 2, 3 ou 4 (número do item)")
print("  - batata frita, pizza margherita...")
print("  - SIM para confirmar")
print("-------------------------------------------")

while True:
    mensagem = input("\nVocê: ").strip()

    # Se apertar Enter sem digitar nada, não faz nada
    if mensagem == "":
        print("Agente: Digite alguma coisa, ex: cardapio")
        continue

    if mensagem.lower() == "sair":
        print("Agente: Tchau! Obrigado pelo pedido.")
        break

    resultado = processar_mensagem(mensagem, "Alexssander")
    print(f"Agente: {resultado['resposta']}")