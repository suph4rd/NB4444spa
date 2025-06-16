FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


RUN apt-get update
RUN apt-get install -y curl

WORKDIR /nb4444
COPY . .

RUN pip3 install -r requirements.txt

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# RUN cd ./vueapp && npm install && npm run build


EXPOSE 9999
CMD python manage.py makemigrations ; \
python manage.py migrate ; \
python manage.py collectstatic --noinput; \
python manage.py runserver 0.0.0.0:9999