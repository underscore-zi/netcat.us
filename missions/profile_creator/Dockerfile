FROM ubuntu:trusty
RUN sudo dpkg --add-architecture i386
RUN sudo apt-get update -y
RUN sudo apt-get upgrade -y
RUN sudo apt-get install libc6 libc6-dev -y
RUN sudo apt-get install -y libc6:i386
RUN sudo apt-get install ucspi-tcp
RUN sudo apt-get update -y
RUN sudo apt-get upgrade -y
RUN sudo apt-get install -y python python-dev python-pip python-virtualenv python3 --fix-missing --fix-broken
RUN adduser ctf
COPY libc.so.6 /lib/i386-linux-gnu/libc.so.6
RUN mkdir /challenge
COPY flag /challenge
COPY profile_creator /challenge/profile_creator
RUN chmod +x /challenge/profile_creator
WORKDIR /challenge
EXPOSE 31337
USER ctf
CMD tcpserver -t 50 -RHl0 0.0.0.0 31337 ./profile_creator
