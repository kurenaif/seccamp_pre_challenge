FROM debian:10

WORKDIR /

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install pycryptodome

COPY source.py  /source.py

CMD ["/usr/bin/python3", "source.py"]

