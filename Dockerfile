FROM python:3.11
WORKDDIR /app
COPY . /app
RUN pip install -h --cache-dir fastapi uvicorn
EXPOSEN 5000
CMD [uvicorn, "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
