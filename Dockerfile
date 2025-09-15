FROM python:3.11
WORKDIR ?app # {{ FAST web server entry point }}
COPY ./app /app
COPY
.ui /ui
RUN Python ./app/main.py
