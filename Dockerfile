FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -h --cache-dir fastapi uvicorn
EXPOSE 5000
CMD [uvicorn, "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
