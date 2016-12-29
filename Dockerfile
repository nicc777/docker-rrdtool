FROM ubuntu:latest
MAINTAINER Nico Coetzee <nicc777@gmail.com>

LABEL Description="A container to experiment with rrdtool" Vendor="none" Version="0.1"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y apt-utils libterm-readline-perl-perl
RUN apt-get -y install rrdtool rrdcached sudo 

EXPOSE 5000

RUN mkdir /rrd_data
RUN mkdir /rrd_tmp
RUN mkdir /rrd_journal

VOLUME ["/rrd_data", "/rrd_tmp", "/rrd_journal"]

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/rrduser && \
    echo "rrduser:x:${uid}:${gid}:Developer,,,:/home/rrduser:/bin/bash" >> /etc/passwd && \
    echo "rrduser:x:${uid}:" >> /etc/group && \
    echo "rrduser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/rrduser && \
    chmod 0440 /etc/sudoers.d/rrduser && \
    chown ${uid}:${gid} -R /home/rrduser /rrd_data /rrd_tmp /rrd_journal

USER rrduser
ENV HOME /home/rrduser

# rrdcached -l 0.0.0.0:5000 -z 2 -f 3600 -p /rrd_tmp/rrdcached.pid -t 8 -j /rrd_journal -g -b /rrd_data
CMD ["rrdcached", "-l", "0.0.0.0:5000", "-z", "2", "-f", "3600", "-p", "/rrd_tmp/rrdcached.pid", "-t", "8", "-j", "/rrd_journal", "-g", "-b", "/rrd_data"]


