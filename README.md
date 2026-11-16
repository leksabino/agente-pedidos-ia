# Agente de Pedidos IA

Agente de pedidos com guardrails, Tool Calling, fallback e Gemini.

## O que ele faz

- Mostra cardapio real, nunca inventa prato
- Valida item e quantidade (1 a 10)
- So confirma pedido com SIM explicito
- Usa Gemini para entender a mensagem, com fallback se falhar
- Entende numero (1 a 4), apelido e quantidade

## Como rodar a API

    pip install -r requirements.txt
    uvicorn app.main:app --reload

Abra no navegador: http://127.0.0.1:8000/docs

## Testar no terminal

    python demo_chat.py

## Testes

    python -m pytest -v

## Endpoints

- GET / - status
- POST /chat - envia mensagem e cliente

## Stack

Python, FastAPI, Pydantic, Pytest, Gemini