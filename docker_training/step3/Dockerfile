FROM debian:10

# これは悪い例です！でも一度動かしてみてください！

COPY source.py  /source.py

WORKDIR /

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install pycryptodome

CMD ["/usr/bin/python3", "source.py"]

