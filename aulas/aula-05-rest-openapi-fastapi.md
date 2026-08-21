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

## Anatomia de uma requisição REST

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="an" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <rect x="30" y="30" width="800" height="106" rx="12" fill="#eef4fb" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="48" y="54" fill="#0d2b57" font-size="13" font-weight="700">REQUISIÇÃO</text>
  <rect x="56" y="66" width="94" height="44" rx="8" fill="#16a34a"/><text x="103" y="94" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">POST</text>
  <text x="168" y="96" fill="#0d2b57" font-size="18" font-family="Consolas,monospace" font-weight="700">/tarefas</text>
  <rect x="336" y="66" width="320" height="44" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/><text x="352" y="94" fill="#334155" font-size="13" font-family="Consolas,monospace">{ "titulo": "estudar SD" }</text>
  <text x="103" y="128" text-anchor="middle" fill="#16a34a" font-size="11.5" font-weight="700">a ação</text>
  <text x="210" y="128" text-anchor="middle" fill="#12437f" font-size="11.5" font-weight="700">o recurso (o quê)</text>
  <text x="496" y="128" text-anchor="middle" fill="#64748b" font-size="11.5" font-weight="700">o dado enviado (corpo)</text>
  <line x1="430" y1="138" x2="430" y2="180" stroke="#94a3b8" stroke-width="2" marker-end="url(#an)"/>
  <text x="512" y="163" fill="#334155" font-size="12" font-weight="700">servidor processa</text>
  <rect x="30" y="184" width="800" height="106" rx="12" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>
  <text x="48" y="208" fill="#14532d" font-size="13" font-weight="700">RESPOSTA</text>
  <rect x="56" y="220" width="150" height="44" rx="8" fill="#16a34a"/><text x="131" y="248" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">201 Created</text>
  <rect x="336" y="220" width="320" height="44" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/><text x="352" y="248" fill="#334155" font-size="13" font-family="Consolas,monospace">{ "id": 1, "titulo": "estudar SD" }</text>
  <text x="131" y="282" text-anchor="middle" fill="#16a34a" font-size="11.5" font-weight="700">o resultado</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é como um balcão dos Correios: o <strong>verbo</strong> é o que você quer fazer (enviar, consultar), a <strong>URL</strong> é o balcão certo, o <strong>status</strong> é o carimbo de volta (deu certo · não achei · deu erro).</div>

---

## Conceito 2/3 — Idempotência (guarde para depois)

- Uma operação é **idempotente** quando, **repetida**, leva ao **mesmo estado final**.
- **GET, PUT e DELETE** são idempotentes; **POST não é** — cada chamada **cria um novo** recurso.

<div class="aviso">⚠️ Essa distinção volta a importar na <strong>resiliência</strong> (Aula 11): só é seguro <strong>repetir automaticamente</strong> (retentativa) uma operação <strong>idempotente</strong>. Repetir um POST pode criar recursos duplicados — a semente da <strong>idempotência</strong> que você viu na Aula 1.</div>

---

## Idempotência, visualmente

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:840px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="ir" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#dc2626"/></marker>
    <marker id="ig" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker>
  </defs>
  <text x="30" y="30" fill="#b91c1c" font-size="14" font-weight="700">POST /tarefas — repetido 3× · NÃO idempotente</text>
  <rect x="30" y="46" width="130" height="56" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/>
  <text x="95" y="70" text-anchor="middle" fill="#7c4a03" font-size="14" font-weight="700">POST ×3</text>
  <text x="95" y="90" text-anchor="middle" fill="#c2740a" font-size="11">cada um cria</text>
  <rect x="300" y="52" width="150" height="44" rx="8" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="375" y="80" text-anchor="middle" fill="#991b1b" font-size="13.5" font-weight="700">Tarefa #1</text>
  <rect x="470" y="52" width="150" height="44" rx="8" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="545" y="80" text-anchor="middle" fill="#991b1b" font-size="13.5" font-weight="700">Tarefa #2</text>
  <rect x="640" y="52" width="150" height="44" rx="8" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="715" y="80" text-anchor="middle" fill="#991b1b" font-size="13.5" font-weight="700">Tarefa #3</text>
  <line x1="160" y1="74" x2="298" y2="74" stroke="#dc2626" stroke-width="2" marker-end="url(#ir)"/>
  <line x1="160" y1="74" x2="468" y2="74" stroke="#dc2626" stroke-width="1.6" opacity="0.5" marker-end="url(#ir)"/>
  <line x1="160" y1="74" x2="638" y2="74" stroke="#dc2626" stroke-width="1.6" opacity="0.5" marker-end="url(#ir)"/>
  <text x="430" y="128" text-anchor="middle" fill="#b91c1c" font-size="12.5" font-weight="700">3 recursos diferentes → repetir cria duplicados</text>
  <line x1="30" y1="150" x2="830" y2="150" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="30" y="186" fill="#16a34a" font-size="14" font-weight="700">PUT /tarefas/7 — repetido 3× · idempotente</text>
  <rect x="30" y="204" width="130" height="56" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/>
  <text x="95" y="228" text-anchor="middle" fill="#7c4a03" font-size="14" font-weight="700">PUT ×3</text>
  <text x="95" y="248" text-anchor="middle" fill="#c2740a" font-size="11">no mesmo item</text>
  <rect x="470" y="204" width="220" height="56" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="580" y="228" text-anchor="middle" fill="#14532d" font-size="13.5" font-weight="700">Tarefa #7</text><text x="580" y="248" text-anchor="middle" fill="#16a34a" font-size="11.5">titulo = X (o mesmo)</text>
  <line x1="160" y1="216" x2="468" y2="216" stroke="#16a34a" stroke-width="2" marker-end="url(#ig)"/>
  <line x1="160" y1="232" x2="468" y2="232" stroke="#16a34a" stroke-width="2" marker-end="url(#ig)"/>
  <line x1="160" y1="248" x2="468" y2="248" stroke="#16a34a" stroke-width="2" marker-end="url(#ig)"/>
  <text x="430" y="292" text-anchor="middle" fill="#16a34a" font-size="12.5" font-weight="700">sempre o MESMO recurso, mesmo estado → seguro repetir (retentativa)</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> apertar o botão de <strong>chamar o elevador</strong> 3× não chama 3 elevadores (idempotente); <strong>enviar um formulário</strong> 3× cria 3 pedidos (não idempotente). Por isso só se pode <strong>repetir sozinho</strong> o que é idempotente.</div>

---

## Conceito 3/3 — OpenAPI: a documentação que não envelhece

- Uma boa API REST precisa de um **contrato** para quem vai consumi-la.
- Com o **FastAPI**, esse contrato — no padrão **OpenAPI** — é **gerado automaticamente** a partir dos **tipos declarados no código**, numa **página interativa** (`/docs`).
- Como **nasce do próprio código**, a documentação **não desatualiza** — o problema crônico da era SOAP, em que contrato e implementação viviam divergindo.

<div class="dica">💡 Você escreve os tipos uma vez; o FastAPI valida a entrada, gera o <code>/docs</code> e mantém tudo em sincronia.</div>

---

## A documentação nasce do código

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="dc" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker></defs>
  <rect x="24" y="34" width="348" height="210" rx="12" fill="#0f172a"/>
  <text x="44" y="60" fill="#94a3b8" font-size="12" font-weight="700" font-family="Consolas,monospace">seu código · app.py</text>
  <text x="44" y="92" fill="#7dd3fc" font-size="13" font-family="Consolas,monospace">class Tarefa(BaseModel):</text>
  <text x="64" y="114" fill="#e2e8f0" font-size="13" font-family="Consolas,monospace">titulo: str</text>
  <text x="44" y="150" fill="#c4b5fd" font-size="13" font-family="Consolas,monospace">@app.post("/tarefas", 201)</text>
  <text x="44" y="172" fill="#7dd3fc" font-size="13" font-family="Consolas,monospace">def criar(t: Tarefa):</text>
  <text x="64" y="194" fill="#e2e8f0" font-size="13" font-family="Consolas,monospace">...</text>
  <text x="44" y="226" fill="#94a3b8" font-size="11.5" font-family="Consolas,monospace">os TIPOS declarados ↑</text>
  <line x1="378" y1="139" x2="470" y2="139" stroke="#12437f" stroke-width="2.5" marker-end="url(#dc)"/>
  <text x="424" y="126" text-anchor="middle" fill="#0d2b57" font-size="12.5" font-weight="700">FastAPI</text>
  <text x="424" y="160" text-anchor="middle" fill="#64748b" font-size="11">lê os tipos</text>
  <rect x="480" y="34" width="356" height="210" rx="12" fill="#fff" stroke="#12437f" stroke-width="2"/>
  <rect x="482" y="36" width="352" height="34" rx="10" fill="#12437f"/>
  <text x="500" y="58" fill="#fff" font-size="13" font-weight="700">/docs · API de Tarefas</text>
  <rect x="500" y="86" width="70" height="30" rx="6" fill="#12437f"/><text x="535" y="106" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">GET</text>
  <text x="586" y="106" fill="#0d2b57" font-size="13" font-family="Consolas,monospace">/tarefas</text>
  <rect x="500" y="126" width="70" height="30" rx="6" fill="#16a34a"/><text x="535" y="146" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">POST</text>
  <text x="586" y="146" fill="#0d2b57" font-size="13" font-family="Consolas,monospace">/tarefas</text>
  <rect x="500" y="166" width="70" height="30" rx="6" fill="#12437f"/><text x="535" y="186" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">GET</text>
  <text x="586" y="186" fill="#0d2b57" font-size="13" font-family="Consolas,monospace">/tarefas/{tid}</text>
  <rect x="700" y="206" width="120" height="28" rx="14" fill="#dbeafe" stroke="#60a5fa" stroke-width="1.5"/><text x="760" y="225" text-anchor="middle" fill="#12437f" font-size="11.5" font-weight="700">Try it out ▶</text>
  <text x="430" y="284" text-anchor="middle" fill="#64748b" font-size="12.5">você não escreveu documentação — ela nasceu dos <tspan fill="#334155" font-weight="700">tipos</tspan>; muda o código → muda o /docs</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> a bula já sai <strong>impressa do próprio remédio</strong>. Como o <code>/docs</code> vem dos tipos do código, ele <strong>nunca fica desatualizado</strong> — o velho problema do WSDL/SOAP, em que a doc vivia divergindo.</div>

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
3. **Escreva 3 testes** (use `TestClient` do FastAPI): criar (201), listar (200), buscar id inexistente (404).
4. Confirme no **`/docs`** que as novas rotas aparecem **sozinhas**.

<div class="dica">🧰 <strong>Modelo pronto:</strong> <code>exemplos/aula05/test_api_EXEMPLO.py</code> tem o <strong>1º teste feito</strong> + 2 <code>#&nbsp;TODO</code>. Instale <code>pip install pytest httpx</code> e rode <code>pytest -v</code>.</div>

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

<a class="proximo" href="aula-04-rpc-grpc.html">← Anterior<small>Aula 4 · gRPC</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
<a class="proximo" href="aula-06-ia-como-servico-ead.html">Próxima aula →<small>Aula 6 · IA como serviço (EAD)</small></a>
