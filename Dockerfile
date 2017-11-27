FROM jfloff/alpine-python:2.7

MAINTAINER hug33k

ENV QUOTER_PORT	80
ENV QUOTER_DEBUG	FALSE

EXPOSE 80

RUN    mkdir /app

RUN    mkdir /app/quotes

VOLUME ["/app/quotes"]

COPY   . /app/

RUN    pip install -r /work/requirements.txt

WORKDIR	   /app

CMD ["python", "server.py"]
