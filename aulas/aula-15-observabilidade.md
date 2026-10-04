---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 15 — Observabilidade: enxergar o que acontece no sistema

C3 · Nuvem, implantação e segurança · 19/11/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C3

<div class="cols">

<div>

**C1** (1–7) ✅ · **C2** (8–12) ✅

**C3 · Nuvem, implantação e segurança** (13–18)
Nuvem ✅ · orquestração ✅ · **observabilidade** · segurança/LGPD · fechamento.

</div>

<div>

<div class="dica">📍 <strong>Aula 15</strong>. Seu sistema tem vários serviços. Quando algo fica lento ou quebra, como você <strong>enxerga</strong> onde?</div>

</div>

</div>

<div class="aviso">🔎 Com um serviço só, um <code>print</code> bastava. Com <strong>vários</strong>, você precisa de <strong>observabilidade</strong>: logs, métricas e <strong>rastreamento</strong> para ver a jornada de uma requisição.</div>

---

## Retomada

<div class="dica">🔄 Você subiu o C3.A2 com um comando e publicou a função serverless (3 medições)?</div>

- A stack tem **gateway + inferência + worker + banco**. Um usuário reclama: "**está lento**".
- **Onde** está a lentidão? No gateway? Na busca? Na chamada ao LLM? Sem instrumentação, é **adivinhação**.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Diferenciar** os **três pilares** da observabilidade: **logs**, **métricas** e **traces**.
2. **Explicar** por que o **rastreamento distribuído** é essencial em vários serviços.
3. **Instrumentar** um fluxo com **OpenTelemetry** e achar a **etapa mais lenta**.

---

## O problema: "está lento" — mas onde?

Uma requisição atravessa **vários serviços**. Se você só olha um por vez, cada um parece "ok" — e ninguém vê o conjunto.

<svg viewBox="0 0 820 160" role="img" style="width:100%;max-width:800px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="q1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#64748b"/></marker></defs>
  <circle cx="50" cy="70" r="18" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="50" y="75" text-anchor="middle" font-size="15">👤</text>
  <rect x="110" y="48" width="110" height="44" rx="9" fill="#eef4fb" stroke="#12437f"/><text x="165" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#0d2b57">gateway</text><text x="165" y="84" text-anchor="middle" font-size="10" fill="#64748b">? ms</text>
  <rect x="260" y="48" width="110" height="44" rx="9" fill="#eef4fb" stroke="#12437f"/><text x="315" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#0d2b57">recuperação</text><text x="315" y="84" text-anchor="middle" font-size="10" fill="#64748b">? ms</text>
  <rect x="410" y="48" width="110" height="44" rx="9" fill="#eef4fb" stroke="#12437f"/><text x="465" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#0d2b57">geração</text><text x="465" y="84" text-anchor="middle" font-size="10" fill="#64748b">? ms</text>
  <rect x="560" y="48" width="110" height="44" rx="9" fill="#fee2e2" stroke="#dc2626"/><text x="615" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#991b1b">LLM (API)</text><text x="615" y="84" text-anchor="middle" font-size="10" fill="#991b1b">? ms</text>
  <line x1="68" y1="70" x2="108" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#q1)"/>
  <line x1="220" y1="70" x2="258" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#q1)"/>
  <line x1="370" y1="70" x2="408" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#q1)"/>
  <line x1="520" y1="70" x2="558" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#q1)"/>
  <text x="700" y="74" fill="#991b1b" font-size="22" font-weight="700">?</text>
  <text x="410" y="128" text-anchor="middle" fill="#334155" font-size="12.5">"a resposta demora 2s" — mas <tspan font-weight="700">qual</tspan> etapa consumiu esse tempo?</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é uma <strong>encomenda que atrasou</strong> passando por vários centros de distribuição. Sem rastreio, você não sabe <strong>em qual</strong> ela ficou parada.</div>

---

## Os três pilares da observabilidade

| pilar | o que é | responde |
|--|--|--|
| **Logs** | registros de **eventos** (texto, com hora) | "**o que** aconteceu neste ponto?" |
| **Métricas** | **números agregados** no tempo (req/s, latência, erros, CPU) | "**quanto / como está** a saúde geral?" |
| **Traces** | a **jornada de UMA requisição** pelos serviços | "**onde** ela passou e **quanto** gastou em cada etapa?" |

<div class="dica">💡 <strong>Em miúdos:</strong> <strong>log</strong> = o diário ("às 10h deu erro X"); <strong>métrica</strong> = o painel do carro (velocidade, temperatura); <strong>trace</strong> = o GPS de uma viagem específica (por onde passou e quando).</div>

---

## Rastreamento distribuído: o `trace_id` costura a jornada

Cada requisição recebe um **`trace_id`** único, propagado a **todos** os serviços. Cada etapa vira um **span** (nome + início + duração). Juntando os spans pelo `trace_id`, monta-se a **linha do tempo** (waterfall).

<svg viewBox="0 0 820 180" role="img" style="width:100%;max-width:800px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <line x1="200" y1="24" x2="200" y2="160" stroke="#e2e8f0" stroke-width="1"/>
  <line x1="760" y1="24" x2="760" y2="160" stroke="#e2e8f0" stroke-width="1"/>
  <text x="200" y="18" text-anchor="middle" fill="#94a3b8" font-size="10">0 ms</text>
  <text x="760" y="18" text-anchor="middle" fill="#94a3b8" font-size="10">180 ms</text>
  <rect x="200" y="30" width="560" height="22" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="30" y="45" fill="#0d2b57" font-size="11.5" font-weight="700">gateway</text><text x="205" y="45" fill="#0d2b57" font-size="10">180 ms (total)</text>
  <rect x="215" y="58" width="78" height="20" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="30" y="72" fill="#0d2b57" font-size="11.5">recuperação</text><text x="297" y="72" fill="#64748b" font-size="10">25 ms</text>
  <rect x="230" y="80" width="62" height="18" rx="5" fill="#eff6ff" stroke="#60a5fa"/><text x="50" y="93" fill="#475569" font-size="10.5">db.embeddings</text>
  <rect x="293" y="104" width="420" height="22" rx="5" fill="#fee2e2" stroke="#dc2626"/><text x="30" y="119" fill="#991b1b" font-size="11.5" font-weight="700">geração</text><text x="298" y="119" fill="#991b1b" font-size="10">140 ms</text>
  <rect x="308" y="130" width="390" height="18" rx="5" fill="#fecaca" stroke="#dc2626"/><text x="50" y="143" fill="#991b1b" font-size="10.5">llm.api.chamada</text><text x="700" y="143" fill="#991b1b" font-size="10">130 ms ◀ gargalo</text>
</svg>

<div class="dica">💡 Na "cascata", bate o olho: a <strong>chamada ao LLM</strong> domina (130 de 180 ms). É exatamente o que o <code>tracing_demo.py</code> imprime.</div>

---

## OpenTelemetry: instrumente uma vez

**OpenTelemetry (OTel)** é o **padrão aberto** do mercado para gerar logs, métricas e traces. Você **instrumenta o código uma vez** e **exporta** para o visualizador que quiser (Jaeger, Grafana, Datadog…), sem ficar preso a um fornecedor.

- Bibliotecas prontas para **FastAPI, requests, etc.** (instrumentação quase automática).
- O **contexto** (o `trace_id`) é propagado **entre serviços** nos cabeçalhos HTTP.

<div class="dica">💡 <strong>Em miúdos:</strong> é uma <strong>tomada padrão</strong>: você liga seu código nela uma vez e pluga <strong>qualquer</strong> painel na outra ponta.</div>

---

<!-- _class: secao -->

# Laboratório
### Rastrear uma requisição de ponta a ponta e achar o gargalo

---

## Mão na massa — siga o Guia do Laboratório

Hoje são **4 missões**: entender o trace no aquecimento, **instrumentar** o fluxo com **OpenTelemetry**, **visualizar** no Jaeger e **achar o gargalo** — depois instrumentar o C3.A2.

### 👉 [Abrir o Guia do Laboratório »](lab-15-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 15 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Aquecimento pronto e testado: <code>exemplos/aula15/tracing_demo.py</code> — monta um trace de exemplo e aponta a etapa mais lenta.</div>

---

## O que o exemplo mostra (aquecimento)

```powershell
python tracing_demo.py
# - POST /pergunta (gateway)    180 ms  ##################
#   - recuperacao.buscar          25 ms  ##
#   - geracao.responder          140 ms  ##############
#     - llm.api.chamada           130 ms  #############
# Etapa mais lenta: 'llm.api.chamada' = 130 ms (72% dos 180 ms totais).
```

<div class="dica">💡 A cascata mostra <strong>onde</strong> o tempo foi gasto. No lab, você gera isso a partir de código <strong>real</strong> com OpenTelemetry.</div>

---

## No seu trabalho — C3.A2

- **Instrumente** o fluxo do RAG com **OpenTelemetry** e colete um **trace completo** de uma pergunta.
- **Identifique o gargalo** (quase sempre a **chamada ao LLM** — e é por isso que ela tem o circuit breaker da Aula 11).
- Entregue uma **imagem do rastreamento** (Jaeger/console) e uma **análise** do gargalo.

<div class="dica">💡 Puxa para o kit: comece instrumentando o <strong>gateway</strong> e a <strong>geração</strong>. Propague o contexto entre eles para o trace "costurar" os dois serviços.</div>

---

## Atividade para casa

1. **Instrumente** o **projeto inteiro** (C3.A2) com OpenTelemetry (gateway + serviços).
2. **Colete** um trace de ponta a ponta e **salve a imagem** do rastreamento.
3. **Escreva** a análise: qual é a **etapa mais lenta** e **o que** você faria para melhorá-la.

<div class="aviso">📌 <strong>Entregar até a próxima aula (EAD de Segurança):</strong> o projeto instrumentado + a imagem do rastreamento + a análise do gargalo. Roteiro no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Os **três pilares**: logs × métricas × traces (o que cada um responde).
- **Rastreamento distribuído** e o papel do **`trace_id`** / span / contexto propagado.
- **OpenTelemetry** como padrão aberto (instrumenta uma vez, exporta para vários).
- Usar o trace para **localizar o gargalo** (a etapa mais lenta).

**Termos-chave:** Observabilidade · Log · Métrica · Trace · Span · trace_id · OpenTelemetry · Gargalo

<div class="dica">💡 Pegadinha: confundir <strong>log</strong> (evento pontual) com <strong>métrica</strong> (número agregado) e com <strong>trace</strong> (jornada de uma requisição específica).</div>

---

## Questão de autoavaliação (estilo ENADE)

Uma requisição passa por **quatro** microsserviços e os usuários relatam lentidão **intermitente**. A equipe quer descobrir **em qual serviço** o tempo é gasto **em cada requisição específica**. O recurso de observabilidade mais adequado é:

A) apenas **logs** de cada serviço, lidos separadamente
B) apenas **métricas** agregadas de CPU
C) **rastreamento distribuído (traces) com um `trace_id` propagado entre os serviços**
D) aumentar o nível de log para DEBUG em produção
E) reiniciar os serviços periodicamente

---

## Resolução — alternativa **C**

- Só o **trace** liga as etapas de **uma mesma requisição** (via `trace_id`) e mostra **onde** o tempo foi gasto.
- **Logs** soltos (A) não costuram a jornada; **métricas** (B) dão o agregado, não a requisição específica; (D) e (E) não localizam o gargalo.

<div class="dica">💡 Para "onde está lento nesta requisição?", a resposta é quase sempre <strong>tracing distribuído</strong>.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- Docs do **OpenTelemetry** (conceitos: trace, span, context).
- **Jaeger** (visualizador de traces) — tutorial de 5 min.
- Rode o `tracing_demo.py` mudando as durações e veja o gargalo mudar.

</div>

<div>

**Glossário**
- **Observabilidade:** capacidade de entender o estado interno pelo que o sistema emite.
- **Log:** registro de um evento.
- **Métrica:** número agregado no tempo.
- **Trace:** jornada de uma requisição; composto de **spans**.
- **trace_id:** identificador que costura a jornada entre serviços.
- **OpenTelemetry:** padrão aberto de instrumentação.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Instrumente o C3.A2, colete um trace e analise o gargalo.

**Próxima (Aula 16 · EAD):** **Segurança, privacidade e LGPD** — proteger a plataforma (TLS, autenticação/JWT, autorização, LGPD) + **revisão para o ENADE**.

<a class="proximo" href="aula-14-orquestracao-serverless-edge.html">← Anterior<small>Aula 14 · Orquestração</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
