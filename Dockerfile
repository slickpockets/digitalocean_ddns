FROM ubuntu:20.04
MAINTAINER slickpockets

RUN apt-get update && apt-get install -y cron python3 python3-pip dnsutils
ADD requirements.txt /requirements.txt
ADD main.py /main.py
ADD entrypoint.sh /entrypoint.sh
ADD .env /.env
RUN pip install -r requirements.txt
RUN chmod +x /main.py /entrypoint.sh
ENTRYPOINT /entrypoint.sh
