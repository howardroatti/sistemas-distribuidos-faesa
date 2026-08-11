---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 8 — Mensageria, eventos e API Gateway

C2 · Coordenação e consistência · 24/09/2026 · Lança o **C2.A2**
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — começa a C2

<div class="cols">

<div>

**C1 · Fundamentos e comunicação** (1–7) ✅
Sockets, concorrência, gRPC, REST, IA como serviço.

**C2 · Coordenação e consistência** (8–12)
**Mensageria**, relógios lógicos, **CAP**, **Raft**, resiliência.

</div>

<div>

**C3 · Nuvem, implantação e segurança** (13–18)
Containers, nuvem, serverless, observabilidade, segurança.

<div class="dica">📍 <strong>Aula 8</strong> — a <strong>fila</strong> que o seu worker já usava, agora com a teoria.</div>

</div>

</div>

---

## Retomada — fechamento da C1

<div class="dica">🔄 A C1 acabou: prova C1.A1 feita e trabalho C1.A2 entregue.</div>

- No **C1.A2**, o seu serviço já enfileirava tarefas e um **worker** processava em segundo plano — mas você usou a fila **sem a teoria**.
- Hoje entendemos **por que** ela existe e **o que** ela resolve.

<div class="aviso">📌 Esta aula também <strong>lança o C2.A2</strong> — RAG Distribuído em Microsserviços (kit novo). A mensageria de hoje é a <strong>espinha</strong> dele.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Diferenciar** comunicação **síncrona** de **assíncrona** e saber quando usar cada uma.
2. **Processar** inferências de IA de forma **assíncrona** com **fila** e **worker**.
3. **Explicar** o papel de um **API Gateway** numa arquitetura de microsserviços.

---

## Conceito 1/4 — Síncrono × Assíncrono

<div class="cols">

<div>

**Síncrono**
- O cliente chama e **fica esperando** a resposta.
- Simples, mas ele **trava** enquanto espera.
- Se muitos esperam ao mesmo tempo, o serviço **satura**.

</div>

<div>

**Assíncrono**
- O cliente **entrega a tarefa** e recebe **na hora** um **comprovante (id)**.
- Vai **buscar o resultado depois**.
- Quebra o **vínculo temporal** entre pedido e processamento.

</div>

</div>

<div class="dica">💡 Para uma inferência de IA que leva <strong>segundos</strong> (Aula 6), segurar o cliente é desperdício. O assíncrono é a resposta ao <strong>cold start / latência</strong> que você mediu.</div>

---

## Conceito 2/4 — A fila como amortecedor

- O mecanismo por trás do assíncrono é a **fila de mensagens**: um **produtor** coloca a tarefa; um **worker** (consumidor) a retira e processa.
- Palavra-chave: **desacoplamento** — quem produz **não precisa saber** quem consome, nem quando, nem **quantos** consumidores existem.

<div class="cols">

<div>

**Absorve picos**
Chegou mais do que a capacidade? As tarefas **se acumulam na fila** em vez de **derrubar** o serviço.

</div>

<div>

**Escala simples**
Precisa de mais vazão? **Suba mais workers** consumindo a mesma fila — **sem mudar** quem produz.

</div>

</div>

<div class="dica">💡 É a <strong>concorrência da Aula 3</strong> num nível acima: em vez de threads no mesmo programa, <strong>processos independentes</strong> puxando da mesma fila.</div>

---

## Conceito 2/4 — Quando o processamento falha: dead-letter

- Uma tarefa pode dar **erro** (entrada inválida, dependência fora do ar). O que fazer?
- **Boa prática:** **reprocessar** algumas vezes; **persistindo** a falha, encaminhar a mensagem para uma **fila de descarte** — a **dead-letter**.

<div class="aviso">⚠️ Os dois extremos são ruins: <strong>tentar para sempre</strong> trava o worker; <strong>perder a mensagem</strong> esconde o problema. A <strong>dead-letter</strong> isola a mensagem para análise e <strong>mantém o fluxo principal saudável</strong>.</div>

---

## Conceito 3/4 — Pub/sub e arquitetura de eventos

<div class="cols">

<div>

**Fila (work queue)**
Cada mensagem é consumida por **um único** worker. Distribui **trabalho**.

</div>

<div>

**Pub/sub (publicar/assinar)**
A mesma mensagem é entregue a **todos os interessados**. Distribui **informação**.

</div>

</div>

- O pub/sub é a base da **arquitetura orientada a eventos**, muito usada em nuvem.
- Ex.: um **pedido concluído** pode, ao mesmo tempo, **atualizar o estoque**, **notificar o cliente** e **alimentar um relatório**.

<div class="dica">💡 Fila = <strong>um</strong> consumidor por mensagem. Pub/sub = <strong>vários</strong> assinantes na mesma mensagem.</div>

---

## Conceito 4/4 — API Gateway: a porta única

- Com vários serviços, o cliente **não deve** conhecer o endereço de cada um.
- O **API Gateway** é a **porta de entrada única**: recebe todas as requisições e **encaminha ao serviço certo**.
- Centraliza o que é **comum a todos**: **autenticação**, **limite de requisições** (rate limit) e **log**. É nele que aplicaremos a **segurança** (C3).

<div class="aviso">⚠️ <strong>Versionamento:</strong> <strong>acrescentar</strong> um campo à resposta é seguro; <strong>remover/renomear</strong> um campo <strong>quebra</strong> os clientes — exige publicar uma nova versão (ex.: <code>/v2</code>) e manter a antiga durante a transição.</div>

---

<!-- _class: secao -->

# Laboratório
### O pipeline assíncrono — da fila em memória ao kit real

---

## Lab · Passo 1 — a fila como conceito (`fila_demo.py`)

Sem Docker ainda: uma fila **em memória** com **3 workers** (threads da Aula 3):

```python
import queue, threading
fila = queue.Queue(); resultados = {}; dead_letter = []

def worker(nome):
    while True:
        try: tarefa = fila.get(timeout=2)          # pega da fila (bloqueia)
        except queue.Empty: return
        try:
            resultados[tarefa["id"]] = processa(tarefa)     # a "inferência"
        except Exception:
            tarefa["tentativas"] += 1
            if tarefa["tentativas"] < 3: fila.put(tarefa)   # RETENTATIVA
            else: dead_letter.append(tarefa)                # DEAD-LETTER

for i in range(9): fila.put({"id": i, "tentativas": 0})     # o PRODUTOR
# 3 WORKERS dividem a carga (escalar = + workers na MESMA fila):
[threading.Thread(target=worker, args=(f"w{i}",), daemon=True).start() for i in range(3)]
```

---

## Lab · Passo 2 — rodar e observar

```powershell
python fila_demo.py
# [produtor] enfileirou 9 tarefas
# [w2] processou tarefa 2      <- os 3 workers dividem a carga
# [w0] processou tarefa 0
# ...
# [w1] 99 -> DEAD-LETTER        <- a tarefa "envenenada" falhou 3x
# processadas: 8 | na dead-letter: 1
```

<div class="dica">💡 Experimente: mude <code>range(3)</code> para <strong>1 worker</strong> e veja demorar mais; para <strong>6 workers</strong> e veja acelerar. É a <strong>escalabilidade</strong> da fila na prática — sem tocar no produtor.</div>

---

## Lab · Passo 3 — o pipeline real, no kit da C1 (Redis)

O kit já traz a fila de verdade (**Redis**) em `app/fila.py`:

```text
POST /predict  →  fila.enfileirar(texto)  →  devolve {"id": ...}   (não espera!)
                        │  (Redis)
worker  →  fila.proxima_tarefa()  →  modelo.prever()  →  fila.guardar_resultado(id, ...)
GET /resultado/{id}  →  fila.buscar_resultado(id)  →  {"status": "pronto", ...}
```

```powershell
docker compose up -d           # sobe o Redis (agora sim, na VM)
uvicorn app.api_rest:app       # a API (POST /predict, GET /resultado)
python -m app.worker           # o worker — suba VÁRIOS e veja dividir
```

<div class="dica">💡 São as <strong>TAREFAS 1, 2 e 3</strong> do C1.A2: <code>POST /predict</code> (enfileira), <code>GET /resultado/{id}</code> (consulta) e o worker <strong>gravar o resultado</strong>.</div>

---

## 🚀 Lançamento do C2.A2 — RAG Distribuído em Microsserviços

Começa o **C2.A2**: um **RAG** (busca + geração) dividido em **microsserviços** (`ingestao`, `recuperacao`, `geracao`), acessados por um **gateway**.

- **Clonar** o kit novo: `sd-2026-2-kit-c2a2`.
- **TAREFA 4 — mensageria:** um **novo worker** + `docker-compose.yml` (ao menos **uma etapa** do fluxo passa por **fila**).
- **Iniciar** o serviço de **ingestão/embeddings**.

<div class="dica">💡 A mensageria de hoje é a <strong>espinha</strong> do C2.A2. Você já sabe o padrão: produtor → fila → worker, com <strong>dead-letter</strong> para falhas.</div>

---

## Atividade para casa

1. **Complete o worker** do C1 (kit): **TAREFA 3** (gravar o resultado) e **TAREFA 5** (**retentativa + dead-letter** em vez de só registrar o erro).
2. **Teste sob carga:** dispare muitos `POST /predict` e confira que a fila **absorve** e os resultados saem pelo `GET /resultado/{id}`.
3. **Inicie o C2.A2:** clone `sd-2026-2-kit-c2a2` e ponha o **serviço de ingestão** no ar.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> worker com <strong>retentativa + dead-letter</strong> + repositório do <strong>C2.A2</strong> com a ingestão iniciada.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Comunicação **síncrona × assíncrona** entre processos.
- **Middleware orientado a mensagens (MOM)**, **filas** e **pub/sub**.
- **Arquitetura orientada a eventos** e **desacoplamento**.
- **Microsserviços**, **API Gateway** e **versionamento** de contratos.

**Termos-chave:** Fila · Produtor · Worker · Pub/sub · Dead-letter · API Gateway · Versionamento

<div class="dica">💡 Papéis: <strong>produtor</strong> publica, <strong>worker</strong> consome. Fila distribui <strong>trabalho</strong>; pub/sub distribui <strong>informação</strong>.</div>

---

## Questão de autoavaliação (estilo ENADE)

Sobre a diferença entre uma **fila de trabalho** e o modelo **publicar/assinar (pub/sub)**, assinale a correta.

A) Na fila as mensagens são descartadas; em pub/sub, persistidas.
B) Na fila, cada mensagem é consumida por **um único** consumidor; em pub/sub, a mesma mensagem é entregue a **todos os assinantes** interessados.
C) A fila exige consistência forte e o pub/sub, consistência eventual.
D) A fila só funciona com UDP e o pub/sub, apenas com TCP.
E) Não há diferença prática entre os dois modelos.

---

## Resolução — alternativa **B**

- A **fila distribui trabalho**: um consumidor por mensagem.
- O **pub/sub distribui informação**: vários assinantes recebem a **mesma** mensagem.
- As demais inventam distinções que **não existem** (descarte, consistência, protocolo de transporte).

<div class="dica">💡 É o seu <code>fila_demo.py</code> (um worker pega cada tarefa) contra o padrão de eventos (todos recebem).</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 6 — Comunicação indireta (mensageria, pub/sub).
- Documentação do **Redis** (listas como fila) — a que o kit usa.
- Releia `app/fila.py` e `app/worker.py` do **kit da C1**.

</div>

<div>

**Glossário**
- **Fila:** guarda tarefas até um consumidor processar.
- **Worker:** processo que retira e executa mensagens.
- **Pub/sub:** uma mensagem publicada chega a vários assinantes.
- **Dead-letter:** fila de descarte para o que falhou demais.
- **API Gateway:** porta única que encaminha aos serviços internos.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Complete o worker (retentativa + dead-letter) e inicie o C2.A2.

**Próxima (Aula 9):** **Tempo e ordenação** — relógios lógicos: por que "que horas são?" é difícil entre máquinas.

<a class="proximo" href="aula-07-revisao-c1-avaliacao.html">← Anterior<small>Aula 7 · Revisão + prova C1</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
