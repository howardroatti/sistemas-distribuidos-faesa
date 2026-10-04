---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 12 — Revisão da C2 + Avaliação C2.A1

C2 · ⬅ **DIA DE AVALIAÇÃO** · entrega do **C2.A2**
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Como funciona o dia de hoje

1. **Revisão consolidada** da Verificação C2 (Aulas 8–11) — o caminho e as **6 perguntas-chave**.
2. **Esquenta** — 5 questões comentadas no estilo ENADE.
3. **Avaliação C2.A1** — prova escrita, estilo ENADE (**5,0 pontos**).
4. **Entrega do C2.A2** — RAG distribuído no repositório (**5,0 pontos**).

<div class="dica">💡 <strong>Nota da C2 = C2.A1 (5,0) + C2.A2 (5,0)</strong>. Hoje fecham as duas.</div>

---

## O caminho que percorremos na C2

A pergunta da C2: **como vários serviços se coordenam e permanecem consistentes e de pé, apesar de falhas?**

- **Aula 8** — **mensageria**: síncrono × assíncrono, **fila/worker**, pub/sub, **API Gateway**.
- **Aula 9** — **tempo e ordenação**: **Lamport** e **relógio vetorial** (causalidade).
- **Aula 10** — **replicação e CAP**: consistência **forte × eventual**, **CP × AP**.
- **Aula 11** — **consenso (Raft)** e **resiliência**: quórum, timeout, retry, **disjuntor**, idempotência.

<div class="dica">💡 Releia os quadros de cada aula e rode de novo <code>replicas_sim.py</code>, <code>raft_sim.py</code> e <code>resiliencia.py</code>.</div>

---

## A trilha da C2 — do acoplamento síncrono ao sistema resiliente

<svg viewBox="0 0 860 230" role="img" style="width:100%;max-width:850px;display:block;margin:8px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="tb" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
    <marker id="tbig" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto"><path d="M0,0 L8,3.5 L0,7 Z" fill="#12437f"/></marker>
  </defs>
  <text x="430" y="24" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">a pergunta da C2: como vários serviços se coordenam e permanecem consistentes apesar de falhas?</text>
  <rect x="40" y="54" width="170" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="125" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 8</text><text x="125" y="100" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Mensageria</text><text x="125" y="117" text-anchor="middle" fill="#64748b" font-size="10.5">fila · gateway</text>
  <rect x="245" y="54" width="170" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="330" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 9</text><text x="330" y="100" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Relógios lógicos</text><text x="330" y="117" text-anchor="middle" fill="#64748b" font-size="10.5">Lamport · vetorial</text>
  <rect x="450" y="54" width="170" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="535" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 10</text><text x="535" y="100" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">CAP</text><text x="535" y="117" text-anchor="middle" fill="#64748b" font-size="10.5">CP × AP</text>
  <rect x="655" y="54" width="170" height="72" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="740" y="80" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">Aula 11</text><text x="740" y="100" text-anchor="middle" fill="#14532d" font-size="12" font-weight="600">Raft + resiliência</text><text x="740" y="117" text-anchor="middle" fill="#16a34a" font-size="10.5">quórum · disjuntor</text>
  <line x1="210" y1="90" x2="243" y2="90" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="415" y1="90" x2="448" y2="90" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="620" y1="90" x2="653" y2="90" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="45" y1="178" x2="815" y2="178" stroke="#12437f" stroke-width="3" marker-end="url(#tbig)"/>
  <text x="48" y="206" fill="#334155" font-size="12.5" font-weight="700">serviços acoplados e síncronos</text>
  <text x="815" y="206" text-anchor="end" fill="#16a34a" font-size="12.5" font-weight="700">sistema coordenado e resiliente</text>
</svg>

<div class="dica">💡 Cada aula atacou um problema de <strong>coordenação</strong>: desacoplar (fila), ordenar (relógios), manter consistente (CAP) e concordar/sobreviver (Raft + resiliência).</div>

---

## As 6 perguntas que você precisa saber responder

Se você responde estas **com segurança**, está pronto para a C2.A1:

1. Quando usar comunicação **assíncrona (fila)** em vez de síncrona — e o que a fila **resolve**?
2. Por que **carimbo de hora não ordena** eventos distribuídos? O que o **Lamport** faz?
3. O que o **relógio vetorial** detecta que o de Lamport **não** distingue?
4. Enuncie o **CAP**: sob **partição**, o que se escolhe — e o que é consistência **eventual**?
5. O que é **quórum** no **Raft** e por que ele é um sistema **CP**?
6. Quais as **3 defesas** de uma chamada remota — e por que **idempotência** é pré-condição da retentativa?

<div class="aviso">📌 Travou em alguma? Volte ao deck da aula correspondente <strong>agora</strong> — é o melhor uso dos próximos minutos.</div>

---

<!-- _class: secao -->

# Esquenta C2
### 5 questões comentadas — estilo ENADE

---

## Questão 1 — pico de carga no serviço de IA

Um serviço de inferência recebe **rajadas** de requisições e, sob pico, começa a **recusar** chamadas (fica sem vazão). A equipe insere uma **fila** entre a API e o processamento. O principal ganho dessa mudança é:

A) eliminar a necessidade de rede entre os serviços.
B) **desacoplar** o recebimento do processamento, **absorvendo os picos** e permitindo escalar com mais **workers**.
C) garantir que toda requisição seja processada **instantaneamente**.
D) tornar o serviço **consistente de forma forte**.
E) dispensar o tratamento de erros.

---

## Questão 1 — resposta **B**

- A fila é um **amortecedor**: a API só **enfileira** (responde rápido) e um ou mais **workers** consomem no seu ritmo.
- Absorve **picos** e escala horizontalmente (**+workers**). Não torna nada instantâneo (**C**) nem trata de consistência (**D**).

<div class="dica">💡 Aula 8 — fila/worker, o amortecedor do sistema.</div>

---

## Questão 2 — ordenação de eventos (Lamport)

No processo **P2**, o relógio de **Lamport** vale **5**. Chega uma mensagem de **P1** com carimbo **9**. Após o recebimento, o relógio de **P2** passa a valer:

A) 5
B) 9
C) **10**
D) 14
E) 6

---

## Questão 2 — resposta **C**

- Regra do **recebimento**: **máximo**(relógio local, carimbo) **+ 1** = **máx(5, 9) + 1 = 10**.
- Cai quem esquece o "**+1**" (marca 9) ou quem **soma** tudo (marca 14).

<div class="dica">💡 Aula 9 — Lamport. Carimbo de hora não serve; o contador causal, sim.</div>

---

## Questão 3 — consistência e CAP (asserção-razão)

**ASSERÇÃO:** Um sistema distribuído com dados replicados **não** consegue oferecer **consistência forte** e **disponibilidade total** ao mesmo tempo **durante uma partição de rede**.
**PORQUE**
**RAZÃO:** Durante a partição, cópias separadas **não conseguem se coordenar**, então ou se **recusa** responder (preserva C) ou se **responde** com dado possivelmente velho (preserva A).

A) **Asserção e razão verdadeiras, e a razão justifica a asserção.**
B) Ambas verdadeiras, mas a razão não justifica.
C) Asserção verdadeira, razão falsa.
D) Asserção falsa, razão verdadeira.
E) Ambas falsas.

---

## Questão 3 — resposta **A**

- É exatamente o **teorema CAP**: sob **partição (P)**, não dá **C** e **A** juntas — e a razão (cópias não se coordenam) **explica** por quê.
- "Eventual" é o lado **AP**: responde já e **converge** depois.

<div class="dica">💡 Aula 10 — CAP. Formato asserção-razão é clássico do ENADE.</div>

---

## Questão 4 — consenso sob partição (Raft)

Um serviço usa **Raft** com **5 réplicas**. Uma partição separa **3 de um lado** e **2 do outro**. Sobre **novas escritas** durante a partição:

A) os dois lados aceitam, cada um com seu líder.
B) nenhum aceita, pois Raft exige unanimidade.
C) **apenas o lado com 3 réplicas aceita, por formar a maioria (3 de 5).**
D) apenas o lado com 2, por ter menos conflito.
E) ambos param até intervenção manual.

---

## Questão 4 — resposta **C**

- Raft comita por **maioria** (`5/2 + 1 = 3`). Só o lado com **3** forma quórum → **elege líder e aceita** escritas.
- O lado com **2** fica **indisponível** para escrita (preserva **C**) → Raft é **CP**.

<div class="dica">💡 Aula 11 — quórum e o elo Raft ↔ CAP. Nunca dois líderes no mesmo mandato.</div>

---

## Questão 5 — resiliência da chamada remota

Uma equipe adiciona **retentativa automática** à chamada que **cria um pagamento** num serviço externo. Logo surgem **cobranças duplicadas**. A causa e a correção adequadas são:

A) a rede está lenta; aumentar o timeout.
B) **a operação não é idempotente; torná-la idempotente (ex.: chave de idempotência) antes de retentar.**
C) faltam workers; adicionar mais.
D) o disjuntor está aberto; fechá-lo manualmente.
E) o problema é o protocolo; trocar REST por gRPC.

---

## Questão 5 — resposta **B**

- Retentar **só** é seguro se repetir **não duplica efeito** — isto é, se a operação é **idempotente**.
- Criar pagamento (um **POST** de criação) **não** é idempotente; a correção é uma **chave de idempotência** para o servidor ignorar a repetição.

<div class="dica">💡 Aula 11 — "pôr retry resolve" é pegadinha: só com idempotência.</div>

---

## Avaliação C2.A1 — a prova

- **Escrita, individual, estilo ENADE** — vale **5,0 pontos**.
- **Integra todo o bloco C2**: mensageria, ordenação (Lamport/vetorial), CAP e consenso/resiliência aparecem **combinados** em estudos de caso.
- **Cobra entendimento operacional** (não formalismo): saber **aplicar** a regra, **classificar** o caso e **escolher** o lado certo.

<div class="aviso">📌 As 5 questões do esquenta são do <strong>mesmo estilo</strong> da prova. Se você as entendeu, está pronto.</div>

---

## Entrega do C2.A2 — checklist antes de submeter

Dia de entrega do **RAG distribuído**. **Rode do zero** e confira contra a **rubrica**:

- **Três microsserviços** — **ingestão**, **recuperação** e **geração** — rodando e se comunicando?
- A comunicação usa **REST/gRPC** e **mensageria** onde faz sentido?
- A chamada ao **LLM** está protegida por **circuit breaker** (timeout + retry + disjuntor)?
- **Clona do zero** e segue o **seu README**? Há **commits ao longo** do período?

<div class="dica">💡 Rubrica: arquitetura <strong>1,5</strong> · comunicação <strong>1,5</strong> · resiliência <strong>1,0</strong> · execução reproduzível <strong>1,0</strong>. A <strong>sofisticação do modelo de IA não pontua</strong>.</div>

---

## ◆ Foco ENADE

- A prova **C2.A1 integra todo o bloco** — e este é o conteúdo **mais abstrato** do semestre.
- No ENADE, **consistência, consenso e ordenação** aparecem como **estudos de caso**: identifique **qual** mecanismo o cenário pede.
- **Treine**: calcular um Lamport, classificar CP/AP, achar a maioria, apontar a falta de idempotência.

**Termos-chave:** Fila/assíncrono · Lamport · Vetorial · CAP · CP/AP · Quórum · Raft · Disjuntor · Idempotência

<div class="dica">💡 Pegadinhas favoritas: "sistema CA", "retry resolve tudo", "carimbo de hora ordena", "dois líderes no mesmo mandato".</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para revisar**
- Os quadros de resumo das Aulas 8–11.
- Os três simuladores: `replicas_sim.py`, `raft_sim.py`, `resiliencia.py`.
- O seu **C2.A2** contra a **rubrica**.

</div>

<div>

**Glossário**
- **C2.A1:** avaliação escrita individual, estilo ENADE (5,0).
- **C2.A2:** RAG distribuído no repositório (5,0).
- **Quórum:** maioria necessária para decidir (N/2 + 1).
- **CP / AP:** o lado do CAP priorizado sob partição.
- **Idempotência:** repetir não muda o efeito final.

</div>

</div>

---

<!-- _class: secao -->

# Boa prova! 🚀
### Entregue o C2.A2 no repositório. A C3 leva o sistema para a **nuvem**.

**Próxima (Aula 13):** **Computação em nuvem, containers e o primeiro deploy** — empacotar o serviço e colocá-lo no ar com URL pública.

<a class="proximo" href="aula-11-consenso-raft-resiliencia.html">← Anterior<small>Aula 11 · Raft e resiliência</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
