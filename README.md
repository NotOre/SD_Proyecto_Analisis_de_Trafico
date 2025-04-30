# SD_Proyecto_Analisis_de_Trafico
En este repositorio se encuentran los codigos y archivos requeridos para el uso de nuestro sistema de analisis de trafico, especificamente sobre la Region Metropolitana de Chile, basado en Docker, el cual funciona mediante un scraper utilizado sobre la plataforma Live-Map de Waze (https://www.waze.com/live-map), asi adquiriendo los eventos dentro del area establecida, almacenandolos en una base de datos y en un cache basados en Redis y, para determinar que almacena el cache, el sistema incluye un simulador de consultas el cual ayuda a definir los eventos almacenados en cache.

Este sistema esta orientado principalmente a usuarios que usen sistemas Unix-like (Linux o macOS), y se asume que dicho usuario ya tiene instaladas las dependencias y todo lo necesario para el uso de Docker y Python3.

Este proyecto sera dividido en 3 entregas que se iran actualizando con respecto a la realizacion de dichos avances.

# Entrega 1: Datos y Cache
Para ejecutar el codigo de esta entrega se prepararon 2 opciones principales, al guiarte por una de estas opciones debe ser ejecutada mediante una terminal que debes abrir dentro de la carpeta que almacena todos los archivos de nuestro sistema (llamada originalmente "SD_Proyecto_Analisis_de_Trafico-main"):

## Opcion 1: Make
Esta opcion fue creada con el objetivo de facilitar aun mas la utilizacion de nuestro sistema, quitando la necesidad de escribir comandos "largos" para ejecutar nuestro sistema basado en Docker, para esto, nuestro "Make" incluye las siguientes funciones:

### Cuando NO se han realizado modificaciones a ningun codigo

#### Construir imagenes y levantar contenedores (Inicia el sistema)
```bash
make up
```

### Cuando SI se han realizado modificaciones a algun codigo

#### 1) Reconstruir las imagenes
```bash
make build
```
#### 2) Levantar contenedores (Inicia el sistema)
```bash
make start
```
### Funciones extra

#### Detener contenedores (Usar en caso de querer detener el sistema, como para modificar algo del codigo o en caso de alguna falla ocurrida)
```bash
make down
```
#### Ver logs en vivo (Usar para ver lo que ocurre durante la ejecucion del sistema)
```bash
make logs
```

## Opcion 2: Docker-compose
Esta siendo la principal forma de iniciar un programa basado en Docker.

### Ejecucion

#### 1) Construir/reconstruir imagenes (Usar cada vez que se haya modificado el codigo o cuando recien se haya descargado el sistema)
```bash
docker-compose build
```
#### 2) Levantar contenedores (Inicia el sistema)
```bash
docker-compose up -d
```
### Detencion

#### Detener contenedores (Usar en caso de querer detener el sistema, como para modificar algo del codigo o en caso de alguna falla ocurrida)
```bash
docker-compose down
```
### Visualizacion

####  Ver logs en vivo (Usar para ver lo que ocurre durante la ejecucion del sistema)
```bash
docker-compose logs -f
```







# Entrega 2: Procesamiento
Coming soon...
# Entrega 3: Visualizacion
Coming soon...
