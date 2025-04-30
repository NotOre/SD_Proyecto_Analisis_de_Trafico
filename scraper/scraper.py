import requests
import json
import random
import time

def scrape_events(max_eventos=10000):

    # Coordenadas
    top = -32.9222
    bottom = -34.2917
    left = -71.7149
    right = -69.7702

    # URL de consulta
    url = f"https://www.waze.com/live-map/api/georss?top={top}&bottom={bottom}&left={left}&right={right}&env=row&types=alerts,traffic"

    # Lista de eventos procesados
    eventos_guardados = []
    
    print(f"Iniciando Scraper")
    
    while len(eventos_guardados) < max_eventos:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            events_alertas = data.get('alerts', [])
            events_trafico = data.get('jams', [])

            # Juntar eventos de tráfico y alertas
            todos_los_eventos = [(event, 'trafico') for event in events_trafico] + [(event, 'alerta') for event in events_alertas]

            # Mezclar aleatoriamente
            random.shuffle(todos_los_eventos)

            # Procesar hasta llenar max_eventos
            for idx, (event, tipo) in enumerate(todos_los_eventos):
                if len(eventos_guardados) >= max_eventos:
                    break

                if tipo == 'trafico' and 'line' in event:
                    evento_formateado = {
                        'ID_evento' : idx,
                        'tipo': 'trafico',
                        'ciudad': event.get('city'),
                        'calle': event.get('street'),
                        'velocidad_kmh': event.get('speedKMH'),
                        'severidad': event.get('severity'),
                        'descripcion_bloqueo': event.get('blockDescription')
                    }
                    if event.get('line'):
                        coord_ini = event['line'][0]
                        coord_fin = event['line'][1]
                        evento_formateado['coordenadas_ini'] = {
                            'latitud': coord_ini.get('y'),
                            'longitud': coord_ini.get('x')
                        }
                        evento_formateado['coordenadas_fin'] = {
                            'latitud': coord_fin.get('y'),
                            'longitud': coord_fin.get('x')
                        }
                    eventos_guardados.append(evento_formateado)

                elif tipo == 'alerta' and 'location' in event:
                    evento_formateado = {
                        'ID_evento' : idx,
                        'tipo': 'alerta',
                        'ciudad': event.get('city'),
                        'calle': event.get('street'),
                        'tipo_alerta': event.get('type'),
                        'subtipo_alerta': event.get('subtype'),
                        'descripcion_reporte': event.get('reportDescription'),
                        'confianza': event.get('reliability')
                    }
                    if event.get('location'):
                        coord = event['location']
                        evento_formateado['coordenadas'] = {
                            'latitud': coord.get('y'),
                            'longitud': coord.get('x')
                        }
                    eventos_guardados.append(evento_formateado)

        else:
            print(f"Error en la solicitud: {response.status_code}")

        print(f" Eventos recolectados: {len(eventos_guardados)} / {max_eventos}")

        time.sleep(5)  # Esperar 5 segundos antes de volver a consultar

    return eventos_guardados
