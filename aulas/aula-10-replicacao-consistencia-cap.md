---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 10 — Replicação, consistência e o teorema CAP

C2 · Coordenação e consistência · 08/10/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — C2

<div class="cols">

<div>

**C1 · Fundamentos** (1–7) ✅

**C2 · Coordenação e consistência** (8–12)
Mensageria ✅ · relógios lógicos ✅ · **CAP** · Raft · resiliência.

</div>

<div>

**C3 · Nuvem e segurança** (13–18)

<div class="dica">📍 <strong>Aula 10</strong>. Ainda no bloco mais abstrato — seguimos por <strong>exemplos</strong> e um <strong>experimento</strong>.</div>

</div>

</div>

<div class="aviso">🧭 Na Aula 9 você aprendeu a <strong>detectar</strong> quando dois eventos são concorrentes. Hoje vemos <strong>onde isso dói</strong>: quando duas <strong>cópias</strong> do mesmo dado são escritas "ao mesmo tempo" e <strong>divergem</strong>.</div>

---

## Retomada

<div class="dica">🔄 Você ampliou a simulação para 4 processos e pôs o serviço de recuperação no ar?</div>

- Relógios vetoriais nos deram uma ferramenta: dizer se duas escritas foram **causais** ou **concorrentes**.
- Mas por que teríamos **duas cópias** do mesmo dado, para começo de conversa? Porque **replicar** é o que mantém o sistema **de pé** — e hoje veremos o **preço** disso.

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** por que replicamos dados — e qual é o **custo** (manter as cópias iguais).
2. **Enunciar** o **teorema CAP** e por que, sob **partição**, só dá para ter **C ou A**.
3. **Distinguir** consistência **forte** de consistência **eventual** e escolher a adequada.

---

## Por que replicar — e o preço

<div class="cols">

<div>

**Ganhos de ter N cópias**
- **Disponibilidade:** uma cópia cai, as outras atendem.
- **Desempenho:** leituras perto do usuário.
- **Durabilidade:** o dado não some com uma máquina.

</div>

<div>

**O preço**
- As cópias precisam ser **mantidas iguais**.
- Toda escrita tem que **chegar a todas** — e a rede **falha**.
- Enquanto não chegam, as cópias **divergem**.

</div>

</div>

<svg viewBox="0 0 860 190" role="img" style="width:100%;max-width:820px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <text x="150" y="24" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">1 cópia — ponto único de falha</text>
  <rect x="104" y="40" width="92" height="52" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="150" y="72" text-anchor="middle" fill="#991b1b" font-size="14" font-weight="700">dado</text>
  <text x="150" y="128" text-anchor="middle" fill="#dc2626" font-size="12">caiu → sistema fora</text>
  <line x1="300" y1="80" x2="360" y2="80" stroke="#94a3b8" stroke-width="2"/>
  <text x="330" y="70" text-anchor="middle" fill="#64748b" font-size="22">→</text>
  <text x="600" y="24" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">N cópias — disponível, mas precisam concordar</text>
  <rect x="470" y="40" width="92" height="52" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="516" y="72" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">cópia A</text>
  <rect x="640" y="40" width="92" height="52" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="686" y="72" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">cópia B</text>
  <line x1="562" y1="66" x2="640" y2="66" stroke="#16a34a" stroke-width="2.5"/>
  <text x="601" y="58" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="700">replica</text>
  <text x="601" y="128" text-anchor="middle" fill="#334155" font-size="12">uma cai, a outra atende</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> ter duas cópias é como manter <strong>dois cadernos</strong> com a mesma anotação. Ótimo se um se perde — mas agora você tem que <strong>copiar toda anotação nos dois</strong>, e às vezes não dá tempo.</div>

---

## O teorema CAP

Em um sistema com dados replicados, há **três** propriedades desejáveis:

- **C — Consistência:** toda leitura vê a escrita **mais recente** (as cópias parecem **uma só**).
- **A — Disponibilidade:** toda requisição recebe uma **resposta** (não trava, não recusa).
- **P — Tolerância a Partição:** o sistema **continua operando** mesmo se a rede **cortar** a comunicação entre as cópias.

<div class="aviso">⚠️ <strong>O enunciado:</strong> quando ocorre uma <strong>partição (P)</strong>, é impossível garantir <strong>C</strong> e <strong>A</strong> ao mesmo tempo. Você escolhe: ou responde (A) com dado possivelmente velho, ou garante o dado certo (C) recusando responder.</div>

---

## CAP — por que só dá para escolher 2

<svg viewBox="0 0 760 330" role="img" style="width:100%;max-width:560px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <polygon points="380,40 150,300 610,300" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <circle cx="380" cy="40" r="7" fill="#0d2b57"/>
  <text x="380" y="28" text-anchor="middle" fill="#0d2b57" font-size="16" font-weight="700">C</text>
  <text x="380" y="14" text-anchor="middle" fill="#64748b" font-size="11">Consistência</text>
  <circle cx="150" cy="300" r="7" fill="#0d2b57"/>
  <text x="150" y="322" text-anchor="middle" fill="#0d2b57" font-size="16" font-weight="700">A</text>
  <text x="104" y="300" text-anchor="middle" fill="#64748b" font-size="11">Disponib.</text>
  <circle cx="610" cy="300" r="7" fill="#0d2b57"/>
  <text x="610" y="322" text-anchor="middle" fill="#0d2b57" font-size="16" font-weight="700">P</text>
  <text x="664" y="300" text-anchor="middle" fill="#64748b" font-size="11">Partição</text>
  <text x="252" y="180" text-anchor="middle" fill="#12437f" font-size="12.5" font-weight="700" transform="rotate(-48 252 180)">CP</text>
  <text x="508" y="180" text-anchor="middle" fill="#c2740a" font-size="12.5" font-weight="700" transform="rotate(48 508 180)">AP</text>
  <text x="380" y="300" text-anchor="middle" fill="#64748b" font-size="12.5" font-weight="700" dy="-8">CA (só sem rede)</text>
  <text x="380" y="210" text-anchor="middle" fill="#334155" font-size="12">a rede real</text>
  <text x="380" y="228" text-anchor="middle" fill="#334155" font-size="12"><tspan font-weight="700">sempre</tspan> pode particionar</text>
</svg>

<div class="dica">💡 <strong>P não é opcional</strong> em sistema distribuído: a rede <em>vai</em> falhar um dia. Logo a escolha real é só <strong>CP</strong> × <strong>AP</strong>. "CA" só existiria numa máquina só, sem rede.</div>

---

## A partição, no detalhe — e a divergência

<svg viewBox="0 0 860 250" role="img" style="width:100%;max-width:840px;display:block;margin:4px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <rect x="60" y="70" width="150" height="60" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="135" y="94" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Réplica A</text>
  <text x="135" y="116" text-anchor="middle" fill="#334155" font-size="13" font-family="Consolas,monospace" font-weight="700">preço=20 (v2)</text>
  <rect x="650" y="70" width="150" height="60" rx="10" fill="#fff8e1" stroke="#e08a00" stroke-width="2"/>
  <text x="725" y="94" text-anchor="middle" fill="#0d2b57" font-size="13.5" font-weight="700">Réplica B</text>
  <text x="725" y="116" text-anchor="middle" fill="#334155" font-size="13" font-family="Consolas,monospace" font-weight="700">preço=10 (v1)</text>
  <line x1="210" y1="100" x2="420" y2="100" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="7 5"/>
  <line x1="440" y1="100" x2="650" y2="100" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="7 5"/>
  <text x="430" y="64" text-anchor="middle" fill="#dc2626" font-size="30" font-weight="700">✂</text>
  <line x1="430" y1="74" x2="430" y2="136" stroke="#dc2626" stroke-width="3"/>
  <text x="430" y="156" text-anchor="middle" fill="#991b1b" font-size="12.5" font-weight="700">rede cortada (partição)</text>
  <text x="135" y="52" text-anchor="middle" fill="#12437f" font-size="12">cliente escreve aqui ✍</text>
  <rect x="150" y="186" width="560" height="46" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="430" y="206" text-anchor="middle" fill="#991b1b" font-size="12.5" font-weight="700">A avança para v2; B não recebe e fica em v1 → as cópias DIVERGEM.</text>
  <text x="430" y="224" text-anchor="middle" fill="#dc2626" font-size="12">Momento da divergência: a 1ª escrita que não cruzou a partição.</text>
</svg>

<div class="dica">💡 <strong>Em miúdos:</strong> dois caixas da mesma loja, telefone mudo entre eles. Um atualiza o preço; o outro continua vendendo pelo antigo. Quem chegar no caixa B vê o <strong>preço velho</strong>.</div>

---

## Sob partição: CP × AP

| | **CP — escolhe Consistência** | **AP — escolhe Disponibilidade** |
|--|--|--|
| Leitura em B (desatualizado) | **recusa** (ex.: erro 503) | **responde** o valor antigo |
| Abre mão de… | **A** (fica indisponível) | **C** (serve dado velho) |
| Quando usar | saldo bancário, estoque, senha | curtidas, catálogo, feed, carrinho |
| Exemplos | bancos relacionais, ZooKeeper, etcd | Cassandra, DynamoDB, DNS |

<div class="aviso">📌 Não existe "melhor": existe <strong>adequado ao dado</strong>. Errar o lado custa caro — servir saldo velho (deveria ser CP) ou derrubar o feed inteiro por um voto perdido (deveria ser AP).</div>

---

## Consistência forte × eventual

<div class="cols">

<div>

**Forte**
- Toda leitura vê a **última** escrita, **sempre**.
- Exige **coordenação** entre as cópias a cada escrita → mais **lento**, menos **disponível** sob falha.
- É o lado **C** (CP).

</div>

<div>

**Eventual**
- As cópias podem ficar **momentaneamente diferentes**.
- **Se as escritas pararem**, todas **convergem** para o mesmo valor (como no Cenário 4 do lab).
- É o lado **A** (AP).

</div>

</div>

<div class="dica">💡 "Eventual" não é "nunca": é <strong>"em algum momento, se der um tempo, todos ficam iguais"</strong>. O preço é ler valores velhos no intervalo.</div>

---

<!-- _class: secao -->

# Laboratório
### O experimento da partição — ver duas réplicas divergirem

---

## Mão na massa — siga o Guia do Laboratório

Hoje o lab é um **experimento em 4 missões**: subir duas réplicas, **provocar a partição**, **registrar o momento da divergência** e **escolher o lado do CAP** (AP × CP) no código.

### 👉 [Abrir o Guia do Laboratório »](lab-10-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 10 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Aquecimento pronto e testado: <code>exemplos/aula10/replicas_sim.py</code> — simula A e B, a partição e a escolha AP/CP. Rode e leia a saída antes de ir para o kit.</div>

---

## O que a simulação mostra (aquecimento)

```powershell
python exemplos/aula10/replicas_sim.py
# Cenario 2 - PARTICAO: a divergencia
#     A <- "preco=20" (v2)
#     B  x  NAO recebe (particao) - continua em v1
#     >>> MOMENTO DA DIVERGENCIA: A=v2  B=v1 <<<
# Cenario 3 - sob particao, a escolha do CAP
#     modo AP (disponivel):   "preco=10" (v1) DESATUALIZADO
#     modo CP (consistente):  503 INDISPONIVEL
```

<div class="dica">💡 O mesmo dado, dois comportamentos legítimos sob partição. A missão pede que <strong>você</strong> implemente e justifique os dois.</div>

---

## No seu trabalho — C2.A2

- No RAG, o **armazenamento vetorial** (índice dos documentos) pode ser **replicado** para escalar as buscas.
- Decisão de projeto: durante uma falha de rede, o serviço de recuperação prefere **responder com o índice possivelmente desatualizado (AP)** ou **recusar (CP)**? Para busca semântica, normalmente **AP** basta.

<div class="dica">💡 Puxa para o kit: pense a <strong>chamada ao LLM</strong> (serviço de geração) — ela é o ponto mais frágil e, na <strong>próxima aula</strong>, vamos blindá-la (timeout + retry + disjuntor).</div>

---

## Atividade para casa

1. **Rode** o experimento do Guia (duas réplicas) e **registre o momento da divergência**.
2. **Escreva** o `relatorio_cap.md`: descreva o experimento e dê **duas justificativas** — um caso em que você escolheria **CP** e outro em que escolheria **AP**, cada um com o **tipo de dado**.
3. **Avance o C2.A2:** deixe o **serviço de recuperação** respondendo a uma consulta de ponta a ponta.

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> o <code>relatorio_cap.md</code> (experimento + as duas justificativas) + o serviço de recuperação funcionando. Roteiro completo no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Teorema CAP** e a escolha **CP × AP** sob partição.
- Consistência **forte × eventual** e **convergência**.
- **Replicação** (ganhos e custo) e ponto único de falha.
- Associar **tipo de dado** à escolha (saldo → C; feed → A).

**Termos-chave:** CAP · Partição · Consistência forte · Consistência eventual · Replicação · CP · AP

<div class="dica">💡 Pegadinha clássica: afirmar que um sistema "é CA". Em rede real, <strong>P é inevitável</strong> — a escolha prática é CP ou AP.</div>

---

## Questão de autoavaliação (estilo ENADE)

Um serviço de **carteira digital** replica o saldo em duas regiões. Durante uma **partição de rede**, chega um pedido de leitura de saldo na réplica que **pode estar desatualizada**. Para **não mostrar um saldo incorreto**, o sistema **recusa** a operação até a rede voltar.

Essa decisão caracteriza um sistema:

A) CA, pois abre mão da partição
B) **CP, pois prioriza a consistência e abre mão da disponibilidade**
C) AP, pois prioriza a disponibilidade
D) sem relação com o teorema CAP
E) de consistência eventual

---

## Resolução — alternativa **B**

- Houve **partição (P)** — logo, "CA" (A) está descartado: P é inevitável.
- O sistema **recusou responder** para **não** mostrar dado errado → preservou **C**, sacrificou **A** → **CP**.
- **AP** (C) e **eventual** (E) fariam o oposto: responder mesmo desatualizado.

<div class="dica">💡 Saldo é o exemplo canônico de dado que pede <strong>C</strong>. Já "quantas curtidas" tolera <strong>A</strong> tranquilamente.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 18 — Replicação.
- Brewer, *"CAP Twelve Years Later"* (2012) — leitura opcional.
- Rode o `replicas_sim.py` mudando a **ordem** das escritas e da partição.

</div>

<div>

**Glossário**
- **Replicação:** manter cópias do mesmo dado em várias máquinas.
- **CAP:** sob partição, escolha entre C e A.
- **Partição:** a rede corta a comunicação entre as cópias.
- **Consistência forte:** toda leitura vê a última escrita.
- **Consistência eventual:** as cópias convergem com o tempo.
- **CP / AP:** o lado do CAP que o sistema prioriza.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Rode o experimento, registre a divergência e escreva o `relatorio_cap.md`.

**Próxima (Aula 11):** **Consenso (Raft) e resiliência** — como as réplicas **combinam um único valor** mesmo com falhas, e como **blindar** a chamada de IA (tempo-limite, retentativa e disjuntor).

<a class="proximo" href="aula-09-relogios-logicos.html">← Anterior<small>Aula 9 · Relógios lógicos</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
