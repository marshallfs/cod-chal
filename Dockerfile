# Usa una imagen oficial de Python 3.12.2 como imagen base
FROM python:3.12.2-alpine

# Establece el directorio de trabajo en el contenedor en /app
WORKDIR /app

# Añade el contenido del directorio actual en el contenedor en /app
ADD . /app

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Haz que el puerto 8000 esté disponible para el mundo exterior a este contenedor
ENV PORT=8000

EXPOSE $PORT

# Ejecuta el comando para iniciar uvicorn
CMD ["uvicorn", "coding_challenge_api:app", "--host", "0.0.0.0", "--port", "8000"]