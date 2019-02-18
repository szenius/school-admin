# school-admin
Administration system for student registration and notification.

## Prerequisites
This project was developed with `Python 3.7.2` and `MySQL 8.0`. Please make sure equivalent Python and MySQL versions are installed on your machine.

## Local Development
### Initialise databases
Before doing any local development, please first run the following to initialise production and test databases. These databases are assumed to be accessible to only the `root` account. You will also be prompted to key in your `root` account password.
```
mysql -u root -p < sql/build_db.sql
mysql -u root -p < sql/build_test_db.sql
```

### Starting the Flask application
To start the Flask application, please run the following from the root directory.
```
python run.py
```

Here's a [Postman collection](https://www.getpostman.com/collections/374ea00428490c14bff7) for you to get started on some example requests.

### Running unit tests
To run unit tests, please run the following from the root directory.
```
python -m unittest discover
```

## Future Work
* Deploying the API to a server for remote access
* Further refactoring of service classes into different files
* Improving on documentation