#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 13 - um servico minimo para conteinerizar e publicar na nuvem.

Expoe o NOME DO HOST (hostname), que no Docker vira o ID do container - util para
VER qual replica respondeu quando o servico for escalado (elasticidade).

Rodar local:   uvicorn app:app --reload --port 8000   ->  http://127.0.0.1:8000
No container:  uvicorn app:app --host 0.0.0.0 --port 8000  (ver Dockerfile)
"""
import os
import socket
from fastapi import FastAPI

app = FastAPI(title="Servico na nuvem - Aula 13")


@app.get("/")
def raiz():
    return {
        "mensagem": "Ola da nuvem!",
        "host": socket.gethostname(),          # no Docker, muda a cada container
        "versao": os.getenv("APP_VERSION", "1.0"),
    }


@app.get("/health")
def health():
    # usada pela nuvem para saber se a instancia esta viva (health check)
    return {"status": "ok"}
