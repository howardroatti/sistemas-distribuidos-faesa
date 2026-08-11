---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 4 — Do RPC ao gRPC: chamada remota moderna

C1 · Fundamentos e comunicação distribuída · 27/08/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — a trilha do semestre

<div class="cols">

<div>

**C1 · Fundamentos e comunicação** (Aulas 1–7)
Sockets, concorrência, **gRPC**, REST e IA como serviço.

**C2 · Coordenação e consistência** (Aulas 8–12)
Mensageria, relógios lógicos, **CAP**, **Raft**, resiliência.

</div>

<div>

**C3 · Nuvem, implantação e segurança** (Aulas 13–18)
Containers, nuvem, serverless, observabilidade, segurança.

<div class="dica">📍 Você está na <strong>Aula 4</strong> — subindo o nível de abstração da comunicação.</div>

</div>

</div>

---

## Retomada — o que você fez em casa

<div class="dica">🔄 A aula começa consolidando a entrega da Aula 3.</div>

- Você escreveu o **`carga.py`** e disparou **N clientes** contra o servidor multicliente?
- O **`relatorio_concorrencia.md`** mostrou **onde o single-thread trava** conforme a carga cresce?
- Confirmou que **uma thread por cliente** aguenta muito mais que o servidor sequencial?

<div class="aviso">📌 Até aqui você trocou <strong>bytes crus</strong> no socket. Hoje vamos fazer uma função em <strong>outra máquina</strong> parecer uma <strong>chamada local</strong>.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** a ideia de **chamada remota de procedimento (RPC)**.
2. **Escrever** um contrato **`.proto`** com Protocol Buffers.
3. **Implementar** um **servidor** e um **cliente gRPC** em Python.

---

## Conceito 1/3 — A ideia do RPC

- **RPC** (*Remote Procedure Call*) nasceu de um desejo simples: fazer uma função que está em **outra máquina** parecer uma **função local**.
- Em vez de escrever bytes no socket e interpretá-los na mão, você chama `servico.somar(2, 3)` — e o **middleware** (a camada entre a sua aplicação e a rede) **empacota** os argumentos, envia, recebe o resultado e devolve.
- Linha do tempo: **RPC clássico → CORBA → RMI** (Invocação de Métodos Remotos do Java) **→ gRPC** (hoje).

<div class="dica">💡 É <strong>transparência de acesso</strong> em ação (Aula 1): usar o remoto <strong>como se fosse local</strong>. A ementa fala de <strong>RPC e RMI</strong> — tratamos ambos como a origem do gRPC.</div>

---

## Conceito 2/3 — O contrato: `.proto` (Protocol Buffers)

- Para trafegar na rede, uma estrutura vira **sequência de bytes** e é remontada do outro lado — isso é a **serialização**.
- No gRPC, o **formato** e o **contrato** do serviço ficam num arquivo **`.proto`** (**Protocol Buffers**): você declara **quais operações** o serviço oferece e **quais mensagens** trafegam (campos e tipos).
- Uma ferramenta lê o `.proto` e **gera o código** de cliente e servidor — os **stubs**, que escondem a rede e fazem a chamada remota **parecer local**.

<div class="aviso">⚠️ A inversão importante: <strong>o contrato existe ANTES do código</strong>, e os dois lados são <strong>obrigados a respeitá-lo</strong>. Muda o contrato → regera os stubs → os dois lados se atualizam.</div>

---

## Conceito 3/3 — Por que gRPC é usado hoje

<div class="cols">

<div>

**Três motivos**
1. **Binário compacto** — o Protocol Buffers trafega **muito menos bytes** que JSON/XML.
2. **HTTP/2** — várias chamadas na **mesma conexão**, sem reabrir a cada pedido.
3. **Contrato tipado** — erros de tipo aparecem **cedo** (na geração dos stubs), não em produção.

</div>

<div>

**Onde usar**
- **Interno** (serviço ↔ serviço, microsserviços de IA): **gRPC** vence.
- **Externo** (público consumindo): **REST** costuma vencer pela **simplicidade** — é a **próxima aula**.

</div>

</div>

<div class="dica">💡 Guarde: <strong>gRPC para dentro</strong>, <strong>REST para fora</strong>. Seu serviço de IA vai ter as duas interfaces.</div>

---

<!-- _class: secao -->

# Laboratório
### Seu primeiro serviço gRPC — passo a passo

---

## Lab · Passo 1 — o contrato `servico.proto`

```proto
syntax = "proto3";

package calculadora;

service Calculadora {
  rpc Somar (Operandos) returns (Resultado);   // a operação remota
}

message Operandos {        // o que o cliente ENVIA
  int32 a = 1;             // o "= 1" é a posição do campo no formato binário
  int32 b = 2;
}

message Resultado {        // o que o servidor DEVOLVE
  int32 valor = 1;
}
```

<div class="dica">💡 Isto é <strong>só o contrato</strong> — nenhuma lógica ainda. Os números (<code>= 1</code>, <code>= 2</code>) identificam o campo nos bytes, <strong>não</strong> são valores.</div>

---

## Lab · Passo 2 — gerar os stubs

No terminal, na pasta do `.proto`, rode o **protoc** (vem no `grpcio-tools`):

```powershell
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
```

Isso **gera dois arquivos** (não edite!):
- **`servico_pb2.py`** — as mensagens (`Operandos`, `Resultado`).
- **`servico_pb2_grpc.py`** — os **stubs** de cliente e servidor.

<div class="aviso">⚠️ Toda vez que você <strong>mudar o <code>.proto</code></strong>, rode este comando de novo para <strong>regerar</strong> os stubs. É o contrato mandando no código.</div>

---

## Lab · Passo 3 — `servidor_grpc.py`

```python
import grpc
from concurrent import futures
import servico_pb2, servico_pb2_grpc

class CalculadoraServicer(servico_pb2_grpc.CalculadoraServicer):
    def Somar(self, request, context):           # implementa a operação
        return servico_pb2.Resultado(valor=request.a + request.b)

servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # threads da Aula 3!
servico_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicer(), servidor)
servidor.add_insecure_port("127.0.0.1:50051")
servidor.start()
print("[servidor gRPC] ouvindo em 127.0.0.1:50051", flush=True)
servidor.wait_for_termination()
```

<div class="dica">💡 Repare no <code>ThreadPoolExecutor</code>: o gRPC atende vários clientes com o <strong>pool de threads</strong> que você estudou na Aula 3.</div>

---

## Lab · Passo 4 — `cliente_grpc.py` e rodar

```python
import grpc
import servico_pb2, servico_pb2_grpc

with grpc.insecure_channel("127.0.0.1:50051") as canal:
    stub = servico_pb2_grpc.CalculadoraStub(canal)
    resposta = stub.Somar(servico_pb2.Operandos(a=2, b=3))   # parece local!
    print("2 + 3 =", resposta.valor)
```

**Dois terminais:**
```powershell
python servidor_grpc.py     # Terminal 1 → ouvindo em 50051
python cliente_grpc.py      # Terminal 2 → 2 + 3 = 5
```

<div class="dica">💡 <code>stub.Somar(...)</code> é uma <strong>chamada de rede</strong> disfarçada de chamada de função. O middleware do gRPC cuidou de tudo.</div>

---

## Lab · Checkpoints & problemas comuns (Windows)

<div class="cols">

<div>

**✅ O que você deve ver**
- `protoc` cria `servico_pb2.py` e `servico_pb2_grpc.py`.
- Servidor: `ouvindo em 127.0.0.1:50051`.
- Cliente: `2 + 3 = 5`.

</div>

<div>

**🛠️ Se der erro**
- `ModuleNotFoundError: servico_pb2` → você não gerou os stubs (Passo 2) ou está em outra pasta.
- `No module named grpc` → falta `pip install grpcio grpcio-tools`.
- Porta ocupada → troque `50051` por outra.
- Mudou o `.proto` e nada mudou? **Regere os stubs.**

</div>

</div>

---

## No seu trabalho — C1.A2

- Uma das **duas interfaces** exigidas pelo C1.A2 é **gRPC**. Com o `.proto` e os stubs desta aula, você **implementa o método** do serviço.

<div class="dica">💡 Puxa direto para o kit:
<br>• <strong>TAREFA 4</strong> — implementar o método gRPC <code>PreverLote</code> e <strong>regerar os stubs</strong>.
<br>Repositório: <code>sd-2026-2-kit-c1a2</code> (o <code>.proto</code> já está lá, em <code>proto/</code>).</div>

---

## Atividade para casa — ampliar o contrato

1. **Adicione um segundo método** ao `servico.proto` — por exemplo `Multiplicar (Operandos) returns (Resultado)`.
2. **Regere os stubs** (Passo 2) e **implemente** o novo método no servidor.
3. **Chame os dois** métodos pelo cliente e confira os resultados.
4. **Escreva um `README.md`** explicando **o que acontece se você mudar o contrato** (renomear um campo, trocar um tipo): por que os **dois lados** precisam regerar os stubs.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> serviço gRPC com <strong>2 métodos</strong> + <code>README</code> sobre o <strong>impacto de mudar o contrato</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Conceito de **RPC** e **transparência de acesso**.
- **RMI** e invocação de métodos remotos.
- **Serialização** e representação de dados na rede.
- **Middleware** de comunicação e **stubs**.

**Termos-chave:** RPC · RMI · gRPC · Protocol Buffers · Stub · Serialização · Middleware

<div class="dica">💡 A serialização (converter estruturas em bytes) costuma aparecer junto, assim como a comparação <strong>gRPC × outras formas de integração</strong> (REST, mensageria).</div>

---

## Questão de autoavaliação (estilo ENADE)

No gRPC, qual é a função do arquivo com extensão **`.proto`**?

A) Conter a **implementação completa** do servidor.
B) **Definir o contrato** (mensagens e operações), a partir do qual se **geram os stubs**.
C) Ser **gerado automaticamente** após a implementação do servidor.
D) **Eliminar** a necessidade de comunicação em rede.
E) Armazenar as **credenciais** de autenticação do serviço.

---

## Resolução — alternativa **B**

- O `.proto` é o **contrato** e vem **antes** do código; a ferramenta **gera**, a partir dele, os **stubs** de cliente e de servidor.
- **C** inverte a ordem (o `.proto` não é gerado — ele **é a origem**).
- **A**, **D** e **E** descrevem coisas que o `.proto` **não** faz (implementação, eliminar a rede, credenciais).

<div class="dica">💡 É o seu <code>servico.proto</code> de hoje virando questão de prova.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 5 — Invocação remota (RPC/RMI).
- Documentação oficial do **gRPC** (Python) e do **Protocol Buffers**.
- Abra o `proto/` do **kit da C1** e leia o contrato já pronto.

</div>

<div>

**Glossário**
- **RPC:** invocar uma função que está em outra máquina.
- **gRPC:** RPC atual, binário, sobre HTTP/2, contrato em `.proto`.
- **Protocol Buffers:** formato binário que define o contrato.
- **Stub:** código gerado que representa o serviço remoto.
- **Middleware:** camada que cuida da comunicação distribuída.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Entregue o serviço gRPC com 2 métodos + README. A Aula 5 começa revendo isto.

<a class="proximo" href="aula-03-concorrencia-multiplos-clientes.html">← Anterior<small>Aula 3 · Concorrência</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
<a class="proximo" href="aula-05-rest-openapi-fastapi.html">Próxima aula →<small>Aula 5 · REST / FastAPI</small></a>
