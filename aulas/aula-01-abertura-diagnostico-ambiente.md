---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 1 — Abertura, diagnóstico e ambiente

C1 · Fundamentos e comunicação distribuída · 06/08/2026
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Onde estamos — a trilha do semestre

<div class="cols">

<div>

**C1 · Fundamentos e comunicação** (Aulas 1–7 · 06/08 a 17/09)
Sockets, concorrência, gRPC, REST e **IA como serviço**.

**C2 · Coordenação e consistência** (Aulas 8–12 · 24/09 a 29/10)
Mensageria, relógios lógicos, **CAP**, **Raft**, resiliência.

</div>

<div>

**C3 · Nuvem, implantação e segurança** (Aulas 13–18 · 05/11 a 03/12)
Containers, nuvem, serverless, observabilidade, segurança/LGPD.

<div class="dica">📍 Você está na <strong>Aula 1</strong>.</div>

</div>

</div>

---

## A disciplina em um slide

- **Ementa:** fundamentos e comunicação → coordenação e consistência → nuvem e implantação → segurança e LGPD.
- **Cinco módulos:** (1) fundamentos e comunicação · (2) serviços, APIs e **IA como serviço** · (3) coordenação, **CAP** e **Raft** · (4) nuvem, containers e implantação · (5) segurança, LGPD e tendências.
- **Fio condutor:** um **serviço de IA** que cresce de cliente-servidor a **plataforma cloud-native** — a IA é **caixa-preta** (você chama API/biblioteca, **nunca treina modelo**).
- **Como serão as aulas:** 90 min **práticos** — o laboratório **começa na aula e termina em casa**; Git e nuvem desde o primeiro dia.

<div class="dica">💡 Você aprende sistemas distribuídos <strong>construindo</strong>, por partes, um serviço de IA cloud-native.</div>

---

## Como você será avaliado

- **Três verificações — C1, C2 e C3.** Cada uma vale até **10,0** = **duas avaliações de 5,0**.
- **A1 — Prova escrita estilo ENADE (5,0).** Datas: **C1 17/09 · C2 29/10 · C3 26/11**.
- **A2 — Trabalho prático sem apresentação (5,0):** código + `README` entregue no repositório.
- **Rubrica do trabalho:** arquitetura **1,5** · comunicação **1,5** · resiliência **1,0** · execução reproduzível **1,0** — a **sofisticação da IA não pontua**.

<div class="dica">💡 <strong>Nota Final = (C1 + C2 + C3) / 3.</strong> Em cada ciclo: uma prova (teoria ENADE) + um trabalho prático.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** o que é um sistema distribuído e por que quase todo software hoje é um.
2. **Reconhecer** o desafio que só existe quando há rede no meio: a **falha parcial**.
3. **Deixar o ambiente pronto**: Python, VS Code, Git e GitHub (VM a partir de amanhã).

---

## Conceito 1/3 — O que é um sistema distribuído

- Vários **computadores independentes** que cooperam pela rede e se apresentam como **um sistema único**.
- Você usa dezenas por dia: **WhatsApp, Netflix, app do banco, Uber, ChatGPT**. Ao ver o saldo, dezenas de máquinas cooperaram — você enxerga só o resultado.
- A cooperação traz **3 ganhos**: **escalabilidade** (mais máquinas, não uma maior), **disponibilidade** (segue de pé se uma cai) e **proximidade** do usuário (servidores por região).
- O preço: existe **uma rede no meio** — lenta, imprevisível e que **falha** (e não falha de forma limpa).

<div class="dica">💡 Sistema distribuído = várias máquinas cooperando que <strong>parecem uma só</strong>.</div>

---

## Duas ideias que acompanham o curso

<div class="cols">

<div>

**Latência**
- Tempo para uma mensagem ir de um ponto a outro da rede.
- Memória local: **nanossegundos**; rede: **milissegundos** — e **variável**.
- Muitas decisões de projeto existem para **esconder/reduzir** a latência.

</div>

<div>

**Transparência**
- Esforço de **esconder** a distribuição do usuário.
- De **acesso** (usar remoto como local), de **localização** (não saber onde está), de **replicação** (não perceber as cópias).
- Mais transparência por fora = mais trabalho por dentro.

</div>

</div>

---

## Conceito 2/3 — Falha parcial (o problema central)

- Num sistema **centralizado**, a falha é **total**: ou tudo funciona, ou tudo para — e fica **evidente**.
- Num sistema **distribuído** surge a **falha parcial**: uma parte para enquanto o resto continua.
- Pior é a **ambiguidade**: se **A** pede a **B** e não recebe resposta, **A não sabe** se B **caiu**, está **lento** ou se a **resposta se perdeu**. As três são **indistinguíveis** para A.

<div class="aviso">⚠️ Guarde esta ideia: relógios lógicos, CAP, consenso e resiliência existem <strong>por causa</strong> da falha parcial. Aprender SD é aprender a projetar <strong>contando com ela</strong>.</div>

---

## Conceito 3/3 — O que você vai construir

- Uma **plataforma de IA como serviço** que nasce como um par **cliente-servidor** e, aula após aula, ganha **interfaces modernas, fila, microsserviços, containers** e vai para a **nuvem**.
- A **IA é a tarefa** que o sistema executa: você **chama um modelo pronto**, **nunca o treina** — sem matemática de aprendizado de máquina.
- Tudo **versionado no Git** desde o 1º dia: é como equipes reais colaboram — e como você **provará** o que construiu.

<div class="dica">💡 <strong>C1.A2 — Serviço de Inferência Distribuído</strong> começa hoje: preparar o ambiente e criar o repositório onde ele vai crescer.</div>

---

## Como usar este material (leia primeiro)

**Onde está o código:** todo exemplo citado nos slides (`servidor_eco.py`, esqueletos…) está no **repositório do curso**, em `aulas/exemplos/aulaNN/`.

```powershell
git clone https://github.com/howardroatti/sistemas-distribuidos-faesa.git
# sem Git? No GitHub: botão verde  Code → Download ZIP
```

- **Dois terminais** (vários labs pedem): no VS Code, menu **Terminal → Split Terminal**.
- **Ativar o venv barrou?** Se o PowerShell disser *"scripts is disabled"*, rode **uma vez**: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (responda **S**).

<div class="dica">💡 Pouca prática com Python/terminal/HTTP? Faça o <strong>roteiro de nivelamento</strong> (<code>nivelamento.md</code> no repositório) antes de começar.</div>

---

## Ambiente — hoje, sem a VM ainda

<div class="aviso">🖥️ A <strong>máquina virtual</strong> da disciplina fica <strong>disponível amanhã</strong>. Hoje usamos o <strong>Windows nativo</strong> do laboratório — que já tem <strong>Python</strong> e <strong>VS Code</strong>. É o suficiente para tudo de hoje.</div>

**No PowerShell, confirme que está tudo à mão:**

```powershell
python --version      # deve mostrar Python 3.x  (se não achar, tente:  py --version)
code --version        # VS Code instalado
git --version         # se aparecer versão, ótimo; se não, use o Plano B (próximo slide)
```

<div class="dica">💡 Os laboratórios de hoje e da próxima aula são <strong>Python puro</strong> — <strong>não</strong> precisam de Docker nem da VM. Docker entra só nos trabalhos, já na VM.</div>

---

## Ambiente — seu repositório `sd-2026-2`

<div class="cols">

<div>

**Caminho A — com Git (recomendado)**

```powershell
cd $HOME\Documents
git init sd-2026-2
cd sd-2026-2
# ...crie seus arquivos...
git add .
git commit -m "primeiro commit"
# crie o repo no GitHub e:
git remote add origin URL_DO_SEU_REPO
git push -u origin main
```

</div>

<div>

**Caminho B — sem Git hoje (plano B)**

1. Entre no **github.com** e clique em **New repository**.
2. Nome: **`sd-2026-2`** → **Create**.
3. Guarde seus arquivos numa pasta local hoje.
4. **Amanhã, na VM**, faça o `commit`/`push` — ou use **Add file → Upload** pelo site.

</div>

</div>

<div class="dica">💡 O objetivo de hoje é <strong>ter o repositório criado</strong>. O push pode ser concluído na VM amanhã.</div>

---

## Kit da C1.A2 — clone e experimente (hoje)

O trabalho da **C1** já tem um **kit de partida** público. A **rota síncrona roda offline, sem Docker** — dá para provar **hoje, no Windows**:

```powershell
git clone https://github.com/howardroatti/sd-2026-2-kit-c1a2.git
cd sd-2026-2-kit-c1a2
python -m venv .venv
.\.venv\Scripts\Activate.ps1                 # ativa o ambiente (PowerShell)
pip install -r requirements.txt
uvicorn app.api_rest:app --reload --port 8000   # abra http://localhost:8000/docs
# em OUTRO terminal (com o .venv ativo):
python exemplos/cliente_rest.py "o atendimento foi otimo"
```

<div class="dica">💡 O "modelo de IA" é um classificador de sentimento <strong>scikit-learn</strong> que treina sozinho na 1ª execução — <strong>100% offline</strong>. A <strong>fila (Docker/Redis)</strong>, o <strong>worker</strong> e o <strong>gRPC</strong> entram na <strong>VM (amanhã)</strong>; o desafio completo abre na <strong>Aula 6</strong>.</div>

---

<!-- _class: secao -->

# Atividade em sala
### Diagnóstico (sem nota) — à prova de LLM

---

## Diagnóstico — como funciona (35 min)

**Sem consulta e sem celular · em papel · não vale nota** (serve para eu calibrar o ritmo das aulas).

<div class="cols">

<div>

**Parte A (10 min) — Desenho**
Desenhe à mão o **caminho de um "oi"** no chat, do seu celular ao do colega. Nomeie as "caixas" que imaginar.

**Parte B (10 min) — Predição**
**B1** *(antes)*: o que acontece se o servidor cair no meio de uma requisição?
**B2/B3** *(depois da demo)*: o que **de fato** ocorreu e por quê.

</div>

<div>

**Parte C (15 min) — Quiz sobre o log**
Você responde **5 questões** olhando **apenas** para o **log projetado** da demonstração ao vivo.

<div class="dica">💡 Não há resposta "certa" no desenho — é o seu <strong>modelo mental de hoje</strong>. No fim do semestre você o refaz.</div>

</div>

</div>

---

## Demonstração ao vivo (professor)

**Dois terminais no projetor**, com os exemplos `exemplos/aula01/servidor_eco.py` e `cliente_eco.py`:

1. **Terminal 1:** `python servidor_eco.py` — ele fica **ouvindo** na porta 5000.
2. **Terminal 2:** `python cliente_eco.py` — envia `"oi"` e **aguarda** a resposta.
3. O servidor **demora de propósito** (simula processamento). Enquanto o cliente espera…
4. **No Terminal 1, aperte `Ctrl + C`** — o servidor **cai** no meio da requisição.
5. Observe o **erro do cliente** e **projete o log** — é o artefato da **Parte C**.

<div class="aviso">⚠️ Frase-chave ao fechar: <strong>"o cliente nunca sabe o que aconteceu do outro lado."</strong></div>

<div class="dica">💡 Os dois arquivos estão prontos no repositório (<code>exemplos/aula01/</code>) — rodam no <strong>Windows</strong>, sem VM.</div>

---

## Diagnóstico — gabarito da Parte C

O log da demo mostra a **falha parcial**. As respostas apontam para o mesmo lugar:

- **C1 = B** — não houve **aviso**; a conexão só parou.
- **C2 = B** — o cliente **esperou alguns segundos** até o tempo-limite.
- **C3 = B** — "caiu" × "lento" são **indistinguíveis** *(a pergunta mais importante)*.
- **C4 = B** — reenviar pode **executar duas vezes** → semente de **idempotência** (Aula 11).
- **C5 = B** — faltou **tempo-limite + nova tentativa** → **resiliência** (Aula 11).

---

## Atividade para casa

1. **Confirme** o ambiente: `python --version` e (se houver) `git --version`.
2. **Crie** o repositório **`sd-2026-2`** no GitHub (Caminho A ou B do slide de ambiente).
3. **Rode** o exemplo `servidor_eco.py` / `cliente_eco.py` no seu Windows (dois terminais) e observe o erro ao derrubar o servidor.
4. **Espie o futuro:** clone o **kit da C1.A2** e rode a **rota síncrona** (passos no slide *"Kit da C1.A2"*).
5. **Opcional:** se tem pouca prática com Python/HTTP, faça o **roteiro de nivelamento** (`nivelamento.md` no repositório).

<div class="aviso">📌 <strong>Entregar até a próxima aula:</strong> link do repositório <code>sd-2026-2</code> criado (o 1º commit pode ser concluído amanhã na VM).</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- Conceito e **caracterização** de sistemas distribuídos.
- Vantagens e desafios: **escalabilidade, disponibilidade** e **falha parcial**.
- Diferença **centralizado × distribuído**.
- Tipos de **transparência** (acesso, localização, replicação).

**Termos-chave:** Sistema distribuído · Falha parcial · Transparência · Escalabilidade · Latência

<div class="dica">💡 A falha parcial aparece <strong>disfarçada em estudos de caso</strong>; a latência costuma justificar decisões de arquitetura.</div>

---

## Questão de autoavaliação (estilo ENADE)

Um serviço **A** envia uma requisição ao serviço **B** e **não recebe resposta** no tempo esperado. Assinale a alternativa correta.

A) A pode concluir **com certeza** que B falhou.
B) A pode concluir que a requisição **certamente não** foi processada.
C) A **não distingue**, só pela ausência de resposta, entre B ter caído, estar lento ou a resposta ter se perdido.
D) A deve **encerrar todo o sistema**, pois é falha total.
E) A situação **não ocorre** com TCP.

---

## Resolução — alternativa **C**

- É a definição de **falha parcial**: a ausência de resposta é **ambígua**.
- O **TCP não elimina** o problema — B pode cair **depois** de receber o pedido.
- As demais afirmam **certezas** que A **não possui**.

<div class="dica">💡 Repare como o mesmo cenário da demo de hoje vira questão de prova.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 1 — Caracterização de SD.
- **Tanenbaum & Van Steen**, *Distributed Systems*, 4ª ed., cap. 1 (PDF grátis dos autores).
- **Guarde o desenho de hoje** — você vai refazê-lo no fim do semestre.

</div>

<div>

**Glossário**
- **Sistema distribuído:** máquinas independentes que se apresentam como uma só.
- **Falha parcial:** parte falha, resto continua.
- **Latência:** tempo de ida de uma mensagem na rede.
- **Transparência:** esconder a complexidade da distribuição.
- **Repositório:** pasta versionada pelo Git.

</div>

</div>

---

<!-- _class: secao -->

# Até a próxima aula 🚀
### Entregue o repositório `sd-2026-2`. A Aula 2 começa revendo isto.

**Próxima:** Modelos de arquitetura e **sockets (TCP/UDP)** — seu primeiro **servidor de eco**.

<a class="proximo" href="../index.html">↩ Voltar ao índice<small>todas as aulas</small></a>
