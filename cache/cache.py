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
            
        self.max_cache_size = 2000
        self.cache_list_key = 'cache_keys'
        self.politica_remocion = 'LRU'  # Cambiar a 'FIFO' si se desea

    def save_to_cache(self, evento):
        
        event_id = evento['ID_evento']
        evento_json = json.dumps(evento)

        if not self.client.exists(event_id):
            current_size = self.client.llen(self.cache_list_key)
            if current_size >= self.max_cache_size:
                
                if self.politica_remocion == 'FIFO':
                    removed_evento_json = self.client.lpop(self.cache_list_key)
                elif self.politica_remocion == 'LRU':
                    removed_evento_json = self.client.lpop(self.cache_list_key)
                else:
                    removed_evento_json = None

                if removed_evento_json:
                    removed_evento = json.loads(removed_evento_json)
                    removed_id = removed_evento['ID_evento']
                    self.client.delete(removed_id)
                    print(f" Evento {removed_id} removido por {self.politica_remocion}.")

            self.client.set(event_id, evento_json, ex=3600)
            self.client.rpush(self.cache_list_key, evento_json)
            print(f" Evento {event_id} agregado a cache.")

        else:
            # El evento ya está en caché
            if self.politica_remocion == 'LRU':
                # Mover al final como más recientemente usado
                self.client.lrem(self.cache_list_key, 0, self.client.get(event_id))
                self.client.rpush(self.cache_list_key, self.client.get(event_id))
                print(f" Evento {event_id} actualizado en orden LRU.")
            else:
                print(f" Evento {event_id} ya existe en el caché (FIFO no reordena).")

    def get_from_cache(self, event_id):
        
        evento_json = self.client.get(event_id)
        if evento_json:
            return json.loads(evento_json)
        return None
        
    def get_all_cache(self, start=0, end=-1):
    
        eventos_json = self.client.lrange(self.cache_list_key, start, end)
        eventos = [json.loads(e) for e in eventos_json]
        for evento in eventos:
            print(json.dumps(evento, indent=2))
            print("\n" + "-" * 40 + "\n")
        return eventos
