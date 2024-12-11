FROM python:3.12.4-slim-bullseye

# Working directory
WORKDIR /app

# Copy the requirements file
COPY app/requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY app/ .

CMD ["python", "main.py"]


# Para generar la imagen
# docker build -t newlife-api .