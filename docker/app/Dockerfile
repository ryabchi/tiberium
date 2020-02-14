FROM python:3.7.4-alpine3.10

LABEL Description='Django Tiberium Backend image'
LABEL maintainer='aryabchi <cyberxx@yandex.ru>'

ENV PYTHONBUFERED=true
ENV PYTHONDONOTWRITEBYTECODE=true

COPY ./pyproject.toml /home/docker/code/app/
WORKDIR /home/docker/code/app

RUN apk update && \
 apk add --virtual .build-deps python3-dev gcc musl-dev linux-headers zlib-dev jpeg-dev build-base py-pip && \
 apk add jpeg postgresql-dev make && \
 pip install -U poetry==0.12.10 --no-cache-dir && \
 poetry config settings.virtualenvs.create false && poetry install && \
 apk --purge del .build-deps

COPY . /home/docker/code/app
#RUN mkdir /home/docker/code/app/static
#RUN cd /home/docker/code/app && python manage.py collectstatic --no-input

COPY ./docker/app/gunicorn.py /

EXPOSE 80

CMD ['python', 'manage.py', 'runserver']
