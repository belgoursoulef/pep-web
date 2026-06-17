FROM python:3.10-slim

# Set timezone/locale if necessary (optional)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy web app files
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
