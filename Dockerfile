# Базовый образ Python 3.10.12
FROM python:3.10.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Открываем порт для вебхуков (если нужно)
EXPOSE 8080

# Команда запуска бота
CMD ["python3", "main.py"]
