FROM python:3.12.4-slim-bullseye

# Working directory
WORKDIR /app

# Copy the requirements file
COPY app/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ .

EXPOSE ${API_PORT}

CMD gunicorn --bind 0.0.0.0:${API_PORT} --workers 1 --threads 4 app:flask_app.app


# Para generar la imagen
# docker build -t newlife-api .