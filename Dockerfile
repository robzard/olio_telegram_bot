FROM python:3.10-slim

# Установите зависимости
COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --upgrade pip && pip install -r requirements.txt

# Скопируйте исходный код бота в контейнер
COPY . .

CMD ["python", "bot.py"]
