FROM debian:latest
MAINTAINER Lucas Menendez "epucas@gmail.com"

ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip python-setuptools sqlite3 libsqlite3-dev libicu-dev

COPY requirements.txt ./

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data all

WORKDIR /workdir
ENTRYPOINT python3 run.py