import redis
import os
import json
import time

class Cache:
    def __init__(self):  
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        for _ in range(10):
            try:
                self.client = redis.Redis(host=redis_host, port=redis_port, db=1, decode_responses=True) # Usamos una base de datos separada para cache
                self.client.ping()
                print("Iniciando Cache...")
                break
                
            except redis.exceptions.ConnectionError:
                print("Esperando a Redis...")
                time.sleep(2)
                
        else:
            raise Exception("No se pudo conectar a Redis después de varios intentos.")
            
        self.max_cache_size = 100
        self.cache_list_key = 'cache_keys'
        self.politica_remocion = 'LRU'  # Cambiar a 'FIFO' si se desea

    def save_to_cache(self, evento):
        
        event_id = evento['ID_evento']

        if not self.client.exists(event_id):
            current_size = self.client.llen(self.cache_list_key)
            if current_size >= self.max_cache_size:
                
                if self.politica_remocion == 'FIFO':
                    removed_id = self.client.lpop(self.cache_list_key)
                elif self.politica_remocion == 'LRU':
                    removed_id = self.client.lpop(self.cache_list_key)
                else:
                    removed_id = None

                if removed_id:
                    self.client.delete(removed_id)
                    print(f" Evento {removed_id} removido por {self.politica_remocion}.")

            self.client.set(event_id, json.dumps(evento), ex=3600)
            print(f" Evento {event_id} agregado a cache.")
            
            self.client.rpush(self.cache_list_key, event_id)

        else:
            # El evento ya está en caché
            if self.politica_remocion == 'LRU':
                # Mover al final como más recientemente usado
                self.client.lrem(self.cache_list_key, 0, event_id)
                self.client.rpush(self.cache_list_key, event_id)
                print(f" Evento {event_id} actualizado en orden LRU.")
            else:
                print(f" Evento {event_id} ya existe en el caché (FIFO no reordena).")

    def get_from_cache(self, event_id):
        
        evento_json = self.client.get(event_id)
        if evento_json:
            return json.loads(evento_json)
        return None
        
    def get_all_cache(self, start=0, end=-1):
    
        event_ids = self.client.lrange(self.cache_list_key, start, end)
        eventos = []
        for event_id in event_ids:
            evento_json = self.client.get(event_id)
            if evento_json:
                evento = json.loads(evento_json)
                eventos.append(evento)
                print(json.dumps(evento, indent=2))  # Impresión legible con sangría
                print("\n" + "-" * 40 + "\n")  # Separador
        return eventos
