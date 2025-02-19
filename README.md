# Task Manager
This is a project that helps you to manage differents tasks in your life.

## Environment Variables

This project uses environment variables stored in a `.env` file. To help set up your environment, a `.env.template` file is provided.

### Setting up the environment file

1. Copy `.env.template` and rename it to `.env`
2. Set your own Json Web Token secret string.

## Setup Project

1. Navigate to the project folder and open a terminal
2. Build Image

 * `docker-compose build`

3. Run Container

 * `docker-compose up -d`

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

## Run tests
With the app running

1. Navigate to the project folder and open a terminal
2. Open interactive Terminal in the Task app container with the command

 * `docker exec -it task-manager-container /bin/sh`

2. Run test command

 * `pytest`