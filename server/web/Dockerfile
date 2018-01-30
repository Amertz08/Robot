FROM python:3.6

RUN pip install \
    Flask==0.12.0

RUN mkdir /app
ADD app.py /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]