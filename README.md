# Task Manager
This is a project that helps you to manage differents tasks in your life.

## Setup

1. Navigate to the project folder
2. Build Image

`docker-compose build`

3. Run Container

`docker-compose up -d`

## Instructions
The tasks endpoints need authentication, for get a valid access token you need to create an user

```
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
```
Then, you have to Log in into the system

```
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
```

## Api Documentation

`curl http://localhost:8000/docs`