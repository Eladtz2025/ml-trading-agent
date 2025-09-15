FROM python:3.11
WORKIDR ?app # {{ FAST web server entry point }}
COPY ./app /app
COPY
.ui /ui
RUN Python ./app/main.py
