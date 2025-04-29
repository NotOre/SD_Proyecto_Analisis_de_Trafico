from scraper.scraper import scrape_events
from storage.storage import EventStorage
from traffic_gen.traffic_gen import traffic_generator
from cache.cache import Cache
import time

def main():
    # Scrapeamos eventos desde Waze
    eventos = scrape_events()
    
    print(f"Fin de funcion Scraper")
    time.sleep(2)
    
    # Almacenamos los eventos en Redis
    storage = EventStorage()
    for evento in eventos:
        storage.save_event(evento)
    print(f" {len(eventos)} eventos almacenados.")

    # Generamos tráfico de consultas y obtenemos los eventos consultados
    traffic_gen = traffic_generator()
    eventos_consultados = traffic_gen.generar_trafico()
    print(f" {len(eventos_consultados)} eventos fueron consultados.")

    # Cacheamos solo eventos consultados
    cache = Cache()
    for evento in eventos_consultados:
        cache.save_to_cache(evento)
    print(f" {len(eventos_consultados)} eventos cacheados.")
    
    # Imprimimos que datos estan almacenados en cache (solo para verificar)
    cache.get_all_cache()

if __name__ == "__main__":
    main()
