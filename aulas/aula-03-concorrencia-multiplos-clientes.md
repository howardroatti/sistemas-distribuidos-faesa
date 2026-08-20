---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 3 — Concorrência: um servidor para vários clientes

C1 · Fundamentos e comunicação distribuída · 20/08/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — a trilha do semestre

<div class="cols">

<div>

**C1 · Fundamentos e comunicação** (Aulas 1–7)
Sockets, concorrência, gRPC, REST e **IA como serviço**.

**C2 · Coordenação e consistência** (Aulas 8–12)
Mensageria, relógios lógicos, **CAP**, **Raft**, resiliência.

</div>

<div>

**C3 · Nuvem, implantação e segurança** (Aulas 13–18)
Containers, nuvem, serverless, observabilidade, segurança.

<div class="dica">📍 Você está na <strong>Aula 3</strong> — e o problema de hoje volta o semestre inteiro.</div>

</div>

</div>

---

## Retomada — o que você fez em casa

<div class="dica">🔄 A aula começa consolidando a entrega da Aula 2.</div>

- Você reescreveu o eco em **UDP** (`SOCK_DGRAM`, `sendto`/`recvfrom`) e **mediu** 100 mensagens em TCP × UDP?
- O que os seus números mostraram: **UDP mais rápido**, TCP com o custo das **garantias**?
- Entregou `eco_udp.py` + `medicao.md`?

<div class="aviso">📌 Hoje o seu servidor de eco vai deixar de atender <strong>um</strong> cliente e passar a atender <strong>vários ao mesmo tempo</strong>.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** por que um servidor simples atende **apenas um cliente por vez**.
2. **Usar threads** para atender **vários clientes ao mesmo tempo**.
3. **Identificar e corrigir** uma **condição de corrida** em estado compartilhado.

---

## Conceito 1/3 — O problema: o servidor bloqueante

- Chamadas de rede como **`accept()`** e **`recv()`** são **bloqueantes**: param a execução até algo acontecer (uma conexão chegar, um dado ser recebido).
- Num servidor **sequencial**, enquanto ele atende **um** cliente, **todos os outros esperam na fila**.
- Basta **um cliente lento** — ou mal-intencionado — para **travar o atendimento de todos**.
- Para um serviço real, com muitos usuários simultâneos, isso é **inaceitável**.

<div class="aviso">⚠️ É exatamente o seu <code>servidor_eco.py</code> da Aula 2: ele faz <code>accept()</code> de <strong>um</strong> cliente e só volta a aceitar outro quando o primeiro termina.</div>

---

## O gargalo, visualmente — fila única

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:860px;display:block;margin:8px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="a1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <text x="30" y="60" fill="#64748b" font-size="14" font-style="italic">fila de espera ⏳</text>
  <rect x="30" y="120" width="120" height="66" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
  <text x="90" y="150" text-anchor="middle" fill="#334155" font-size="15" font-weight="700">Cliente D</text>
  <text x="90" y="170" text-anchor="middle" fill="#94a3b8" font-size="12">esperando</text>
  <rect x="180" y="120" width="120" height="66" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
  <text x="240" y="150" text-anchor="middle" fill="#334155" font-size="15" font-weight="700">Cliente C</text>
  <text x="240" y="170" text-anchor="middle" fill="#94a3b8" font-size="12">esperando</text>
  <rect x="330" y="120" width="120" height="66" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
  <text x="390" y="150" text-anchor="middle" fill="#334155" font-size="15" font-weight="700">Cliente B</text>
  <text x="390" y="170" text-anchor="middle" fill="#94a3b8" font-size="12">esperando</text>
  <rect x="480" y="120" width="120" height="66" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="540" y="150" text-anchor="middle" fill="#14532d" font-size="15" font-weight="700">Cliente A</text>
  <text x="540" y="170" text-anchor="middle" fill="#16a34a" font-size="12" font-weight="600">atendido</text>
  <line x1="150" y1="153" x2="178" y2="153" stroke="#94a3b8" stroke-width="2" marker-end="url(#a1)"/>
  <line x1="300" y1="153" x2="328" y2="153" stroke="#94a3b8" stroke-width="2" marker-end="url(#a1)"/>
  <line x1="450" y1="153" x2="478" y2="153" stroke="#94a3b8" stroke-width="2" marker-end="url(#a1)"/>
  <line x1="600" y1="153" x2="648" y2="153" stroke="#16a34a" stroke-width="2.5" marker-end="url(#a1)"/>
  <rect x="650" y="110" width="170" height="86" rx="12" fill="#12437f"/>
  <text x="735" y="147" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">servidor</text>
  <text x="735" y="170" text-anchor="middle" fill="#bcd3f0" font-size="12">1 cliente por vez</text>
  <text x="430" y="250" text-anchor="middle" fill="#b91c1c" font-size="14.5" font-weight="600">⚠ um cliente lento na frente → todos os de trás travam</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é um <strong>caixa único</strong> no banco. Enquanto a pessoa da frente resolve tudo, a fila inteira só olha o relógio.</div>

---

## Conceito 2/3 — A solução: uma thread por cliente

- **Concorrência:** transformar cada atendimento em uma **thread** — uma linha de execução independente **dentro do mesmo programa**.
- Ao aceitar uma conexão, o servidor **entrega aquele cliente a uma thread própria** e **volta na hora** para o `accept()`, pronto para o próximo.
- Muitos clientes atendidos ao mesmo tempo; um cliente lento atrapalha **só a própria thread**.

<div class="cols">

<div>

**Concorrência**
Lidar com **várias tarefas em andamento**, revezando o processador.

</div>

<div>

**Paralelismo**
Executá-las **literalmente ao mesmo tempo**, em núcleos diferentes.

</div>

</div>

<div class="dica">💡 Para servidores de rede (que passam o tempo <strong>esperando</strong> a rede), threads são ideais: enquanto uma espera, as outras trabalham.</div>

---

## A vazão com threads, visualmente

<svg viewBox="0 0 860 330" role="img" style="width:100%;max-width:860px;display:block;margin:8px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="a2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="a2g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
  <rect x="40" y="118" width="210" height="100" rx="12" fill="#12437f"/>
  <text x="145" y="156" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">laço accept()</text>
  <text x="145" y="180" text-anchor="middle" fill="#bcd3f0" font-size="12.5">aceita → cria thread</text>
  <text x="145" y="199" text-anchor="middle" fill="#bcd3f0" font-size="12.5">→ volta na hora</text>
  <path d="M60,118 C40,86 62,70 92,70 C124,70 152,84 152,114" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#a2g)"/>
  <text x="106" y="60" text-anchor="middle" fill="#64748b" font-size="11.5" font-style="italic">volta já</text>
  <line x1="250" y1="150" x2="558" y2="72" stroke="#12437f" stroke-width="2.2" marker-end="url(#a2)"/>
  <rect x="560" y="44" width="260" height="58" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="690" y="70" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Thread 1 → Cliente A</text>
  <text x="690" y="90" text-anchor="middle" fill="#16a34a" font-size="12">atende sozinha</text>
  <line x1="250" y1="168" x2="558" y2="168" stroke="#12437f" stroke-width="2.2" marker-end="url(#a2)"/>
  <rect x="560" y="139" width="260" height="58" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="690" y="165" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Thread 2 → Cliente B</text>
  <text x="690" y="185" text-anchor="middle" fill="#16a34a" font-size="12">atende sozinha</text>
  <line x1="250" y1="186" x2="558" y2="264" stroke="#12437f" stroke-width="2.2" marker-end="url(#a2)"/>
  <rect x="560" y="234" width="260" height="58" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="690" y="260" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Thread 3 → Cliente C</text>
  <text x="690" y="280" text-anchor="middle" fill="#16a34a" font-size="12">atende sozinha</text>
  <text x="430" y="320" text-anchor="middle" fill="#334155" font-size="13.5" font-weight="600">todos ao mesmo tempo · um lento afeta só a própria thread</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> agora são <strong>vários caixas</strong> abertos. Chegou cliente → abre um caixa só pra ele; o balcão da entrada nunca para.</div>

---

## Concorrência × Paralelismo — a diferença

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:820px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <text x="30" y="40" fill="#0d2b57" font-size="15" font-weight="700">1 núcleo — concorrência (reveza)</text>
  <text x="820" y="40" text-anchor="end" fill="#64748b" font-size="12.5" font-style="italic">tempo →</text>
  <rect x="120" y="56" width="86" height="40" rx="6" fill="#12437f"/><text x="163" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">A</text>
  <rect x="208" y="56" width="86" height="40" rx="6" fill="#e08a00"/><text x="251" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">B</text>
  <rect x="296" y="56" width="86" height="40" rx="6" fill="#12437f"/><text x="339" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">A</text>
  <rect x="384" y="56" width="86" height="40" rx="6" fill="#e08a00"/><text x="427" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">B</text>
  <rect x="472" y="56" width="86" height="40" rx="6" fill="#12437f"/><text x="515" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">A</text>
  <rect x="560" y="56" width="86" height="40" rx="6" fill="#e08a00"/><text x="603" y="81" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">B</text>
  <text x="120" y="128" fill="#64748b" font-size="12.5">um de cada vez, alternando rápido — <tspan font-weight="700" fill="#334155">parece</tspan> simultâneo</text>
  <line x1="30" y1="160" x2="830" y2="160" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="30" y="196" fill="#0d2b57" font-size="15" font-weight="700">2 núcleos — paralelismo (ao mesmo tempo)</text>
  <text x="60" y="235" fill="#334155" font-size="13" font-weight="700">núcleo 1</text>
  <rect x="130" y="214" width="500" height="34" rx="6" fill="#12437f"/><text x="380" y="237" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">Cliente A</text>
  <text x="60" y="281" fill="#334155" font-size="13" font-weight="700">núcleo 2</text>
  <rect x="130" y="260" width="500" height="34" rx="6" fill="#e08a00"/><text x="380" y="283" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">Cliente B</text>
  <line x1="660" y1="206" x2="660" y2="302" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="675" y="256" fill="#16a34a" font-size="12.5" font-weight="700">mesmo</text>
  <text x="675" y="272" fill="#16a34a" font-size="12.5" font-weight="700">instante</text>
</svg>

<div class="dica">💡 Threads dão <strong>concorrência</strong> sempre; viram <strong>paralelismo</strong> real só quando há <strong>vários núcleos</strong>. Para servidor de rede (que vive <em>esperando</em>), a concorrência já resolve.</div>

---

## Conceito 3/3 — O preço: condição de corrida

- A concorrência resolve um problema e **cria outro**. Se **duas threads alteram a mesma variável ao mesmo tempo**, o resultado fica **imprevisível** — é a **condição de corrida**.
- **Exemplo clássico (contador):** duas threads leem **41**, ambas somam 1 e ambas gravam **42** — quando o certo seria **43**. Uma contagem se perdeu.
- Traiçoeiro: o erro aparece **só às vezes**, dependendo do instante em que as threads se cruzam.

<div class="dica">💡 Proteção: <strong>exclusão mútua</strong> — só <strong>uma thread por vez</strong> executa o trecho que mexe no dado compartilhado (a <strong>seção crítica</strong>), usando um <strong>lock</strong> (trava). Essa ideia volta o semestre inteiro — entre <strong>réplicas de um banco</strong>, não mais entre threads.</div>

---

## A corrida, passo a passo (o que dá errado)

<svg viewBox="0 0 880 424" role="img" style="width:100%;max-width:880px;display:block;margin:0 auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="rb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="ro" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#e08a00"/></marker>
  </defs>
  <rect x="120" y="24" width="180" height="42" rx="10" fill="#12437f"/>
  <text x="210" y="51" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">Thread 1</text>
  <rect x="580" y="24" width="180" height="42" rx="10" fill="#e08a00"/>
  <text x="670" y="51" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">Thread 2</text>
  <text x="440" y="20" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">total (compartilhado)</text>
  <line x1="210" y1="70" x2="210" y2="392" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4 4"/>
  <line x1="670" y1="70" x2="670" y2="392" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4 4"/>
  <line x1="440" y1="70" x2="440" y2="352" stroke="#e2e8f0" stroke-width="2"/>
  <rect x="405" y="88" width="70" height="34" rx="17" fill="#eef4fb" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="440" y="111" text-anchor="middle" fill="#0d2b57" font-size="16" font-weight="700">41</text>
  <rect x="405" y="226" width="70" height="34" rx="17" fill="#eef4fb" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="440" y="249" text-anchor="middle" fill="#0d2b57" font-size="16" font-weight="700">42</text>
  <text x="36" y="110" fill="#94a3b8" font-size="12">t1</text>
  <line x1="405" y1="105" x2="214" y2="105" stroke="#12437f" stroke-width="2.2" marker-end="url(#rb)"/>
  <text x="300" y="96" text-anchor="middle" fill="#12437f" font-size="13" font-weight="600">lê → vê 41</text>
  <text x="36" y="176" fill="#94a3b8" font-size="12">t2</text>
  <line x1="475" y1="171" x2="666" y2="171" stroke="#e08a00" stroke-width="2.2" marker-end="url(#ro)"/>
  <text x="580" y="162" text-anchor="middle" fill="#c2740a" font-size="13" font-weight="600">lê → vê 41</text>
  <text x="440" y="198" text-anchor="middle" fill="#b91c1c" font-size="13" font-weight="700">⚠ os dois leram 41</text>
  <text x="36" y="248" fill="#94a3b8" font-size="12">t3</text>
  <line x1="214" y1="243" x2="401" y2="243" stroke="#12437f" stroke-width="2.2" marker-end="url(#rb)"/>
  <text x="300" y="234" text-anchor="middle" fill="#12437f" font-size="13" font-weight="600">grava 42</text>
  <text x="36" y="312" fill="#94a3b8" font-size="12">t4</text>
  <line x1="666" y1="307" x2="479" y2="307" stroke="#e08a00" stroke-width="2.2" marker-end="url(#ro)"/>
  <text x="580" y="298" text-anchor="middle" fill="#c2740a" font-size="13" font-weight="600">grava 42 (por cima)</text>
  <rect x="326" y="356" width="228" height="54" rx="12" fill="#fee2e2" stroke="#dc2626" stroke-width="2.5"/>
  <text x="440" y="379" text-anchor="middle" fill="#991b1b" font-size="15" font-weight="700">total = 42</text>
  <text x="440" y="399" text-anchor="middle" fill="#dc2626" font-size="12.5" font-weight="600">deveria ser 43 — 1 incremento sumiu</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> dois garçons leem o <strong>mesmo caderno</strong> ("mesa 41"), cada um escreve "42" sem ver o outro. Uma anotação some.</div>

---

<!-- _class: secao -->

# Laboratório
### Servidor que atende vários clientes — passo a passo

---

## Lab · Passo 1 — `servidor_multicliente.py`

```python
import socket, threading
HOST, PORT = "127.0.0.1", 5000

def atender(conexao, endereco):          # roda em uma THREAD por cliente
    print(f"[servidor] {endereco} conectou", flush=True)
    while True:
        dado = conexao.recv(1024)
        if not dado: break
        conexao.sendall(dado)            # eco
    conexao.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)); s.listen()
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)
while True:
    conexao, endereco = s.accept()       # aceita um cliente...
    threading.Thread(target=atender, args=(conexao, endereco),
                     daemon=True).start() # entrega à thread e VOLTA já
```

---

## Lab · Passo 2 — rodar com vários clientes

**Terminal 1 — servidor:**
```powershell
cd $HOME\Documents\sd-2026-2
python servidor_multicliente.py
# [servidor] ouvindo em 127.0.0.1:5000
```

**Terminais 2, 3 e 4 — clientes (abra três!):**
```powershell
python cliente.py
> ola do cliente A
eco: ola do cliente A
```

<div class="dica">💡 No VS Code, use <em>Split Terminal</em> para abrir vários terminais lado a lado. Reaproveite o <code>cliente_eco.py</code> da Aula 2 (renomeie para <code>cliente.py</code>).</div>

---

## Lab · Passo 3 — o experimento que prova o ganho

Com **três clientes conectados ao mesmo tempo**, observe no terminal do servidor as **três linhas de conexão** — ele fala com todos **em paralelo**.

- Compare com o `servidor_eco.py` da Aula 2 (single-thread): abra dois clientes nele e veja o **segundo travar** até o primeiro sair.
- Agora um cliente lento **não** congela os outros — cada um tem a **sua thread**.

<div class="aviso">⚠️ O laço principal <strong>nunca fica preso</strong> num cliente: ele só faz <code>accept()</code> → cria thread → volta ao <code>accept()</code>. O trabalho pesado fica nas threads.</div>

---

## O preço aparece — condição de corrida (`contador.py`)

Duas threads somam **2000 vezes** na **mesma variável**. O `+= 1` é, na real, **ler → somar → gravar**:

```python
import threading, time
total = 0
def soma_muitas():
    global total
    for _ in range(2000):
        atual = total         # LER
        time.sleep(0)         # força a troca de thread aqui
        total = atual + 1     # GRAVAR

ts = [threading.Thread(target=soma_muitas) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("total:", total)        # deveria ser 4000 — mas sai bem MENOS
```

<div class="aviso">⚠️ Em CPython, o <strong>GIL</strong> costuma <em>esconder</em> a corrida no <code>+= 1</code>; o <code>time.sleep(0)</code> escancara a janela entre <strong>ler</strong> e <strong>gravar</strong>. As duas threads leem o mesmo valor e uma soma se perde — o total despenca (some metade).</div>

---

## A correção — `lock` na seção crítica

```python
import threading, time
total = 0
lock = threading.Lock()          # a trava

def soma_muitas():
    global total
    for _ in range(2000):
        with lock:               # SEÇÃO CRÍTICA: uma thread por vez
            atual = total
            time.sleep(0)
            total = atual + 1

ts = [threading.Thread(target=soma_muitas) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("total:", total)           # agora SEMPRE 4000
```

<div class="dica">💡 O <code>with lock:</code> garante <strong>exclusão mútua</strong>: enquanto uma thread está dentro, as outras <strong>esperam a vez</strong>. Custa desempenho — proteja só o <strong>mínimo</strong> necessário.</div>

---

## Como o lock conserta, visualmente

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:860px;display:block;margin:10px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs><marker id="lk" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
  <rect x="30" y="110" width="150" height="70" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
  <text x="105" y="140" text-anchor="middle" fill="#334155" font-size="15" font-weight="700">Thread 2</text>
  <text x="105" y="162" text-anchor="middle" fill="#94a3b8" font-size="12">aguarda a vez</text>
  <text x="232" y="150" text-anchor="middle" font-size="32">🔒</text>
  <line x1="182" y1="145" x2="210" y2="145" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#lk)"/>
  <text x="232" y="188" text-anchor="middle" fill="#b91c1c" font-size="11.5" font-weight="600">bloqueada</text>
  <rect x="296" y="80" width="240" height="140" rx="14" fill="#eef4fb" stroke="#12437f" stroke-width="2.5"/>
  <text x="416" y="106" text-anchor="middle" fill="#0d2b57" font-size="14" font-weight="700">seção crítica</text>
  <rect x="326" y="120" width="180" height="66" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="416" y="147" text-anchor="middle" fill="#14532d" font-size="14.5" font-weight="700">Thread 1</text>
  <text x="416" y="167" text-anchor="middle" fill="#16a34a" font-size="12">com a trava · total += 1</text>
  <text x="700" y="98" text-anchor="middle" fill="#334155" font-size="13" font-weight="700">um de cada vez</text>
  <rect x="665" y="108" width="70" height="30" rx="15" fill="#eef4fb" stroke="#94a3b8" stroke-width="1.5"/><text x="700" y="129" text-anchor="middle" fill="#0d2b57" font-size="15" font-weight="700">41</text>
  <line x1="700" y1="138" x2="700" y2="154" stroke="#94a3b8" stroke-width="2" marker-end="url(#lk)"/><text x="748" y="152" fill="#12437f" font-size="11" font-weight="600">T1</text>
  <rect x="665" y="156" width="70" height="30" rx="15" fill="#eef4fb" stroke="#94a3b8" stroke-width="1.5"/><text x="700" y="177" text-anchor="middle" fill="#0d2b57" font-size="15" font-weight="700">42</text>
  <line x1="700" y1="186" x2="700" y2="202" stroke="#94a3b8" stroke-width="2" marker-end="url(#lk)"/><text x="748" y="200" fill="#c2740a" font-size="11" font-weight="600">T2</text>
  <rect x="665" y="204" width="70" height="30" rx="15" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="700" y="225" text-anchor="middle" fill="#14532d" font-size="15" font-weight="700">43</text>
  <text x="700" y="258" text-anchor="middle" fill="#16a34a" font-size="13" font-weight="700">✓ nada se perde</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> o caderno agora fica com a <strong>caneta única</strong>. Quem quer anotar pega a caneta, escreve, devolve — o outro espera. Ninguém escreve por cima.</div>

---

## No seu trabalho — C1.A2

- O seu serviço processa inferências **em segundo plano** com um **worker** — e a concorrência desta aula é o que o **sustenta**.
- A **fila** já vem pronta no kit; a **teoria** dela chega na **Aula 8**.

<div class="dica">💡 Puxa direto para as tarefas do kit:
<br>• <strong>TAREFA 3</strong> — o worker <strong>grava o resultado</strong> processado para consulta posterior.
<br>• <strong>TAREFA 5</strong> — <strong>tratamento de erro</strong> no worker (retentativa).
<br>Repositório: <code>sd-2026-2-kit-c1a2</code>.</div>

---

## Atividade para casa — teste de carga

1. **Escreva `carga.py`:** dispare **N clientes** (ex.: 10, 50, 100) contra o `servidor_multicliente.py`, cada um enviando algumas mensagens; use **threads** no cliente para lançá-los juntos.
2. **Meça** o tempo total e o tempo médio por cliente conforme **N cresce**.
3. **Compare** com o servidor single-thread da Aula 2 sob a mesma carga.
4. **Escreva `relatorio_concorrencia.md`** com os tempos e a **análise**: onde o single-thread trava e por quê.

<div class="dica">🧰 <strong>Comece pelo</strong> <code>exemplos/aula03/carga_ESQUELETO.py</code>: a lógica de <strong>um cliente já está pronta</strong> — você completa os <code>#&nbsp;TODO</code> que <strong>disparam N threads</strong> e medem o total.</div>

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> <code>carga.py</code> + <code>relatorio_concorrencia.md</code> com os números que <strong>você</strong> mediu.</div>

---

## Lab · Checkpoints & problemas comuns (Windows)

<div class="cols">

<div>

**✅ O que você deve ver**
- O servidor imprime **uma linha de conexão por cliente**, sem esperar o anterior sair.
- Cada cliente recebe o **eco** das suas mensagens.
- `contador.py` sai **bem < 4000**; a versão com `lock` sai **= 4000**.

</div>

<div>

**🛠️ Se der erro**
- `[WinError 10048]` (porta ocupada) → feche servidores antigos ou troque a porta.
- Threads não aparecem “ao mesmo tempo”? Confirme o `daemon=True` e que o `accept()` está **dentro** do laço.
- `Ctrl + C` encerra tudo (threads `daemon` morrem com o principal).

</div>

</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Concorrência × paralelismo:** a diferença entre os dois.
- **Condição de corrida, exclusão mútua** e **seção crítica**.
- **Threads e processos:** quando usar cada um.
- **Escalabilidade** de servidores e **gargalos**.

**Termos-chave:** Thread · Condição de corrida · Exclusão mútua · Seção crítica · Lock · Bloqueante

<div class="dica">💡 Questões costumam mostrar um <strong>contador incorreto</strong> ou um cenário de acesso simultâneo e pedir o <strong>diagnóstico</strong> e a <strong>correção</strong>.</div>

---

## Questão de autoavaliação (estilo ENADE)

Duas threads incrementam a **mesma variável sem sincronização** e o total final fica **menor que o esperado**. Qual é o problema e a correção adequada?

A) *Deadlock*; aumentar o número de threads.
B) **Condição de corrida**; proteger a seção crítica com exclusão mútua.
C) Inanição (*starvation*); elevar a prioridade das threads.
D) Falha de rede; substituir o protocolo de transporte.
E) *Cold start*; pré-aquecer o serviço.

---

## Resolução — alternativa **B**

- Acesso concorrente **não sincronizado** a dado compartilhado é uma **condição de corrida**.
- Corrige-se garantindo **exclusão mútua** na **seção crítica**, com um **lock**.
- As demais descrevem problemas **diferentes** (deadlock, starvation, rede, cold start) que não explicam a **perda de contagens**.

<div class="dica">💡 É o seu <code>contador.py</code> de hoje virando questão de prova.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 7 — Sistemas operacionais e concorrência.
- Documentação do módulo **`threading`** do Python (`Thread`, `Lock`).
- **Guarde** o `contador.py`: a mesma corrida reaparece entre **réplicas** na Aula 10.

</div>

<div>

**Glossário**
- **Thread:** linha de execução independente no mesmo programa.
- **Condição de corrida:** duas threads alteram o mesmo dado ao mesmo tempo.
- **Seção crítica:** trecho que só uma thread pode executar por vez.
- **Lock:** garante exclusão mútua na seção crítica.
- **Bloqueante:** chamada que para a execução até terminar.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Entregue `carga.py` + `relatorio_concorrencia.md`. A Aula 4 começa revendo isto.

<a class="proximo" href="aula-02-modelos-arquitetura-sockets.html">← Anterior<small>Aula 2 · Sockets</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
<a class="proximo" href="aula-04-rpc-grpc.html">Próxima aula →<small>Aula 4 · Do RPC ao gRPC</small></a>
