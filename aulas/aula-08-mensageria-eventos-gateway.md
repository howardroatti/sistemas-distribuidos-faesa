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

## Síncrono × Assíncrono, visualmente

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:840px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="sb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="sg" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker>
    <marker id="sgy" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
  <text x="30" y="28" fill="#b91c1c" font-size="14" font-weight="700">SÍNCRONO — o cliente fica travado esperando</text>
  <rect x="40" y="44" width="140" height="52" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="110" y="75" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Cliente</text>
  <rect x="640" y="44" width="150" height="52" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="715" y="75" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Serviço</text>
  <line x1="182" y1="58" x2="636" y2="58" stroke="#12437f" stroke-width="2" marker-end="url(#sb)"/><text x="410" y="52" text-anchor="middle" fill="#12437f" font-size="12" font-weight="700">chama e aguarda</text>
  <line x1="636" y1="86" x2="184" y2="86" stroke="#16a34a" stroke-width="2" marker-end="url(#sg)"/><text x="410" y="104" text-anchor="middle" fill="#16a34a" font-size="12" font-weight="700">resposta (só quando pronto)</text>
  <rect x="190" y="112" width="440" height="22" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/><text x="410" y="128" text-anchor="middle" fill="#991b1b" font-size="11.5" font-weight="700">🔒 cliente bloqueado esse tempo todo</text>
  <line x1="30" y1="152" x2="830" y2="152" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="30" y="184" fill="#16a34a" font-size="14" font-weight="700">ASSÍNCRONO — entrega, recebe um id e segue livre</text>
  <rect x="40" y="200" width="130" height="56" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="105" y="232" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Cliente</text>
  <rect x="300" y="200" width="120" height="56" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/><text x="360" y="232" text-anchor="middle" fill="#7c4a03" font-size="13.5" font-weight="700">Fila</text>
  <rect x="560" y="200" width="150" height="56" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="635" y="226" text-anchor="middle" fill="#14532d" font-size="13.5" font-weight="700">Worker</text><text x="635" y="245" text-anchor="middle" fill="#16a34a" font-size="11">processa depois</text>
  <line x1="172" y1="216" x2="298" y2="216" stroke="#12437f" stroke-width="2" marker-end="url(#sb)"/><text x="235" y="210" text-anchor="middle" fill="#12437f" font-size="11">entrega</text>
  <line x1="298" y1="242" x2="172" y2="242" stroke="#16a34a" stroke-width="2" marker-end="url(#sg)"/><text x="235" y="256" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="700">id na hora ✓</text>
  <line x1="420" y1="228" x2="558" y2="228" stroke="#94a3b8" stroke-width="2" marker-end="url(#sgy)"/><text x="489" y="222" text-anchor="middle" fill="#64748b" font-size="11">worker puxa</text>
  <text x="360" y="296" text-anchor="middle" fill="#334155" font-size="12" font-weight="700">cliente segue livre e busca depois: GET /resultado/{id}</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> síncrono é a <strong>fila do caixa</strong> (você espera parado). Assíncrono é a <strong>senha da lanchonete</strong>: você pede, pega a senha (o id) e vai sentar; quando fica pronto, chamam o número.</div>

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

## A fila como amortecedor, visualmente

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="fb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#e08a00"/></marker>
    <marker id="fg" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker>
  </defs>
  <rect x="30" y="108" width="140" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="100" y="138" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Produtor</text>
  <text x="100" y="158" text-anchor="middle" fill="#64748b" font-size="11">pico de tarefas</text>
  <line x1="172" y1="118" x2="296" y2="128" stroke="#e08a00" stroke-width="2" marker-end="url(#fb)"/>
  <line x1="172" y1="143" x2="296" y2="143" stroke="#e08a00" stroke-width="2" marker-end="url(#fb)"/>
  <line x1="172" y1="168" x2="296" y2="158" stroke="#e08a00" stroke-width="2" marker-end="url(#fb)"/>
  <rect x="300" y="70" width="170" height="150" rx="12" fill="#fff7ec" stroke="#e08a00" stroke-width="2.5"/>
  <text x="385" y="94" text-anchor="middle" fill="#7c4a03" font-size="13.5" font-weight="700">FILA</text>
  <rect x="318" y="104" width="134" height="20" rx="4" fill="#fde3bf"/><rect x="318" y="128" width="134" height="20" rx="4" fill="#fde3bf"/><rect x="318" y="152" width="134" height="20" rx="4" fill="#fde3bf"/><rect x="318" y="176" width="134" height="20" rx="4" fill="#fde3bf"/><rect x="318" y="200" width="134" height="14" rx="4" fill="#fdd39c"/>
  <line x1="470" y1="118" x2="596" y2="126" stroke="#16a34a" stroke-width="2" marker-end="url(#fg)"/>
  <line x1="470" y1="170" x2="596" y2="188" stroke="#16a34a" stroke-width="2" marker-end="url(#fg)"/>
  <rect x="600" y="100" width="150" height="52" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="675" y="131" text-anchor="middle" fill="#14532d" font-size="13.5" font-weight="700">Worker 1</text>
  <rect x="600" y="176" width="150" height="52" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="675" y="200" text-anchor="middle" fill="#14532d" font-size="13.5" font-weight="700">Worker 2</text><text x="675" y="218" text-anchor="middle" fill="#16a34a" font-size="10.5">+escala</text>
  <text x="385" y="248" text-anchor="middle" fill="#c2740a" font-size="12" font-weight="700">picos se acumulam na fila — não derrubam o serviço</text>
  <text x="675" y="252" text-anchor="middle" fill="#16a34a" font-size="11.5" font-weight="700">mais vazão? +workers</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> a fila é a <strong>caixa de entrada</strong> do restaurante. Os pedidos entram e ficam guardados; a cozinha (workers) puxa no ritmo dela. Movimento demais? <strong>Coloque mais cozinheiros</strong> na mesma caixa.</div>

---

## Conceito 2/4 — Quando o processamento falha: dead-letter

- Uma tarefa pode dar **erro** (entrada inválida, dependência fora do ar). O que fazer?
- **Boa prática:** **reprocessar** algumas vezes; **persistindo** a falha, encaminhar a mensagem para uma **fila de descarte** — a **dead-letter**.

<div class="aviso">⚠️ Os dois extremos são ruins: <strong>tentar para sempre</strong> trava o worker; <strong>perder a mensagem</strong> esconde o problema. A <strong>dead-letter</strong> isola a mensagem para análise e <strong>mantém o fluxo principal saudável</strong>.</div>

---

## O que fazer quando falha — dead-letter

<svg viewBox="0 0 860 290" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="db" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94a3b8"/></marker>
    <marker id="dg" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#16a34a"/></marker>
    <marker id="dr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#dc2626"/></marker>
  </defs>
  <rect x="30" y="112" width="120" height="60" rx="10" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/><text x="90" y="147" text-anchor="middle" fill="#7c4a03" font-size="13.5" font-weight="700">Fila</text>
  <line x1="152" y1="142" x2="288" y2="142" stroke="#94a3b8" stroke-width="2" marker-end="url(#db)"/>
  <rect x="290" y="106" width="160" height="72" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="370" y="136" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Worker</text><text x="370" y="156" text-anchor="middle" fill="#64748b" font-size="11">tenta processar</text>
  <path d="M300,106 C288,74 320,58 350,58 C380,58 410,72 410,104" fill="none" stroke="#e08a00" stroke-width="2" marker-end="url(#db)"/>
  <text x="355" y="50" text-anchor="middle" fill="#c2740a" font-size="11.5" font-weight="700">retenta (até N×)</text>
  <line x1="450" y1="126" x2="586" y2="100" stroke="#16a34a" stroke-width="2" marker-end="url(#dg)"/>
  <rect x="590" y="72" width="220" height="52" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="700" y="103" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">✓ processado → resultado</text>
  <line x1="450" y1="158" x2="586" y2="188" stroke="#dc2626" stroke-width="2" marker-end="url(#dr)"/>
  <text x="500" y="200" text-anchor="middle" fill="#b91c1c" font-size="11" font-weight="700">falhou N×</text>
  <rect x="590" y="164" width="220" height="60" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2.5"/><text x="700" y="190" text-anchor="middle" fill="#991b1b" font-size="13" font-weight="700">Dead-letter</text><text x="700" y="209" text-anchor="middle" fill="#dc2626" font-size="11">isola p/ análise</text>
  <text x="430" y="266" text-anchor="middle" fill="#334155" font-size="12" font-weight="700">a mensagem problemática sai do caminho → o fluxo principal segue saudável</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é a <strong>bandeja de "pendências"</strong> do balcão. Tentou atender, não deu depois de algumas vezes? Põe naquela bandeja para olhar com calma — <strong>sem travar a fila</strong> de quem vem atrás.</div>

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

## Fila × Pub/sub, visualmente

<svg viewBox="0 0 860 320" role="img" style="width:100%;max-width:840px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="pb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
    <marker id="pgy" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#cbd5e1"/></marker>
  </defs>
  <text x="30" y="28" fill="#0d2b57" font-size="14" font-weight="700">FILA — 1 consumidor por mensagem · distribui TRABALHO</text>
  <rect x="30" y="44" width="110" height="48" rx="9" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/><text x="85" y="73" text-anchor="middle" fill="#7c4a03" font-size="12.5" font-weight="700">Fila · msg</text>
  <line x1="142" y1="68" x2="278" y2="68" stroke="#12437f" stroke-width="2.2" marker-end="url(#pb)"/>
  <rect x="282" y="42" width="150" height="52" rx="9" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="357" y="73" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">Worker A ✓</text>
  <rect x="452" y="46" width="120" height="44" rx="9" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 3"/><text x="512" y="73" text-anchor="middle" fill="#94a3b8" font-size="12">Worker B</text>
  <rect x="590" y="46" width="120" height="44" rx="9" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 3"/><text x="650" y="73" text-anchor="middle" fill="#94a3b8" font-size="12">Worker C</text>
  <text x="640" y="110" text-anchor="middle" fill="#94a3b8" font-size="11">ociosos nesta mensagem</text>
  <line x1="30" y1="132" x2="830" y2="132" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="30" y="162" fill="#0d2b57" font-size="14" font-weight="700">PUB/SUB — todos os assinantes recebem · distribui INFORMAÇÃO</text>
  <rect x="30" y="196" width="170" height="70" rx="10" fill="#12437f"/><text x="115" y="226" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">evento</text><text x="115" y="246" text-anchor="middle" fill="#bcd3f0" font-size="11.5">"pedido concluído"</text>
  <rect x="250" y="204" width="110" height="54" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="305" y="236" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Tópico</text>
  <line x1="200" y1="231" x2="248" y2="231" stroke="#12437f" stroke-width="2.2" marker-end="url(#pb)"/>
  <line x1="360" y1="214" x2="576" y2="188" stroke="#12437f" stroke-width="2.2" marker-end="url(#pb)"/>
  <line x1="360" y1="231" x2="576" y2="231" stroke="#12437f" stroke-width="2.2" marker-end="url(#pb)"/>
  <line x1="360" y1="248" x2="576" y2="274" stroke="#12437f" stroke-width="2.2" marker-end="url(#pb)"/>
  <rect x="580" y="166" width="230" height="42" rx="9" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="695" y="192" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">Estoque (dá baixa)</text>
  <rect x="580" y="212" width="230" height="42" rx="9" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="695" y="238" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">Notificação (avisa)</text>
  <rect x="580" y="258" width="230" height="42" rx="9" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="695" y="284" text-anchor="middle" fill="#14532d" font-size="12.5" font-weight="700">Relatório (registra)</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> a fila é o <strong>próximo, por favor!</strong> — um atendente pega cada senha. O pub/sub é o <strong>alto-falante do aeroporto</strong>: um aviso, e <strong>todo mundo interessado</strong> ouve ao mesmo tempo.</div>

---

## Conceito 4/4 — API Gateway: a porta única

- Com vários serviços, o cliente **não deve** conhecer o endereço de cada um.
- O **API Gateway** é a **porta de entrada única**: recebe todas as requisições e **encaminha ao serviço certo**.
- Centraliza o que é **comum a todos**: **autenticação**, **limite de requisições** (rate limit) e **log**. É nele que aplicaremos a **segurança** (C3).

<div class="aviso">⚠️ <strong>Versionamento:</strong> <strong>acrescentar</strong> um campo à resposta é seguro; <strong>remover/renomear</strong> um campo <strong>quebra</strong> os clientes — exige publicar uma nova versão (ex.: <code>/v2</code>) e manter a antiga durante a transição.</div>

---

## API Gateway — a porta única

<svg viewBox="0 0 860 300" role="img" style="width:100%;max-width:840px;display:block;margin:6px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="ggb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#e08a00"/></marker>
    <marker id="ggr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#12437f"/></marker>
  </defs>
  <rect x="24" y="60" width="130" height="48" rx="9" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/><text x="89" y="89" text-anchor="middle" fill="#7c4a03" font-size="13" font-weight="700">Navegador</text>
  <rect x="24" y="180" width="130" height="48" rx="9" fill="#fff7ec" stroke="#e08a00" stroke-width="2"/><text x="89" y="209" text-anchor="middle" fill="#7c4a03" font-size="13" font-weight="700">App mobile</text>
  <line x1="156" y1="84" x2="316" y2="128" stroke="#e08a00" stroke-width="2.2" marker-end="url(#ggb)"/>
  <line x1="156" y1="204" x2="316" y2="164" stroke="#e08a00" stroke-width="2.2" marker-end="url(#ggb)"/>
  <rect x="320" y="96" width="180" height="100" rx="12" fill="#12437f"/>
  <text x="410" y="126" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">API Gateway</text>
  <text x="410" y="150" text-anchor="middle" fill="#bcd3f0" font-size="11.5">🔒 autenticação</text>
  <text x="410" y="168" text-anchor="middle" fill="#bcd3f0" font-size="11.5">⏱ rate limit · 📝 log</text>
  <text x="410" y="186" text-anchor="middle" fill="#bcd3f0" font-size="11.5">↳ roteia p/ o serviço certo</text>
  <line x1="500" y1="118" x2="606" y2="92" stroke="#12437f" stroke-width="2.2" marker-end="url(#ggr)"/>
  <line x1="500" y1="146" x2="606" y2="146" stroke="#12437f" stroke-width="2.2" marker-end="url(#ggr)"/>
  <line x1="500" y1="174" x2="606" y2="200" stroke="#12437f" stroke-width="2.2" marker-end="url(#ggr)"/>
  <rect x="610" y="66" width="200" height="46" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="710" y="94" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Serviço de Inferência</text>
  <rect x="610" y="124" width="200" height="46" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="710" y="152" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Serviço de Dados</text>
  <rect x="610" y="182" width="200" height="46" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="710" y="210" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Serviço de Busca</text>
  <text x="410" y="256" text-anchor="middle" fill="#334155" font-size="12" font-weight="700">o cliente conhece só uma porta — não o endereço de cada serviço</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> é a <strong>recepção do prédio</strong>. Ninguém entra direto na sala de cada setor: passa pela recepção, que <strong>confere o crachá</strong> (auth), controla o fluxo e <strong>indica a sala certa</strong>.</div>

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

<a class="proximo" href="aula-07-revisao-c1-avaliacao.html">← Anterior<small>Aula 7 · Revisão + prova C1</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
<a class="proximo" href="aula-09-relogios-logicos.html">Próxima aula →<small>Aula 9 · Relógios lógicos</small></a>
