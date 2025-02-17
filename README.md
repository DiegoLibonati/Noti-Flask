# Noti-Flask

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Execute: `python -m venv venv`
4. Execute in Windows: `venv\Scripts\activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Use `python -m src.app`

## Description

This is a Web Application made with Flask. This application allows you to create your own notes for each user, it has a home and registration of the same. You will be able to create, edit and delete unique notes for each user created.

## Technologies used

1. Python
2. CSS3
3. SCSS
4. Javascript

## Libraries used

#### Dependencies JS

```
No dependecies in package.json
```

#### devDependencies JS

```
"@babel/preset-env": "^7.26.9"
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.3"
"@testing-library/user-event": "^14.5.2"
"babel-jest": "^29.7.0"
"jest": "^29.7.0"
"jest-environment-jsdom": "^29.7.0"
```

#### Flask Requirements.txt

```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
Flask-Login==0.6.3
Werkzeug==3.1.3
python-dotenv==1.0.1
libsass==0.23.0
Flask-Scss==0.5
gunicorn==23.0.0
```

#### Flask Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Noti-Flask`](https://www.diegolibonati.com.ar/#/project/Noti-Flask)

# Video 

https://github.com/user-attachments/assets/069dc4e6-fb4c-4ae2-a2aa-629125ed4921

## Testing Backend

1. Join to the correct path of the clone
2. Execute in Windows: `venv\Scripts\activate`
3. Execute: `pytest --log-cli-level=INFO`

## Testing JS Files

1. Join to the correct path of the clone
2. Enter to `src/static/js` directory
3. Execute `yarn install` or `npm install` to install depedencies
4. Execute `yarn test` or `npm test`

NOTE: If you have already installed the node modules, just execute point 2 and 4.