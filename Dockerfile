# Usamos Python 3.11 ya que tu entorno actual usa esta versión
FROM python:3.11-slim

# Establecemos la carpeta de trabajo
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar el caché
COPY requirements.txt .

# Instalamos tus dependencias (discord.py, python-dotenv, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos del bot
COPY . .

# Comando para encender el bot
CMD ["python", "main.py"]