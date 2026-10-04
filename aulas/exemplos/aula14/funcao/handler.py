#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 14 - funcao SERVERLESS (FaaS).

No modelo serverless voce entrega SO a funcao; a plataforma (AWS Lambda, Google
Cloud Functions, Azure Functions) cuida de servidor, escala e de rodar a funcao
SOB DEMANDA - uma instancia por requisicao, escalando a zero quando ociosa.

'event'  = o payload que a plataforma entrega na invocacao.
'context'= metadados da execucao (aqui, ignorado).

Teste local:  python handler.py
"""


def handler(event, context=None):
    nome = (event or {}).get("nome", "mundo")
    return {
        "statusCode": 200,
        "body": f"Ola, {nome}! Esta funcao rodou sob demanda, sem servidor dedicado.",
    }


if __name__ == "__main__":
    # simula duas invocacoes independentes (cada uma poderia cair numa instancia diferente)
    print(handler({"nome": "FAESA"}))
    print(handler({}))
