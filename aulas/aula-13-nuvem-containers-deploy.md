---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 13 — Computação em nuvem, containers e o primeiro deploy

C3 · Nuvem, implantação e segurança · 05/11/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C3

<div class="cols">

<div>

**C1 · Fundamentos** (1–7) ✅
**C2 · Coordenação e consistência** (8–12) ✅

**C3 · Nuvem, implantação e segurança** (13–18)
**Nuvem/containers** · orquestração · observabilidade · segurança.

</div>

<div>

<div class="dica">📍 <strong>Aula 13</strong>. Começa o bloco final: tirar o sistema do seu computador e colocá-lo <strong>no ar</strong>.</div>

</div>

</div>

<div class="aviso">🚀 Hoje <strong>lança o C3.A2</strong> — o projeto integrador: a <strong>Plataforma de IA como Serviço</strong>, que reúne tudo (microsserviços + fila + resiliência) rodando <strong>na nuvem</strong>.</div>

---

## Retomada

<div class="dica">🔄 Você entregou o C2.A2 (RAG distribuído) com a chamada ao LLM protegida?</div>

- Até aqui, tudo rodava **na sua máquina** (ou na VM). Funciona — mas **ninguém** no mundo acessa.
- Hoje: empacotar o serviço num **container** e publicá-lo na **nuvem** com uma **URL pública**.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Distinguir** os modelos de serviço em nuvem: **IaaS**, **PaaS** e **SaaS**.
2. **Explicar** **elasticidade** e o modelo de **custo por uso**.
3. **Empacotar** um serviço em um **container** (Docker) e **publicá-lo** com URL pública.

---

## O que é computação em nuvem

Usar, **pela internet** e **sob demanda**, recursos de computação (servidores, armazenamento, banco) de **outra pessoa** — pagando **pelo uso**, sem comprar hardware.

- **Sob demanda:** sobe e desce conforme a necessidade.
- **Pague pelo uso:** não paga servidor ocioso.
- **Autoatendimento:** você provisiona sozinho, em minutos.

<div class="dica">💡 <strong>Em miúdos:</strong> é a diferença entre <strong>comprar um gerador</strong> (e mantê-lo) e <strong>ligar na tomada</strong> e pagar a conta de luz do que usou.</div>

---

## Modelos de serviço: IaaS, PaaS, SaaS

<svg viewBox="0 0 860 250" role="img" style="width:100%;max-width:850px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <text x="140" y="24" text-anchor="middle" fill="#0d2b57" font-size="14" font-weight="700">IaaS</text>
  <text x="140" y="40" text-anchor="middle" fill="#64748b" font-size="11">infraestrutura</text>
  <text x="430" y="24" text-anchor="middle" fill="#0d2b57" font-size="14" font-weight="700">PaaS</text>
  <text x="430" y="40" text-anchor="middle" fill="#64748b" font-size="11">plataforma</text>
  <text x="720" y="24" text-anchor="middle" fill="#0d2b57" font-size="14" font-weight="700">SaaS</text>
  <text x="720" y="40" text-anchor="middle" fill="#64748b" font-size="11">software pronto</text>
  <!-- camadas: de baixo (hardware) a cima (aplicacao). Azul=voce gerencia, cinza=provedor -->
  <!-- IaaS -->
  <rect x="40" y="52" width="200" height="30" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="140" y="72" text-anchor="middle" font-size="11.5" fill="#0d2b57">sua aplicação</text>
  <rect x="40" y="84" width="200" height="30" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="140" y="104" text-anchor="middle" font-size="11.5" fill="#0d2b57">runtime / libs</text>
  <rect x="40" y="116" width="200" height="30" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="140" y="136" text-anchor="middle" font-size="11.5" fill="#0d2b57">sist. operacional</text>
  <rect x="40" y="148" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="140" y="168" text-anchor="middle" font-size="11.5" fill="#475569">virtualização / HW</text>
  <!-- PaaS -->
  <rect x="330" y="52" width="200" height="30" rx="5" fill="#dbeafe" stroke="#12437f"/><text x="430" y="72" text-anchor="middle" font-size="11.5" fill="#0d2b57">sua aplicação</text>
  <rect x="330" y="84" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="430" y="104" text-anchor="middle" font-size="11.5" fill="#475569">runtime / libs</text>
  <rect x="330" y="116" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="430" y="136" text-anchor="middle" font-size="11.5" fill="#475569">sist. operacional</text>
  <rect x="330" y="148" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="430" y="168" text-anchor="middle" font-size="11.5" fill="#475569">virtualização / HW</text>
  <!-- SaaS -->
  <rect x="620" y="52" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="720" y="72" text-anchor="middle" font-size="11.5" fill="#475569">aplicação pronta</text>
  <rect x="620" y="84" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="720" y="104" text-anchor="middle" font-size="11.5" fill="#475569">runtime / libs</text>
  <rect x="620" y="116" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="720" y="136" text-anchor="middle" font-size="11.5" fill="#475569">sist. operacional</text>
  <rect x="620" y="148" width="200" height="30" rx="5" fill="#e5e7eb" stroke="#94a3b8"/><text x="720" y="168" text-anchor="middle" font-size="11.5" fill="#475569">virtualização / HW</text>
  <rect x="40" y="196" width="130" height="22" rx="4" fill="#dbeafe" stroke="#12437f"/><text x="180" y="212" font-size="11.5" fill="#0d2b57">você gerencia</text>
  <rect x="300" y="196" width="130" height="22" rx="4" fill="#e5e7eb" stroke="#94a3b8"/><text x="440" y="212" font-size="11.5" fill="#475569">o provedor gerencia</text>
</svg>

<div class="dica">💡 <strong>Em miúdos (pizza):</strong> <strong>IaaS</strong> = massa pronta, você monta e assa; <strong>PaaS</strong> = pizzaria assa, você só escolhe o recheio (seu código); <strong>SaaS</strong> = pizza entregue pronta (ex.: Gmail).</div>

---

## Elasticidade e custo

- **Elasticidade:** a nuvem **adiciona** instâncias quando a carga sobe e **remove** quando cai — **automaticamente**.
- **Custo por uso:** você paga pelas instâncias **enquanto existem**. Escalar para zero = **custo zero**.

<svg viewBox="0 0 820 180" role="img" style="width:100%;max-width:780px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="e1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <line x1="60" y1="140" x2="780" y2="140" stroke="#94a3b8" stroke-width="2" marker-end="url(#e1)"/>
  <text x="780" y="158" text-anchor="end" fill="#64748b" font-size="11">tempo</text>
  <path d="M60,120 C180,120 200,40 320,40 S460,120 540,120 S700,60 760,60" fill="none" stroke="#e08a00" stroke-width="2.5"/>
  <text x="300" y="30" fill="#c2740a" font-size="12" font-weight="700">carga (requisições)</text>
  <g fill="#12437f" font-size="11" text-anchor="middle">
    <rect x="120" y="150" width="16" height="16" rx="3" fill="#dbeafe" stroke="#12437f"/>
    <rect x="300" y="150" width="16" height="16" rx="3" fill="#dbeafe" stroke="#12437f"/><rect x="320" y="150" width="16" height="16" rx="3" fill="#dbeafe" stroke="#12437f"/><rect x="340" y="150" width="16" height="16" rx="3" fill="#dbeafe" stroke="#12437f"/>
    <rect x="540" y="150" width="16" height="16" rx="3" fill="#dbeafe" stroke="#12437f"/>
  </g>
  <text x="128" y="178" text-anchor="middle" fill="#334155" font-size="10.5">1 instância</text>
  <text x="328" y="178" text-anchor="middle" fill="#334155" font-size="10.5">3 instâncias (pico)</text>
  <text x="548" y="178" text-anchor="middle" fill="#334155" font-size="10.5">1 de novo</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é contratar <strong>mais caixas no supermercado</strong> quando a fila cresce e <strong>dispensá-los</strong> quando esvazia — você paga só pelas horas trabalhadas.</div>

---

## O problema do "na minha máquina funciona"

O serviço depende de uma **versão** de Python, de **bibliotecas**, de variáveis de ambiente… Mudou a máquina, **quebrou**. O **container** resolve: empacota **o app + o ambiente inteiro** numa unidade que roda **igual** em qualquer lugar.

<svg viewBox="0 0 820 190" role="img" style="width:100%;max-width:800px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <text x="200" y="22" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Máquina virtual (pesada)</text>
  <rect x="70" y="34" width="260" height="30" rx="4" fill="#dbeafe" stroke="#12437f"/><text x="200" y="54" text-anchor="middle" font-size="11" fill="#0d2b57">app A · app B</text>
  <rect x="70" y="66" width="260" height="30" rx="4" fill="#e5e7eb" stroke="#94a3b8"/><text x="200" y="86" text-anchor="middle" font-size="11" fill="#475569">S.O. convidado (completo) ×N</text>
  <rect x="70" y="98" width="260" height="26" rx="4" fill="#e5e7eb" stroke="#94a3b8"/><text x="200" y="116" text-anchor="middle" font-size="11" fill="#475569">hipervisor</text>
  <rect x="70" y="124" width="260" height="26" rx="4" fill="#f1f5f9" stroke="#94a3b8"/><text x="200" y="142" text-anchor="middle" font-size="11" fill="#475569">hardware</text>
  <text x="620" y="22" text-anchor="middle" fill="#166534" font-size="13" font-weight="700">Containers (leves)</text>
  <rect x="490" y="34" width="80" height="44" rx="5" fill="#dcfce7" stroke="#16a34a"/><text x="530" y="60" text-anchor="middle" font-size="11" fill="#14532d">app A</text>
  <rect x="580" y="34" width="80" height="44" rx="5" fill="#dcfce7" stroke="#16a34a"/><text x="620" y="60" text-anchor="middle" font-size="11" fill="#14532d">app B</text>
  <rect x="670" y="34" width="80" height="44" rx="5" fill="#dcfce7" stroke="#16a34a"/><text x="710" y="60" text-anchor="middle" font-size="11" fill="#14532d">app C</text>
  <rect x="490" y="80" width="260" height="28" rx="4" fill="#e5e7eb" stroke="#94a3b8"/><text x="620" y="99" text-anchor="middle" font-size="11" fill="#475569">motor de containers (Docker)</text>
  <rect x="490" y="108" width="260" height="24" rx="4" fill="#e5e7eb" stroke="#94a3b8"/><text x="620" y="125" text-anchor="middle" font-size="11" fill="#475569">S.O. do host (compartilhado)</text>
  <rect x="490" y="132" width="260" height="22" rx="4" fill="#f1f5f9" stroke="#94a3b8"/><text x="620" y="148" text-anchor="middle" font-size="11" fill="#475569">hardware</text>
</svg>

<div class="dica">💡 Container <strong>compartilha</strong> o S.O. do host → sobe em <strong>segundos</strong> e pesa <strong>MB</strong> (a VM leva minutos e pesa GB). Por isso é a unidade de deploy na nuvem.</div>

---

## Imagem × container · o Dockerfile

- **Imagem:** o **pacote** (receita assada) — app + dependências + instruções de execução. Imutável.
- **Container:** uma **instância em execução** da imagem. Você sobe **vários** da mesma imagem.

```docker
FROM python:3.12-slim          # base: S.O. mínimo + Python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt   # instala as deps (vira uma camada em cache)
COPY app.py .
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
```

<div class="dica">💡 <strong>Em miúdos:</strong> a <strong>imagem</strong> é a receita assada; o <strong>container</strong> é cada fatia servida. <code>0.0.0.0</code> = "ouça em todas as interfaces", senão ninguém de fora acessa.</div>

---

<!-- _class: secao -->

# Laboratório
### Conteinerizar o serviço e publicar na nuvem

---

## Mão na massa — siga o Guia do Laboratório

Hoje são **4 missões**: rodar o serviço local, **conteinerizar** (build + run), **publicar** na nuvem com URL pública e **lançar o C3.A2** (conteinerizar os serviços do projeto).

### 👉 [Abrir o Guia do Laboratório »](lab-13-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 13 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Exemplo pronto e testado: <code>exemplos/aula13/</code> — <code>app.py</code> (FastAPI que mostra o host), <code>Dockerfile</code>, <code>requirements.txt</code> e <code>.dockerignore</code>.</div>

---

## O que o exemplo mostra (aquecimento)

```powershell
# 1) local (sem Docker): sobe e testa
uvicorn app:app --port 8000      # GET / -> {"mensagem":"Ola da nuvem!","host":"...","versao":"1.0"}

# 2) conteineriza e roda igual, isolado:
docker build -t servico-nuvem .
docker run -p 8000:8000 servico-nuvem   # o "host" no JSON agora e o ID do container
```

<div class="dica">💡 O campo <code>host</code> muda quando roda em container (vira o ID do container) — é como você vai <strong>ver</strong> réplicas diferentes respondendo quando escalar.</div>

---

## No seu trabalho — C3.A2 (lançado hoje)

O **C3.A2** é o **projeto integrador**: API Gateway + serviço de inferência + worker de fila + armazenamento vetorial, **conteinerizados** e **na nuvem**.

- **Hoje:** cada serviço ganha o **seu** `Dockerfile` e **builda** individualmente.
- Na **próxima aula**: subir **tudo junto** com um comando (orquestração).

<div class="dica">💡 Puxa para o kit: comece pelo serviço mais simples. Um <code>Dockerfile</code> por serviço, cada um buildando sozinho, é a meta de hoje.</div>

---

## Atividade para casa

1. **Publique** o serviço de exemplo (ou um do seu projeto) em uma nuvem **free tier** (Render/Railway) e obtenha uma **URL pública**.
2. **Conteinerize** **todos** os serviços do **C3.A2** (um `Dockerfile` por serviço, cada um buildando).
3. **Registre** no README o comando de build/run de cada serviço.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> a <strong>URL pública</strong> do serviço no ar + todos os serviços do C3.A2 conteinerizados. Roteiro completo no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Modelos de serviço **IaaS × PaaS × SaaS** (quem gerencia o quê).
- **Elasticidade** e **custo por uso** (escala sob demanda).
- **Container × VM** (compartilha o S.O. do host; leve e rápido).
- **Portabilidade**: "roda igual em qualquer lugar".

**Termos-chave:** Nuvem · IaaS/PaaS/SaaS · Elasticidade · Container · Imagem · Dockerfile · Deploy

<div class="dica">💡 Pegadinha: confundir <strong>container</strong> com <strong>VM</strong>. Container compartilha o S.O. do host; VM carrega um S.O. convidado inteiro.</div>

---

## Questão de autoavaliação (estilo ENADE)

Uma equipe quer **implantar sua própria aplicação** sem gerenciar sistema operacional nem servidores, enviando **apenas o código** para uma plataforma que cuida do runtime e da execução. O modelo de serviço em nuvem mais adequado é:

A) IaaS, pois oferece máquinas virtuais cruas
B) **PaaS, pois entrega a plataforma e o runtime, bastando enviar o código**
C) SaaS, pois entrega um software pronto ao usuário final
D) nenhum, pois exige comprar servidores físicos
E) on-premises, pois roda no datacenter próprio

---

## Resolução — alternativa **B**

- **PaaS**: o provedor cuida de S.O., runtime e escala; a equipe entrega **só o código** (ex.: Render, Railway, App Engine).
- **IaaS** (A) daria a VM crua (você gerencia o S.O.); **SaaS** (C) é software pronto para o usuário final, não para hospedar o seu app.

<div class="dica">💡 "Enviar só o código" é a assinatura do <strong>PaaS</strong> — exatamente o free tier que você usa no deploy.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 7 — Virtualização e nuvem (visão geral).
- Docs do **Docker** (Get Started) e do **Render**/**Railway**.
- Rode o exemplo: compare o `host` local × no container.

</div>

<div>

**Glossário**
- **IaaS/PaaS/SaaS:** camadas de serviço (infra / plataforma / software).
- **Elasticidade:** ajustar instâncias conforme a carga.
- **Container:** app + ambiente empacotados; compartilha o S.O. do host.
- **Imagem:** o pacote imutável; **container** é a imagem em execução.
- **Dockerfile:** receita que descreve a imagem.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Publique o serviço (URL pública) e conteinerize os serviços do C3.A2.

**Próxima (Aula 14):** **Orquestração, serverless e computação na borda** — subir a stack inteira com um comando e entregar funções sem gerenciar servidor.

<a class="proximo" href="aula-12-revisao-c2-avaliacao.html">← Anterior<small>Aula 12 · Revisão C2</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
