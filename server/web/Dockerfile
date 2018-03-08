FROM python:3.6

RUN pip install \
    pymysql==0.8.0 \
    Flask==0.12.0 \
    Flask-Bootstrap==3.3.7.1 \
    Flask-SQLAlchemy==2.2 \
    Flask-WTF==0.14 \
    Flask-Login==0.4.1

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "-u", "app.py"]
