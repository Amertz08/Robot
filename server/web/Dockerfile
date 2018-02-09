FROM python:3.6

RUN pip install \
    Flask==0.12.0 \
    Flask-Bootstrap==3.3.7.1

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]
