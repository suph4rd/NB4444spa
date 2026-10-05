# Backend Guidelines

## Project Structure

This directory contains the Django backend. Project settings and URL configuration live in `NB4444/`; domain models and admin code are in `B4/`; API code is in `api/`; web views and forms are in `web/`; templates are in `templates/`.

## Development Commands

- `python manage.py migrate`: apply database migrations.
- `python manage.py runserver 0.0.0.0:8008`: start the local Django server.
- `python manage.py test -v 2`: run the Django test suite.
- `./test_start.sh`: run the repository's backend test script.
- Run `flake8` from this directory for Python linting when making substantial backend changes.

## Conventions

- Use 4-space indentation, `snake_case` for functions and fields, and `PascalCase` for classes.
- Keep Django migrations committed whenever models change.
- Put tests near the app they cover, such as `B4/tests.py` or `api/tests.py`, and name test methods `test_<behavior>`.
- Follow existing Django patterns and preserve public API behavior unless the task requires a change.

## Configuration and Data

- Do not commit production secrets, database dumps, or user uploads.
- Use environment variables for secrets; `NB4444/local_settings.py` is available for local overrides.
- Treat `db/` and `media/foto/` as runtime data when backing up or deploying.
