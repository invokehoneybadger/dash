# Simple Flask app for HoneyBadger Swarm Dashboard
FROM python:3.11-slim

# Environment setup
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy app
COPY app.py /app/

EXPOSE 8181

# Run Flask directly
CMD ["python", "app.py"]
