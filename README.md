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

All note mutations go through a REST JSON API (`/api/v1/notes/`) that the TypeScript frontend calls asynchronously, keeping the user experience smooth while the server stays the source of truth.

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

A custom `BaseAPIError` exception class lets any layer raise a typed error that the Flask error handler automatically converts into a consistent JSON response with the correct HTTP status code.

**Infrastructure & deployment:**

The application is fully containerized with Docker. The development stack (`dev.docker-compose.yml`) runs Flask with a Livereload/Tornado dev server and a MySQL 8 container, with SCSS and TypeScript watch modes active. The production stack (`prod.docker-compose.yml`) swaps in Gunicorn as the WSGI server behind an Nginx reverse proxy, with a separate MySQL container. Database credentials, ports, and Flask secrets are all configured via environment variables (see the **Env Keys** section). Pre-commit hooks (via `pre-commit` + `.githooks/pre-commit`) enforce code quality on every commit.

### Endpoints API

The REST API exposed by the Flask backend. All mutations on notes go through these endpoints; the TypeScript frontend consumes them asynchronously.

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

1. Ruff (Python linter)
2. ESLint + Prettier (TypeScript linter/formatter)
3. Husky + lint-staged (Git hooks for JS)
4. pre-commit (Git hooks for Python)

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
"husky": "^9.1.7"
"jest": "^30.3.0"
"jest-environment-jsdom": "^30.3.0"
"lint-staged": "^16.2.7"
"prettier": "^3.8.1"
"ts-jest": "^29.4.6"
"tsc-alias": "^1.8.16"
"typescript": "^5.6.3"
"typescript-eslint": "^8.54.0"
```

#### Flask requirements.txt

```
flask==3.1.3
flask-sqlalchemy==3.1.1
flask-migrate==4.1.0
flask-login==0.6.3
werkzeug==3.1.8
gunicorn==23.0.0
pymysql==1.1.3
cryptography==48.0.0
```

#### Flask requirements.dev.txt

```
-r requirements.txt
livereload==2.7.0
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Flask requirements.test.txt

```
pytest==8.4.2
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
- Python 3.11+ — only required if you want to run pre-commit, tests, or migrations outside Docker
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

### Pre-Commit for Development

Pre-commit hooks (Ruff lint + format, pip-audit) run automatically on every `git commit`. Setup requires a local Python virtual environment because `pre-commit` is a Python package and is also the same env you'll use for [Migrations](#migrations) and [Testing](#testing).

1. **Create and activate the virtual environment** at the repository root:

   ```sh
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Linux / macOS
   ```

2. **Install all Python dependencies:**

   ```sh
   pip install -r requirements.txt
   pip install -r requirements.dev.txt
   pip install -r requirements.test.txt
   ```

3. **Install the pre-commit hooks** declared in `.pre-commit-config.yaml`:

   ```sh
   pre-commit install
   ```

   From now on, every `git commit` will trigger the hooks. To run them manually against the entire repo:

   ```sh
   pre-commit run --all-files
   ```

## Env Keys

The variables loaded from `.env` (created in step 2 of [Setup](#setup)). Defaults provided in `.env.example` work out of the box for local Docker development; production deploys must override `SECRET_KEY` and the MySQL credentials.

| Key | Description |
|---|---|
| `HOST` | Network interface where Flask listens (`0.0.0.0` to accept all connections). |
| `PORT` | Port where the Flask app is exposed inside the container. |
| `SECRET_KEY` | Flask secret key used for session signing and CSRF protection. Use a long random string in production. |
| `MYSQL_ROOT_PASSWORD` | Root password for the MySQL service. Used internally by Docker for initialization only. |
| `MYSQL_HOST` | Hostname of the MySQL container in the Docker network (service name in Compose). |
| `MYSQL_PORT` | Port where MySQL listens inside the Docker network (`3306`). |
| `MYSQL_USER` | Non-root MySQL user that the Flask app uses to connect. |
| `MYSQL_PASSWORD` | Password for `MYSQL_USER`. |
| `MYSQL_DB_NAME` | Name of the MySQL database created automatically by the container. |

```sh
HOST="0.0.0.0"
PORT=5050
SECRET_KEY="secret_key"

MYSQL_ROOT_PASSWORD=root
MYSQL_HOST=noti-db
MYSQL_PORT=3306
MYSQL_USER=noti_user
MYSQL_PASSWORD=noti_pass
MYSQL_DB_NAME=noti_db
```

## Migrations

Schema changes that follow from modifying ORM models are managed through **Flask-Migrate** (Alembic under the hood). Migration scripts live in `migrations/versions/`.

> Requires the local virtual environment from [Pre-Commit for Development](#pre-commit-for-development) and a running MySQL instance (or the dev Docker stack).

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

> Requires the local virtual environment from [Pre-Commit for Development](#pre-commit-for-development).

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

> Requires the local virtual environment from [Pre-Commit for Development](#pre-commit-for-development) (so `pip-audit` is installed).

```sh
pip-audit -r requirements.txt
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
README UPDATED: 10/05/2026
AUTHOR: Diego Libonati
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/noti`](https://www.diegolibonati.com.ar/#/project/noti)
