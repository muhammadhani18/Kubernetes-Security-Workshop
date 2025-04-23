FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# VULNERABILITY: Running as root
# Should use: USER 1000

CMD ["python", "app.py"]