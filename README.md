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

#### Requirements.txt

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

#### Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Noti-Flask`](https://www.diegolibonati.com.ar/#/project/Noti-Flask)

# Video 

Coming soon...

## Testing

1. Join to the correct path of the clone
2. Execute in Windows: `venv\Scripts\activate`
3. Execute: `pytest --log-cli-level=INFO`