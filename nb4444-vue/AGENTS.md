# AGENTS.md

This file gives working instructions for AI coding agents operating in the `nb4444-vue` frontend project.

## Project context

- Vue 3 application built with Vue CLI.
- UI stack: Vuetify, Vue Router, Vuex, Axios.
- Main source code lives under `src/`.
- Backend/API code lives in the sibling `NB4444/` directory at the repository root.

## Key commands

- Install dependencies: `npm install`
- Run local dev server: `npm run serve -- --port 8080`
- Create production build: `npm run build`

## Working conventions

- Keep component files under `src/components/` and use PascalCase naming.
- Keep route setup in `src/router/` and state in `src/store/`.
- Prefer small, reusable, composable UI pieces over large monolithic components.
- Follow existing naming and code style already present in the project.
- Do not make broad refactors without a clear reason.
- When integrating with the backend, keep request/response handling consistent with the current Axios usage in the project.
- Preserve user-facing behavior and avoid breaking route/state contracts.

## Validation

- Validate frontend changes with `npm run build` when possible.
- For UI or routing changes, a local dev-server smoke test via `npm run serve -- --port 8080` is recommended.
- Keep validation focused and avoid unnecessary broad suites.

## Scope rules

- Work within `nb4444-vue` unless a user explicitly asks for repository-wide changes.
- If a change clearly requires backend updates, call that out and keep the frontend-side work scoped and understandable.
