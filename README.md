# Noti-Flask

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Join to `./src/static/ts` folder and execute: `npm install` or `yarn install` in the terminal
3. Go to the root folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development (Python)

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

This is a Web Application made with Flask. This application allows you to create your own notes for each user, it has a home and registration of the same. You will be able to create, edit and delete unique notes for each user created.

## Technologies used

1. Python -> Flask
2. Typescript
3. CSS3
4. HTML5
5. SCSS
6. Jinja2

Deploy:

1. Docker
2. Gunicorn
3. Nginx

Database:

1. SQL -> SQlAlchemy

## Libraries used

#### Dependencies JS

```
No dependecies in package.json
```

#### devDependencies JS

```
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.3"
"@testing-library/user-event": "^14.5.2"
"@types/jest": "^29.5.14"
"chokidar-cli": "^3.0.0"
"globby": "^15.0.0"
"jest": "^29.7.0"
"jest-environment-jsdom": "^29.7.0"
"ts-jest": "^29.2.5"
"ts-node": "^10.9.2"
"tsc-alias": "^1.8.16"
"typescript": "^5.6.3"
```

#### Flask Requirements.txt

```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
Flask-Login==0.6.3
Werkzeug==3.1.3
libsass==0.23.0
Flask-Scss==0.5
gunicorn==23.0.0
pre-commit==4.3.0

# If you use docker
PyMySQL==1.1.2
cryptography==46.0.2
```

#### Flask Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Noti-Flask`](https://www.diegolibonati.com.ar/#/project/Noti-Flask)

# Video 

https://github.com/user-attachments/assets/069dc4e6-fb4c-4ae2-a2aa-629125ed4921

## Testing Backend

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

## Testing TS Files

1. Join to the correct path of the clone
2. Enter to `src/static/ts` directory
3. Execute `yarn install` or `npm install` to install depedencies
4. Execute `yarn test` or `npm test`

NOTE: If you have already installed the node modules, just execute point 2 and 4.

## Migrations

- Every time you change or add models in `src/models/orm/`, run:

```sh
flask db migrate -m "feat: new column in User model"
```

### **Version**

```ts
APP VERSION: 0.0.1
README UPDATED: 05/10/2025
AUTHOR: Diego Libonati
```

### **Env Keys**

1. `HOST`: Refers to the network interface where the Flask backend listens.
2. `PORT`: Refers to the port number where the Flask backend will be exposed.
3. `SECRET_KEY`: Refers to the Flask secret key used for session management, CSRF protection, and cryptographic signing.
4. `MYSQL_ROOT_PASSWORD`: Refers to the root user password for the MySQL service used internally by Docker for initialization.
5. `MYSQL_DATABASE`: Refers to the default database name that will be automatically created in the MySQL container.
6. `MYSQL_USER`: Refers to the MySQL non-root username that the Flask app uses to connect to the database.
7. `MYSQL_PASSWORD`: Refers to the password of the MySQL non-root user defined in MYSQL_USER.
8. `MYSQL_PORT`: Refers to the port where the MySQL service listens inside the Docker network.
9. `MYSQL_SERVICE`: Refers to the internal hostname of the MySQL container in the Docker network, allowing Flask to connect using service discovery.
10. `SQL_DB_NAME`: Refers to the local database name when running the app without Docker, typically for SQLite or development environments.

```ts
# With Docker

HOST="0.0.0.0"
PORT=5000
SECRET_KEY="secret_key"

MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=notidb
MYSQL_USER=notiuser
MYSQL_PASSWORD=notipass
MYSQL_PORT=3306
MYSQL_SERVICE=noti-db

# Without Docker

HOST="0.0.0.0"
PORT=5000
SECRET_KEY="secret_key"

SQL_DB_NAME="noti"
```

### **Endpoints API**

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