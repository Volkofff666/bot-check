# Базовый образ Python
FROM python:3.12-slim


WORKDIR /bot


COPY . .


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["python", "main.py"]
