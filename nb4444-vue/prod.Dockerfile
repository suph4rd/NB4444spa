FROM node:24-alpine AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
ARG VITE_API_PORT=9999
RUN npm run build

FROM nginx:alpine AS production-stage

COPY nginx.prod.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
