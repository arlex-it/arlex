Unit tests are used to verify the integrity of the project.

These tests are launched after a developer made a push on Travis platform.

Unit tests have to follow the following methods:

Structure:
```
unit_test
├── init_unit_test.py
├── [route_name]
│   ├── [route_name]_model.py
│   ├── sql
│   │   └── sql_[request_method].py
│   ├── test_[route_name]_utilities.py
│   └── tests
│       ├── [request_method].py
│       ├── [request_method].py
│       └── [request_method].py
| ( example: )
└── user
    ├── sql
    │   └── sql_post.py
    ├── test_user_utilities.py
    ├── tests
    │   ├── tests_delete.py
    │   └── tests_post.py
    └── user_model.py
```

Files: 
* init_unit_test.py is used to init unit tests there should be no need to change it.

* \[route_name]\_model.py is used to save a model in the database.

* sql_\[request_method].py is used to modify the database during the unit tests.

* test_\[route_name]_utilities.py is used for utilities functions.

* \[request_method].py is used to do the tests.

How to launch unit_test:

* First you have to launch the API, for this: ```python main.py unit_test```
* If it's the first time, you need a local database.  
To install one:
```
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation utility
sudo systemctl start mysql
sudo mysql -u root < bdd/script_sql/create_database.sql
```
The last command will create the tables used by the API.

* Launch your unit test with: ```python unit_test/[route_name]/tests/tests_[request_method].py```

To deploy your unit tests:
* Add the command to execute your script in .travis.yml ```python unit_test/[route_name]/tests/tests_[request_method].py```
* And don't forget to push your work !

To have a better understanding of what to put in each file, please refer to the directory ```unit_test_template```. 