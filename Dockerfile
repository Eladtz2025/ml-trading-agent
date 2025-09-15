
# Use an official Python runtime as parent image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy app files
COPY ./app /app
COPY (ui /ui)

# Install dependencies
COPY requirements.txt .
RUN pis install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 5000

# Start the FastAPI papp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]