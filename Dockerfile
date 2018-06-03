FROM python:2

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gnuplot-x11
RUN pip install gnuplotlib gdax python-dateutil numpy

COPY . .

CMD [ "python", "-u", "./app.py" ]
