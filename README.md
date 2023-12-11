# FEEDBACK FORM

<div>
  <p align="center">
    <img src="feedback_form/static/images/feedbackform.png" width="800"> 
  </p>
</div>

The Feedback Form project is an online platform that enables clients to provide valuable suggestions and reviews, fostering an interactive and user-driven improvement process. Built with Flask, MySQL, Celery, and Redis, all components are containerized in Docker, ensuring seamless communication between them.

![OS](https://img.shields.io/badge/OS-Linux-red?style=flat&logo=linux)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203.8-1f425f.svg?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-available-green.svg?style=flat&logo=docker)](https://github.com/emalderson/ThePhish/tree/master/docker)
[![Maintenance](https://img.shields.io/badge/Maintained-yes-green.svg)](https://github.com/KafuiAdaku/FeedbackForm)
[![Documentation](https://img.shields.io/badge/Documentation-complete-green.svg?style=flat)](https://github.com/KafuiAdaku/FeedbackForm)

## Table of Contents

- [Project Overview](#project-overview)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Setting Up Feedback Form](#setting-up-feedback-form)
  - [Environment Configuration](#environment-configuration)
- [Build and Run](#build-and-run)
- [Testing](#testing)
  - [Running pytest](#running-pytest)
  - [Test Coverage](#test-coverage)
- [Initializing Database](#initializing-database)
- [Test in Browser](#test-in-browser)
- [Contact](#contact)
- [License](#license)

## Project Overview

The Feedback Form project serves as an online suggestion and review platform, allowing users to share their feedback and improve the overall user experience.

## Project Setup

### Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed `Docker` and `Docker Compose`.
* You have a suitable text editor to edit .env and other files.

## Setting Up Feedback Form

To install Feedback Form, follow these steps:

1. Clone the repository.
2. Set up your environment variables in the .env file:

### Environment Configuration

Create a `.env` file in the project root and set the following values:

```env
# Email Configuration
MAIL_USERNAME='yourgmail@email.com'
MAIL_PASSWORD='google app password'
MAIL_DEFAULT_SENDER='yourgmail@email.com'
ADMIN_EMAIL='random@email.com'

# Database Configuration
DATABASE_URL='mysql+pymysql://feedback:yourpassword@mysql:3306/feedback_form'
MYSQL_ROOT_PASSWORD='yourpassword'
MYSQL_DATABASE='feedback_form'
MYSQL_USER='feedback'
MYSQL_PASSWORD='yourpassword'
```
> These values will be used by the config/settings.py file


## To build a container from a docker compose file
```bash
docker-compose up --build
```

## Run a docker-compose after already building
```bash
docker-compose up
```

## To stop a running docker-compose app 
```bash
docker-compose stop
```

# TESTING THE APP AND COVERAGE

## Running pytest directly inside the docker container
```bash
docker-compose exec website pytest feedback_form/tests
```

## Testing the test coverage of our entire code to see if we missed some tests out
```bash
docker-compose exec website pytest --cov-report term-missing --cov feedback_form
```

# INITIALIZING DATABASE
> Before testing code, database has to be initialized with the commands below in a different terminal
```docker
docker-compose exec website env FLASK_APP=feedback_form/app.py flask db init
docker-compose exec website env FLASK_APP=feedback_form/app.py flask db migrate
docker-compose exec website env FLASK_APP=feedback_form/app.py flask db upgrade
```

# TEST IN BROWSER

Visit [localhost:8000](http://localhost:8000) or [0.0.0.0:8000](http://0.0.0.0:8000) in your web browser to test the application.


## Contact

## Authors

- [Theophilus Ackom](https://github.com/TeamKweku)
- [Dennis Adaku](https://github.com/KafuiAdaku)


## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

