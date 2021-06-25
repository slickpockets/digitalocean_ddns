FROM ubuntu:20.04
MAINTAINER slickpockets

RUN apt-get update && apt-get install -y cron python3 python3-pip
ADD requirements.txt /requirements.txt
ADD main.py /main.py
ADD entrypoint.sh /entrypoint.sh
ADD run.sh /run.sh
ADD .env /.env
RUN pip install -r requirements.txt
#RUN chmod +x /main.py /entrypoint.sh
RUN chmod +x /run.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
