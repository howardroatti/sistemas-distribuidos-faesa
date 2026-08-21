---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 7 — Revisão da C1 + Avaliação C1.A1

C1 · ⬅ **DIA DE AVALIAÇÃO** · entrega do **C1.A2**
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Como funciona o dia de hoje

1. **Revisão consolidada** da Verificação C1 (Aulas 1–6) — o caminho e as **6 perguntas-chave**.
2. **Esquenta** — 5 questões comentadas no estilo ENADE.
3. **Avaliação C1.A1** — prova escrita, estilo ENADE (**5,0 pontos**).
4. **Entrega do C1.A2** — trabalho prático no repositório (**5,0 pontos**).

<div class="dica">💡 <strong>Nota da C1 = C1.A1 (5,0) + C1.A2 (5,0)</strong>. Hoje fecham as duas.</div>

---

## O caminho que percorremos na C1

A pergunta da C1: **como dois programas conversam de forma confiável pela rede?** Do **byte cru** no socket até um **serviço de IA publicado**:

- **Aula 1** — sistemas distribuídos, **falha parcial**, ambiente.
- **Aula 2** — **sockets**, cliente-servidor × P2P, **TCP × UDP**.
- **Aula 3** — **concorrência** (thread por cliente) e **condição de corrida**.
- **Aula 4** — **RPC → gRPC** e o contrato **`.proto`**.
- **Aula 5** — **REST**, verbos e códigos de status, **OpenAPI**.
- **Aula 6** — **IA como serviço** (o modelo atrás de uma API).

<div class="dica">💡 Releia os quadros <strong>EM RESUMO</strong> de cada aula antes da prova.</div>

---

## A trilha da C1 — de byte cru a serviço de IA

<svg viewBox="0 0 860 250" role="img" style="width:100%;max-width:850px;display:block;margin:8px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <defs>
    <marker id="tb" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
    <marker id="tbig" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto"><path d="M0,0 L8,3.5 L0,7 Z" fill="#12437f"/></marker>
  </defs>
  <text x="430" y="24" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">a pergunta da C1: como dois programas conversam de forma confiável pela rede?</text>
  <rect x="20" y="52" width="120" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="80" y="76" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 1</text><text x="80" y="96" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Fundamentos</text><text x="80" y="113" text-anchor="middle" fill="#64748b" font-size="10.5">falha parcial</text>
  <rect x="160" y="52" width="120" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="220" y="76" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 2</text><text x="220" y="96" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Sockets</text><text x="220" y="113" text-anchor="middle" fill="#64748b" font-size="10.5">TCP × UDP</text>
  <rect x="300" y="52" width="120" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="360" y="76" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 3</text><text x="360" y="96" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Concorrência</text><text x="360" y="113" text-anchor="middle" fill="#64748b" font-size="10.5">corrida + lock</text>
  <rect x="440" y="52" width="120" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="500" y="76" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 4</text><text x="500" y="96" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">gRPC</text><text x="500" y="113" text-anchor="middle" fill="#64748b" font-size="10.5">contrato .proto</text>
  <rect x="580" y="52" width="120" height="70" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="640" y="76" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Aula 5</text><text x="640" y="96" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">REST</text><text x="640" y="113" text-anchor="middle" fill="#64748b" font-size="10.5">verbos/status</text>
  <rect x="720" y="52" width="120" height="70" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/><text x="780" y="76" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">Aula 6</text><text x="780" y="96" text-anchor="middle" fill="#14532d" font-size="12" font-weight="600">IA serviço</text><text x="780" y="113" text-anchor="middle" fill="#16a34a" font-size="10.5">modelo + API</text>
  <line x1="140" y1="87" x2="158" y2="87" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="280" y1="87" x2="298" y2="87" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="420" y1="87" x2="438" y2="87" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="560" y1="87" x2="578" y2="87" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="700" y1="87" x2="718" y2="87" stroke="#94a3b8" stroke-width="2" marker-end="url(#tb)"/>
  <line x1="40" y1="176" x2="812" y2="176" stroke="#12437f" stroke-width="3" marker-end="url(#tbig)"/>
  <text x="44" y="206" fill="#334155" font-size="12.5" font-weight="700">byte cru no socket</text>
  <text x="812" y="206" text-anchor="end" fill="#16a34a" font-size="12.5" font-weight="700">serviço de IA publicado</text>
</svg>

<div class="dica">💡 Cada aula acrescentou <strong>uma camada de abstração</strong> sobre a anterior — do byte solto no socket até uma API de IA que o mundo consome. As 5 questões a seguir percorrem exatamente essa trilha.</div>

---

## As 6 perguntas que você precisa saber responder

Se você responde estas **com segurança**, está pronto para a C1.A1:

1. Por que **TCP** difere de **UDP**?
2. O que é **falha parcial**?
3. O que uma **thread** resolve — e qual problema ela **cria**?
4. Para que serve o arquivo **`.proto`**?
5. O que determina o **verbo** e o **código de status** de uma rota REST?
6. Por que a **inferência de IA** muda o **desenho** do serviço?

<div class="aviso">📌 Se travar em alguma, volte ao deck da aula correspondente <strong>agora</strong> — é o melhor uso dos próximos minutos.</div>

---

<!-- _class: secao -->

# Esquenta C1
### 5 questões comentadas — estilo ENADE

---

## Questão 1 — transporte para áudio ao vivo

Uma equipe desenvolve um serviço de **transmissão de áudio ao vivo**. Nos testes, a **retransmissão** de pacotes perdidos provocava **travamentos e atraso acumulado**, prejudicando mais a experiência do que a perda de trechos curtos. O protocolo de transporte mais adequado é:

A) TCP, por garantir entrega ordenada.
B) TCP, por realizar controle de fluxo.
C) UDP, por **não retransmitir** pacotes perdidos, evitando o atraso acumulado.
D) UDP, por confirmar cada pacote.
E) UDP, por estabelecer conexão prévia.

---

## Questão 1 — resposta **C**

- Em **tempo real, atraso é pior que perda**: o **UDP não retransmite** e mantém o fluxo.
- **D** e **E** descrevem o UDP **incorretamente** (ele não confirma pacotes nem estabelece conexão).

<div class="dica">💡 Aula 2 — TCP × UDP. O critério é sempre o <strong>trade-off</strong> garantia × latência.</div>

---

## Questão 2 — comunicação e concorrência

Analise as afirmações:

- **I.** Um socket é identificado por **IP + porta**.
- **II.** Num servidor **sequencial**, um cliente lento pode **bloquear** os demais.
- **III.** Uma condição de corrida **só ocorre** em sistemas com **mais de uma máquina**.
- **IV.** A **exclusão mútua** na seção crítica evita resultados imprevisíveis no dado compartilhado.

É correto o que se afirma em:
A) I e III · B) II e III · C) **I, II e IV** · D) III e IV · E) I, II, III e IV

---

## Questão 2 — resposta **C**

- **I, II e IV** são corretas.
- **III é falsa:** a condição de corrida ocorre entre **threads na mesma máquina** — não exige várias máquinas.

<div class="dica">💡 Aulas 2 e 3 — socket (IP+porta), servidor bloqueante e exclusão mútua.</div>

---

## Questão 3 — asserção e razão (idempotência)

**ASSERÇÃO:** É seguro **reenviar automaticamente** uma requisição **idempotente** que não obteve resposta.
**PORQUE**
**RAZÃO:** Uma operação idempotente, **repetida, leva ao mesmo estado final**.

A) Asserção e razão verdadeiras, e a razão **justifica** a asserção.
B) Ambas verdadeiras, mas a razão **não** justifica.
C) Asserção verdadeira, razão falsa.
D) Asserção falsa, razão verdadeira.
E) Ambas falsas.

---

## Questão 3 — resposta **A**

- **Ambas são verdadeiras e a razão explica a asserção:** é **justamente por levar ao mesmo estado final** que a operação idempotente pode ser **retentada com segurança**.

<div class="dica">💡 Aula 5 (idempotência) + prévia da <strong>resiliência</strong> (Aula 11). Formato <strong>asserção-razão</strong> é clássico do ENADE.</div>

---

## Questão 4 — comunicação entre microsserviços

Uma equipe precisa de comunicação **interna de alto volume** entre **microsserviços**, com **contrato tipado** e **baixa sobrecarga** de dados na rede. A tecnologia mais adequada é:

A) SOAP com XML.
B) **gRPC** com Protocol Buffers.
C) REST sobre JSON, exclusivamente.
D) Troca de arquivos por FTP.
E) Mensagens por e-mail.

---

## Questão 4 — resposta **B**

- O **gRPC** oferece **contrato tipado** (`.proto`), **serialização binária compacta** e **HTTP/2** — ideal para comunicação **interna de alto volume** entre serviços.

<div class="dica">💡 Aula 4 — <strong>gRPC para dentro</strong>, REST para fora. A pista é "interno + alto volume + tipado".</div>

---

## Questão 5 — atender vários clientes

Um servidor **sequencial** trava o atendimento quando um cliente demora. A técnica que permite atender **vários clientes simultaneamente**, sem que um bloqueie os outros, é:

A) Reduzir o tamanho do buffer.
B) Usar **uma thread por conexão** aceita.
C) Trocar TCP por UDP.
D) Diminuir o número da porta.
E) Desativar o registro de log.

---

## Questão 5 — resposta **B**

- Atribuir uma **thread a cada conexão** libera o laço principal para **aceitar o próximo** cliente; um cliente lento afeta **apenas a sua própria thread**.

<div class="dica">💡 Aula 3 — o servidor multicliente. Foi exatamente o seu lab.</div>

---

## Avaliação C1.A1 — a prova

- **Escrita, individual, estilo ENADE** — vale **5,0 pontos**.
- **Integra todo o bloco C1**: comunicação (socket, TCP/UDP, RPC/RMI, REST) e concorrência (thread) aparecem **combinados** em estudos de caso.
- **Estratégia:** **leia o cenário inteiro antes** de olhar as alternativas; identifique **qual conceito** o caso está cobrando; elimine as que descrevem a tecnologia **errada**.

<div class="aviso">📌 As 5 questões do esquenta são do <strong>mesmo estilo</strong> da prova. Se você as entendeu, está pronto.</div>

---

## Entrega do C1.A2 — checklist antes de submeter

Dia de entrega do trabalho. **Rode o projeto do zero** e confira contra a **rubrica**:

- **Clonar do zero** e seguir o **seu próprio README** — funciona?
- **REST e gRPC** devolvem o **mesmo resultado** para o mesmo texto?
- O **modelo** é carregado **UMA vez** (não a cada requisição)?
- Há **commits ao longo** do período (não um único no final)?

<div class="dica">💡 Rubrica: arquitetura <strong>1,5</strong> · comunicação <strong>1,5</strong> · resiliência <strong>1,0</strong> · execução reproduzível <strong>1,0</strong>. Entrega <strong>no repositório</strong>, sem apresentação oral.</div>

---

## ◆ Foco ENADE

- A prova **C1.A1 integra todo o bloco**.
- No ENADE, **comunicação** (socket, TCP/UDP, RPC/RMI, REST) e **concorrência** (thread) aparecem **quase sempre combinados** em estudos de caso.
- **Treine a leitura do cenário** antes de escolher a alternativa.

**Termos-chave:** Socket · TCP/UDP · Thread · RPC/gRPC · REST · Inferência

<div class="dica">💡 As questões do ENADE raramente cobram um conceito isolado — elas <strong>misturam</strong>. Pratique identificar <em>qual</em> conceito o caso está pedindo.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para revisar**
- Os quadros **EM RESUMO** das Aulas 1–6.
- Os **labs** que você mesmo rodou (socket, multicliente, gRPC, REST).
- O seu **C1.A2** contra a **rubrica**.

</div>

<div>

**Glossário**
- **C1.A1:** avaliação escrita individual, estilo ENADE (5,0).
- **C1.A2:** trabalho prático no repositório (5,0).
- **Rubrica:** tabela que define como os pontos do trabalho são distribuídos.

</div>

</div>

---

<!-- _class: secao -->

# Boa prova! 🚀
### Entregue o C1.A2 no repositório. A C2 começa com um novo tipo de problema.

<a class="proximo" href="aula-06-ia-como-servico-ead.html">← Anterior<small>Aula 6 · IA como serviço</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
<a class="proximo" href="aula-08-mensageria-eventos-gateway.html">Próxima aula →<small>Aula 8 · Mensageria/fila</small></a>
