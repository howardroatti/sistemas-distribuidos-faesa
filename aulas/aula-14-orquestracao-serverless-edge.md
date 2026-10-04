---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 14 — Orquestração, serverless e computação na borda

C3 · Nuvem, implantação e segurança · 12/11/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C3

<div class="cols">

<div>

**C1** (1–7) ✅ · **C2** (8–12) ✅

**C3 · Nuvem, implantação e segurança** (13–18)
Nuvem/containers ✅ · **orquestração/serverless** · observabilidade · segurança.

</div>

<div>

<div class="dica">📍 <strong>Aula 14</strong>. Você já tem containers soltos; hoje eles viram um <strong>sistema</strong> que sobe com <strong>um comando</strong>.</div>

</div>

</div>

<div class="aviso">🧩 Três ideias: <strong>orquestração</strong> (coordenar vários containers), <strong>serverless</strong> (entregar só a função) e <strong>borda</strong> (processar perto do usuário).</div>

---

## Retomada

<div class="dica">🔄 Você publicou o serviço (URL pública) e conteinerizou os serviços do C3.A2?</div>

- Cada serviço tem seu container — mas subir **4 containers na mão**, na ordem certa, com a rede certa, é **inviável**.
- Hoje: **um comando** sobe a stack inteira, e vemos alternativas (**serverless**, **borda**) para partes do sistema.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Orquestrar** múltiplos containers com **docker-compose** (subir e **escalar** com um comando).
2. **Explicar** o modelo **serverless (FaaS)** e seu preço (**cold start**, limites, sem estado).
3. **Reconhecer** quando a **computação na borda (edge)** reduz latência.

---

## Orquestração: containers isolados não são um sistema

Um serviço precisa **achar** o outro, subir na **ordem** certa, compartilhar uma **rede**. O **docker-compose** descreve tudo num arquivo e sobe com **um comando**.

<svg viewBox="0 0 860 220" role="img" style="width:100%;max-width:840px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="o1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#64748b"/></marker></defs>
  <rect x="40" y="70" width="210" height="80" rx="10" fill="#0d2b57"/>
  <text x="145" y="98" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">docker-compose.yml</text>
  <text x="145" y="118" text-anchor="middle" fill="#cfe0f5" font-size="11">descreve a stack</text>
  <text x="145" y="135" text-anchor="middle" fill="#cfe0f5" font-size="11" font-family="Consolas,monospace">docker compose up</text>
  <line x1="250" y1="110" x2="320" y2="110" stroke="#64748b" stroke-width="2" marker-end="url(#o1)"/>
  <rect x="330" y="30" width="180" height="46" rx="9" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="420" y="50" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">gateway</text>
  <text x="420" y="66" text-anchor="middle" fill="#166534" font-size="10.5">porta 8000 (pública)</text>
  <rect x="330" y="92" width="180" height="46" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="420" y="112" text-anchor="middle" fill="#0d2b57" font-size="12.5" font-weight="700">inferência</text>
  <text x="420" y="128" text-anchor="middle" fill="#64748b" font-size="10.5">interna</text>
  <rect x="330" y="154" width="180" height="40" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="420" y="178" text-anchor="middle" fill="#0d2b57" font-size="12.5" font-weight="700">fila / banco</text>
  <rect x="560" y="60" width="260" height="110" rx="10" fill="none" stroke="#94a3b8" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="690" y="52" text-anchor="middle" fill="#64748b" font-size="11.5" font-weight="700">rede interna do compose</text>
  <text x="690" y="98" text-anchor="middle" fill="#334155" font-size="11.5">serviços se acham</text>
  <text x="690" y="116" text-anchor="middle" fill="#334155" font-size="11.5">pelo <tspan font-weight="700">nome</tspan> (DNS interno)</text>
  <text x="690" y="140" text-anchor="middle" fill="#334155" font-size="11.5">só o gateway é exposto</text>
  <line x1="510" y1="110" x2="558" y2="110" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3"/>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> o compose é a <strong>planta do condomínio</strong>: diz quais prédios existem, como se ligam e quem tem portão para a rua. Um comando ergue tudo.</div>

---

## Escalar com um comando

- Precisa de mais capacidade num serviço? **`docker compose up --scale inferencia=3`** → 3 réplicas.
- O gateway distribui entre elas; você **vê** réplicas diferentes respondendo (o `host` muda).
- Em **produção**, o orquestrador padrão é o **Kubernetes**: faz isso em **vários servidores**, reinicia o que cai e escala sozinho (noção — não é foco da disciplina).

<div class="aviso">📌 Orquestração resolve o "como rodar <strong>muitos</strong> containers juntos, de forma confiável". Compose no laboratório; Kubernetes no mundo de produção.</div>

---

## Serverless (FaaS): você entrega a função

Você **não** gerencia servidor: envia **uma função**, e a plataforma a **executa sob demanda**, criando **uma instância por requisição** e **escalando a zero** quando ociosa.

<svg viewBox="0 0 820 190" role="img" style="width:100%;max-width:800px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="s1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#64748b"/></marker></defs>
  <text x="90" y="60" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">requisições</text>
  <circle cx="60" cy="90" r="9" fill="#12437f"/><circle cx="90" cy="90" r="9" fill="#12437f"/><circle cx="120" cy="90" r="9" fill="#12437f"/>
  <line x1="140" y1="90" x2="250" y2="90" stroke="#64748b" stroke-width="2" marker-end="url(#s1)"/>
  <rect x="260" y="40" width="250" height="110" rx="12" fill="#f3effe" stroke="#7c3aed" stroke-width="2"/>
  <text x="385" y="64" text-anchor="middle" fill="#5b21b6" font-size="13" font-weight="700">plataforma serverless</text>
  <rect x="285" y="78" width="60" height="30" rx="6" fill="#ede9fe" stroke="#7c3aed"/><text x="315" y="98" text-anchor="middle" fill="#5b21b6" font-size="11">f()</text>
  <rect x="355" y="78" width="60" height="30" rx="6" fill="#ede9fe" stroke="#7c3aed"/><text x="385" y="98" text-anchor="middle" fill="#5b21b6" font-size="11">f()</text>
  <rect x="425" y="78" width="60" height="30" rx="6" fill="#ede9fe" stroke="#7c3aed"/><text x="455" y="98" text-anchor="middle" fill="#5b21b6" font-size="11">f()</text>
  <text x="385" y="130" text-anchor="middle" fill="#6b21a8" font-size="11">cria 1 instância por requisição</text>
  <line x1="510" y1="90" x2="620" y2="90" stroke="#64748b" stroke-width="2" marker-end="url(#s1)"/>
  <rect x="630" y="66" width="150" height="48" rx="9" fill="#e5e7eb" stroke="#94a3b8"/>
  <text x="705" y="86" text-anchor="middle" fill="#334155" font-size="12" font-weight="700">ocioso</text>
  <text x="705" y="103" text-anchor="middle" fill="#475569" font-size="11">escala a 0 · custo 0</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é a <strong>luz com sensor de presença</strong> — acende quando alguém chega, apaga sozinha. Você paga só os segundos que a função rodou.</div>

---

## O preço do serverless

- **Cold start:** se a função estava "apagada", a **1ª** invocação demora mais (subir o ambiente). Já vimos esse nome na Aula 6.
- **Limites:** tempo máximo de execução, memória e tamanho — **não** serve para tarefas longas.
- **Sem estado:** cada invocação é **independente**; guarde estado **fora** (banco, fila, cache).

<div class="aviso">⚠️ Serverless brilha em cargas <strong>esporádicas</strong> e <strong>curtas</strong> (um webhook, um redimensionar imagem). Para um serviço <strong>sempre quente</strong> e de alto volume, um container dedicado costuma sair melhor.</div>

---

## Computação na borda (edge)

Em vez de ir até um datacenter **distante**, parte do processamento acontece **perto do usuário** (CDN, pontos de presença, dispositivos IoT).

<svg viewBox="0 0 820 160" role="img" style="width:100%;max-width:780px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="ed" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker><marker id="ed2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#dc2626"/></marker></defs>
  <circle cx="70" cy="80" r="22" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="70" y="85" text-anchor="middle" font-size="16">👤</text>
  <text x="70" y="120" text-anchor="middle" fill="#334155" font-size="11">usuário</text>
  <rect x="200" y="56" width="140" height="48" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="270" y="78" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">borda (perto)</text>
  <text x="270" y="95" text-anchor="middle" fill="#166534" font-size="10.5">latência baixa</text>
  <rect x="610" y="56" width="160" height="48" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="690" y="78" text-anchor="middle" fill="#0d2b57" font-size="12.5" font-weight="700">origem (datacenter)</text>
  <text x="690" y="95" text-anchor="middle" fill="#64748b" font-size="10.5">longe</text>
  <line x1="92" y1="80" x2="196" y2="80" stroke="#16a34a" stroke-width="2.5" marker-end="url(#ed)"/>
  <text x="144" y="50" text-anchor="middle" fill="#166534" font-size="11" font-weight="700">curto</text>
  <line x1="92" y1="104" x2="606" y2="104" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ed2)"/>
  <text x="430" y="128" text-anchor="middle" fill="#991b1b" font-size="11" font-weight="700">longo (só quando necessário)</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é a <strong>farmácia do bairro</strong> em vez do <strong>centro de distribuição</strong>: o que é comum fica pertinho (rápido); o resto vem de longe só quando preciso.</div>

---

<!-- _class: secao -->

# Laboratório
### Subir a stack com um comando + publicar uma função serverless

---

## Mão na massa — siga o Guia do Laboratório

Hoje são **4 missões**: subir a stack com **um comando**, **escalar** um serviço, **publicar uma função serverless** (com 3 medições de tempo) e **compor a stack do C3.A2**.

### 👉 [Abrir o Guia do Laboratório »](lab-14-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 14 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Exemplo pronto e testado: <code>exemplos/aula14/</code> — <code>gateway/</code> + <code>inferencia/</code> + <code>docker-compose.yml</code> (stack) e <code>funcao/handler.py</code> (serverless).</div>

---

## O que o exemplo mostra (aquecimento)

```powershell
docker compose up --build            # sobe gateway + inferencia juntos
curl -X POST localhost:8000/infer -d "{\"texto\":\"gostei, otimo\"}"
# {"via":"gateway","resultado":{"sentimento":"positivo","host":"<id-do-container>"}}
docker compose up --scale inferencia=3   # 3 replicas; o "host" varia nas respostas

python funcao/handler.py             # a funcao serverless, rodando "sob demanda"
```

<div class="dica">💡 O gateway acha a inferência pelo <strong>nome do serviço</strong> (<code>http://inferencia:8000</code>) na rede do compose — sem IP fixo.</div>

---

## No seu trabalho — C3.A2

- **Componha** a stack inteira do projeto num **`docker-compose.yml`**: gateway + inferência + worker + armazenamento vetorial, subindo com **um comando**.
- **Integre a borda:** identifique uma parte que ganharia com **edge/serverless** (ex.: um pré-processamento curto ou um webhook) e descreva/implemente.

<div class="dica">💡 Puxa para o kit: só o <strong>gateway</strong> expõe porta; os demais são internos e se acham pelo nome. É o padrão de hoje aplicado ao seu projeto.</div>

---

## Atividade para casa

1. **Componha** o `docker-compose.yml` do **C3.A2** e suba o projeto **inteiro com um comando**.
2. **Publique** uma **função serverless** (um componente simples do projeto) e registre **3 medições** de tempo de resposta (incluindo a **1ª**, para ver o cold start).
3. **Integre** o componente serverless/edge ao fluxo do projeto.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> o projeto subindo com um comando + a função serverless publicada com as **3 medições**. Roteiro no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Orquestração** (compose/Kubernetes): coordenar e **escalar** containers.
- **Serverless/FaaS:** sob demanda, escala a zero, **cold start**, **sem estado**.
- Quando usar serverless × container dedicado (esporádico/curto × sempre quente).
- **Edge computing:** processar perto do usuário para **reduzir latência**.

**Termos-chave:** Orquestração · docker-compose · Kubernetes · Serverless/FaaS · Cold start · Edge

<div class="dica">💡 Pegadinha: serverless "nunca tem custo de latência". Tem: o <strong>cold start</strong> da 1ª invocação após ociosidade.</div>

---

## Questão de autoavaliação (estilo ENADE)

Uma função **serverless** que ficou **ociosa** recebe uma requisição e demora bem mais para responder **nessa primeira** chamada; as seguintes são rápidas. Esse atraso inicial é explicado por:

A) uma falha de rede intermitente
B) **o cold start: a plataforma precisa inicializar o ambiente da função antes de executá-la**
C) o fato de funções serverless serem sempre lentas
D) a ausência de internet no datacenter
E) um erro de idempotência

---

## Resolução — alternativa **B**

- **Cold start:** quando a função está "apagada" (escalou a zero), a plataforma **sobe o ambiente** antes de rodar → a 1ª chamada paga esse custo.
- As seguintes reaproveitam a instância "quente" → rápidas. Não é rede (A/D) nem idempotência (E).

<div class="dica">💡 Mesmo conceito da Aula 6 (carregar o modelo). Serverless troca custo de servidor ocioso por cold start ocasional.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- Docs do **Docker Compose** e, por curiosidade, do **Kubernetes** (conceitos).
- Docs de **AWS Lambda** / **Cloud Functions** (o que é um handler).
- Rode o exemplo com `--scale` e veja o `host` variar.

</div>

<div>

**Glossário**
- **Orquestração:** coordenar vários containers como um sistema.
- **docker-compose:** descreve e sobe a stack local.
- **Kubernetes:** orquestrador de produção (vários servidores).
- **Serverless/FaaS:** você entrega a função; a plataforma executa sob demanda.
- **Cold start:** atraso da 1ª invocação após ociosidade.
- **Edge:** processar perto do usuário.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Suba o C3.A2 com um comando e publique a função serverless (3 medições).

**Próxima (Aula 15):** **Observabilidade** — quando algo fica lento numa stack de vários serviços, como **enxergar** onde está o gargalo (logs, métricas e **tracing**).

<a class="proximo" href="aula-13-nuvem-containers-deploy.html">← Anterior<small>Aula 13 · Nuvem/containers</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
