FROM python:3.11-slim

# 1. Установка зависимостей
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Установка переменных окружения
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
ENV PATH="/usr/bin:$PATH"

# 3. Копирование файлов
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4. Запуск
CMD ["python", "telegrambot.py"]
