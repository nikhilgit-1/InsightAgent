# Python 3.10 slim image use kar rahe hain taaki size chota rahe
FROM python:3.14-slim

WORKDIR /app

# Pehle requirements copy karke install karenge taaki caching ka fayda mile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Phir baaki saara code copy karenge
COPY . .

EXPOSE 8000

# Uvicorn ko 0.0.0.0 par bind karna zaroori hai taaki container ke bahar se access ho sake
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]