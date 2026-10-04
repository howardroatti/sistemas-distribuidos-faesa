---
marp: true
theme: faesa
paginate: true
footer: 'Prof. M.Sc. Howard Cruz Roatti · FAESA · Sistemas Distribuídos e Computação em Nuvem · 2026/2 · [☰ Sumário](../index.html)'
---

<!-- _class: capa -->
<!-- _paginate: false -->

# Sistemas Distribuídos e Computação em Nuvem

## Aula 16 — Segurança, privacidade e LGPD

C3 · 📶 **Estudo Dirigido (EAD)** · véspera do ENADE
Prof. M.Sc. Howard Cruz Roatti · FAESA · 2026/2

---

## Como funciona este Estudo Dirigido (EAD)

Aula **assíncrona**. Siga nesta ordem:

1. **Leia** os conceitos de segurança (criptografia, TLS, autenticação/autorização, LGPD).
2. **Faça o roteiro guiado** — proteger a plataforma (JWT, HTTPS, logs limpos).
3. **Resolva o simulado ENADE** (corrigido no início da próxima aula).
4. **Conclua o C3.A2** — completo, **seguro** e documentado.

<div class="aviso">📌 <strong>O ENADE é no próximo domingo (29/11).</strong> A revisão do fim deste material é parte essencial do EAD.</div>

---

## Objetivos desta aula

Ao final, você será capaz de:

1. **Explicar** criptografia (simétrica/assimétrica/hash) e o papel do **TLS/HTTPS**.
2. **Diferenciar** **autenticação** de **autorização** e usar **JWT** no gateway.
3. **Aplicar** princípios da **LGPD** no pipeline de IA (minimização, anonimização).

---

## Criptografia — o essencial

<div class="cols">

<div>

- **Simétrica:** **uma** chave secreta cifra e decifra. Rápida; o desafio é **compartilhar** a chave.
- **Assimétrica:** um **par** (pública + privada). Cifra-se com a pública, só a privada decifra (e vice-versa p/ assinar).
- **Hash:** resumo **de mão única** (senhas, integridade). Não "descriptografa".

</div>

<div>

<svg viewBox="0 0 360 200" role="img" style="width:100%;max-width:340px;display:block;margin:0 auto;font-family:'Segoe UI',Arial,sans-serif">
  <text x="90" y="18" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">simétrica</text>
  <rect x="20" y="28" width="60" height="30" rx="5" fill="#eef4fb" stroke="#12437f"/><text x="50" y="48" text-anchor="middle" font-size="10">texto</text>
  <rect x="100" y="28" width="60" height="30" rx="5" fill="#dcfce7" stroke="#16a34a"/><text x="130" y="48" text-anchor="middle" font-size="10">cifrado</text>
  <text x="90" y="74" text-anchor="middle" fill="#334155" font-size="10">🔑 mesma chave</text>
  <text x="270" y="18" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">assimétrica</text>
  <rect x="200" y="28" width="60" height="30" rx="5" fill="#eef4fb" stroke="#12437f"/><text x="230" y="48" text-anchor="middle" font-size="10">texto</text>
  <rect x="280" y="28" width="60" height="30" rx="5" fill="#dcfce7" stroke="#16a34a"/><text x="310" y="48" text-anchor="middle" font-size="10">cifrado</text>
  <text x="270" y="74" text-anchor="middle" fill="#334155" font-size="9.5">🔓 pública / 🔑 privada</text>
  <text x="180" y="110" text-anchor="middle" fill="#0d2b57" font-size="12" font-weight="700">hash (mão única)</text>
  <rect x="60" y="122" width="90" height="28" rx="5" fill="#eef4fb" stroke="#12437f"/><text x="105" y="140" text-anchor="middle" font-size="10">senha123</text>
  <text x="175" y="140" font-size="16">→</text>
  <rect x="200" y="122" width="120" height="28" rx="5" fill="#f1f5f9" stroke="#94a3b8"/><text x="260" y="140" text-anchor="middle" font-size="9.5" font-family="Consolas,monospace">a1f9c3… (resumo)</text>
  <text x="180" y="176" text-anchor="middle" fill="#dc2626" font-size="10">não há volta ←</text>
</svg>

</div>

</div>

<div class="dica">💡 <strong>Em miúdos:</strong> simétrica = <strong>cadeado com uma chave</strong> (os dois lados têm cópia); assimétrica = <strong>caixa de correio</strong> (qualquer um deposita pela fenda pública; só o dono abre); hash = <strong>triturar o papel</strong> (não dá para recompor).</div>

---

## TLS/HTTPS — o cadeado do transporte

O **HTTPS** é o HTTP **dentro de um túnel TLS**: o que trafega entre o cliente e o servidor vai **cifrado**, protegido contra **escuta** e **adulteração** no caminho.

<svg viewBox="0 0 800 140" role="img" style="width:100%;max-width:780px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <rect x="40" y="46" width="130" height="48" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="105" y="75" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">cliente 👤</text>
  <rect x="630" y="46" width="130" height="48" rx="9" fill="#eef4fb" stroke="#12437f" stroke-width="2"/><text x="695" y="75" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">servidor</text>
  <rect x="200" y="40" width="400" height="60" rx="30" fill="#dcfce7" stroke="#16a34a" stroke-width="2" stroke-dasharray="2 0"/>
  <text x="400" y="66" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">🔒 túnel TLS (tudo cifrado)</text>
  <text x="400" y="86" text-anchor="middle" fill="#166534" font-size="11">um bisbilhoteiro no meio só vê bytes embaralhados</text>
  <line x1="170" y1="70" x2="200" y2="70" stroke="#16a34a" stroke-width="2.5"/>
  <line x1="600" y1="70" x2="630" y2="70" stroke="#16a34a" stroke-width="2.5"/>
  <text x="400" y="126" text-anchor="middle" fill="#dc2626" font-size="11.5">HTTP puro = cartão-postal (todos leem) · HTTPS = carta lacrada</text>
</svg>

<div class="dica">💡 Na nuvem, o provedor (Render/Railway) normalmente já entrega <strong>HTTPS</strong> no domínio. Nunca envie token ou senha por <strong>HTTP puro</strong>.</div>

---

## Autenticação × autorização (e o JWT)

- **Autenticação (quem é você?):** provar a identidade (login/senha, token). 
- **Autorização (o que você pode?):** quais ações/recursos aquele usuário tem permissão.

<svg viewBox="0 0 800 120" role="img" style="width:100%;max-width:760px;display:block;margin:2px auto 0;font-family:'Segoe UI',Arial,sans-serif">
  <rect x="40" y="30" width="330" height="60" rx="10" fill="#eef4fb" stroke="#12437f" stroke-width="2"/>
  <text x="205" y="54" text-anchor="middle" fill="#0d2b57" font-size="13" font-weight="700">Autenticação</text>
  <text x="205" y="74" text-anchor="middle" fill="#334155" font-size="11.5">a portaria confere o documento 🪪</text>
  <rect x="430" y="30" width="330" height="60" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="595" y="54" text-anchor="middle" fill="#14532d" font-size="13" font-weight="700">Autorização</text>
  <text x="595" y="74" text-anchor="middle" fill="#166534" font-size="11.5">o crachá diz quais andares você acessa 🔑</text>
</svg>

<div class="dica">💡 O <strong>JWT</strong> resolve os dois: após o login, o servidor emite um token <strong>assinado</strong> que o cliente manda a cada requisição. Dentro dele vão a identidade (<code>sub</code>) e permissões (<code>role</code>).</div>

---

## Como um JWT funciona

Três partes: **`header.payload.assinatura`**. A assinatura é um **HMAC** de `header.payload` com um **segredo** que só o servidor tem.

```
eyJhbGciOiJIUzI1NiJ9 . eyJzdWIiOiJhbHVubzQyIiwicm9sZSI6ImFsdW5vIn0 . aptC2OKH...
   └─ header (alg)        └─ payload (sub, role, exp)                  └─ assinatura
```

- **Adulterar** o payload (ex.: `role: admin`) **quebra** a assinatura → o servidor **rejeita**.
- O payload é só **codificado** (base64), **não** cifrado: **nunca** coloque segredo nele.

<div class="dica">💡 O <code>auth_demo.py</code> cria um JWT real (HS256) e mostra os 4 casos: válido, adulterado, segredo errado e expirado.</div>

---

## LGPD no pipeline de IA

A **LGPD** rege o tratamento de **dados pessoais**. No seu serviço de IA:

- **Minimização:** só colete/envie o **necessário**. **Não** mande dados pessoais (CPF, nome, e-mail) ao **LLM** se não precisa.
- **Anonimização:** remova/mascare identificadores antes de processar.
- **Finalidade e consentimento:** use o dado só para o fim informado; registre a base legal.
- **Segurança:** cifrar em trânsito (TLS) e em repouso; **logs sem** dados sensíveis.

<div class="aviso">⚠️ Risco clássico: <strong>logar o prompt inteiro</strong> do usuário (com dados pessoais) ou <strong>enviar PII</strong> para uma API de LLM de terceiros sem necessidade. Minimize.</div>

---

<!-- _class: secao -->

# Roteiro guiado
### Proteger a plataforma — JWT, HTTPS e logs limpos

---

## Mão na massa — siga o Guia do Laboratório

Roteiro em **4 missões**: entender o JWT no aquecimento, **proteger o gateway com JWT**, **garantir HTTPS e logs limpos (LGPD)** e **fechar o C3.A2**.

### 👉 [Abrir o Guia do Laboratório »](lab-16-missoes.html)

<span style="font-size:0.62em;color:#6b7280">no índice do site: Aula 16 → <strong>Guia do Lab</strong></span>

<div class="dica">💡 Aquecimento pronto e testado: <code>exemplos/aula16/auth_demo.py</code> — JWT HS256 em Python puro (criar, verificar, detectar adulteração).</div>

---

## O que o exemplo mostra (aquecimento)

```powershell
python auth_demo.py
#   1) token valido: OK -> {'sub': 'aluno42', 'role': 'aluno', ...}
#   2) payload adulterado (role=admin): REJEITADO -> assinatura invalida
#   3) segredo errado: REJEITADO -> assinatura invalida
#   4) token expirado: REJEITADO -> token expirado
```

<div class="dica">💡 É a garantia de integridade: sem o <strong>segredo</strong>, ninguém forja nem altera um token sem ser pego.</div>

---

## Revisão para o ENADE — o semestre em uma página

<div class="cols">

<div>

**C1 · Comunicação**
Falha parcial · socket · **TCP/UDP** · thread/corrida · **gRPC/.proto** · **REST**/status/idempotência · IA como serviço.

**C2 · Coordenação**
Fila/assíncrono · **Lamport**/vetorial · **CAP** (CP×AP) · **Raft**/quórum · resiliência (timeout/retry/**disjuntor**).

</div>

<div>

**C3 · Nuvem e segurança**
IaaS/PaaS/SaaS · **container**/imagem · elasticidade · orquestração · **serverless**/cold start · **observabilidade** (log/métrica/**trace**) · **TLS/JWT**/LGPD.

<div class="dica">💡 Releia os quadros <strong>Foco ENADE</strong> de cada aula. É o melhor resumo possível.</div>

</div>

</div>

---

## No seu trabalho — C3.A2

- **Proteja o gateway** com **JWT**: rota de login emite o token; rotas sensíveis exigem `Authorization: Bearer <token>`.
- **HTTPS** ativo (o provedor de nuvem entrega) e **logs limpos** (sem dados pessoais).
- **LGPD:** minimize o que vai ao LLM; documente a base legal no README.

<div class="dica">💡 Puxa para o kit: adicione o middleware de JWT no gateway e um teste simples — requisição sem token recebe <strong>401</strong>; com token válido, passa.</div>

---

## Atividade para casa

1. **Proteja** o gateway do **C3.A2** com **JWT** (login + rotas protegidas).
2. **Garanta HTTPS** no deploy e **remova dados sensíveis** dos logs.
3. **Resolva o simulado ENADE** e **conclua o C3.A2** (completo, seguro, documentado).

<div class="aviso">📌 <strong>Entregar até a Aula 17 (prova C3.A1):</strong> o C3.A2 completo, com JWT, HTTPS e notas de LGPD no README + o simulado ENADE resolvido. Roteiro no <strong>Guia do Laboratório</strong>.</div>

---

## ◆ Foco ENADE

**O que costuma cair:**
- **Criptografia** simétrica × assimétrica; **hash**; **TLS/HTTPS**.
- **Autenticação × autorização**; **JWT** (assinado, não cifrado).
- **LGPD:** minimização, anonimização, finalidade, segurança.
- Boas práticas: segredo fora do código, logs sem PII.

**Termos-chave:** Criptografia · TLS/HTTPS · Autenticação · Autorização · JWT · LGPD · Minimização

<div class="dica">💡 Pegadinha: achar que o payload do JWT é secreto. Ele é só <strong>codificado</strong> (base64) — qualquer um lê; a proteção é a <strong>assinatura</strong>.</div>

---

## Questão de autoavaliação (estilo ENADE)

Um desenvolvedor afirma que pode guardar a **senha do usuário** dentro do **payload de um JWT**, pois "o token é seguro". Sobre essa afirmação, é correto dizer que:

A) está certo, pois o JWT é totalmente cifrado
B) **está errado: o payload do JWT é apenas codificado (base64) e pode ser lido por qualquer um; a assinatura garante integridade, não sigilo**
C) está certo, desde que o token expire
D) está errado, pois o JWT não permite campos personalizados
E) está certo, pois o HTTPS já protege tudo

---

## Resolução — alternativa **B**

- O **payload** do JWT é **base64** (reversível) — **não** é cifrado. Qualquer um que receba o token **lê** o conteúdo.
- A assinatura garante **integridade/autenticidade** (não foi adulterado), **não sigilo**. Logo, **nunca** coloque senha/segredo no payload.

<div class="dica">💡 É exatamente o que o <code>auth_demo.py</code> evidencia: o payload é legível; o que protege é a assinatura com o segredo do servidor.</div>

---

## Fora da sala · Glossário

<div class="cols">

<div>

**Para estudar**
- **Coulouris**, cap. 11 — Segurança.
- Texto da **LGPD** (art. 6º — princípios) — leitura dirigida.
- Decodifique o token do `auth_demo.py` em **jwt.io** e veja o payload legível.

</div>

<div>

**Glossário**
- **Simétrica/assimétrica:** criptografia com uma chave / par de chaves.
- **Hash:** resumo de mão única.
- **TLS/HTTPS:** criptografia do transporte.
- **Autenticação/autorização:** quem é você / o que pode.
- **JWT:** token assinado (header.payload.assinatura).
- **LGPD:** lei de proteção de dados pessoais.

</div>

</div>

---

<!-- _class: secao -->

# Bons estudos! 🚀
### Proteja o C3.A2 (JWT + HTTPS + LGPD), resolva o simulado e **arrase no ENADE**.

**Próxima (Aula 17):** **Revisão e Avaliação C3.A1** + entrega do C3.A2 — o semestre inteiro em uma página e a prova final do ciclo.

<a class="proximo" href="aula-15-observabilidade.html">← Anterior<small>Aula 15 · Observabilidade</small></a>
<a class="proximo" href="../index.html">☰ Índice<small>todas as aulas</small></a>
