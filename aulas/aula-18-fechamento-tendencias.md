---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 18 — Fechamento: retrospectiva e tendências

C3 · Encerramento do semestre · 03/12/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Chegamos ao fim

Hoje não há conteúdo novo nem entrega avaliativa — é dia de **olhar para trás** e **para frente**:

1. **O que você construiu** ao longo do semestre.
2. **As grandes ideias** que ficam.
3. **Para onde a área está indo** — e **o que fazer depois** desta disciplina.

<div class="dica">💡 Pós-ENADE: respire. Você percorreu um caminho longo — vale ver o tamanho dele.</div>

---

## O que você construiu

Um mesmo fio condutor — **um serviço de IA** — cresceu, aula a aula, de um **socket** a uma **plataforma cloud-native**:

<svg viewBox="0 0 860 170" role="img" style="width:100%;max-width:850px;display:block;margin:8px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="tb" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto"><path d="M0,0 L8,3.5 L0,7 Z" fill="#12437f"/></marker></defs>
  <rect x="30" y="54" width="150" height="62" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="105" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">C1</text><text x="105" y="100" text-anchor="middle" fill="#334155" font-size="11">socket → serviço de IA</text>
  <rect x="245" y="54" width="150" height="62" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="320" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">C2</text><text x="320" y="100" text-anchor="middle" fill="#334155" font-size="11">coordenação + resiliência</text>
  <rect x="460" y="54" width="150" height="62" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="535" y="80" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">C3</text><text x="535" y="100" text-anchor="middle" fill="#334155" font-size="11">nuvem · observável · segura</text>
  <rect x="675" y="48" width="160" height="74" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="755" y="76" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">Plataforma</text><text x="755" y="96" text-anchor="middle" fill="#166534" font-size="11">de IA como serviço</text><text x="755" y="112" text-anchor="middle" fill="#16a34a" font-size="10.5">cloud-native</text>
  <line x1="180" y1="85" x2="243" y2="85" stroke="#12437f" stroke-width="2.5" marker-end="url(#tb)"/>
  <line x1="395" y1="85" x2="458" y2="85" stroke="#12437f" stroke-width="2.5" marker-end="url(#tb)"/>
  <line x1="610" y1="85" x2="673" y2="85" stroke="#12437f" stroke-width="2.5" marker-end="url(#tb)"/>
</svg>

<div class="dica">💡 Você escreveu <strong>código real e testado</strong> em cada etapa: eco TCP, servidor multicliente, gRPC, API REST, fila/worker, simulações de relógios/CAP/Raft, containers, tracing e JWT.</div>

---

## As grandes ideias que ficam

Além das tecnologias, **princípios** que valem para qualquer sistema distribuído:

- **A rede falha** — e a **falha parcial** é a regra, não a exceção. Projete para ela.
- **Não há um "agora" global** — ordene por **causalidade**, não por relógio.
- **Trade-offs são inevitáveis** — **CAP** (consistência × disponibilidade), custo × latência.
- **Desacople e torne resiliente** — fila, timeout, retry, **disjuntor**, idempotência.
- **Se não dá para medir, não dá para melhorar** — **observabilidade**.
- **Segurança e privacidade** não são opcionais — **TLS, autenticação, minimização (LGPD)**.

<div class="aviso">📌 Tecnologias mudam; <strong>esses princípios</strong> seguem. São eles que o ENADE — e o mercado — cobram de verdade.</div>

---

## Para onde a área está indo

<div class="cols">

<div>

**Infraestrutura**
- **Kubernetes** e *service mesh* como padrão de produção.
- **Serverless** mais maduro; **edge/5G** empurrando o processamento para perto.
- **FinOps** e **sustentabilidade**: custo e energia como requisitos.

</div>

<div>

**IA + sistemas**
- **LLMs e agentes** como componentes distribuídos de 1ª classe.
- **RAG** e bancos **vetoriais** no centro das arquiteturas.
- **Observabilidade com IA** (detecção de anomalia) e **plataformas** internas (Platform Engineering).

</div>

</div>

<div class="dica">💡 Repare: tudo isso é <strong>mais do mesmo</strong> que você viu — coordenação, resiliência, escala e segurança, agora com IA como carga de trabalho central.</div>

---

## Depois desta disciplina

- **Aprofunde a nuvem:** uma certificação *foundational* (AWS/GCP/Azure) consolida o vocabulário.
- **Construa um portfólio:** publique seus projetos (C1.A2, C2.A2, C3.A2) no GitHub, com README caprichado e URL no ar.
- **Explore carreiras:** **DevOps/SRE**, **Plataforma/Cloud**, **Backend distribuído**, **MLOps/ML Infra**.
- **Continue praticando:** reproduza um sistema real em pequena escala e **instrumente** tudo.

<div class="dica">💡 O seu <strong>C3.A2</strong> já é um projeto de portfólio: microsserviços, deploy, resiliência, observabilidade e segurança. Deixe-o apresentável.</div>

---

## Como continuar aprendendo

<div class="cols">

<div>

**Livros**
- **Coulouris** — *Distributed Systems* (a base da disciplina).
- **Kleppmann** — *Designing Data-Intensive Applications* (o próximo nível).

</div>

<div>

**Prática**
- Docs oficiais: Docker, Kubernetes, OpenTelemetry.
- Recrie um serviço e **meça** tudo (latência, traces, custo).
- Contribua para um projeto open-source distribuído.

</div>

</div>

<div class="aviso">📌 O melhor aprendizado em sistemas distribuídos é <strong>quebrar coisas de propósito</strong> e observar — como você fez nos labs (derrubar o worker, particionar réplicas, abrir o disjuntor).</div>

---

<!-- _class: secao -->

# Obrigado! 🚀
### Você saiu daqui sabendo construir, coordenar, implantar e proteger um sistema distribuído real.

Foi um prazer percorrer esse caminho com vocês. **Bons projetos — e até a próxima.**

<a class="proximo" href="aula-17-revisao-c3-avaliacao.html">← Anterior<small>Aula 17 · Revisão C3</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
