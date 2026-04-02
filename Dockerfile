# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies needed for PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Expose port (Render sets PORT environment variable)
ENV PORT=8000
EXPOSE $PORT

# Command to run the application using Gunicorn
CMD gunicorn nepse_trade_journal.wsgi:application --bind 0.0.0.0:$PORT
