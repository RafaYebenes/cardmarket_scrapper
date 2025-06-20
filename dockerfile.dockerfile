# Usa imagen base oficial de Python
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r playwright install

# Lanza el bot
CMD ["python", "-m", "bot.bot"]
