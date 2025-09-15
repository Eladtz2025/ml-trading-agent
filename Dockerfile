FROM python:3.11
WORKING_DIR /app
COPY . /app
COPY . /ui

RUN pip install uvicorn fastapi tailwind

WORKDIR /ui
ENTRYPOINT [ "/ui/build/index.html" ]

XPOSEN 5000
RUN uvicorn api.app:app --host 0.0.0.0 --port 5000
