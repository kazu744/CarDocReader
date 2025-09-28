FROM --platform=linux/amd64 python:3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
EXPOSE 8000 8001

COPY ./requirements.txt /tmp/requirements.txt

ARG DEV=false

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements*.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        app-user

USER app-user