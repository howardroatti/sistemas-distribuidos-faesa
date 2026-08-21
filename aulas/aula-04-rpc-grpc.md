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

## A chamada remota, passo a passo

<svg viewBox="0 0 880 320" role="img" style="width:100%;max-width:880px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="rq" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="rs" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker>
    <marker id="gy" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
  <line x1="70" y1="82" x2="795" y2="82" stroke="#12437f" stroke-width="2.5" marker-end="url(#rq)"/>
  <text x="430" y="72" text-anchor="middle" fill="#12437f" font-size="13.5" font-weight="700">chamada: Somar(2, 3) — você escreve como se fosse local</text>
  <rect x="20" y="100" width="150" height="118" rx="12" fill="#eef4fb" stroke="#12437f" stroke-width="2.5"/>
  <text x="95" y="128" text-anchor="middle" fill="#0d2b57" font-size="15" font-weight="700">Cliente</text>
  <text x="95" y="156" text-anchor="middle" fill="#12437f" font-size="12.5" font-family="Consolas,monospace">stub.Somar</text>
  <text x="95" y="174" text-anchor="middle" fill="#12437f" font-size="12.5" font-family="Consolas,monospace">(2, 3)</text>
  <text x="95" y="200" text-anchor="middle" fill="#64748b" font-size="11">parece local</text>
  <rect x="190" y="118" width="110" height="82" rx="10" fill="#dbeafe" stroke="#60a5fa" stroke-width="2"/>
  <text x="245" y="150" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">stub</text>
  <text x="245" y="172" text-anchor="middle" fill="#334155" font-size="11.5">serializa</text>
  <rect x="322" y="118" width="150" height="82" rx="10" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 3"/>
  <text x="397" y="150" text-anchor="middle" fill="#334155" font-size="13.5" font-weight="700">REDE</text>
  <text x="397" y="172" text-anchor="middle" fill="#64748b" font-size="11.5">HTTP/2</text>
  <rect x="494" y="118" width="110" height="82" rx="10" fill="#dbeafe" stroke="#60a5fa" stroke-width="2"/>
  <text x="549" y="150" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">stub</text>
  <text x="549" y="172" text-anchor="middle" fill="#334155" font-size="11.5">desserializa</text>
  <rect x="626" y="100" width="234" height="118" rx="12" fill="#eef4fb" stroke="#12437f" stroke-width="2.5"/>
  <text x="743" y="128" text-anchor="middle" fill="#0d2b57" font-size="15" font-weight="700">Servidor</text>
  <text x="743" y="158" text-anchor="middle" fill="#12437f" font-size="12.5" font-family="Consolas,monospace">Somar(a, b):</text>
  <text x="743" y="178" text-anchor="middle" fill="#12437f" font-size="12.5" font-family="Consolas,monospace">return a + b</text>
  <line x1="170" y1="159" x2="188" y2="159" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#gy)"/>
  <line x1="300" y1="159" x2="320" y2="159" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#gy)"/>
  <line x1="472" y1="159" x2="492" y2="159" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#gy)"/>
  <line x1="604" y1="159" x2="624" y2="159" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#gy)"/>
  <line x1="795" y1="250" x2="70" y2="250" stroke="#16a34a" stroke-width="2.5" marker-end="url(#rs)"/>
  <text x="430" y="272" text-anchor="middle" fill="#16a34a" font-size="13.5" font-weight="700">resposta: 5 — o middleware trouxe de volta</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> o <strong>stub</strong> é o <strong>garçom</strong>. Você pede "a soma de 2 e 3" na mesa; ele leva à cozinha (servidor) e volta com o prato (5). Você nunca entra na cozinha nem vê o caminho.</div>

---

## Conceito 2/3 — O contrato: `.proto` (Protocol Buffers)

- Para trafegar na rede, uma estrutura vira **sequência de bytes** e é remontada do outro lado — isso é a **serialização**.
- No gRPC, o **formato** e o **contrato** do serviço ficam num arquivo **`.proto`** (**Protocol Buffers**): você declara **quais operações** o serviço oferece e **quais mensagens** trafegam (campos e tipos).
- Uma ferramenta lê o `.proto` e **gera o código** de cliente e servidor — os **stubs**, que escondem a rede e fazem a chamada remota **parecer local**.

<div class="aviso">⚠️ A inversão importante: <strong>o contrato existe ANTES do código</strong>, e os dois lados são <strong>obrigados a respeitá-lo</strong>. Muda o contrato → regera os stubs → os dois lados se atualizam.</div>

---

## O contrato manda: uma fonte, dois lados

<svg viewBox="0 0 860 336" role="img" style="width:100%;max-width:820px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="p1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
  <marker id="p1g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <rect x="330" y="20" width="200" height="60" rx="12" fill="#12437f"/>
  <text x="430" y="46" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">servico.proto</text>
  <text x="430" y="66" text-anchor="middle" fill="#bcd3f0" font-size="12">o contrato (vem antes)</text>
  <line x1="430" y1="80" x2="430" y2="120" stroke="#12437f" stroke-width="2.2" marker-end="url(#p1)"/>
  <text x="508" y="105" text-anchor="middle" fill="#334155" font-size="12.5" font-weight="700">protoc gera</text>
  <rect x="250" y="124" width="360" height="70" rx="12" fill="#eef4fb" stroke="#60a5fa" stroke-width="2"/>
  <rect x="266" y="138" width="160" height="42" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="346" y="158" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">servico_pb2</text>
  <text x="346" y="173" text-anchor="middle" fill="#64748b" font-size="11">mensagens</text>
  <rect x="434" y="138" width="160" height="42" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="514" y="158" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">servico_pb2_grpc</text>
  <text x="514" y="173" text-anchor="middle" fill="#64748b" font-size="11">stubs</text>
  <line x1="330" y1="196" x2="182" y2="256" stroke="#94a3b8" stroke-width="2" marker-end="url(#p1g)"/>
  <line x1="530" y1="196" x2="678" y2="256" stroke="#94a3b8" stroke-width="2" marker-end="url(#p1g)"/>
  <rect x="60" y="262" width="220" height="64" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="170" y="290" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Cliente</text>
  <text x="170" y="310" text-anchor="middle" fill="#16a34a" font-size="12">usa o stub</text>
  <rect x="580" y="262" width="220" height="64" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="690" y="290" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Servidor</text>
  <text x="690" y="310" text-anchor="middle" fill="#16a34a" font-size="12">implementa o servicer</text>
  <text x="430" y="238" text-anchor="middle" fill="#b91c1c" font-size="12.5" font-weight="700">muda o .proto → regera → os dois lados se atualizam</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> o <code>.proto</code> é o <strong>cardápio</strong> acordado entre salão e cozinha. Os dois seguem o mesmo cardápio; mudou um prato, <strong>os dois recebem a nova versão</strong> — ninguém inventa por conta própria.</div>

---

## Serialização — e por que o binário é menor

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="s1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <rect x="30" y="30" width="150" height="60" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="105" y="55" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">objeto</text>
  <text x="105" y="76" text-anchor="middle" fill="#334155" font-size="12" font-family="Consolas,monospace">a=2, b=3</text>
  <line x1="180" y1="60" x2="238" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#s1)"/>
  <text x="209" y="49" text-anchor="middle" fill="#64748b" font-size="11">serializa</text>
  <rect x="242" y="30" width="180" height="60" rx="10" fill="#0f172a"/>
  <text x="332" y="55" text-anchor="middle" fill="#38bdf8" font-size="13" font-family="Consolas,monospace" font-weight="700">08 02 10 03</text>
  <text x="332" y="76" text-anchor="middle" fill="#94a3b8" font-size="11">bytes na rede</text>
  <line x1="422" y1="60" x2="480" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#s1)"/>
  <text x="451" y="49" text-anchor="middle" fill="#64748b" font-size="11">desserializa</text>
  <rect x="484" y="30" width="150" height="60" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="559" y="55" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">objeto</text>
  <text x="559" y="76" text-anchor="middle" fill="#334155" font-size="12" font-family="Consolas,monospace">a=2, b=3</text>
  <text x="700" y="52" fill="#16a34a" font-size="12.5" font-weight="700">mesma</text>
  <text x="700" y="70" fill="#16a34a" font-size="12.5" font-weight="700">informação</text>
  <text x="30" y="140" fill="#0d2b57" font-size="14" font-weight="700">Os mesmos dados, dois tamanhos:</text>
  <text x="30" y="182" fill="#334155" font-size="13" font-weight="700">JSON (texto)</text>
  <rect x="180" y="166" width="470" height="26" rx="5" fill="#e08a00"/>
  <text x="190" y="184" fill="#fff" font-size="12.5" font-family="Consolas,monospace">{"a":2,"b":3}</text>
  <text x="662" y="184" fill="#c2740a" font-size="12.5" font-weight="700">~13 bytes</text>
  <text x="30" y="230" fill="#334155" font-size="13" font-weight="700">Protobuf (binário)</text>
  <rect x="180" y="214" width="145" height="26" rx="5" fill="#12437f"/>
  <text x="190" y="232" fill="#fff" font-size="12.5" font-family="Consolas,monospace">08 02 10 03</text>
  <text x="337" y="232" fill="#12437f" font-size="12.5" font-weight="700">~4 bytes</text>
  <text x="180" y="268" fill="#64748b" font-size="12">menos bytes → menos rede → mais rápido, principalmente em <tspan fill="#334155" font-weight="700">escala</tspan></text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> o JSON escreve tudo por extenso ("<em>o campo a vale 2</em>"). O Protobuf manda só o <strong>número do campo + valor</strong> ("<em>1: 2</em>"), porque os <strong>dois lados já têm o cardápio</strong> (o <code>.proto</code>) e sabem o que é o campo 1.</div>

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

## gRPC para dentro, REST para fora

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="g1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="r1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#e08a00"/></marker>
  </defs>
  <rect x="320" y="34" width="516" height="256" rx="16" fill="#f8fafc" stroke="#12437f" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="578" y="58" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">seus microsserviços · interno</text>
  <rect x="356" y="140" width="130" height="60" rx="10" fill="#12437f"/>
  <text x="421" y="166" text-anchor="middle" fill="#fff" font-size="13.5" font-weight="700">API Gateway</text>
  <text x="421" y="185" text-anchor="middle" fill="#bcd3f0" font-size="11">fala os dois</text>
  <rect x="560" y="86" width="150" height="58" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="635" y="112" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Serviço IA</text>
  <text x="635" y="131" text-anchor="middle" fill="#64748b" font-size="11">inferência</text>
  <rect x="560" y="196" width="150" height="58" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="635" y="222" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Serviço Dados</text>
  <text x="635" y="241" text-anchor="middle" fill="#64748b" font-size="11">persistência</text>
  <line x1="486" y1="160" x2="558" y2="120" stroke="#12437f" stroke-width="2.2" marker-end="url(#g1)"/>
  <line x1="486" y1="180" x2="558" y2="220" stroke="#12437f" stroke-width="2.2" marker-end="url(#g1)"/>
  <text x="524" y="150" text-anchor="middle" fill="#12437f" font-size="11.5" font-weight="700">gRPC</text>
  <text x="470" y="284" text-anchor="middle" fill="#12437f" font-size="12" font-weight="700">gRPC · binário · rápido</text>
  <rect x="24" y="78" width="140" height="54" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/>
  <text x="94" y="104" text-anchor="middle" fill="#7c4a03" font-size="13.5" font-weight="700">Navegador</text>
  <text x="94" y="122" text-anchor="middle" fill="#c2740a" font-size="11">usuário final</text>
  <rect x="24" y="196" width="140" height="54" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/>
  <text x="94" y="222" text-anchor="middle" fill="#7c4a03" font-size="13.5" font-weight="700">App mobile</text>
  <text x="94" y="240" text-anchor="middle" fill="#c2740a" font-size="11">usuário final</text>
  <line x1="164" y1="108" x2="354" y2="156" stroke="#e08a00" stroke-width="2.2" marker-end="url(#r1)"/>
  <line x1="164" y1="222" x2="354" y2="184" stroke="#e08a00" stroke-width="2.2" marker-end="url(#r1)"/>
  <text x="250" y="150" text-anchor="middle" fill="#c2740a" font-size="11.5" font-weight="700">REST/JSON</text>
  <text x="210" y="300" text-anchor="middle" fill="#c2740a" font-size="12" font-weight="700">REST · JSON · simples</text>
</svg>

<div class="dica">💡 <strong>gRPC para dentro, REST para fora.</strong> Entre os seus serviços, velocidade importa → <strong>gRPC</strong>. Para o mundo consumir, simplicidade importa → <strong>REST</strong> (próxima aula). Seu serviço de IA terá <strong>as duas portas</strong>.</div>

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
