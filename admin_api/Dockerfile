FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# VULNERABILITY: No resource limits in container
# No USER directive, runs as root

CMD ["python", "app.py"]
