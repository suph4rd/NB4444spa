# MCP for NB4444

## Running with Docker (Codex)

From the project root:

```sh
cp mcp_server/.env.example mcp_server/.env
docker compose -f docker/docker-compose.yml up -d nb4_api_dev
docker compose -f docker/docker-compose.yml --profile mcp build mcp
```

Obtain JWT tokens via `POST http://localhost:8008/auth/jwt/create/`
with the JSON body `{"username":"your username","password":"your password"}`.
Save the response fields `access` and `refresh` as `NB4444_ACCESS_TOKEN` and
`NB4444_REFRESH_TOKEN` in `mcp_server/.env`. This file is excluded from Git
and the Docker build context.

Add the following to `~/.codex/config.toml` (replace `/absolute/project` with the project path):

```toml
[mcp_servers.nb4444]
command = "docker"
args = ["compose", "-f", "/absolute/project/docker/docker-compose.yml", "--env-file", "/absolute/project/mcp_server/.env", "run", "--rm", "--no-deps", "-T", "mcp"]
```

Open a new agent session and ask: “Call get_current_user through the nb4444 MCP server.”
Docker must be running. Each client starts its own MCP container;
`-T` keeps the stdio protocol running without a terminal. The service with the `mcp` profile does not start
with a regular `docker compose -f docker/docker-compose.yml up`. It does not need a separate HTTP port.

By default, MCP connects to `nb4-api-dev:8008` over the Compose network.
The network alias uses hyphens: Django rejects names containing underscores in the `Host` header.
If the API runs on the host, set
`NB4444_API_URL=http://host.docker.internal:8008` in `.env` (Docker Desktop).

To upload images, place files in `mcp_server/uploads/` or set
`NB4444_UPLOAD_DIR` in `.env`. Pass a path inside the container
to the `set_note_image` tool, for example `/uploads/photo.jpg`. Use an absolute path for `NB4444_UPLOAD_DIR`; relative paths are resolved from the `docker/` directory. The directory is mounted read-only.
Restart the MCP client after changing tokens; rebuild the image after changing code.

## Production Compose

On the machine running the production application, from the project root:

```sh
cp mcp_server/.env.prod.example mcp_server/.env.prod
docker compose -f docker/docker-compose-prod.yml up -d nb4_api_prod
docker compose -f docker/docker-compose-prod.yml --profile mcp build mcp
```

Obtain JWT tokens for a production user via `/auth/jwt/create/` on the production API
(`http://localhost:9999/auth/jwt/create/` for local access).
Save the tokens in `mcp_server/.env.prod`, which is excluded from Git.
Use separate environment files for dev and production: their API URLs differ.

Use the production Compose file and environment file in the Codex configuration:

```toml
[mcp_servers.nb4444_prod]
command = "docker"
args = ["compose", "-f", "/absolute/project/docker/docker-compose-prod.yml", "--env-file", "/absolute/project/mcp_server/.env.prod", "run", "--rm", "--no-deps", "-T", "mcp"]
```

This command assumes that the agent and Docker run on the production machine.
MCP connects to `http://nb4-api-prod:9999` within the production Compose network.
The client starts the `mcp` profile over stdio; a regular production `up` does not start it.
Image upload settings are the same as in the dev setup.

## Running without Docker

A local stdio server connects to the running application's REST API.
Use Python 3.14 (the same version as the backend Docker image).

```sh
python3.14 -m venv mcp_server/.venv
mcp_server/.venv/bin/pip install -r mcp_server/requirements.txt
```

Obtain JWT tokens by sending a POST request to `/auth/jwt/create/` with username/password.
Pass the access and refresh tokens through environment variables; do not store them in Git.

Example MCP client configuration (replace the absolute paths):

```json
{
  "mcpServers": {
    "nb4444": {
      "command": "/absolute/project/mcp_server/.venv/bin/python",
      "args": ["/absolute/project/mcp_server/server.py"],
      "env": {
        "NB4444_API_URL": "http://localhost:8008",
        "NB4444_ACCESS_TOKEN": "REPLACE",
        "NB4444_REFRESH_TOKEN": "REPLACE",
        "NB4444_UPLOAD_ROOT": "/absolute/uploads",
        "NB4444_HTTP_TIMEOUT": "30"
      }
    }
  }
}
```

The notes, plans, tasks, and deductions support list/get/create/update/delete operations.
Singular tool names use note/plan/task/deduction.
Create operations accept `data`; update operations accept `id` and `data`.
For example, create_plan: `{"data":{"name":"Week"}}`;
create_task: `{"data":{"plan":1,"section":null,"description":"Walk","priority":1}}`.
Pass the house/travel/phone/food monetary fields for deductions as strings.

List operations accept offset, page_size (1–100), and search;
task lists also accept plan, section, priority, and is_ready.
List responses contain items and next_offset. Fetch pages until next_offset is null.

Additional tools: get_current_user, list_sections, get_latest_deductions,
get_note_image(id), set_note_image(id,path), remove_note_image(id).
Uploads: JPEG/PNG/WebP files up to 10 MiB from NB4444_UPLOAD_ROOT.
Sections are read-only. Deletion is soft; tasks belonging to a deleted plan are hidden.
The nb4444://guide resource describes the fields; the review_plan and summarize_notes prompts
help prepare summaries.

If authentication_required occurs, obtain new JWT tokens and restart the process.
If a network error occurs during a write operation, check the result before retrying.
Logs go to stderr; stdout is reserved for MCP.

Backend tests: `cd NB4444 && python manage.py test -v 2`.
Run integration tests against a separate test database.

## Regression checks

Run MCP unit tests with the installed requirements:
`cd mcp_server && python -m unittest -v test_server`.
Backend contract tests: `cd NB4444 && python manage.py test -v 2`.
Tests use a separate database and temporary media files.

`list_notes` accepts `has_image=true/false`. `get_random_notes_with_images(count=10)`
returns up to count unique accessible notes with image references (count: 1–100).
Use `get_note_image` to display their image content. Unsupported entity filters
produce a validation error. HTTP 403 is permission_denied; HTTP 401 requires authentication.
Downloads enforce the 10 MiB limit while streaming and verify image contents.
After rebuilding MCP, reconnect the client to use the new tools.

Full protocol/HTTP integration check (requires backend and MCP requirements):
`python mcp_server/integration_check.py` from the repository root.
This script overrides database/media settings with temporary paths, starts a local
HTTP server, and runs CRUD plus image tools through a real stdio MCP session.
It does not connect to the configured dev or production API.
Write tool schemas document allowed fields; unknown fields are rejected.

## Environment-safe launcher

Use `python3 /absolute/project/mcp_server/launch.py --env prod` (or `--env dev`) as the MCP command in Codex or Desktop. Without `--env`, only the single configured environment is selected. Both configured or neither configured causes an error. Name connections distinctly: NB4444 dev / NB4444 prod. In prod request `list_notes` with `offset=0, page_size=10` for the ten newest posts.
