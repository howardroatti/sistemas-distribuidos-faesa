---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 5 — Serviços web: REST e OpenAPI com FastAPI

C1 · Fundamentos e comunicação distribuída · 10/09/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — a trilha do semestre

<div class="cols">

<div>

**C1 · Fundamentos e comunicação** (Aulas 1–7)
Sockets, concorrência, gRPC, **REST** e IA como serviço.

**C2 · Coordenação e consistência** (Aulas 8–12)
Mensageria, relógios lógicos, **CAP**, **Raft**, resiliência.

</div>

<div>

**C3 · Nuvem, implantação e segurança** (Aulas 13–18)
Containers, nuvem, serverless, observabilidade, segurança.

<div class="dica">📍 Você está na <strong>Aula 5</strong> — a interface <strong>para fora</strong> do seu serviço.</div>

</div>

</div>

---

## Retomada — o que você fez em casa

<div class="dica">🔄 A aula começa consolidando a entrega da Aula 4.</div>

- Você **ampliou o `.proto`** com um segundo método e **regerou os stubs**?
- O `README` explicou **o impacto de mudar o contrato** (os dois lados regeram)?
- Ficou claro: **gRPC é a interface para dentro** (serviço ↔ serviço)?

<div class="aviso">📌 Hoje montamos a interface <strong>para fora</strong> — a que o mundo consome: uma <strong>API REST</strong>, com documentação que <strong>se escreve sozinha</strong>.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** os princípios **REST** e a diferença para o **SOAP**.
2. **Construir** uma API REST com **FastAPI**, usando os **verbos** e **códigos** corretos.
3. **Ler e usar** a documentação automática gerada pelo **OpenAPI**.

---

## Conceito 1/3 — Do SOAP ao REST

- **Serviços web** deixam sistemas diferentes conversarem pela internet.
- A geração anterior, **SOAP**, usava mensagens em **XML** e contrato rígido em **WSDL**: poderoso, mas **verboso e pesado** — sobrevive em legados e bancos.
- O **REST** (*Representational State Transfer*), dominante hoje, é **bem mais simples**: usa o **próprio HTTP como ele já é**, sem camada extra.

<div class="dica">💡 Um serviço novo nasce <strong>REST</strong> — ou <strong>gRPC</strong> — quase nunca SOAP. Saber os dois ajuda a entender a evolução da <strong>SOA</strong> (Arquitetura Orientada a Serviços) rumo aos <strong>microsserviços</strong>.</div>

---

## Conceito 2/3 — Recursos, verbos e status

O REST organiza tudo em torno de **recursos** (substantivos → URLs): `/tarefas` (a coleção), `/tarefas/7` (um item).

<div class="cols">

<div>

**O verbo diz a ação**
- **GET** — lê
- **POST** — cria
- **PUT** — atualiza
- **DELETE** — remove

</div>

<div>

**O status diz o resultado**
- **200** OK · **201** Criado
- **400** erro do cliente
- **404** não encontrado
- **500** erro do servidor

</div>

</div>

<div class="dica">💡 A <strong>URL</strong> diz <em>o quê</em>, o <strong>verbo</strong> diz <em>a ação</em>, o <strong>status</strong> diz <em>o resultado</em>. Essa separação é o que torna a API <strong>previsível</strong>.</div>

---

## Conceito 2/3 — Idempotência (guarde para depois)

- Uma operação é **idempotente** quando, **repetida**, leva ao **mesmo estado final**.
- **GET, PUT e DELETE** são idempotentes; **POST não é** — cada chamada **cria um novo** recurso.

<div class="aviso">⚠️ Essa distinção volta a importar na <strong>resiliência</strong> (Aula 11): só é seguro <strong>repetir automaticamente</strong> (retentativa) uma operação <strong>idempotente</strong>. Repetir um POST pode criar recursos duplicados — a semente da <strong>idempotência</strong> que você viu na Aula 1.</div>

---

## Conceito 3/3 — OpenAPI: a documentação que não envelhece

- Uma boa API REST precisa de um **contrato** para quem vai consumi-la.
- Com o **FastAPI**, esse contrato — no padrão **OpenAPI** — é **gerado automaticamente** a partir dos **tipos declarados no código**, numa **página interativa** (`/docs`).
- Como **nasce do próprio código**, a documentação **não desatualiza** — o problema crônico da era SOAP, em que contrato e implementação viviam divergindo.

<div class="dica">💡 Você escreve os tipos uma vez; o FastAPI valida a entrada, gera o <code>/docs</code> e mantém tudo em sincronia.</div>

---

<!-- _class: secao -->

# Laboratório
### Uma API REST com FastAPI — passo a passo

---

## Lab · Passo 1 — instalar e o esqueleto (`app.py`)

```powershell
pip install fastapi "uvicorn[standard]"
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Tarefas")
tarefas = []                         # "banco" em memória (só para a aula)

class Tarefa(BaseModel):             # o TIPO da entrada → vira validação + /docs
    titulo: str
```

<div class="dica">💡 O <code>BaseModel</code> do Pydantic declara o formato do dado. É dele que o FastAPI tira a <strong>validação</strong> e a <strong>documentação</strong>.</div>

---

## Lab · Passo 2 — as 3 rotas

```python
@app.get("/tarefas")                 # LER a coleção
def listar():
    return tarefas

@app.post("/tarefas", status_code=201)   # CRIAR (201 = Created)
def criar(tarefa: Tarefa):
    nova = {"id": len(tarefas) + 1, "titulo": tarefa.titulo}
    tarefas.append(nova)
    return nova

@app.get("/tarefas/{tid}")           # LER um item
def obter(tid: int):
    for t in tarefas:
        if t["id"] == tid:
            return t
    raise HTTPException(status_code=404, detail="tarefa não encontrada")
```

---

## Lab · Passo 3 — rodar e abrir o `/docs`

```powershell
uvicorn app:app --reload --port 8000
# abra no navegador:  http://localhost:8000/docs
```

- No **`/docs`** (OpenAPI) você **testa as rotas pelo navegador**: clique em **POST /tarefas**, *Try it out*, envie `{"titulo": "estudar SD"}` → resposta **201**.
- Depois **GET /tarefas** lista o que criou; **GET /tarefas/99** devolve **404**.

<div class="dica">💡 Você não escreveu <strong>uma linha</strong> de documentação — o <code>/docs</code> nasceu dos <strong>tipos</strong> do seu código.</div>

---

## Lab · Checkpoints & problemas comuns (Windows)

<div class="cols">

<div>

**✅ O que você deve ver**
- `uvicorn` sobe em `http://127.0.0.1:8000`.
- `/docs` abre a página interativa.
- POST devolve **201**; GET de id inexistente devolve **404**.

</div>

<div>

**🛠️ Se der erro**
- `No module named fastapi` → `pip install fastapi "uvicorn[standard]"`.
- `app:app` = **arquivo** `app.py` : **variável** `app`. Nome diferente? Ajuste.
- Porta ocupada → troque `8000`.
- Alterou o código? O `--reload` recarrega sozinho.

</div>

</div>

---

## No seu trabalho — C1.A2

- A **outra interface** do trabalho é **REST**. As rotas de **submissão** e de **consulta do resultado** são o **coração** da API.

<div class="dica">💡 Puxa direto para o kit:
<br>• <strong>TAREFA 1</strong> — <code>POST /predict</code> que <strong>enfileira</strong> a tarefa e devolve um <strong>id</strong>.
<br>• <strong>TAREFA 2</strong> — <code>GET /resultado/{id}</code> para buscar o resultado quando pronto.
<br>• <strong>TAREFA 6</strong> — registrar <strong>log</strong> de cada requisição.
<br>Repositório: <code>sd-2026-2-kit-c1a2</code> (a rota síncrona já roda; veja a Aula 1).</div>

---

## Atividade para casa — completar o CRUD

1. **Adicione** `PUT /tarefas/{id}` (atualiza o título) e `DELETE /tarefas/{id}` (remove) — com os **status corretos**.
2. **Trate os erros:** id inexistente → **404**.
3. **Escreva 3 testes** (use `TestClient` do FastAPI ou `requests`): criar (201), listar (200), buscar id inexistente (404).
4. Confirme no **`/docs`** que as novas rotas aparecem **sozinhas**.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> API REST com <strong>CRUD completo</strong> e <strong>3 testes passando</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Web services: SOAP × REST** — diferenças e aplicabilidade.
- **Verbos HTTP**, **códigos de status** e **idempotência**.
- **SOA** (Arquitetura Orientada a Serviços) e **interoperabilidade**.
- **Contratos de API** e documentação (**WSDL**, **OpenAPI**).

**Termos-chave:** REST · SOAP · Recurso · Verbo HTTP · Código de status · OpenAPI · Idempotência

<div class="dica">💡 Decore o mapa: <strong>POST→201</strong>, <strong>GET→200</strong>, <strong>404</strong> não encontrado, <strong>400</strong> cliente errou, <strong>500</strong> servidor falhou. E qual verbo é idempotente.</div>

---

## Questão de autoavaliação (estilo ENADE)

Em uma API REST, para **criar** um novo recurso e sinalizar **sucesso**, o verbo e o código de status esperados são, respectivamente:

A) **GET** e **200** (OK).
B) **POST** e **201** (Created).
C) **PUT** e **204** (No Content).
D) **POST** e **404** (Not Found).
E) **DELETE** e **200** (OK).

---

## Resolução — alternativa **B**

- **POST** cria o recurso e **201 (Created)** indica **criação bem-sucedida**.
- **D** erra o status: **404** sinaliza recurso **inexistente** — não faz sentido como resposta de criação.
- **A**, **C** e **E** usam verbos que **não criam** (ler, atualizar, remover).

<div class="dica">💡 É a rota <code>POST /tarefas</code> do seu lab de hoje virando questão de prova.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 9 — Serviços web.
- Documentação oficial do **FastAPI** (o tutorial é excelente).
- Abra o `app/api_rest.py` do **kit da C1** e compare com o seu.

</div>

<div>

**Glossário**
- **REST:** recursos em URLs + verbos HTTP.
- **SOAP:** web service em XML, contrato em WSDL.
- **Recurso:** entidade exposta por uma URL.
- **Código de status:** número que informa o resultado.
- **Idempotência:** repetir não muda o resultado final.
- **OpenAPI:** contrato da API gerado pelo FastAPI.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Entregue a API com CRUD completo + 3 testes. A Aula 6 (EAD) consolida o serviço.

**Próxima (Aula 6 · EAD):** **IA como serviço distribuído** — o marco do curso: juntar REST + gRPC + fila no seu serviço.

<a class="proximo" href="../index.html">↩ Voltar ao índice<small>todas as aulas</small></a>
