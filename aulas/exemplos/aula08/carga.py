# carga.py - Aula 8: mede a vazao do pipeline assincrono variando o no de workers.
#
# Dispara N tarefas em POST /predict (assincrono) e cronometra quanto a fila
# leva para ESVAZIAR (todos os resultados ficando "pronto"). Rode o MESMO teste
# com 1, 3 e 6 workers e compare a vazao.
#
# Pre-requisito: TAREFAS 1, 2 e 3 implementadas (POST /predict, GET /resultado,
# worker guardando o resultado). Suba o Redis (docker compose up -d), a API
# (uvicorn app.api_rest:app) e os workers (python -m app.worker), cada um no seu
# terminal, antes de rodar isto.
#
# Uso:  python carga.py           # 50 tarefas (padrao)
#       python carga.py 100       # 100 tarefas
#
# IMPORTANTE: use 127.0.0.1, NAO "localhost". No Windows, "localhost" custa
# ~2s por requisicao (IPv6/proxy); com 127.0.0.1 cai para milissegundos.
import sys
import time

import requests

BASE = "http://127.0.0.1:8000"


def main(n: int) -> None:
    textos = [f"a tarefa numero {i} foi otima" for i in range(n)]

    inicio = time.time()
    ids = []
    for texto in textos:
        r = requests.post(f"{BASE}/predict", json={"texto": texto}, timeout=10)
        r.raise_for_status()
        ids.append(r.json()["id"])
    t_envio = time.time() - inicio
    print(f"[carga] {n} tarefas enfileiradas em {t_envio:.2f}s "
          f"({n / t_envio:.0f} req/s de submissao)")

    # espera a fila drenar: todos os resultados com status "pronto"
    prontos = 0
    while prontos < n:
        prontos = sum(
            1
            for tid in ids
            if requests.get(f"{BASE}/resultado/{tid}", timeout=10).json()
            .get("status") == "pronto"
        )
        print(f"\r[carga] prontos: {prontos}/{n}", end="", flush=True)
        if prontos < n:
            time.sleep(0.5)

    total = time.time() - inicio
    print(f"\n[carga] TODAS prontas em {total:.2f}s "
          f"| vazao media: {n / total:.1f} tarefas/s")
    print("[carga] anote o tempo e repita com 1, 3 e 6 workers.")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    main(n)
