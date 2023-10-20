FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


RUN apt-get update
RUN apt-get install curl

# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
# RUN #apt-get install -y nodejs

COPY . /NB4444

WORKDIR /NB4444

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# RUN cd ./vueapp && npm install && npm run build

RUN mkdir common_static
RUN mkdir db

EXPOSE 9999
CMD python manage.py makemigrations ; \
python manage.py migrate ; \
python manage.py collectstatic --noinput; \
python manage.py runserver 0.0.0.0:9999