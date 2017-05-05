FROM debian:latest
MAINTAINER Lucas Menendez "epucas@gmail.com"


RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip python-imaging python-setuptools zlib1g-dev libjpeg-dev python-xmltodict

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

WORKDIR /workdir
ENTRYPOINT python3 run.py