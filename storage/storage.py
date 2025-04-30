import redis
import os
import json
import time

class EventStorage:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        
        for _ in range(10):
            try:
                self.client = redis.Redis(host=redis_host, port=redis_port, db=0)
                self.client.ping()
                print("Iniciando Storage")
                break
                
            except redis.exceptions.ConnectionError:
                print("Esperando a Redis...")
                time.sleep(2)
                
        else:
            raise Exception("No se pudo conectar a Redis después de varios intentos.")
            
        self.list_name = "eventos"

    def save_event(self, event):
        self.client.lpush(self.list_name, json.dumps(event))

    def get_events(self, start=0, end=-1):
        events = self.client.lrange(self.list_name, start, end)
        return [json.loads(event) for event in events]

    def count_events(self):
        return self.client.llen(self.list_name)

    def clear_storage(self):
        self.client.delete(self.list_name)
