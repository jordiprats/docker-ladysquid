FROM python:3.8-alpine

ENV YOUTUBE_KEY="1234"

RUN apk --no-cache add ca-certificates squid musl-dev make cmake gcc g++ gfortran curl

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY evildetector.py .
RUN chmod +x /code/evildetector.py

COPY squid.conf /etc/squid/squid.conf

EXPOSE 3128

CMD [ "/usr/sbin/squid", "--foreground" ]