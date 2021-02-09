FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DEBUG 0
WORKDIR /code

# install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements-server.txt

COPY . /code/

CMD gunicorn netguru.wsgi:application --bind 0.0.0.0:$PORT