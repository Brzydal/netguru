FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DEBUG 0
WORKDIR /code

# install dependencies
COPY requirements.txt /code/
COPY requirements-server.txt /code/
RUN pip install -r requirements-server.txt

COPY . /code/

# collect static files
RUN python manage.py collectstatic --noinput

CMD gunicorn netguru.wsgi:application --bind 0.0.0.0:$PORT