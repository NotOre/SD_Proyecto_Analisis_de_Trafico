import redis
import os
import json
import time
import random
import numpy as np

LAMBDA_POISSON = 100      # promedio de eventos por segundo (para Poisson)
ALPHA_PARETO = 2.0    # parámetro de forma de la distribución
SCALE_PARETO = 0.2    # escala base para el intervalo mínimo en segundos

class traffic_generator:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        
        for _ in range(10):
            try:
                self.client = redis.Redis(host=redis_host, port=redis_port, db=0)
                self.client.ping()
                print("Iniciando Generador de Trafico (Alternando aleatoriamente entre los modelos de llegada Poisson y Burst/Pareto/Heavy-Tailed)")
                break
            except redis.exceptions.ConnectionError:
                print("Esperando a Redis...")
                time.sleep(2)
        else:
            raise Exception("No se pudo conectar a Redis después de varios intentos.")
            
    def random_alternator(self):
        # Alterna aleatoriamente entre intervalo Poisson y Pareto.
        if random.random() < 0.5:
            return np.random.exponential(1 / LAMBDA_POISSON)
        else:
            return SCALE_PARETO * (1 + np.random.pareto(ALPHA_PARETO))

    def generar_trafico(self):
        eventos_consultados = []
        max_eventos = 5000

        while len(eventos_consultados) < max_eventos:
            total_eventos = self.client.llen('eventos')
            if total_eventos == 0:
                print("¿No hay eventos?...")
                time.sleep(1)
                continue

            index = random.randint(0, total_eventos - 1)
            evento_json = self.client.lindex('eventos', index)
            if evento_json:
                evento = json.loads(evento_json)
                eventos_consultados.append(evento)

            print(f"Eventos consultados: {len(eventos_consultados)} / {max_eventos}")
            intervalo = self.random_alternator()
            time.sleep(intervalo)

        return eventos_consultados
