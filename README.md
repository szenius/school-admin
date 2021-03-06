# school-admin
Administration system for student registration and notification.

## Prerequisites
This project was developed with `Python 3.7.2` and `MySQL 8.0`. Please make sure equivalent Python and MySQL versions are installed on your machine.

## Local Development
### Installation
After cloning this repository to your local directory, run the following to install the necessary Python packages.
```
pip install -r requirements.txt
```

### Initialise databases
Before doing any local development, please first run the following to initialise production and test databases. These databases are assumed to be accessible to only the `root` account. You will also be prompted to key in your `root` account password.
```
mysql -u root -p < sql/build_db.sql
mysql -u root -p < sql/build_test_db.sql
```

Each database consists of three tables `teacher`, `student` and `registration`. Take a look at the diagram below to see the entity relationship model.

![DB Entity RS Model](https://github.com/szenius/school-admin/blob/master/db_entity_rs_model.png)

The tables `teacher` and `student` in the production database are also initialised with 9 emails each. Please refer to the [build script](https://github.com/szenius/school-admin/blob/master/sql/build_db.sql) to see the values added into the tables.

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
* Improving on documentation
