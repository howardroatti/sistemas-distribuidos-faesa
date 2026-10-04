#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 14 - servico de INFERENCIA (interno). O gateway fala com ele; o mundo nao.

'Modelo' trivial e deterministico (so para a aula): classifica sentimento por
palavras-chave. Roda:  uvicorn app:app --host 0.0.0.0 --port 8000
"""
import socket
from fastapi import FastAPI

app = FastAPI(title="Inferencia - Aula 14")

POSITIVAS = ("bom", "otimo", "ótimo", "gostei", "excelente", "adorei")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/prever")
def prever(payload: dict):
    texto = (payload or {}).get("texto", "")
    sentimento = "positivo" if any(p in texto.lower() for p in POSITIVAS) else "negativo"
    return {
        "sentimento": sentimento,
        "n_palavras": len(texto.split()),
        "host": socket.gethostname(),   # qual container respondeu
    }
