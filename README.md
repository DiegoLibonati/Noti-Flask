# Noti

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Description

**Noti** is a full-stack personal note-taking web application built with Python and Flask, following a clean MVC architecture with a strict separation between the API layer and the server-side rendered views.

**What the application does:**

The app lets users create an account, log in, and manage a private collection of short-form notes. Every note belongs exclusively to the authenticated user who created it — no user can see or interact with another user's notes. Each note stores its content and a UTC-aware creation timestamp so the user always knows when it was written.

**Authentication & session management:**

Registration requires a username, email, and password. Passwords are stored hashed (never in plain text). Once logged in, Flask-Login maintains the session securely using a signed cookie backed by the application's `SECRET_KEY`. Unauthenticated requests to any protected route are automatically redirected to the login page; authenticated users who try to reach the login or registration pages are redirected straight to their home dashboard. The logout endpoint invalidates the session immediately.

**Note lifecycle:**

From the home dashboard a logged-in user can:
- **Create** a new blank note with a single click — the note is persisted to the database and appears instantly in the UI without a full page reload.
- **Edit** any of their notes inline — the content is sent to the API via a PATCH request and the DOM is updated in place.
- **Delete** any note — a DELETE request removes it from the database and the card disappears from the view immediately.

All note mutations go through a REST JSON API (`/api/v1/notes/`) that the TypeScript frontend calls asynchronously, keeping the user experience smooth while the server stays the source of truth. A `/api/v1/health/` endpoint is also exposed so Docker, load balancers, and orchestrators can probe application liveness without authenticating.

**Frontend architecture:**

The UI is built with plain HTML5, Jinja2 templates, SCSS (compiled server-side via `libsass`), and vanilla TypeScript — no frontend framework. TypeScript is compiled and bundled at build time with a `tsc`-based pipeline that uses `tsc-alias` for path resolution and `chokidar` for watch mode during development. The compiled JavaScript is what the browser actually loads. Testing Library + Jest (via `ts-jest` and `jest-environment-jsdom`) covers the TypeScript layer.

**Backend architecture:**

The Flask application factory (`create_app`) wires together:
- **Blueprints** — one for the API routes (`/api/v1/...`) and one for the HTML view routes.
- **Controllers** — thin HTTP handlers that delegate all logic to services.
- **Services** — the business-logic layer, calling DAOs to read/write data.
- **DAOs (Data Access Objects)** — the only layer that talks to SQLAlchemy directly.
- **ORM models** — `User` and `Note`, defined with SQLAlchemy's typed `Mapped` columns.
- **Flask-Migrate** — handles all database schema migrations via Alembic.
- **Startup connection checks** (`src/startup/check_connections.py`) — at the end of `create_app`, the factory pings MySQL (`SELECT 1`) up to 5 times with a 2s delay between attempts and a 3s connect timeout per attempt. If the database is unreachable after all attempts, the app logs a warning and **boots anyway** — it never crashes because a service is down; DB-dependent features simply fail until the connection recovers. The check is gated by the `CHECK_CONNECTIONS` config flag (`True` by default, `False` in `TestingConfig` so the test suite never touches the network).

A custom `BaseAPIError` exception class lets any layer raise a typed error that the Flask error handler automatically converts into a consistent JSON response with the correct HTTP status code.

**Infrastructure & deployment:**

The application is fully containerized with Docker. The development stack (`dev.docker-compose.yml`) runs Flask with a Livereload/Tornado dev server and a MySQL 8 container, with SCSS and TypeScript watch modes active. The production stack (`prod.docker-compose.yml`) swaps in Gunicorn as the WSGI server behind an Nginx reverse proxy, with a separate MySQL container; the production image ships with a `HEALTHCHECK` that hits `/api/v1/health/`. Database credentials, ports, and Flask secrets are all configured via environment variables (see the **Env Keys** section). A shared `.githooks/pre-commit` shell hook (activated with `git config core.hooksPath .githooks`) enforces code quality on every commit, and a GitHub Actions workflow (`.github/workflows/ci.yml`) runs lint, audit, tests, and Docker builds on every push and pull request.

### Endpoints API

The REST API exposed by the Flask backend. All mutations on notes go through these endpoints; the TypeScript frontend consumes them asynchronously.

---

- **Endpoint Name**: Health
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/health/
- **Endpoint Fn**: Liveness probe — returns `200` with `{code, message}` so orchestrators and Docker `HEALTHCHECK` can verify the app is up
- **Endpoint Params**: None

---

- **Endpoint Name**: Logout
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/auth/logout
- **Endpoint Fn**: This endpoint logout the current user
- **Endpoint Params**: None

---

- **Endpoint Name**: Login
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/auth/login
- **Endpoint Fn**: This endpoint allows to login a existing user
- **Endpoint Body**:

```ts
{
    username: string;
    password: string;
}
```

---

- **Endpoint Name**: Sign Up
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/auth/sign_up
- **Endpoint Fn**: This endpoint creates a new user
- **Endpoint Body**:

```ts
{
    username: string;
    password: string;
    email: string;
}
```

---

- **Endpoint Name**: Create a Note
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/notes/
- **Endpoint Fn**: This endpoint creates a new note
- **Endpoint Body**: None

---

- **Endpoint Name**: Delete a Note
- **Endpoint Method**: DELETE
- **Endpoint Prefix**: /api/v1/notes/:id
- **Endpoint Fn**: This endpoint deletes a Note by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

- **Endpoint Name**: Update a Note
- **Endpoint Method**: PATCH
- **Endpoint Prefix**: /api/v1/notes/:id
- **Endpoint Fn**: This endpoint updates a Note by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

- **Endpoint Body**:

```ts
{
    content: string;
}
```

---

## Technologies used

Backend:

1. Python + Flask 3.1
2. SQLAlchemy (via Flask-SQLAlchemy)
3. Flask-Login (session management)
4. Flask-Migrate / Alembic (migrations)
5. Jinja2 (server-side templating)
6. MySQL 8

Frontend:

1. TypeScript 5
2. SCSS / CSS3
3. HTML5

Deploy:

1. Docker
2. Gunicorn
3. Nginx

Dev tooling:

1. Ruff (Python linter/formatter)
2. mypy (Python static type checker)
3. ESLint + Prettier (TypeScript linter/formatter)
4. lint-staged + shared `.githooks/pre-commit` shell hook (Ruff + mypy for Python, lint-staged for TS — no Husky, no `pre-commit` framework)
5. GitHub Actions (CI: backend lint/audit/test → frontend lint/audit/test/build → Docker dev & prod image builds)

## Libraries used

#### dependencies JS

```
No runtime dependencies in package.json
```

#### devDependencies JS

```
"sass": "^1.89.0"
"@eslint/js": "^9.39.2"
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.3"
"@testing-library/user-event": "^14.5.2"
"@types/jest": "^30.0.0"
"@types/node": "^22.0.0"
"chokidar-cli": "^3.0.0"
"eslint": "^9.39.2"
"eslint-config-prettier": "^10.1.8"
"eslint-plugin-prettier": "^5.5.5"
"globals": "^17.3.0"
"globby": "^15.0.0"
"jest": "^30.3.0"
"jest-environment-jsdom": "^30.3.0"
"lint-staged": "^16.2.7"
"msw": "2.10.4"
"prettier": "^3.8.1"
"ts-jest": "^29.4.6"
"tsc-alias": "^1.8.16"
"typescript": "^5.6.3"
"typescript-eslint": "^8.54.0"
"undici": "^7.25.0"
```

#### Python dependencies (PEP 621)

All Python dependencies are declared in `pyproject.toml` under `[project] dependencies` (runtime) and `[project.optional-dependencies]` (`dev` and `test` extras). The `requirements*.txt` files are thin pip-installable shortcuts that re-export those groups.

#### Runtime (`[project.dependencies]`)

```
flask==3.1.3
flask-sqlalchemy==3.1.1
flask-migrate==4.1.0
flask-login==0.6.3
werkzeug==3.1.8
gunicorn==23.0.0
pymysql==1.1.3
cryptography==50.0.0
python-dotenv==1.2.2
```

#### Dev (`[project.optional-dependencies]` dev)

```
livereload==2.7.0
pip-audit==2.7.3
ruff==0.11.12
mypy==1.13.0
```

#### Test (`[project.optional-dependencies]` test)

```
pytest==9.0.3
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Getting Started

With the stack and libraries above in mind, follow these steps to get a working dev environment.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — must be running before executing any compose command
- [Node.js](https://nodejs.org/) 22+ with npm or yarn — required to install frontend dependencies
- Python 3.11+ — only required if you want to run the pre-commit hook, tests, or migrations outside Docker
- Git

### Setup

1. **Clone the repository:**

   ```sh
   git clone "repository link"
   cd noti
   ```

2. **Create the environment file** from the provided example and fill in the values (see [Env Keys](#env-keys) for what each variable does):

   ```sh
   cp .env.example .env        # macOS / Linux / Git Bash
   copy .env.example .env      # Windows CMD
   ```

3. **Install frontend dependencies** (required for the TypeScript watcher inside Docker):

   ```sh
   cd src/static/ts
   npm install
   # or
   yarn install
   ```

4. **Build the Docker image** from the project root:

   ```sh
   docker compose -f dev.docker-compose.yml build --no-cache
   ```

5. **Start the containers:**

   ```sh
   docker compose -f dev.docker-compose.yml up --force-recreate
   ```

Once running, the services are available at:

| Service | URL |
|---|---|
| Flask app | http://localhost:5050 |
| Adminer (DB UI) | http://localhost:8080 |

### Running without Docker

The app can also run directly on the host — `.env` is honored either way thanks to `python-dotenv` (see [Env Keys](#env-keys) for how loading works).

1. Set up the local virtual environment as described in [Local Development Setup](#local-development-setup) (`pip install -e ".[dev]"` is enough to run the app).

2. Create `.env` from `.env.example` and point `MYSQL_HOST` at a reachable MySQL instance — e.g. `127.0.0.1` with the dev stack's database container running (`docker compose -f dev.docker-compose.yml up noti-db -d`), or any other local MySQL.

3. Start the dev server from the repo root:

   ```sh
   python app.py
   ```

The app listens on `HOST:PORT` from `.env` (http://localhost:5050 with the example values). If MySQL is unreachable, startup logs 5 connection warnings (~25s) and the app boots anyway — see **Startup connection checks** in the backend architecture section.

### Local Development Setup

The repository ships with a self-contained `.githooks/pre-commit` shell hook that runs Ruff (lint + format) and mypy on staged Python files, and `lint-staged` on staged frontend files. It calls each tool directly from the project's virtual environment — no `pre-commit` framework, no caching/isolation layer. Setup is the same local Python virtual environment used for [Migrations](#local-development-setup) and [Testing](#testing).

1. **Create and activate the virtual environment** at the repository root:

   ```sh
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Linux / macOS
   ```

2. **Install all Python dependencies** (PEP 621 extras declared in `pyproject.toml`):

   ```sh
   pip install --upgrade pip
   pip install -e ".[dev,test]"
   ```

   Or install each group separately:

   ```sh
   pip install -e .            # runtime
   pip install -e ".[dev]"     # + livereload, pip-audit, ruff, mypy
   pip install -e ".[test]"    # + pytest, pytest-env, pytest-cov, pytest-timeout, pytest-xdist
   ```

3. **Point git at the shared hooks directory** (one-time, per clone):

   ```sh
   git config core.hooksPath .githooks
   ```

   From now on, every `git commit` triggers `.githooks/pre-commit`. To run the same checks manually against the entire repo:

   ```sh
   ruff check --fix .
   ruff format .
   mypy --config-file=pyproject.toml .
   ```

## Env Keys

The variables loaded from `.env` (created in step 2 of [Setup](#setup)). Defaults provided in `.env.example` work out of the box for local Docker development; production deploys must override `SECRET_KEY` and the MySQL credentials.

**How `.env` is loaded.** There are two load paths, so the file is honored with or without Docker:

- **Docker** — both compose stacks declare `env_file: .env`, so Docker injects the values as real environment variables into the containers.
- **Without Docker** — `load_dotenv()` runs at import time in the two modules that read environment variables: `src/configs/default_config.py` (Flask config, imported by both `app.py` and `wsgi.py`) and `src/configs/gunicorn_config.py` (loaded directly by Gunicorn, outside Flask). No other entry point needs to load it.

**Precedence** — `load_dotenv()` never overrides existing variables, so: real environment variables > `.env` values > coded defaults. CI has no `.env`, so coded defaults (plus the values pytest-env sets) apply there.

| Key | Description |
|---|---|
| `TZ` | Timezone for the app/container (defaults to `America/Argentina/Buenos_Aires`). |
| `HOST` | Network interface where Flask listens (`0.0.0.0` to accept all connections). |
| `PORT` | Port where the Flask app is exposed inside the container. |
| `SECRET_KEY` | Flask secret key used for session signing and CSRF protection. Use a long random string in production. |
| `MAX_CONTENT_LENGTH` | Maximum request body size in bytes accepted by Flask (`1048576` = 1 MiB). |
| `MYSQL_ROOT_PASSWORD` | Root password for the MySQL service. Used internally by Docker for initialization only. |
| `MYSQL_HOST` | Hostname of the MySQL container in the Docker network (service name in Compose). |
| `MYSQL_PORT` | Port where MySQL listens inside the Docker network (`3306`). |
| `MYSQL_USER` | Non-root MySQL user that the Flask app uses to connect. |
| `MYSQL_PASSWORD` | Password for `MYSQL_USER`. |
| `MYSQL_DB_NAME` | Name of the MySQL database created automatically by the container. |

```sh
TZ="America/Argentina/Buenos_Aires"

HOST="0.0.0.0"
PORT=5050
SECRET_KEY="secret_key"
MAX_CONTENT_LENGTH=1048576

MYSQL_ROOT_PASSWORD=root
MYSQL_HOST=noti-db
MYSQL_PORT=3306
MYSQL_USER=noti_user
MYSQL_PASSWORD=noti_pass
MYSQL_DB_NAME=noti_db
```

## Migrations

Schema changes that follow from modifying ORM models are managed through **Flask-Migrate** (Alembic under the hood). Migration scripts live in `migrations/versions/`.

> Requires the local virtual environment from [Local Development Setup](#local-development-setup) and a running MySQL instance (or the dev Docker stack).

**Generate a new migration** after changing or adding a model in `src/models/orm/`:

```sh
flask db migrate -m "feat: add email column to User model"
```

Always review the generated script in `migrations/versions/` before applying — Alembic may miss certain changes (e.g., column type changes, constraints).

**Apply pending migrations:**

```sh
flask db upgrade
```

**Roll back the last migration:**

```sh
flask db downgrade
```

**Roll back to a specific revision:**

```sh
flask db downgrade <revision_id>
```

**Check current migration state:**

```sh
flask db current   # show applied revision
flask db history   # show full migration history
```

> In production, `flask db upgrade` runs automatically at container startup via `entrypoint.production.sh` — no manual step needed.

## Testing

With migrations applied and the app running, verify behavior end-to-end with the test suites for both backend and frontend.

### Backend

> Requires the local virtual environment from [Local Development Setup](#local-development-setup).

**Run all tests:**

```sh
python -m pytest
```

**Run with coverage report:**

```sh
python -m pytest --cov=src --cov-report=term-missing
```

**Run by marker:**

```sh
python -m pytest -m unit         # unit tests only (mocks, no DB)
python -m pytest -m integration  # integration tests only (real DB)
```

**Run integration tests with a real MySQL database:**

```sh
# 1. Start the test database
docker compose -f test.docker-compose.yml up -d

# 2. Run integration tests
python -m pytest -m integration

# 3. Tear down the test database
docker compose -f test.docker-compose.yml down -v
```

### Frontend

> Requires Node.js >=22.0.0.

1. Navigate to the `src/static/ts` directory:

```sh
cd src/static/ts
```

2. Install dependencies (skip if already installed):

```sh
npm install
```

3. Run the tests:

```sh
npm test                  # run all tests
npm run test:watch        # watch mode
npm run test:coverage     # with coverage report
```

## Security Audit

Beyond functional correctness, scan dependencies for known vulnerabilities before shipping.

### Backend

> Requires the local virtual environment from [Local Development Setup](#local-development-setup) (so `pip-audit` is installed).

```sh
pip-audit --skip-editable
```

### Frontend

```sh
cd src/static/ts
npm audit
```

## Build

When tests and audits pass, produce the distributable artifacts.

### Frontend (TypeScript → JavaScript)

The frontend has no JS framework. TypeScript sources in `src/static/ts/` are compiled to plain JavaScript in `src/static/js/` via `tsc` (with `tsc-alias` resolving path aliases and a post-processing step fixing relative imports).

```sh
cd src/static/ts
npm install        # skip if already installed
npm run build
```

The output in `src/static/js/` is what Flask serves in development and what Nginx serves directly in production.

### Docker images

Both stacks ship as Docker images.

**Development image** (Flask + auto-reload + TS watcher):

```sh
docker compose -f dev.docker-compose.yml build --no-cache
```

**Production image** — multi-stage `Dockerfile.production`: a `builder` stage compiles TypeScript and installs Python dependencies; a lean `runner` stage copies only the final artifacts and runs Gunicorn as a non-root user (`appuser`):

```sh
docker compose -f prod.docker-compose.yml build --no-cache
```

## Continuous Integration

The repository ships with a **GitHub Actions** pipeline defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml). It runs automatically on every `push` and `pull_request` targeting the `main` branch, and re-uses the same commands you can run locally — the ones documented in the [Testing](#testing), [Security Audit](#security-audit), and [Build](#build) sections.

It is a **validation-only pipeline**: nothing is published, tagged, or released. A failure in any earlier job short-circuits the rest, so the cheap checks (lint/type-check) run before the expensive ones (Docker builds).

### Pipeline overview

```
                ┌─── PR or push to main ───┐
                ▼                          ▼
┌────────────────────────────────┐
│   backend-lint-and-audit       │  ruff (check + format) · mypy · pip-audit
└────────────────────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   backend-test                 │  pytest --tb=short
└────────────────────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   frontend-lint-and-audit      │  eslint · tsc --noEmit · npm audit (high+)
└────────────────────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   frontend-test                │  jest (ts-jest + jsdom)
└────────────────────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   frontend-build               │  tsc + tsc-alias
└────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────┐
│   docker-build  (matrix — runs in parallel)          │
│   ├── Dockerfile.development → app:dev               │
│   └── Dockerfile.production  → app:prod              │
└──────────────────────────────────────────────────────┘
```

### Jobs

1. **`backend-lint-and-audit`** — installs the `[dev]` extra from `pyproject.toml` on Python 3.11 and runs `ruff check .`, `ruff format --check .`, `mypy --config-file=pyproject.toml .`, and `pip-audit --skip-editable`.
2. **`backend-test`** — installs the `[test]` extra and runs `python -m pytest --tb=short`.
3. **`frontend-lint-and-audit`** — installs `src/static/ts` deps with `npm ci --ignore-scripts` (the `--ignore-scripts` flag skips the local Git-hook `prepare` step, which expects a writable `.git` parent not always present in CI) and runs `npm run lint`, `npm run type-check`, and `npm audit --audit-level=high`. The audit step is marked `continue-on-error: true` so transitive advisories don't break the build — they still appear in the logs for review.
4. **`frontend-test`** — runs `npm run test` (Jest + `ts-jest` + `jest-environment-jsdom`).
5. **`frontend-build`** — runs `npm run build`, exercising the same `tsc` + `tsc-alias` pipeline documented in [Build → Frontend (TypeScript → JavaScript)](#frontend-typescript--javascript).
6. **`docker-build`** — uses `docker/setup-buildx-action` plus a matrix to build `Dockerfile.development` and `Dockerfile.production` in parallel **without pushing them anywhere**. It's purely a smoke test that both images still build end-to-end.

### Where the CI outputs live

| Output | Location |
|---|---|
| Validation logs (lint, audit, tests, build) | **Actions** tab on GitHub |
| Docker images (`app:dev`, `app:prod`) | Ephemeral, kept only inside the runner |

> **Note:** the pipeline does not push images to any registry, create Git tags, or publish GitHub Releases. Promoting the production image to a registry is left to the deployment environment.

### Running the same checks locally

```sh
# 1. backend-lint-and-audit
ruff check .
ruff format --check .
mypy --config-file=pyproject.toml .
pip-audit --skip-editable

# 2. backend-test
python -m pytest --tb=short

# 3. frontend-lint-and-audit
cd src/static/ts
npm ci --ignore-scripts
npm run lint
npm run type-check
npm audit --audit-level=high

# 4. frontend-test
npm run test

# 5. frontend-build
npm run build

# 6. docker-build (from the repo root)
docker compose -f dev.docker-compose.yml build --no-cache
docker compose -f prod.docker-compose.yml build --no-cache
```

## Production

With [Tested](#testing), [Audited](#security-audit), and [Built](#build) artifacts ready, deploy the production stack: **Gunicorn** (WSGI server) behind **Nginx** (reverse proxy), with **MySQL 8.0** as the database — all orchestrated by Docker Compose.

### Architecture

```
Browser → Nginx (:8080) → Gunicorn (:5050) → Flask app
                ↓
        /static/ served directly by Nginx (no Python involved)
```

- **Nginx** handles TLS termination, static file serving with long-lived cache headers, gzip compression, and proxies all dynamic requests to Gunicorn.
- **Gunicorn** runs `cpu_count * 2 + 1` workers with 2 threads each. Config lives in `src/configs/gunicorn_config.py`.
- **MySQL** data is persisted in a named Docker volume (`db-data`). The container is never exposed to the host.

### Startup sequence

On every container start, `entrypoint.production.sh` runs automatically:

1. Waits until `flask db upgrade` succeeds (retries every 2s until the DB is ready).
2. Copies compiled static files to a shared Docker volume (consumed by Nginx).
3. Launches Gunicorn.

Additionally, every worker that builds the app through `create_app` runs the **startup connection checks** described in the backend architecture section: MySQL is pinged up to 5 times (2s between attempts, 3s connect timeout) and, if still unreachable, the app logs a warning and continues serving instead of crashing.

### Deploy

> Make sure the production image has been built — see [Build → Docker images](#docker-images).

1. **Configure production environment** — copy `.env.example` to `.env` and override the values for production (strong random `SECRET_KEY`, real DB credentials, the public host you'll bind to). Refer to [Env Keys](#env-keys) for the full list:

   ```sh
   cp .env.example .env
   ```

2. **Start all services:**

   ```sh
   docker compose -f prod.docker-compose.yml up -d
   ```

   Once running, the app is available at:

   | Service | URL |
   |---|---|
   | App (via Nginx) | http://localhost:8080 |

3. **Stop and tear down:**

   ```sh
   docker compose -f prod.docker-compose.yml down
   ```

   To also remove the database volume (destructive — deletes all data):

   ```sh
   docker compose -f prod.docker-compose.yml down -v
   ```

### Logs

```sh
docker compose -f prod.docker-compose.yml logs -f         # all services
docker compose -f prod.docker-compose.yml logs -f noti    # Flask/Gunicorn only
docker compose -f prod.docker-compose.yml logs -f nginx   # Nginx only
```

## Known Issues

None at the moment.

## Version

```
APP VERSION: 0.0.1
README UPDATED: 12/08/2026
AUTHOR: Diego Libonati
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/noti`](https://www.diegolibonati.com.ar/#/project/noti)
