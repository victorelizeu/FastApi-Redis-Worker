import redis
import time

redis_client = redis.Redis("redis", 6379, decode_responses=True)

while True:
    tarefa = redis_client.brpop("minha_fila", timeout=0)

    print("COMEÇOU!")

    time.sleep(5)

    print("TERMINOU!")
