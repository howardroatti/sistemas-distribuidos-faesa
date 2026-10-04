#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 14 - API GATEWAY (porta de entrada unica). Encaminha ao servico interno.

O endereco do servico vem de uma variavel de ambiente (INFER_URL) - no
docker-compose ele e o NOME do servico (http://inferencia:8000); local, 127.0.0.1.
Roda:  uvicorn app:app --host 0.0.0.0 --port 8000
"""
import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Gateway - Aula 14")
INFER_URL = os.getenv("INFER_URL", "http://127.0.0.1:8001")


@app.get("/health")
def health():
    return {"status": "ok", "infer_url": INFER_URL}


@app.post("/infer")
def infer(payload: dict):
    try:
        r = httpx.post(f"{INFER_URL}/prever", json=payload, timeout=5)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"servico de inferencia indisponivel: {e}")
    return {"via": "gateway", "resultado": r.json()}
