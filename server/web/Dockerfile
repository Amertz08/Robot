FROM python:3.6

RUN pip install \
    pymysql==0.8.0 \
    Flask==0.12.0 \
    Flask-Bootstrap==3.3.7.1 \
    Flask-SQLAlchemy==2.2 \
    Flask-WTF==0.14 \
    Flask-Login==0.4.1 \
    blinker==1.4.0 \
    Flask-Testing==0.6.0 \
    Flask-Mail==0.9.1 \
    pyyaml==3.12

RUN mkdir /web
ADD . /web
WORKDIR /web

EXPOSE 5000

CMD ["python", "-u", "app.py"]
