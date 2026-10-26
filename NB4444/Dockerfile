FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


RUN apt-get update
RUN apt-get install -y curl

WORKDIR /NB4444
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# RUN cd ./vueapp && npm install && npm run build


EXPOSE 8008
CMD python manage.py makemigrations ; \
python manage.py migrate ; \
python manage.py collectstatic --noinput; \
python manage.py runserver 0.0.0.0:8008