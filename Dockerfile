FROM python:3.5
ENV PYTHONUNBUFFERED "1"
RUN mkdir /web_docker
WORKDIR /web_docker
ENV CELERY_APP "conference_room_reservation.celery:app"
ADD requirements.txt /web_docker/
RUN pip install -r requirements.txt
ADD . /web_docker/
ENTRYPOINT python manage.py
CMD runserver