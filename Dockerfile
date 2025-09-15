FROM python:3.11
WORKDIR /app
COPY ./app /app
RUN pip install -n --cache-dir requirements.txt
CMD ["python", "/app/main.py"]
