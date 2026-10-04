# Aula 13 - empacota o servico (codigo + ambiente) numa imagem Docker.
# Build:  docker build -t servico-nuvem .
# Run:    docker run -p 8000:8000 servico-nuvem   ->  http://127.0.0.1:8000

FROM python:3.12-slim

# 1) diretorio de trabalho dentro da imagem
WORKDIR /app

# 2) instala as dependencias primeiro (aproveita o cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copia o codigo da aplicacao
COPY app.py .

# 4) documenta a porta e sobe o servidor ouvindo em 0.0.0.0 (todas as interfaces)
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
