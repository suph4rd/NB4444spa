# NB4444spa

An application for keeping personal notes and recording facts about your life. The project consists of a Django backend and a Vue 3 frontend.

## Project structure

- `NB4444/` — Django application, API, templates, database, and user-uploaded media.
- `nb4444-vue/` — Vue 3 frontend built with Vite.
- `docker-compose.yml` — local frontend and backend setup.
- `docker-compose-test.yml` — backend test setup.
- `docker-compose-prod.yml` — deployment configuration.

## Local development

Docker and Docker Compose are required. From the repository root, run:

```sh
./start-dev.sh
```

Once the services start:

- Frontend: <http://localhost:8080>
- Backend: <http://localhost:8008>

Backend database migrations are applied automatically at startup. The script runs development containers in the separate `nb4444-dev` Compose project, so starting them does not stop or replace production containers. To stop and remove only the development containers, run:

```sh
docker-compose -p nb4444-dev -f docker-compose.yml down
```

### Running without Docker

Backend (Python and dependencies from `NB4444/requirements.txt`):

```sh
cd NB4444
python manage.py migrate
python manage.py runserver 0.0.0.0:8008
```

Frontend (Node.js `^20.19.0` or `>=22.12.0`):

```sh
cd nb4444-vue
npm ci
npm run serve -- --port 8080
```

By default, the frontend connects to the API on port `8008`. For a production frontend build, the API port is set with the Docker build argument `VITE_API_PORT`; the default is `9999`. If the API is available on a different port, set it when building, for example:

```sh
VITE_API_PORT=10000 docker-compose -f docker-compose-prod.yml up -d --build
```

The value is embedded in the frontend during the build, so rebuild the frontend after changing it.

## Tests

To run the backend tests with Docker:

```sh
docker-compose -f docker-compose-test.yml up --build --remove-orphans
```

Or run them locally from the `NB4444/` directory:

```sh
python manage.py test -v 2
```

The `NB4444/test_start.sh` script runs the Docker tests and then executes `docker image prune -f`. The latter removes dangling images from the Docker host, including images unrelated to this project.

## Deployment

Git, Docker, and Docker Compose must be installed on the server. From the repository root, run:

```sh
./start-prod.sh
```

The script starts the production containers and removes dangling Docker images. The frontend is available on port `90`, and the API on port `9999`. To change the frontend's external port, edit the host-side port in the corresponding `ports` mapping in `docker-compose-prod.yml`. If you change the API's external port, update the host-side port mapping and set the same port in `VITE_API_PORT` when rebuilding the frontend.

The `update-prod.sh` script pulls changes with `git pull`, rebuilds and restarts the containers, and then runs `docker image prune -f`. Before running it, make sure your local changes are saved and be aware that pruning affects dangling images across the entire Docker host.

> The current production configuration runs Django using the built-in `runserver`; `DEBUG` is also enabled and `ALLOWED_HOSTS` accepts all hosts. Do not expose this configuration to the public internet without hardening Django settings and configuring a production-grade application server.

The first database migration creates an administrator account with a fixed initial password. Change this password before making the application publicly available. From the repository root, run:

```sh
docker-compose -f docker-compose-prod.yml exec nb4_api_prod python manage.py changepassword admin
```

## Backup and recovery

Back up both of these directories to restore the application:

- `NB4444/db/` — the SQLite database and related files.
- `NB4444/media/foto/` — uploaded photos.

Create a consistent database backup while the backend is stopped, or use an appropriate SQLite backup mechanism. Store backups separately from the application server. To restore the application, stop the containers, restore both directories from the backup, and start the application again.

## Configuration

- `SECRET_KEY` can be provided through an environment variable; do not use the default value in production.
- `NB4444/NB4444/local_settings.py` is intended for local overrides and is excluded from Git. Do not put secrets in the repository, and do not rely on this file as a secure way to configure the production container.
