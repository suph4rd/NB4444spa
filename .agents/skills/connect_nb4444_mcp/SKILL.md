---
name: connect_nb4444_mcp
description: Connect the NB4444 project's MCP server to local Codex using Docker and JWT, verify settings, and troubleshoot the connection. Use when asked to connect or restore nb4444 MCP in dev or production.
---

# Connecting NB4444 MCP

Respond in Russian. Complete the available connection steps when the user asks to configure MCP. If they only ask for instructions, provide commands without changing the environment.

## Preparation

Determine the project root from the actual path of this `SKILL.md`, obtained when loading the skill. The file is located at `<root>/.agents/skills/connect_nb4444_mcp/SKILL.md`; in Python, calculate the root as `Path(skill_file).resolve().parents[3]` (`Path` from `pathlib`). Do not use the current working directory or a hardcoded absolute path. Check that `mcp_server/README.md` and `docker/` exist in the identified root; if the structure does not match, locate the checkout. Calculate absolute paths only for local commands and the Codex configuration; do not write them to the repository.

Use the environment specified in the request. Otherwise run the checkout-local mcp_server/launch.py environment selection: choose the only env file with configured API URL and non-placeholder JWTs. If both or neither are configured, require explicit selection; never default to dev. Production may be selected automatically when it is the only configured environment. If both environments are requested, configure and verify each separately. Read the current `mcp_server/README.md`, the selected Compose file, and the environment template: they define the services and settings.

| Parameter | dev | prod |
| --- | --- | --- |
| Compose file relative to root | `docker/docker-compose.yml` | `docker/docker-compose-prod.yml` |
| Environment file | `mcp_server/.env` | `mcp_server/.env.prod` |
| Template | `mcp_server/.env.example` | `mcp_server/.env.prod.example` |
| API service | `nb4_api_dev` | `nb4_api_prod` |
| API inside Compose | `http://nb4-api-dev:8008` | `http://nb4-api-prod:9999` |
| JWT endpoint for local access | `http://localhost:8008/auth/jwt/create/` | `http://localhost:9999/auth/jwt/create/` |
| MCP name in Codex | `nb4444` | `nb4444_prod` |

The name `nb4444` is retained for dev connection compatibility. Production Compose assumes that Codex and Docker run on the production application's machine. For a remote production API, set `NB4444_API_URL` in `.env.prod` to the URL explicitly provided by the user and accessible from the container; do not start a local production API in this case. Do not invent domains or SSH access.

Check that the Docker CLI, Docker Compose, and Docker daemon are available. If Docker Desktop is stopped, explain that it needs to be started and continue with independent configuration preparation.

Create the selected environment file from the corresponding template only if the file does not exist, using umask 077. During an authorized connection setup, set its permissions to 0600 without changing its contents; in instructions-only mode, provide the command instead. Preserve existing settings and tokens. Do not print `.env` contents, passwords, or JWTs in messages or logs. Check that the file is excluded from Git.

Calculate absolute `COMPOSE_FILE` and `ENV_FILE` paths from the identified root, and take `API_SERVICE` from the table. Set PROJECT_ROOT to the calculated root. For every Compose invocation, including commands below, use this prefix to prevent inherited values from overriding the selected environment file:

```sh
env -u NB4444_API_URL -u NB4444_ACCESS_TOKEN -u NB4444_REFRESH_TOKEN -u NB4444_HTTP_TIMEOUT -u NB4444_UPLOAD_DIR docker compose ...
```

Preserve the remaining environment, including Docker connection settings. Inspect effective `compose config --format json` only inside a process: report the environment, API URL (without credentials/query), and token-presence booleans, never the full configuration or token values.

When Docker is available, check the services and build MCP for the selected environment:

```sh
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" --profile mcp build mcp
```

Before starting anything, check the selected API URL, Compose service state, and whether a dev API already listens on the Docker Desktop host. Use an existing reachable API. For a host API, set NB4444_API_URL=http://host.docker.internal:8008; for Compose use the table. A listening port alone does not identify NB4444: inspect the process/container and API response. If the port belongs to an unknown service, stop startup and explain the conflict. Do not overwrite an existing custom URL without establishing that it needs changing.

Only when dev API is absent and connection setup was requested, start it using the environment-clearing prefix:

```sh
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d "$API_SERVICE"
```

Startup runs migrations. Wait at most 60 seconds for an HTTP response from the expected API, using short bounded requests; authentication errors can establish reachability but do not verify authentication. Diagnose failures without printing secrets. Start or recreate production API only if explicitly authorized. For a remote production URL, never start a local API. Do not mix URLs and JWTs between environments.

## JWT

Use existing configured tokens if available. To obtain new ones, the user sends a `POST` request to `/auth/jwt/create/` on the selected environment's API with a JSON body containing `username` and `password`, and saves the response fields:

```dotenv
NB4444_ACCESS_TOKEN=access_value
NB4444_REFRESH_TOKEN=refresh_value
```

If tokens are missing and no secure authentication method has been provided, ask the user to obtain them and fill in the local environment file for the selected mode; do not ask them to send secrets in chat. Complete the other available preparation steps while waiting for a response. Do not store the password in the skill or the Codex configuration.

## Codex configuration

In the user's `${CODEX_HOME:-$HOME/.codex}/config.toml`, add or update only the `mcp_servers.nb4444` section for dev or `mcp_servers.nb4444_prod` for prod. Preserve the connection for the other environment. Preserve all other settings; create a backup before modifying an existing file. Do not create duplicate TOML sections. Use the calculated absolute paths of the actual checkout with correct TOML escaping. In the template below, replace `SERVER_NAME` with the name from the table and the path placeholders with the calculated values: Codex does not automatically expand shell variables in `args`.

```toml
[mcp_servers.SERVER_NAME]
command = "python3"
args = ["ABSOLUTE_PROJECT_ROOT/mcp_server/launch.py", "--env", "SELECTED_MODE"]
```

Tokens are passed from the selected environment file through Compose. MCP does not need a separate HTTP port: the server uses stdio, and Codex reuses the environment container. `-T` disables the terminal, and `--no-deps` assumes that the API is already running. Use a persistent MCP service with sleep infinity; the launcher prepares it with up --no-deps and opens independent sessions with exec -T.

## Verification and result

Before editing config.toml, locate Python 3.11+ with tomllib or an existing interpreter with tomli. Validate the prepared TOML before writing it, keeping the backup and unrelated sections. If no parser is available, prepare the proposed edit but leave config.toml untouched and report the missing prerequisite. If the Codex CLI is installed, verify registration with `codex mcp list` without exposing secret values. Registration alone does not prove successful authentication.

Verify the connection using the available `get_current_user` tool on the selected server (`nb4444` or `nb4444_prod`). Do not report the connection as verified until the call succeeds.

For reconnection after rebuilding, read [the reconnect procedure](references/reconnect.md). Do not restart the app-server daemon or kill an attached MCP container to refresh an integration.

Verify the new image independently through a fresh configured container. Apply the environment-clearing prefix described above to this command:

```sh
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" \
  exec -T mcp python - \
  < "$PROJECT_ROOT/mcp_server/smoke_check.py"
```

The script is supplied over stdin because it is deliberately absent from the image; it starts /app/server.py internally. This check reads application data but does not write it. Distinguish registration, fresh-container smoke success, accepted reload, and successful current-thread get_current_user. None implies the others. If refresh was accepted, check tools on the next turn; do not claim the current thread was refreshed before checking its tools and get_current_user.

For `authentication_required`, suggest updating JWTs in the selected environment file and restarting the MCP client; for a network error, check Docker, the running API, and `NB4444_API_URL`. Rebuild the image for the selected environment after changing MCP code. Do not write to application data to test the connection.

At the end, state the environment, the local configuration path, what was configured and verified, and any remaining user actions if needed.

## Unified launcher

Register command `python3` with args `[ABSOLUTE_PROJECT_ROOT/mcp_server/launch.py, --env, SELECTED_MODE]`. Use the actual interpreter path if needed. Both Codex and Desktop integrations must use this launcher. Label connections NB4444 dev and NB4444 prod distinctly; retain existing dev registration compatibility. Never silently fall back between environments. Diagnostics go to stderr, keeping stdout for MCP.
