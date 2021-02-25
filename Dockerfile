FROM python:stretch
ENV PYTHONUNBUFFERED 1
ENV IN_DOCKER 1

COPY requirements.txt /requirements.txt

RUN pip3 install pip --upgrade \
    && pip3 install -r /requirements.txt

EXPOSE 8080

WORKDIR /cars_app

ADD . /cars_app

VOLUME /cars_app

CMD python -m cars_app.main