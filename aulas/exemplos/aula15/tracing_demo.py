#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 15 - mini-rastreamento distribuido (tracing).

Uma requisicao atravessa varios servicos; cada etapa e um SPAN (nome + duracao).
O conjunto de spans ligados por pai->filho e um TRACE. O programa monta a arvore
e aponta a ETAPA MAIS LENTA - onde otimizar rende mais.

Duracoes fixas (ms) para a saida ser reproduzivel. Num sistema real, o
OpenTelemetry mede esses tempos e manda para um visualizador (ex.: Jaeger).

Roda:  python tracing_demo.py
"""


class Span:
    def __init__(self, nome, dur_ms, filhos=None):
        self.nome = nome
        self.dur_ms = dur_ms            # duracao total desta etapa
        self.filhos = filhos or []


def imprimir(span, nivel=0):
    barra = "#" * max(1, span.dur_ms // 10)           # "waterfall" em texto
    print(f"{'  ' * nivel}- {span.nome:<26} {span.dur_ms:>4} ms  {barra}")
    for f in span.filhos:
        imprimir(f, nivel + 1)


def todos(span):
    yield span
    for f in span.filhos:
        yield from todos(f)


if __name__ == "__main__":
    # Um trace do RAG: gateway -> recuperacao -> geracao (LLM). Tempos em ms.
    trace = Span("POST /pergunta (gateway)", 180, [
        Span("recuperacao.buscar", 25, [
            Span("db.embeddings.query", 20),
        ]),
        Span("geracao.responder", 140, [
            Span("llm.api.chamada", 130),              # o gargalo
        ]),
    ])

    print("TRACE - uma requisicao de ponta a ponta")
    print("trace_id: 7f3a9c..  (o mesmo id percorre TODOS os servicos)\n")
    imprimir(trace)

    folhas = [s for s in todos(trace) if not s.filhos]
    gargalo = max(folhas, key=lambda s: s.dur_ms)
    total = trace.dur_ms
    pct = round(100 * gargalo.dur_ms / total)
    print(f"\nEtapa mais lenta: '{gargalo.nome}' = {gargalo.dur_ms} ms "
          f"({pct}% dos {total} ms totais).")
    print("=> otimizar aqui tem o maior impacto. Sem o trace, voce nao saberia "
          "QUAL servico esta lento.")
