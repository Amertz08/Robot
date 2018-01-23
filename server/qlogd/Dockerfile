FROM python:3.6

RUN pip install \
  paho-mqtt==1.3.1 \
  pymongo==3.6.0

RUN mkdir /code /var/app
ADD app.py /code
ADD wait-for-it.sh /code
WORKDIR /code

CMD ["./wait-for-it.sh", "broker:1883", "--", "python", "app.py"]
