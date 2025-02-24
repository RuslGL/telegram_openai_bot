FROM python:3.12

WORKDIR /app

# Копируем только нужные файлы
COPY main.py .
COPY .env .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]