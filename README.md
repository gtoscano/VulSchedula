# VulSchedula – Vulnerable Scheduling App

**VulSchedula** is a Django-based web application developed as a playful yet educational tool for students enrolled in _Introduction to Secure Computing_. Inspired by doodle-like applications, VulSchedula allows users to create scheduling polls and share them via email for voting.

However, beware! VulSchedula intentionally contains hidden vulnerabilities and security pitfalls, designed specifically for educational purposes.

## Educational Objectives

- **Identify Security Vulnerabilities:** Students must analyze and audit the provided codebase, identifying vulnerabilities that expose sensitive data.
- **Understanding Risks of Downloaded Software:** Highlighting the importance of code auditing and discouraging blind trust in downloaded or publicly available software.
- **Simulate Malicious Web Hosting:** Students also take on the role of a mischievous hosting provider aiming to exploit vulnerabilities to steal sensitive information, specifically passwords provided by the instructor.

## Features

- **Poll Creation:** Users can select multiple date/time options.
- **Poll Sharing:** Share polls directly via generated URLs sent through email.
- **Poll Voting:** External users can vote on their preferred date/time.
- **Hidden Vulnerabilities:** Built-in vulnerabilities and mischievous code snippets intentionally designed to leak poll data or user passwords.

## Setup

### Requirements

- Docker
- Docker Compose

### Installation

Update the file variables.env

```bash

RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
AMQP_HOST=rabbitmq
AMQP_USERNAME=guest
AMQP_PASSWORD=guest
AMQP_PORT=5672
AMQP_VHOST=/

REDIS_HOST=redis
REDIS_USERNAME=guest
REDIS_PORT=6379
REDIS_DB=1
REDIS_DB_OPT=1
REDIS_DB_CELERY=1
REDIS_DB_RESULT=1
REDIS_DB_CACHE=3
CELERY_BROKER=redis://redis:6379/1
CELERY_BACKEND=redis://redis:6379/2

DB_HOST=postgres
DB_ENGINE=django.db.backends.postgresql
DB_PORT=5432
POSTGRES_DB=vul_schedula
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword

DJANGO_SUPERUSER_FIRST_NAME=admin
DJANGO_SUPERUSER_LAST_NAME=root
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=youremail@cua.edu
DJANGO_SUPERUSER_PASSWORD=yourpassword
HOST_IP=192.168.1.X
HOST_NAME=home-vulschedula.catholic-u.ai
SECURE_SSL_REDIRECT=True
RUN_INIT_SCRIPT=True
CREATE_SUPERUSER=True
HOST_DIR=/PATH_TO/VulShedula/
PARENT_DIR=/app
DOCKER_GID=994

```

Clone the repository:

```bash
git clone git@github.com:gtoscano/VulSchedula.git
cd VulSchedula
sudo bash mod_permissions.sh
```

Run the application:

```bash
docker compose up -d
```

Check the application: Go to your browser at address: 127.0.0.1 and check the app.

## Tasks for Students

## Make sure that

- Only registered users can crate a new poll
- Only the users who created a poll can close it
- If a poll is private, then only invited users should be able to vote
- If a poll is private, then only invited users should be able to download the calendar.
- I don't deceive you

### Task 1: Security Analyst

- Audit the code to find and document vulnerabilities that could expose user poll data.
- Identify and explain potential risks associated with using unverified third-party code.

### Task 2: Mischievous Hosting Provider

- Attempt to exploit vulnerabilities to steal three pre-created usernames/passwords provided by the instructor.
- Document how the exploits were carried out successfully.

## Important Note

**Always thoroughly review code downloaded from external sources!**

Feel free to dive into the Docker containers and source files. Watch out for those sneaky traps and "cheap tricks" deliberately hidden in the code. Remember, it's all in good fun—and education!

Happy hacking!
