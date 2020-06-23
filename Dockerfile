FROM python:3.8.2-slim
RUN mkdir /app && \
    apt-get update
RUN apt-get install build-essential python -y
WORKDIR /app
RUN pip install pip-tools
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]