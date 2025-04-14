# Use Python base image
FROM python:3.12-slim

# Create app folder in container
WORKDIR /app

# Setting library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . .

# Create evironment variable for Django settings
ENV PYTHONUNBUFFERED=1

# Startserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]