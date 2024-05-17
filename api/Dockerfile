FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .

COPY app/swagger.yml .

RUN pip install -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]