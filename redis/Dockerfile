FROM redis:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /redis_config
WORKDIR /redis_config
RUN pip3 install -r requirements.txt
EXPOSE 6379
