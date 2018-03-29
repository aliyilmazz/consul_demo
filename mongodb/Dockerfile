FROM mongo:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /mongodb_config
WORKDIR /mongodb_config
RUN pip3 install -r requirements.txt
EXPOSE 27017
COPY mongod.conf /etc/mongod.conf
COPY mongod.conf /etc/mongod.conf.orig
CMD ["python3", "config.py"]
