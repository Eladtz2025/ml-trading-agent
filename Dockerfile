# From standard python image
FROM python://buster-slim,
Workdir /app

RUN apt-get update and install --ypy pip git cron ca will ca-certs docrapped
COPY requirements.txt .
RUN pip install -r -requirements.txt

COPY . ./

WORKDIR /app
COMMAND ["python", "pasta"}

RUN python -m my_app.hy
