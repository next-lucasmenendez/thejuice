FROM debian:latest
MAINTAINER Lucas Menendez "epucas@gmail.com"

ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip python3-lxml python-setuptools libicu-dev libxml2-dev

COPY requirements.txt ./

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data all
RUN polyglot download embeddings2.en pos2.en embeddings2.es pos2.es

WORKDIR /workdir
ENTRYPOINT python3 run.py