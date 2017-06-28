FROM debian:latest
MAINTAINER Lucas Menendez "epucas@gmail.com"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip python-setuptools python3-lxml libxml2-dev

COPY requirements.txt ./

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data all
RUN python3 -m textblob.download_corpora
RUN python3 -c "import nltk; nltk.download(['cess_esp', 'omw'])"

ENV LANG=ascii LANGUAGE=ascii

WORKDIR /workdir
ENTRYPOINT python3 run.py