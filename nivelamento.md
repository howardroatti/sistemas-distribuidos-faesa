# Roteiro de nivelamento — Python, terminal e HTTP

> Para quem tem pouca prática. Não é conteúdo de prova: é o **mínimo** para conseguir
> seguir os labs sem travar. Leve ~30 minutos. Tudo funciona no **Windows nativo**.

---

## 1. Abrir o terminal (e dois de uma vez)

- **PowerShell:** menu Iniciar → digite `PowerShell` → Enter.
- **No VS Code:** menu **Terminal → New Terminal**. Para um **segundo** terminal lado a lado,
  use **Terminal → Split Terminal** (vários labs pedem servidor num, cliente no outro).
- **Trocar de pasta:** `cd caminho\da\pasta`. Ver onde está: `pwd`. Listar arquivos: `ls`.

## 2. Python está instalado?

```powershell
python --version      # deve mostrar Python 3.x
# se "não é reconhecido", tente:
py --version
```

- Rodar um programa: `python arquivo.py`.
- Parar um programa travado/servidor: **Ctrl + C**.

## 3. Ambiente virtual (venv) e pacotes

Um **venv** isola os pacotes de um projeto. Só é preciso nos labs que usam bibliotecas
(FastAPI, gRPC); os labs de socket são **Python puro** e não precisam.

```powershell
python -m venv .venv               # cria o ambiente
.\.venv\Scripts\Activate.ps1       # ativa (o prompt passa a mostrar (.venv))
pip install nome-do-pacote         # instala pacotes DENTRO do venv
```

> **Se o PowerShell barrar com "running scripts is disabled on this system":**
> rode **uma vez** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e responda **S**.
> Alternativa: use `.\.venv\Scripts\activate.bat` (no Prompt de Comando, não no PowerShell).

## 4. Git e GitHub (o essencial)

```powershell
git --version
git clone URL_DO_REPOSITORIO       # baixa um repositório
git add .                          # marca as mudanças
git commit -m "mensagem"           # salva um ponto na história
git push                           # envia para o GitHub
```

- **Sem Git?** No site do repositório, botão verde **Code → Download ZIP**.

## 5. Vocabulário de rede e HTTP (para as Aulas 2, 4 e 5)

- **IP `127.0.0.1` (localhost):** "a própria máquina". Serve para testar cliente e servidor
  no mesmo PC.
- **Porta:** número que diz **qual programa** recebe a conexão (ex.: site na 443, seu lab na 5000).
- **Cliente × servidor:** o cliente **pede**, o servidor **responde**.
- **HTTP — verbos:** `GET` lê · `POST` cria · `PUT` atualiza · `DELETE` remove.
- **HTTP — status:** `200` ok · `201` criado · `400` erro do cliente · `404` não encontrado ·
  `500` erro do servidor.

## 6. Checklist antes da Aula 1

- [ ] `python --version` (ou `py --version`) responde.
- [ ] Consigo abrir **dois terminais** no VS Code.
- [ ] Sei **clonar** um repositório (ou baixar o ZIP).
- [ ] Entendo o que são **IP, porta e localhost**.

Se marcou os quatro, você está pronto. 🚀
