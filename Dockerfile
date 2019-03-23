FROM joyzoursky/python-chromedriver:3.6

# Dependecies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

ADD . /app
WORKDIR /app
CMD python server.py