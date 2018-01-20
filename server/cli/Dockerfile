FROM python:3.6

RUN pip install \
  paho-mqtt==1.3.1 \
  click==6.0 \
  arrow==0.12.0

RUN mkdir /code
ADD app.py /code
WORKDIR /code

CMD ["/bin/bash"]
