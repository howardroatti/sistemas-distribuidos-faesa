#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 16 - como um JWT funciona, em Python puro (sem bibliotecas).

Um JWT (HS256) tem 3 partes separadas por ponto:  header.payload.assinatura
A assinatura e um HMAC-SHA256 de 'header.payload' com um SEGREDO que so o
servidor conhece. Por isso o cliente NAO consegue forjar nem adulterar o token:
mudar o payload invalida a assinatura.

Roda:  python auth_demo.py
"""
import base64
import hashlib
import hmac
import json
import time

SEGREDO = "chave-secreta-do-servidor"   # em producao: variavel de ambiente/secret


def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _b64url_dec(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def criar_token(payload: dict, segredo: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    assinatura = hmac.new(segredo.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url(assinatura)}"


def verificar_token(token: str, segredo: str) -> dict:
    partes = token.split(".")
    if len(partes) != 3:
        raise ValueError("formato invalido")
    h, p, s = partes
    esperado = _b64url(hmac.new(segredo.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(esperado, s):       # compara em tempo constante
        raise ValueError("assinatura invalida (token adulterado ou segredo errado)")
    payload = json.loads(_b64url_dec(p))
    if "exp" in payload and payload["exp"] < time.time():
        raise ValueError("token expirado")
    return payload


def tenta(desc, fn):
    try:
        print(f"  {desc}: OK -> {fn()}")
    except Exception as e:
        print(f"  {desc}: REJEITADO -> {e}")


if __name__ == "__main__":
    # exp fixo (bem no futuro) para a saida ser reproduzivel
    token = criar_token({"sub": "aluno42", "role": "aluno", "exp": 4102444800}, SEGREDO)
    print("Token emitido (header.payload.assinatura):")
    print("  " + token + "\n")

    print("Verificacoes:")
    tenta("1) token valido", lambda: verificar_token(token, SEGREDO))

    # adultera o payload (troca role para admin) SEM reassinar
    h, p, s = token.split(".")
    payload_falso = _b64url(json.dumps({"sub": "aluno42", "role": "admin", "exp": 4102444800},
                                       separators=(",", ":")).encode())
    token_adulterado = f"{h}.{payload_falso}.{s}"
    tenta("2) payload adulterado (role=admin)", lambda: verificar_token(token_adulterado, SEGREDO))

    tenta("3) segredo errado", lambda: verificar_token(token, "chave-errada"))

    token_velho = criar_token({"sub": "aluno42", "role": "aluno", "exp": 1000000000}, SEGREDO)
    tenta("4) token expirado", lambda: verificar_token(token_velho, SEGREDO))

    print("\nLicao: so quem tem o SEGREDO assina/valida. Adulterar o payload quebra "
          "a assinatura -> o servidor rejeita.")
