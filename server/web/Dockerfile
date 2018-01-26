FROM python:3.6

RUN pip install Flask

RUN mkdir /app
ADD app.py /app
WORKDIR /app

EXPOSE 80

CMD ["python", "app.py"]