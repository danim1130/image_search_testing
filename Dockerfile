FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3.6 python3-pip libsm6 libxext6 libxrender1 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD gunicorn -b 0.0.0.0:8080 -w $(cat /proc/cpuinfo | grep processor | wc -l) --max-requests 10 --max-requests-jitter 4 --timeout 20 main


