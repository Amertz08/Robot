FROM python:3.6

RUN pip install \
    PyYAML==3.12

RUN mkdir /code
ADD RouteSolver.py /code
ADD Graph.py /code
ADD route1.yml /code
WORKDIR /code

CMD ["python", "RouteSolver.py", "-c", "route1.yml" ]
