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
( If port 90 and 9999 is busy, you can change the port in the docker-compose-prod.yml file <br>
and change port for app.config.globalProperties.$apiHost <br> 
in ./nb4444-vue/src/mail.js   )
5. Run file update.sh in console, witch situated in the root of the project

In the end, project will available on the 90 port (If you haven't changed the default port)

# Information for reserve copy:
1) folder media/foto !!!!!!!!!!!
2) copy DB
