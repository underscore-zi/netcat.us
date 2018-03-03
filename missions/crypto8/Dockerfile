FROM ubuntu:trusty
RUN sudo dpkg --add-architecture i386
RUN sudo apt-get update
RUN sudo apt-get install -y libc6:i386
RUN sudo apt-get install ucspi-tcp
RUN sudo apt-get install -y python python-dev python-pip python-virtualenv
RUN adduser noob
COPY * /
WORKDIR /
EXPOSE 31337
USER noob
CMD tcpserver -t 50 -RHl0 0.0.0.0 31337 python main.py
