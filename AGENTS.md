# Repository Guidelines

# language
Use russian language

## Project Structure & Module Organization

This repository contains a Django backend and a Vue frontend. Backend code lives in `NB4444/`: settings in `NB4444/NB4444/`, models and admin code in `B4/`, API code in `api/`, web views in `web/`, templates in `templates/`, and media under `media/`. Frontend code lives in `nb4444-vue/`, with components in `src/components/`, routing in `src/router/`, state in `src/store/`, plugins in `src/plugins/`, and assets in `src/assets/`. Docker Compose files and deployment scripts are at the repository root.

## Build, Test, and Development Commands

- `docker-compose up --build`: starts the local Django API on port `8008` and Vue dev server on port `8080`.
- `docker-compose -f docker-compose-test.yml up --build`: builds the backend test image and runs Django tests.
- `cd NB4444 && python manage.py migrate`: applies backend database migrations.
- `cd NB4444 && python manage.py runserver 0.0.0.0:8008`: runs the backend locally.
- `cd nb4444-vue && npm install`: installs frontend dependencies.
- `cd nb4444-vue && npm run serve -- --port 8080`: starts the Vue dev server.
- `cd nb4444-vue && npm run build`: creates the production frontend bundle.

## Coding Style & Naming Conventions

Use 4-space indentation for Python and Django naming: `snake_case` for functions and fields, `PascalCase` for classes, and descriptive modules. Keep migrations committed when models change. Vue files should use `PascalCase.vue` component names, camelCase JavaScript variables, and the existing Vue 3 style used in `src/components/` and `src/mixins/`. `flake8` is listed for backend checks; run it from `NB4444/` before larger Python changes.

## Testing Guidelines

Backend tests should use Django's test framework and live near the app they cover, for example `NB4444/B4/tests.py` or `NB4444/api/tests.py`. Name methods `test_<behavior>`. Run `python manage.py test -v 2` from `NB4444/`, or use `NB4444/test_start.sh`. No frontend test script is configured; add one to `nb4444-vue/package.json` before adding frontend tests.

## Commit & Pull Request Guidelines

Recent commits use short scope prefixes such as `docker:`, `backend:`, `front:`, `api:`, and `hotfix`. Keep commits focused and write messages like `scope: concise change summary`, for example `api: add note serializer validation`. Pull requests should explain the change, list verification commands, mention migrations or config changes, link issues when available, and include screenshots for visible Vue UI changes.

## Security & Configuration Tips

Do not commit production secrets, database dumps, or user uploads. `SECRET_KEY` can come from the environment, and `local_settings.py` is supported for local overrides. Treat `NB4444/media/foto/` and `NB4444/db/` as runtime data when backing up or deploying.
