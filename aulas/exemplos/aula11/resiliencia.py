#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 11 - Blindar a chamada de IA: timeout + retentativa + disjuntor.

Deterministico (sem rede real): o "servico de IA" segue um ROTEIRO de respostas,
onde cada resposta tem uma latencia (em "ticks") e um resultado (ok/erro).
Mostra, em ordem:
  - TIMEOUT: se a latencia passa do limite, a chamada e abortada (conta como falha);
  - RETENTATIVA: tenta de novo algumas vezes antes de desistir;
  - DISJUNTOR (circuit breaker): apos N falhas seguidas, ABRE e passa a falhar RAPIDO,
    protegendo o sistema; depois de um tempo de descanso, tenta "meia-volta".

Roda no Windows/venv:  python resiliencia.py
"""

LIMITE_TIMEOUT = 3   # ticks: acima disso, e timeout


class ServicoInstavel:
    """Servico fake cujas respostas vem de um roteiro: (latencia, 'ok'|'erro')."""
    def __init__(self, roteiro):
        self.roteiro = list(roteiro)
        self.i = 0

    def chamar(self):
        lat, res = self.roteiro[min(self.i, len(self.roteiro) - 1)]
        self.i += 1
        if lat > LIMITE_TIMEOUT:
            raise TimeoutError(f"timeout (latencia {lat} > {LIMITE_TIMEOUT})")
        if res == "erro":
            raise RuntimeError("erro do servico")
        return f"resposta ok (latencia {lat})"


class Disjuntor:
    """fechado: deixa passar | aberto: bloqueia | meia-volta: deixa 1 tentar."""
    def __init__(self, limite_falhas=3, descanso=3):
        self.limite = limite_falhas
        self.descanso = descanso
        self.falhas = 0
        self.estado = "fechado"
        self.aberto_em = None

    def permite(self, agora):
        if self.estado == "aberto":
            if agora - self.aberto_em >= self.descanso:
                self.estado = "meia-volta"
                print(f"    [t{agora}] descanso terminou -> MEIA-VOLTA (deixa UMA sondagem)")
                return True          # deixa UMA tentativa de sondagem
            return False             # ainda em descanso: falha rapido
        return True

    def sucesso(self):
        self.falhas = 0
        self.estado = "fechado"

    def falha(self, agora):
        self.falhas += 1
        if self.falhas >= self.limite:
            self.estado = "aberto"
            self.aberto_em = agora


def chamar_blindado(servico, disjuntor, agora, tentativas=2):
    """Uma chamada protegida: consulta o disjuntor; se passar, tenta com retentativa."""
    if not disjuntor.permite(agora):
        return f"[t{agora}] disjuntor ABERTO -> falha rapido (nem chama o servico)"
    for tentativa in range(1, tentativas + 1):
        try:
            r = servico.chamar()
            disjuntor.sucesso()
            return f"[t{agora}] OK na tentativa {tentativa}: {r}  | disjuntor={disjuntor.estado}"
        except Exception as e:
            motivo = f"{type(e).__name__}: {e}"
            if tentativa < tentativas:
                print(f"    [t{agora}] falha ({motivo}) -> retenta ({tentativa+1}/{tentativas})")
    disjuntor.falha(agora)
    return (f"[t{agora}] FALHOU apos {tentativas} tentativas ({motivo})  | "
            f"disjuntor={disjuntor.estado} (falhas={disjuntor.falhas})")


if __name__ == "__main__":
    # Roteiro: uma rajada ruim (timeouts/erros) que abre o disjuntor, depois o servico volta a ok.
    # Cada CHAMADA faz ate 2 tentativas, logo consome ate 2 itens do roteiro.
    roteiro = [
        (9, "ok"), (1, "erro"),   # t0: timeout + erro  -> chamada FALHA (falhas=1)
        (1, "erro"), (9, "ok"),   # t1: erro + timeout  -> chamada FALHA (falhas=2)
        (1, "erro"), (1, "erro"), # t2: erro + erro     -> chamada FALHA (falhas=3 -> ABRE)
        (1, "ok"), (1, "ok"),     # servico ja se recuperou (mas t3 nem chega a chamar)
        (1, "ok"), (1, "ok"),
    ]
    servico = ServicoInstavel(roteiro)
    disjuntor = Disjuntor(limite_falhas=3, descanso=2)

    print("Chamadas blindadas (timeout + retentativa + disjuntor)")
    print("-" * 54)
    for agora in range(10):
        print(chamar_blindado(servico, disjuntor, agora))

    print("\nLeitura: timeouts e erros contam como falha (cada chamada ja tenta 2x);")
    print("na 3a chamada falha o disjuntor ABRE e em t3 falha RAPIDO (nem bate no servico);")
    print("passado o descanso, entra em MEIA-VOLTA, sonda em t4, da certo e FECHA de novo.")
