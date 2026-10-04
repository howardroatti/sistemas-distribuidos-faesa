---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 11 — Consenso (Raft) e resiliência

C2 · Coordenação e consistência · 22/10/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C2

<div class="cols">

<div>

**C1 · Fundamentos** (1–7) ✅

**C2 · Coordenação e consistência** (8–12)
Mensageria ✅ · relógios ✅ · CAP ✅ · **Raft + resiliência**.

</div>

<div>

**C3 · Nuvem e segurança** (13–18)

<div class="dica">📍 <strong>Aula 11</strong>. Última aula de conteúdo novo da C2 — a Aula 12 é revisão + prova.</div>

</div>

</div>

<div class="aviso">🧩 No CAP vimos que, sob partição, as réplicas <strong>divergem</strong>. Hoje a pergunta vira: como um grupo de réplicas <strong>concorda em um único valor</strong> apesar de falhas? E como <strong>blindar</strong> a parte mais frágil — a chamada de rede à IA.</div>

---

## Retomada

<div class="dica">🔄 Você rodou o experimento da partição e escreveu o <code>relatorio_cap.md</code> com as duas justificativas (CP e AP)?</div>

- CAP mostrou o **problema**: cópias que divergem.
- Hoje vem a **ferramenta** que muitos sistemas usam para o lado **C**: um **protocolo de consenso** que elege um **líder** e mantém um **log replicado** — o **Raft**.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** o problema do **consenso** e o papel da **maioria (quórum)**.
2. **Descrever** o **Raft**: eleição de líder e log replicado.
3. **Blindar** uma chamada remota com **tempo-limite, retentativa e disjuntor**, apoiada em **idempotência**.

---

## O problema do consenso

Várias réplicas, cada uma recebendo pedidos. Elas precisam **concordar em um único valor** (ou numa **ordem** única de operações) mesmo que **mensagens se percam** e **máquinas caiam**.

<svg viewBox="0 0 820 230" role="img" style="width:100%;max-width:760px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <rect x="70" y="60" width="130" height="56" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="135" y="84" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Nó 1</text>
  <text x="135" y="104" text-anchor="middle" fill="#334155" font-size="13" font-family="Consolas,monospace">propõe x=10</text>
  <rect x="345" y="60" width="130" height="56" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="410" y="84" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Nó 2</text>
  <text x="410" y="104" text-anchor="middle" fill="#334155" font-size="13" font-family="Consolas,monospace">propõe x=20</text>
  <rect x="620" y="60" width="130" height="56" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="685" y="84" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Nó 3</text>
  <text x="685" y="104" text-anchor="middle" fill="#334155" font-size="13" font-family="Consolas,monospace">propõe x=10</text>
  <rect x="250" y="160" width="320" height="46" rx="10" fill="#e7f6ec" stroke="#16a34a" stroke-width="2"/>
  <text x="410" y="182" text-anchor="middle" fill="#166534" font-size="13" font-weight="700">Consenso: TODOS decidem o MESMO valor…</text>
  <text x="410" y="199" text-anchor="middle" fill="#166534" font-size="12">…e o valor decidido foi realmente proposto por alguém.</text>
  <line x1="135" y1="116" x2="360" y2="160" stroke="#94a3b8" stroke-width="1.6"/>
  <line x1="410" y1="116" x2="410" y2="160" stroke="#94a3b8" stroke-width="1.6"/>
  <line x1="685" y1="116" x2="460" y2="160" stroke="#94a3b8" stroke-width="1.6"/>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é um grupo decidindo onde almoçar por <strong>voto</strong>. Não precisa de unanimidade — basta a <strong>maioria</strong> fechar, e ninguém pode "trocar o voto" depois de combinado.</div>

---

## Raft em uma ideia: um líder manda

Em vez de todos discutirem entre si (difícil), o Raft **elege um líder**. O líder recebe as escritas, **ordena** e **replica** para os seguidores. Se o líder cair, os seguidores **elegem outro**.

- Simplifica: só o **líder** decide a ordem → todos seguem a **mesma** sequência.
- Tudo gira em torno de **mandatos** (*terms*): cada eleição abre um mandato numerado.

<div class="aviso">⚠️ A peça-chave é a <strong>maioria (quórum = N/2 + 1)</strong>: eleger líder e confirmar uma escrita exigem maioria. Com 5 nós, a maioria é <strong>3</strong>.</div>

---

## Raft · Eleição de líder (por maioria)

<svg viewBox="0 0 820 250" role="img" style="width:100%;max-width:780px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="v" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker></defs>
  <circle cx="410" cy="60" r="34" fill="#12437f"/>
  <text x="410" y="56" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">Nó 1</text>
  <text x="410" y="72" text-anchor="middle" fill="#cfe0f5" font-size="11">candidato</text>
  <text x="410" y="22" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">mandato 1 · "me elejam"</text>
  <g font-size="12">
    <rect x="70" y="170" width="120" height="48" rx="9" fill="#e7f6ec" stroke="#16a34a" stroke-width="1.6"/>
    <text x="130" y="190" text-anchor="middle" fill="#166534" font-weight="700">Nó 2</text>
    <text x="130" y="207" text-anchor="middle" fill="#166534">voto ✓</text>
    <rect x="230" y="170" width="120" height="48" rx="9" fill="#e7f6ec" stroke="#16a34a" stroke-width="1.6"/>
    <text x="290" y="190" text-anchor="middle" fill="#166534" font-weight="700">Nó 3</text>
    <text x="290" y="207" text-anchor="middle" fill="#166534">voto ✓</text>
    <rect x="470" y="170" width="120" height="48" rx="9" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.6"/>
    <text x="530" y="190" text-anchor="middle" fill="#334155" font-weight="700">Nó 4</text>
    <text x="530" y="207" text-anchor="middle" fill="#64748b">—</text>
    <rect x="630" y="170" width="120" height="48" rx="9" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.6"/>
    <text x="690" y="190" text-anchor="middle" fill="#334155" font-weight="700">Nó 5</text>
    <text x="690" y="207" text-anchor="middle" fill="#64748b">—</text>
  </g>
  <line x1="390" y1="88" x2="150" y2="168" stroke="#16a34a" stroke-width="2" marker-end="url(#v)"/>
  <line x1="405" y1="94" x2="300" y2="168" stroke="#16a34a" stroke-width="2" marker-end="url(#v)"/>
  <rect x="300" y="110" width="220" height="30" rx="8" fill="#e7f6ec" stroke="#16a34a" stroke-width="1.6"/>
  <text x="410" y="130" text-anchor="middle" fill="#166534" font-size="12.5" font-weight="700">3 votos (ele + 2) ≥ maioria → LÍDER</text>
</svg>

<div class="dica">💡 Cada nó vota <strong>uma vez por mandato</strong>. Quem junta a <strong>maioria</strong> vira líder. Empatou/ninguém fez maioria? Abre-se um <strong>novo mandato</strong> e tenta de novo.</div>

---

## Raft · Log replicado (commit por maioria)

O líder anexa a entrada ao seu **log** e manda aos seguidores. A entrada é **comitada** (vale de verdade) quando a **maioria** gravou.

| passo | o que acontece |
|--|--|
| 1 | líder recebe `x=10`, grava no próprio log |
| 2 | envia a entrada aos seguidores |
| 3 | **maioria** confirma a gravação |
| 4 | líder marca **COMITADA** e avisa o cliente |

<div class="aviso">📌 Ligando ao <strong>CAP</strong>: exigir <strong>maioria</strong> é o preço da <strong>consistência (C)</strong>. Se a rede particiona e um lado fica <strong>sem maioria</strong>, esse lado <strong>para</strong> de aceitar escritas (abre mão de <strong>A</strong>) — Raft é um sistema <strong>CP</strong>.</div>

---

## Quando o líder cai

- Os seguidores param de receber o "sinal de vida" do líder → suspeitam da queda.
- Um deles vira **candidato**, abre um **mandato novo** (número maior) e pede votos.
- Com a **maioria**, assume e o sistema **continua** — as entradas já comitadas **permanecem**.

<div class="dica">💡 É o que o <code>raft_sim.py</code> mostra: o Nó 1 cai, o Nó 2 abre o mandato 2, junta maioria e a vida segue — sem perder o <code>x=10</code> que já tinha sido comitado.</div>

---

## A outra metade: resiliência da chamada de IA

A chamada ao serviço de IA (ou a qualquer serviço remoto) é o ponto **mais frágil**: a rede atrasa, o serviço cai, a resposta se perde. Três defesas:

- **Tempo-limite (timeout):** não espere para sempre — desista após X e trate como falha.
- **Retentativa (retry):** tente de novo algumas vezes (idealmente com **espera crescente**).
- **Disjuntor (circuit breaker):** se o serviço está claramente fora, **pare de insistir** por um tempo.

<div class="dica">💡 Sem timeout, uma única chamada travada pode <strong>prender</strong> um worker para sempre. Sem disjuntor, mil retentativas <strong>afundam</strong> um serviço que já está mal.</div>

---

## O disjuntor (circuit breaker) — 3 estados

<svg viewBox="0 0 820 230" role="img" style="width:100%;max-width:800px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#64748b"/></marker></defs>
  <rect x="60" y="86" width="170" height="58" rx="12" fill="#e7f6ec" stroke="#16a34a" stroke-width="2"/>
  <text x="145" y="110" text-anchor="middle" fill="#166534" font-size="15" font-weight="700">FECHADO</text>
  <text x="145" y="130" text-anchor="middle" fill="#166534" font-size="12">deixa passar</text>
  <rect x="590" y="86" width="170" height="58" rx="12" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="675" y="110" text-anchor="middle" fill="#991b1b" font-size="15" font-weight="700">ABERTO</text>
  <text x="675" y="130" text-anchor="middle" fill="#991b1b" font-size="12">falha rápido</text>
  <rect x="325" y="10" width="170" height="56" rx="12" fill="#fff8e1" stroke="#e08a00" stroke-width="2"/>
  <text x="410" y="33" text-anchor="middle" fill="#a56a00" font-size="15" font-weight="700">MEIA-VOLTA</text>
  <text x="410" y="51" text-anchor="middle" fill="#a56a00" font-size="12">deixa 1 sondar</text>
  <line x1="230" y1="108" x2="588" y2="108" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
  <text x="409" y="100" text-anchor="middle" fill="#991b1b" font-size="12" font-weight="700">N falhas seguidas</text>
  <line x1="620" y1="86" x2="470" y2="44" stroke="#64748b" stroke-width="2" marker-end="url(#a)"/>
  <text x="560" y="52" text-anchor="middle" fill="#a56a00" font-size="12" font-weight="700">após descanso</text>
  <line x1="360" y1="60" x2="190" y2="88" stroke="#16a34a" stroke-width="2" marker-end="url(#a)"/>
  <text x="250" y="60" text-anchor="middle" fill="#166534" font-size="12" font-weight="700">sondagem OK</text>
  <line x1="470" y1="62" x2="640" y2="88" stroke="#dc2626" stroke-width="2" marker-end="url(#a)"/>
  <text x="585" y="78" text-anchor="middle" fill="#991b1b" font-size="12" font-weight="700">sondagem falha</text>
  <text x="410" y="200" text-anchor="middle" fill="#334155" font-size="12.5">Fechado → (N falhas) → Aberto → (descanso) → Meia-volta → (OK) → Fechado</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é o <strong>disjuntor do quadro de luz</strong>. Deu curto demais, ele desarma (abre) para não queimar a casa. Depois você religa com cuidado (meia-volta) e, se estiver tudo bem, deixa ligado (fechado).</div>

---

## Idempotência: a garantia que permite retentar

- **Retentar** é seguro **só** se repetir a operação **não duplica efeito**. Isso é **idempotência** (visto na Aula 5).
- `GET`, `PUT` e `DELETE` são idempotentes; um `POST` de criação **não** é.
- Truque comum: dar à requisição uma **chave de idempotência** (um id único) para o servidor **ignorar** uma repetição.

<div class="aviso">⚠️ Retentativa <strong>sem</strong> idempotência = cobrar o cartão <strong>duas vezes</strong>. Antes de pôr retry, pergunte: "repetir isso faz mal?".</div>

---

<!-- _class: secao -->

# Laboratório
### Ver o Raft acontecer e blindar a chamada de IA

---

## Mão na massa — siga o Guia do Laboratório

Hoje são **4 missões**: ver a **eleição de líder** e o **log replicado** na simulação; **blindar** uma chamada com timeout + retentativa + disjuntor; e **concluir o C2.A2**.

### 👉 [Abrir o Guia do Laboratório »](lab-11-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 11 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Aquecimentos prontos e testados: <code>exemplos/aula11/raft_sim.py</code> (eleição + log) e <code>exemplos/aula11/resiliencia.py</code> (timeout + retry + disjuntor).</div>

---

## O que as simulações mostram (aquecimento)

```powershell
python raft_sim.py        # Nó 1 cai -> Nó 2 abre mandato 2 -> maioria -> segue
# => 'x=10' COMITADA (maioria)   ... depois ...   No 2 eleito LIDER (mandato 2)

python resiliencia.py     # disjuntor em acao
# [t2] FALHOU ... | disjuntor=aberto (falhas=3)
# [t3] disjuntor ABERTO -> falha rapido (nem chama o servico)
# [t4] descanso terminou -> MEIA-VOLTA -> OK -> disjuntor=fechado
```

<div class="dica">💡 Os dois pilares da aula, rodando: <strong>maioria</strong> (consenso) e <strong>falhar rápido</strong> (resiliência).</div>

---

## No seu trabalho — C2.A2

- O **serviço de geração** do RAG chama um **LLM por API** — a parte mais sujeita a lentidão e falha.
- O **núcleo do trabalho** pede um **circuit breaker** nessa chamada: timeout + retentativa + disjuntor, exatamente o de hoje.

<div class="dica">💡 Puxa para o kit: proteja a chamada ao LLM com o padrão do <code>resiliencia.py</code>. Garanta que a operação é <strong>idempotente</strong> (ou use uma chave) antes de retentar.</div>

---

## Atividade para casa

1. **Rode** `raft_sim.py` e `resiliencia.py` e **responda** ao roteiro do Guia (eleição, maioria, estados do disjuntor).
2. **Blinde** a chamada ao LLM no C2.A2 com **timeout + retentativa + disjuntor**.
3. **Conclua o C2.A2:** RAG distribuído (ingestão, recuperação, geração) **funcionando de ponta a ponta**.

<div class="aviso">📌 <strong>Entregar até a próxima aula (que é a prova C2.A1):</strong> o RAG completo com a chamada ao LLM protegida. Roteiro completo no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Consenso** e **quórum/maioria**; eleição de líder e log replicado (**Raft**).
- Relação **Raft ↔ CAP** (exigir maioria = lado **CP**).
- **Resiliência:** timeout, retentativa (com backoff), **disjuntor** e seus estados.
- **Idempotência** como pré-condição da retentativa segura.

**Termos-chave:** Consenso · Quórum · Raft · Líder · Log replicado · Timeout · Retry · Circuit breaker · Idempotência

<div class="dica">💡 Pegadinha: "pôr retry resolve". Só resolve se a operação for <strong>idempotente</strong> — senão, duplica efeito.</div>

---

## Questão de autoavaliação (estilo ENADE)

Em um sistema que usa **Raft** com **5 réplicas**, uma **partição** separa o grupo em **3 nós de um lado** e **2 do outro**. Sobre a aceitação de **novas escritas** durante a partição, é correto afirmar que:

A) nenhum lado aceita escritas, pois Raft exige unanimidade
B) ambos os lados aceitam, cada um com seu líder
C) **apenas o lado com 3 nós aceita, pois só ele forma maioria (3 de 5)**
D) apenas o lado com 2 nós, por ter menos conflito
E) os dois lados param até um administrador intervir

---

## Resolução — alternativa **C**

- Raft comita por **maioria** = `5/2 + 1 = 3`.
- O lado com **3 nós** forma maioria → **elege líder e aceita** escritas.
- O lado com **2 nós** **não** alcança maioria → fica **indisponível** para escrita (preserva **C**, abre mão de **A** → **CP**).

<div class="dica">💡 É o elo Raft ↔ CAP: a maioria garante um único líder e evita divergência — ao custo de indisponibilizar a minoria.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 15 — Coordenação e acordo.
- *The Raft Paper* (Ongaro & Ousterhout) e a animação **thesecretlivesofdata.com/raft**.
- Rode `resiliencia.py` mudando o roteiro: provoque o disjuntor a reabrir.

</div>

<div>

**Glossário**
- **Consenso:** acordar um único valor apesar de falhas.
- **Quórum:** maioria necessária (N/2 + 1).
- **Raft:** consenso por líder + log replicado.
- **Timeout:** limite de espera de uma chamada.
- **Disjuntor:** corta chamadas a um serviço que falha muito.
- **Idempotência:** repetir não muda o efeito final.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Conclua o C2.A2 (RAG completo, chamada ao LLM protegida) — a próxima é a **prova C2.A1**.

**Próxima (Aula 12):** **Revisão e Avaliação C2.A1** — o caminho da C2 (mensageria → relógios → CAP → Raft) e as 6 perguntas que você precisa saber responder.

<a class="proximo" href="aula-10-replicacao-consistencia-cap.html">← Anterior<small>Aula 10 · CAP</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
