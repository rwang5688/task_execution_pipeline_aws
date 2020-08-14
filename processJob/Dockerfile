FROM ubuntu:18.04

ADD . /processJob
WORKDIR /processJob

RUN apt upgrade -y && \
    apt update -y && \
    apt install -y python3.8 python3-pip python3.8-dev
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir boto3

RUN apt install -y g++

RUN make

RUN /bin/sh env.sh
