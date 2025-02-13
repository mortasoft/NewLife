FROM python:3.12.4-slim-bullseye

# Configure environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Stablish the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE ${API_PORT}

#CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${API_PORT} --workers 1 --threads 4 app:flask_app.app"]
CMD ["python", "app.py"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "app:flask_app.app"]


# Para generar la imagen
# docker build -t newlife-api .
# Para correr la imagen
# docker run -it -e API_PORT=5000 -p 5000:5000 test:latest