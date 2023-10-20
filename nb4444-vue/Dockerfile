#FROM node:lts-alpine
#
#WORKDIR app/
#
#COPY . ./app/
#
#RUN #npm install

FROM node:lts-alpine as build-stage

RUN apk --no-cache add curl

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
RUN mkdir app
COPY . ./app
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)

#COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
#COPY . .

# build app for production with minification
RUN #npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]
