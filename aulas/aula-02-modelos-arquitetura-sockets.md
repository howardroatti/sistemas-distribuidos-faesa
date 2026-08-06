---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 2 — Modelos de arquitetura e sockets (TCP/UDP)

C1 · Fundamentos e comunicação distribuída · 13/08/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Retomada — o que você fez em casa

<div class="dica">🔄 A aula começa consolidando a entrega da Aula 1.</div>

- Sua **VM** (ou o Windows nativo) roda **Python** e **Git** sem erro?
- O repositório **`sd-2026-2`** está no GitHub com o primeiro commit?
- Conseguiu rodar `servidor_eco.py` / `cliente_eco.py` e **ver o erro** ao derrubar o servidor?

<div class="aviso">📌 Dúvida sobre a atividade de casa? <strong>É agora o momento de perguntar.</strong></div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Diferenciar** os modelos **cliente-servidor** e **ponto a ponto (P2P)**.
2. **Explicar**, com suas palavras, a diferença prática entre **TCP** e **UDP**.
3. **Escrever** um cliente e um servidor que trocam mensagens por **socket**.

---

## Conceito 1/3 — Cliente-servidor × P2P

<div class="cols">

<div>

**Cliente-servidor**
- Papéis **fixos**: um **pede** (cliente), o outro **responde** (servidor).
- Modelo **dominante** na web.
- Simples de gerenciar e proteger, **mas** concentra carga e é **ponto único de falha**.

</div>

<div>

**Ponto a ponto (P2P)**
- Todos têm o **mesmo papel** e trocam direto, **sem** servidor central.
- Ex.: **BitTorrent** (cada um baixa e envia).
- Distribui carga e não tem centro que caia, **mas** é bem mais difícil de **coordenar e proteger**.

</div>

</div>

<div class="dica">💡 Cliente-servidor tem papéis fixos; em P2P todos fazem os dois papéis. A maioria do que você vai construir é <strong>cliente-servidor</strong>.</div>

---

## Conceito 2/3 — Socket: a ponta do cano

- Toda comunicação em rede passa, por baixo, por **sockets**.
- Um **socket** é a **ponta de uma conexão**, identificada por **IP + porta**: o **IP** diz *em qual máquina*; a **porta** diz *qual programa* dentro dela recebe.
- Por isso um mesmo servidor roda um **site na 443** e um **banco na 5432** sem confusão — cada serviço **escuta a sua porta**.

**O servidor** abre a porta e espera → `bind` · `listen` · `accept`
**O cliente** se conecta àquela porta → `connect` · e então os dois **trocam bytes**.

<div class="dica">💡 Tudo que vem depois no curso — <strong>gRPC, REST, filas</strong> — roda sobre essa base.</div>

---

## Conceito 3/3 — TCP × UDP: garantia × velocidade

<div class="cols">

<div>

**TCP** — garantia
- **Cria conexão** antes de enviar.
- **Garante** entrega **e ordem**; **retransmite** o que se perde.
- Custa **tempo** e pacotes de controle.
- Use quando **não pode perder**: arquivo, chat, **transação bancária**.

</div>

<div>

**UDP** — velocidade
- **Sem conexão**, **não garante** nada.
- **Rápido e leve**; pode **perder** e **desordenar**.
- Sua aplicação lida com isso.
- Use quando **atraso é pior que perda**: **voz, vídeo ao vivo, jogo, telemetria**.

</div>

</div>

<div class="dica">💡 Regra prática: <strong>TCP</strong> quando receber tudo, na ordem, importa mais que a pressa; <strong>UDP</strong> quando é melhor descartar um quadro atrasado do que travar esperando por ele.</div>

---

<!-- _class: secao -->

# Laboratório
### Servidor de eco em TCP — passo a passo

---

## Lab · Passo 1 — o servidor (`servidor_eco.py`)

```python
import socket

HOST, PORT = "127.0.0.1", 5000               # localhost + porta escolhida

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reusar a porta
s.bind((HOST, PORT))                          # reserva o endereço
s.listen()                                    # passa a ESCUTAR
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

conexao, endereco = s.accept()                # ACEITA um cliente (bloqueia)
print(f"[servidor] cliente conectado: {endereco}", flush=True)
while True:
    dado = conexao.recv(1024)                 # RECEBE bytes
    if not dado:                              # cliente fechou → sai
        break
    print(f"[servidor] recebi: {dado.decode()}", flush=True)
    conexao.sendall(dado)                     # ECO: devolve o mesmo
conexao.close()
```

---

## Lab · Passo 2 — o cliente (`cliente_eco.py`)

```python
import socket

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP
s.connect((HOST, PORT))                        # CONECTA no servidor
print("Conectado. Digite mensagens (ou 'sair'):")
while True:
    msg = input("> ")
    if msg == "sair":
        break
    s.sendall(msg.encode())                    # ENVIA bytes
    eco = s.recv(1024)                         # RECEBE o eco
    print("eco:", eco.decode())
s.close()
```

<div class="dica">💡 Note a simetria: o servidor faz <code>bind/listen/accept</code> e o cliente faz <code>connect</code>; depois <strong>os dois</strong> usam <code>send</code>/<code>recv</code>.</div>

---

## Da demo (Aula 1) ao lab (Aula 2)

Os scripts têm o **mesmo esqueleto de socket**, mas propósitos diferentes:

<div class="cols">

<div>

**Demo da Aula 1 — ver a falha**
- Cliente manda **uma** mensagem fixa (`"oi"`).
- Servidor **finge processar** (`time.sleep(15)`) para você **derrubá-lo** no meio.
- Cliente tem **`settimeout`** + **`try/except`** só para **observar** o erro.

</div>

<div>

**Lab da Aula 2 — o eco funcional**
- Cliente **interativo** (`input`), envia **várias** mensagens até `sair`.
- Servidor em **`while True`** ecoa mensagem após mensagem (sem `sleep`).
- **Sem** timeout e **sem** tratamento de erro — o **caminho feliz**.

</div>

</div>

<div class="aviso">⚠️ O <code>timeout</code> e o tratamento de falha <strong>voltam na Aula 11 (resiliência)</strong>. Por isso o <strong>Passo 4</strong> derruba o servidor: você reencontra a <strong>falha parcial</strong>, agora no <strong>seu</strong> eco.</div>

---

## Lab · Passo 3 — rodar (dois terminais)

**Terminal 1 — servidor:**
```powershell
cd $HOME\Documents\sd-2026-2
python servidor_eco.py
# [servidor] ouvindo em 127.0.0.1:5000
```

**Terminal 2 — cliente:**
```powershell
cd $HOME\Documents\sd-2026-2
python cliente_eco.py
# Conectado. Digite mensagens (ou 'sair'):
> ola mundo
eco: ola mundo
```

<div class="dica">💡 No VS Code, abra <strong>dois terminais</strong> (menu Terminal → <em>Split Terminal</em>) e rode um em cada.</div>

---

## Lab · Passo 4 — o experimento

Com o **cliente conectado**, volte ao **Terminal 1** e **derrube o servidor** com `Ctrl + C`. Depois, no cliente, **envie outra mensagem**.

- O que acontece com o cliente?
- Ele **avisa** claramente que o servidor caiu, ou só **falha ao esperar**?

<div class="aviso">⚠️ É a <strong>falha parcial</strong> da Aula 1, agora no seu código: do lado do cliente, "o servidor caiu" e "o servidor está lento" chegam do <strong>mesmo jeito</strong>. Guarde isso — na fase de resiliência vamos tratar com <strong>tempo-limite + nova tentativa</strong>.</div>

---

## Lab · Checkpoints & problemas comuns (Windows)

<div class="cols">

<div>

**✅ O que você deve ver**
- Servidor: `ouvindo em 127.0.0.1:5000`.
- Cliente: cada `> mensagem` volta como `eco: mensagem`.
- Entrega: `servidor_eco.py` + `cliente_eco.py` **commitados**.

</div>

<div>

**🛠️ Se der erro**
- `python` não encontrado → use **`py`**.
- `[WinError 10048]` (porta ocupada) → troque a porta (ex.: 5001) ou feche o outro processo.
- `[WinError 10054]` (conexão resetada) → é o **servidor que caiu** (o experimento!).
- Prompt do **Firewall** → como usamos `127.0.0.1`, normalmente nem aparece; se aparecer, permita em rede privada.

</div>

</div>

---

## Atividade para casa — UDP e comparação

1. **Reescreva** o eco em **UDP**: use `socket.SOCK_DGRAM`; **não há** `listen/accept/connect`. Troque `send`/`recv` por **`sendto`/`recvfrom`** (que já trazem o endereço do remetente).
2. **Meça** o tempo de ida e volta (*round-trip*) de **100 mensagens** em **TCP** e depois em **UDP**.
3. **Escreva 5 linhas** em `medicao.md` comparando os dois resultados que você **mediu**.
4. **Commit e push.**

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> <code>eco_udp.py</code> + <code>medicao.md</code> com a comparação TCP × UDP.</div>

<div class="dica">💡 Dica de medição: use <code>time.perf_counter()</code> antes e depois do laço de 100 mensagens e divida pela quantidade.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Modelo **cliente-servidor** comparado ao **P2P**.
- **Características de TCP e UDP** e o **critério** para escolher entre eles.
- Conceito de **socket, porta e endereçamento**.
- **Camadas do modelo TCP/IP** e encapsulamento.

**Termos-chave:** Cliente-servidor · P2P · Socket · Porta · TCP · UDP

<div class="dica">💡 Um dos tópicos <strong>mais cobrados</strong>: espere cenários (streaming, transferência de arquivo, telemetria) que pedem a escolha <strong>justificada</strong> entre TCP e UDP.</div>

---

## Questão de autoavaliação (estilo ENADE)

Uma aplicação de **voz sobre IP** prioriza **baixa latência** e **tolera a perda ocasional** de pequenos trechos de áudio. Qual protocolo de transporte é o mais adequado e por quê?

A) TCP, porque garante a entrega ordenada de todos os pacotes.
B) TCP, porque realiza controle de fluxo e congestionamento.
C) UDP, porque não retransmite pacotes perdidos, evitando o atraso acumulado.
D) UDP, porque confirma o recebimento de cada pacote enviado.
E) UDP, porque estabelece conexão prévia e reduz a latência.

---

## Resolução — alternativa **C**

- Em **mídia de tempo real**, o **atraso é pior que a perda**: o **UDP não retransmite** e mantém o **fluxo fluido**.
- **D** e **E** descrevem o UDP **incorretamente** — ele **não** confirma recebimento nem **estabelece conexão**.
- **A** e **B** trazem garantias do TCP, que aqui **atrapalhariam** (retransmissão = atraso acumulado).

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 4 — Comunicação entre processos.
- Documentação oficial do módulo **`socket`** do Python.
- **Refaça o desenho** do diagnóstico da Aula 1, agora com os **nomes corretos** (socket, porta, TCP…).

</div>

<div>

**Glossário**
- **Socket:** ponta de conexão (IP + porta).
- **Porta:** número que diz qual programa recebe.
- **TCP:** com conexão; garante entrega e ordem.
- **UDP:** sem conexão; rápido, sem garantias.
- **P2P:** todos com o mesmo papel.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Entregue `eco_udp.py` + `medicao.md`. A Aula 3 começa revendo isto.

**Próxima:** Concorrência — **um servidor para vários clientes** (threads).
