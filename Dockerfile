FROM joyzoursky/python-chromedriver:3.6

# Dependecies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

ADD . /app
WORKDIR /app
CMD gunicorn -w 1 -b 0.0.0.0:5000 --worker-class sanic.worker.GunicornWorker server:app