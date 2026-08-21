---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 9 — Tempo e ordenação: relógios lógicos

C2 · Coordenação e consistência · 01/10/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C2

<div class="cols">

<div>

**C1 · Fundamentos** (1–7) ✅

**C2 · Coordenação e consistência** (8–12)
Mensageria ✅ · **relógios lógicos** · CAP · Raft · resiliência.

</div>

<div>

**C3 · Nuvem e segurança** (13–18)

<div class="dica">📍 <strong>Aula 9</strong>. Aviso de largada 👇</div>

</div>

</div>

<div class="aviso">🧠 Este é, com sinceridade, o tópico <strong>mais abstrato</strong> do semestre. Por isso vamos <strong>devagar</strong>, por <strong>exemplos numéricos</strong> e uma <strong>simulação</strong> — <strong>zero</strong> fórmula decorada. Se não "clicar" de primeira, é normal: relemos a tabela e roda o código.</div>

---

## Retomada

<div class="dica">🔄 Você completou o worker (retentativa + dead-letter) e começou o C2.A2?</div>

- Na fila, as tarefas eram processadas **em alguma ordem** — mas **qual** ordem é a "certa" quando as coisas acontecem em **máquinas diferentes**?
- Hoje descobrimos que **carimbo de hora não serve** para isso — e o que serve.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** por que **não existe relógio global confiável** em sistemas distribuídos.
2. **Aplicar** o relógio de **Lamport** para ordenar eventos (a regra do **máximo + 1**).
3. **Usar** o relógio **vetorial** para identificar eventos **concorrentes**.

---

## O problema: não existe um "agora" comum

- Cada máquina tem **seu próprio relógio**, e dois relógios **nunca** marcam o mesmo instante — eles andam em ritmos um pouco diferentes (**clock drift**, desvio de relógio).
- Sincronizar pela rede **não resolve de vez**: a própria mensagem de acerto leva um tempo **variável** para chegar.

<div class="aviso">⚠️ Consequência séria: <strong>não dá para confiar no carimbo de hora</strong> para decidir a ordem dos eventos. Se dois pedidos chegam quase juntos a servidores diferentes, comparar os relógios físicos pode <strong>inverter</strong> a ordem real.</div>

---

## Por que o relógio engana — um exemplo

<svg viewBox="0 0 860 280" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="lt" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
  <text x="120" y="34" fill="#0d2b57" font-size="13" font-weight="700">tempo real — o que de fato aconteceu</text>
  <line x1="120" y1="64" x2="756" y2="64" stroke="#cbd5e1" stroke-width="2" marker-end="url(#lt)"/>
  <text x="770" y="68" fill="#94a3b8" font-size="12" font-style="italic">→</text>
  <text x="322" y="50" text-anchor="middle" fill="#12437f" font-size="12.5" font-weight="700">Pedido A · 1º</text>
  <circle cx="322" cy="64" r="8" fill="#12437f"/>
  <text x="582" y="50" text-anchor="middle" fill="#c2740a" font-size="12.5" font-weight="700">Pedido B · 2º</text>
  <circle cx="582" cy="64" r="8" fill="#e08a00"/>
  <line x1="322" y1="74" x2="322" y2="106" stroke="#94a3b8" stroke-width="1.6" stroke-dasharray="4 3"/>
  <line x1="582" y1="74" x2="582" y2="106" stroke="#94a3b8" stroke-width="1.6" stroke-dasharray="4 3"/>
  <rect x="246" y="108" width="152" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="322" y="134" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Servidor 1</text>
  <text x="322" y="160" text-anchor="middle" fill="#334155" font-size="14" font-family="Consolas,monospace" font-weight="700">🕙 10:00:05</text>
  <rect x="506" y="108" width="172" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="592" y="130" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Servidor 2</text>
  <text x="592" y="152" text-anchor="middle" fill="#334155" font-size="14" font-family="Consolas,monospace" font-weight="700">🕙 10:00:02</text>
  <text x="592" y="170" text-anchor="middle" fill="#b91c1c" font-size="11">relógio atrasado</text>
  <rect x="150" y="204" width="560" height="52" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="430" y="226" text-anchor="middle" fill="#991b1b" font-size="12.5" font-weight="700">Ordenando pelo carimbo: 02 (B) &lt; 05 (A) → pareceria B antes de A.</text>
  <text x="430" y="245" text-anchor="middle" fill="#dc2626" font-size="12" font-weight="700">ERRADO — A aconteceu primeiro. O relógio inverteu a ordem real.</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> dois relógios de parede nunca batem igual. Se cada foto guarda a hora do <em>seu</em> relógio, <strong>não dá para confiar nela</strong> para dizer o que aconteceu primeiro.</div>

---

## A virada de chave 💡

Se não podemos confiar na **hora**, o que sobra?

<div class="dica">💡 Não precisamos saber <strong>QUANDO</strong> (a hora) — precisamos saber <strong>O QUE VEIO ANTES DE QUÊ</strong> (a ordem). Trocamos "hora real" por <strong>causalidade</strong>.</div>

- **Causalidade:** a relação em que um evento **influenciou** a ocorrência de outro.
- É como **numerar suas cartas** para saber a sequência — mesmo sem olhar o relógio.

---

## "Aconteceu antes" (→) — 3 regrinhas

Dizemos que **A → B** ("A aconteceu antes de B") quando:

1. **Mesmo processo:** A e B estão na mesma máquina e A veio **primeiro**.
2. **Mensagem:** A é o **envio** e B é o **recebimento** da mesma mensagem (enviar vem antes de receber).
3. **Transitividade:** se **A → B** e **B → C**, então **A → C**.

<div class="aviso">⚠️ Se <strong>nenhuma</strong> das regras liga A e B, eles são <strong>concorrentes</strong> (A ‖ B): aconteceram sem que um influenciasse o outro. Guardar esse termo — ele é a estrela da aula.</div>

---

## Relógio de Lamport — uma regra só

Um **contador por processo** (começa em 0). Três passos:

1. **Evento local:** contador **+1**.
2. **Ao enviar:** faça +1 e **mande junto** o valor do contador (o "carimbo").
3. **Ao receber:** contador = **máximo**(o meu, o carimbo recebido) **+ 1**.

<div class="dica">💡 É só isso: <strong>máximo + 1</strong> no recebimento; <strong>+1</strong> nos demais. Vamos ver rodando.</div>

---

## Exemplo — a execução (o número no círculo é o relógio)

<svg viewBox="0 0 840 400" role="img" style="width:100%;max-width:880px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="tm" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker>
    <marker id="mm" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#e08a00"/></marker>
  </defs>
  <text x="820" y="58" text-anchor="end" fill="#94a3b8" font-size="13" font-style="italic">tempo →</text>
  <text x="72" y="96" text-anchor="end" font-weight="700" fill="#0d2b57" font-size="17">P1</text>
  <line x1="90" y1="90" x2="820" y2="90" stroke="#cbd5e1" stroke-width="2" marker-end="url(#tm)"/>
  <text x="72" y="216" text-anchor="end" font-weight="700" fill="#0d2b57" font-size="17">P2</text>
  <line x1="90" y1="210" x2="820" y2="210" stroke="#cbd5e1" stroke-width="2" marker-end="url(#tm)"/>
  <text x="72" y="336" text-anchor="end" font-weight="700" fill="#0d2b57" font-size="17">P3</text>
  <line x1="90" y1="330" x2="820" y2="330" stroke="#cbd5e1" stroke-width="2" marker-end="url(#tm)"/>
  <line x1="334" y1="101" x2="437" y2="199" stroke="#e08a00" stroke-width="2.5" marker-end="url(#mm)"/>
  <text x="238" y="150" fill="#c2740a" font-size="13" font-weight="600">m1 · carimbo 2</text>
  <line x1="601" y1="221" x2="709" y2="319" stroke="#e08a00" stroke-width="2.5" marker-end="url(#mm)"/>
  <text x="512" y="268" fill="#c2740a" font-size="13" font-weight="600">m2 · carimbo 4</text>
  <text x="160" y="58" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">a</text>
  <circle cx="160" cy="90" r="17" fill="#12437f"/><text x="160" y="96" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">1</text>
  <text x="320" y="58" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">b · envia</text>
  <circle cx="320" cy="90" r="17" fill="#12437f"/><text x="320" y="96" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">2</text>
  <text x="240" y="180" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">c</text>
  <circle cx="240" cy="210" r="17" fill="#12437f"/><text x="240" y="216" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">1</text>
  <text x="450" y="180" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">d · recebe</text>
  <circle cx="450" cy="210" r="17" fill="#12437f"/><text x="450" y="216" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">3</text>
  <text x="450" y="252" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="600">máx(1,2)+1</text>
  <text x="590" y="180" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">e · envia</text>
  <circle cx="590" cy="210" r="17" fill="#12437f"/><text x="590" y="216" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">4</text>
  <text x="520" y="300" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">f</text>
  <circle cx="520" cy="330" r="17" fill="#12437f"/><text x="520" y="336" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">1</text>
  <text x="720" y="300" text-anchor="middle" fill="#334155" font-size="14" font-weight="700">g · recebe</text>
  <circle cx="720" cy="330" r="17" fill="#12437f"/><text x="720" y="336" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">5</text>
  <text x="720" y="372" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="600">máx(1,4)+1</text>
</svg>

<div class="dica">💡 <strong>Círculo azul</strong> = um evento (o número dentro é o <strong>relógio de Lamport</strong>). <strong>Seta laranja</strong> = mensagem, que leva o <strong>carimbo</strong> junto. Nos recebimentos (<strong>d</strong>, <strong>g</strong>): <strong>máximo + 1</strong>.</div>

---

## Exemplo — o contador de Lamport passo a passo

| evento | processo | o que acontece | cálculo | **Lamport** |
|--|--|--|--|--|
| a | P1 | evento local | 0 + 1 | **1** |
| b | P1 | **envia** m1 (carimbo 2) | 1 + 1 | **2** |
| c | P2 | evento local | 0 + 1 | **1** |
| d | P2 | **recebe** m1 (carimbo 2) | **máx(1, 2) + 1** | **3** |
| e | P2 | **envia** m2 (carimbo 4) | 3 + 1 | **4** |
| f | P3 | evento local | 0 + 1 | **1** |
| g | P3 | **recebe** m2 (carimbo 4) | **máx(1, 4) + 1** | **5** |

<div class="dica">💡 Olhe a linha <strong>d</strong>: o carimbo (2) "puxou" o relógio de P2 para frente. É o <strong>máximo + 1</strong> em ação.</div>

---

## A garantia — e a pegadinha

- **Garantia:** se **A → B** (A causou B), então **Lamport(A) < Lamport(B)**. A causa **sempre** tem número menor que o efeito. ✅
- **Pegadinha:** a recíproca **NÃO vale**. Um número menor **não prova** que houve causa.

<div class="aviso">⚠️ Veja na tabela: <strong>c</strong> (P2, Lamport 1) e <strong>a</strong> (P1, Lamport 1) têm o <strong>mesmo</strong> número, mas são <strong>concorrentes</strong>. E <strong>f</strong> (1) &lt; <strong>b</strong> (2) sem que um tenha causado o outro. Lamport <strong>ordena</strong>, mas <strong>não distingue</strong> concorrência.</div>

---

## Relógio vetorial — quem sabe o quê

Para **ter certeza** se dois eventos são causais ou **concorrentes**, cada processo guarda um **vetor**: um contador **para cada processo**.

- **Local/envio:** +1 na **sua** posição.
- **Recebimento:** pega o **máximo posição a posição** com o vetor recebido, depois +1 na sua posição.

<div class="dica">💡 Em vez de "um número", cada evento carrega "o que <strong>cada</strong> processo já tinha visto". Isso é o suficiente para detectar concorrência.</div>

---

## Vetorial — os 3 casos (comparando posição a posição)

Com os vetores da nossa execução:

| par | vetores | veredito |
|--|--|--|
| **d → g** | `[2,2,0]` ≤ `[2,3,2]` | **causal** (d causou g) |
| **c ‖ f** | `[0,1,0]` vs `[0,0,1]` | **concorrentes** (nenhum ≤ o outro) |

- Se um vetor é **≤ o outro em todas as posições** → um **causou** o outro.
- Se **cada um é maior em alguma posição** (nenhum domina) → **concorrentes**.

<div class="aviso">📌 Detectar concorrência é a base para achar <strong>conflitos entre réplicas</strong> — quando duas cópias são escritas ao mesmo tempo (próxima aula, CAP).</div>

---

<!-- _class: secao -->

# Laboratório
### Simular a ordenação — e achar o par concorrente

---

## Lab · Passo 1 — a simulação (`lamport_sim.py`)

Descrevemos a **ordem real** dos eventos; o programa aplica as regras:

```python
for proc, tipo, rotulo, msg in execucao:      # execucao = lista de eventos
    if tipo in ("local", "send"):
        lamport[proc] += 1                     # +1
        if tipo == "send":
            carimbo_l[msg] = lamport[proc]     # manda o relógio junto
    else:  # recv
        lamport[proc] = max(lamport[proc], carimbo_l[msg]) + 1   # MÁXIMO + 1
    eventos.append((rotulo, proc, lamport[proc]))
```

<div class="dica">💡 O arquivo completo (<code>exemplos/aula09/lamport_sim.py</code>) faz também o <strong>vetorial</strong> e lista os pares concorrentes.</div>

---

## Lab · Passo 2 — rodar e ler a saída

```powershell
python lamport_sim.py
# evento proc  Lamport  vetor
# a      P1    1        [1, 0, 0]
# c      P2    1        [0, 1, 0]
# d      P2    3        [2, 2, 0]
# ...
# Pares concorrentes (nem um causou o outro):
#   c(P2)  ||  f(P3)      <- dois eventos locais que nunca se falaram
```

<div class="dica">💡 Experimente: <strong>adicione um processo P4</strong> e uma mensagem nova, rode de novo e veja quais pares viram concorrentes.</div>

---

## No seu trabalho — C2.A2

- No RAG, o **serviço de recuperação** compara a pergunta com os documentos por **similaridade** (conteúdo).
- A teoria de hoje reforça um cuidado: a recuperação deve depender do **conteúdo**, **não** da **hora** de cada máquina.

<div class="dica">💡 Puxa para o kit: <strong>TAREFA 2</strong> — busca por similaridade no serviço de recuperação. Repositório: <code>sd-2026-2-kit-c2a2</code>.</div>

---

## Atividade para casa

1. **Amplie a simulação** para **4 processos** e pelo menos **3 mensagens** trocadas.
2. **Explique por escrito** (5 linhas): escolha **um par causal** e **um par concorrente** da sua execução e justifique **pelos vetores**.
3. **Avance o C2.A2:** ponha o **serviço de recuperação** (busca por similaridade) no ar.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> <code>lamport_sim.py</code> com 4 processos + a explicação escrita + o serviço de recuperação iniciado.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Sincronização de relógios físicos e **desvio (clock drift)**.
- Relógio de **Lamport** e relação **"aconteceu antes"**.
- **Relógios vetoriais** e detecção de **concorrência**.
- Ordenação de eventos e **exclusão mútua distribuída**.

**Termos-chave:** Relógio lógico · Lamport · Relógio vetorial · Causalidade · Eventos concorrentes · Clock drift

<div class="dica">💡 Quase certo na prova: <strong>calcular</strong> um Lamport após um recebimento (máximo + 1) e <strong>classificar</strong> dois eventos (causal × concorrente) por vetores.</div>

---

## Questão de autoavaliação (estilo ENADE)

No processo **P1**, um evento leva seu relógio de Lamport a **3**. P1 envia uma mensagem a **P2** com o carimbo **3**. No recebimento, o relógio de **P2** valia **7**. Após o recebimento, o relógio de P2 passa a valer:

A) 3
B) 7
C) **8**
D) 10
E) 4

---

## Resolução — alternativa **C**

- Regra do **recebimento**: **máximo**(relógio local, carimbo) **+ 1**.
- **máx(7, 3) + 1 = 8.**
- Cai em quem esquece o "**+1**" (marca 7) ou quem **soma** tudo (marca 10).

<div class="dica">💡 É a linha <strong>d</strong> da nossa tabela, com outros números: máx(local, carimbo) + 1.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 14 — Tempo e estados globais.
- O artigo clássico de **Lamport** (1978) — leitura opcional.
- Rode o `lamport_sim.py` mudando a **ordem** dos eventos e observe.

</div>

<div>

**Glossário**
- **Relógio lógico:** contador que ordena eventos sem depender da hora real.
- **Lamport:** um contador por processo (máximo + 1).
- **Relógio vetorial:** um vetor de contadores; detecta concorrência.
- **Causalidade:** um evento influenciou o outro.
- **Concorrentes:** sem relação de causa entre si.
- **Clock drift:** desvio entre relógios físicos.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Amplie a simulação (4 processos) e avance o serviço de recuperação.

**Próxima (Aula 10):** **Replicação, consistência e o teorema CAP** — quando duas cópias divergem, o que a concorrência de hoje ajuda a detectar.

<a class="proximo" href="aula-08-mensageria-eventos-gateway.html">← Anterior<small>Aula 8 · Mensageria/fila</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
