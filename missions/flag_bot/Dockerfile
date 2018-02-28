FROM debian:stable-slim

RUN apt-get update && apt-get install -y socat

EXPOSE 9999
WORKDIR /

USER root

ADD ./forgetfulflagbot /forgetfulflagbot
ADD ./flag.txt /flag.txt

RUN chmod +x ./forgetfulflagbot

CMD ["/usr/bin/socat", "TCP4-LISTEN:9999,reuseaddr,fork", "EXEC:./forgetfulflagbot"]