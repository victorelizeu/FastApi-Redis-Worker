from fastapi import FastAPI, Response, Request, HTTPException
import redis
import time

app = FastAPI()

redis_client = redis.Redis("redis", 6379, decode_responses=True)


@app.get("/processar")
def processar_dados(response: Response):
    chave_cache = "meu_resultado"

    dados_cache = redis_client.get(chave_cache)

    if dados_cache:
        response.headers["X-Cache"] = "HIT"

        return {"resultado": dados_cache, "origem": "Memória ultrarrápida Redis"}
    else:
        time.sleep(3)

        resultado_calculado = "Este é o dado processado de forma lenta e dolorosa"

        redis_client.setex(chave_cache, 30, resultado_calculado)

        response.headers["X-Cache"] = "MISS"

        return {"resultado": resultado_calculado, "origem": "Processamento no momento"}


@app.post("/enviar-tarefa")
def postar_dados():
    redis_client.lpush("minha_fila", "gerar_pdf")

    return {"status": "Tarefa recebida, estamos processando em background!"}


@app.get("/protegido")
def ip(request: Request):
    ip_usuario = request.client.host

    chave_limite = f"limite_ip:{ip_usuario}"

    acessos = redis_client.incr(chave_limite)

    if acessos == 1:
        redis_client.expire(chave_limite, 60)

    if acessos > 5:
        raise HTTPException(
            status_code=429, detail="Calma aí! Limite de 5 acessos por minuto atingido."
        )
    return {"mensagem": "Acesso liberado!", "acessos_neste_minuto": acessos}
