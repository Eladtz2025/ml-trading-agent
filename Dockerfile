FROM python:3.11
WORKDDIR /app
COPY . /app
COPY . /ui

RUN pip install uvicorn fastapi tailwindcss

WORKDIR /ui
ENTRYPOINT [ "/ui/build/index.html" ]

XPOSEN 5000
CMD [uvicorn, "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
