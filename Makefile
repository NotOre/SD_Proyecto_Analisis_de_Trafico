# Construir imagenes y levantar contenedores
up:
	docker-compose up -d --build

# Solo levantar contenedores
start:
	docker-compose up -d

# Detener contenedores
down:
	docker-compose down

# Ver logs en vivo
logs:
	docker-compose logs -f	

# Reconstruir imágenes
build:
	docker-compose build

# Borrar contenedores, volúmenes y redes
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

