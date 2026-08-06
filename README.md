# Sistemas Distribuídos e Computação em Nuvem · FAESA

Material didático da disciplina **Sistemas Distribuídos e Computação em Nuvem** (2026/2), do Prof. M.Sc. **Howard Cruz Roatti** — FAESA Centro Universitário.

🌐 **Sumário (vivo):** https://howardroatti.github.io/sistemas-distribuidos-faesa/

Decks modernos em **Marp** (Markdown → slides), em HTML e PDF, aula a aula. A disciplina é **prática e cloud-native**: constrói-se, por partes, um **serviço de IA distribuído** — dos sockets à nuvem. Cada aula traz **laboratório detalhado**, foco no **ENADE** e um glossário.

## Estrutura

```
aulas/    slides das aulas (Marp): .md (fonte), .html e .pdf
themes/   tema visual FAESA (faesa.css)
index.html   sumário vivo (roteiro das 18 aulas)
build.sh     renderiza os decks (.md → .html) com o tema FAESA
```

## Como gerar os slides

Requer [`@marp-team/marp-cli`](https://github.com/marp-team/marp-cli).

```bash
./build.sh                          # renderiza todos os decks em aulas/
./build.sh aulas/aula-01-....md     # renderiza um deck específico
```

## Licença

Conteúdo sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br).
