FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app.py .
COPY FrontEnd ./FrontEnd

# Cloud Run requires listening on PORT env variable
ENV PORT=8080
EXPOSE 8080

# CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT} --workers 1

