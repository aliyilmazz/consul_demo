FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /flaskapp
WORKDIR /flaskapp
RUN pip3 install -r requirements.txt
