# Usamos una imagen oficial de Python
FROM python:3.11-slim

# Variables de entorno para que Python no guarde cache y sea más limpio
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el scraper
CMD ["python", "main.py"]
