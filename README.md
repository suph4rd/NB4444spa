# NB4444spa
My own daily!

This is system for write some facts about life.

---------------------------------
# Deploy project
If you want to run project in production, you should to do next steps:

1. Copy the project ```https://github.com/suph4rd/NB4444spa.git```
2. Move to the project directory ```cd NB4444spa```
3. If you don't have docker and docker-compose on your system, you should install its
4. Check availability and openness of ports 90 and 9999 <br>
( If port 90 is busy, change the host port in `docker-compose-prod.yml`. If the API port is changed, set `VUE_APP_API_PORT` in the shell or `.env` file before building; it is embedded in the frontend during the production build. )
5. Run file update.sh in console, witch situated in the root of the project
   After a successful deployment, `docker image prune -f` removes dangling images from the Docker host (not only this project); tagged or in-use images are retained.
6. Default superuser credentials:
    - username: admin
    - password: 55555

In the end, project will available on the 90 port (If you haven't changed the default port)

# Information for reserve copy:
1) folder media/foto !!!!!!!!!!!
2) copy DB
