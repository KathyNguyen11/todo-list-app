A flask-driven restful API for TodoList interactions


## Technologies used
* **[Python3](https://www.python.org/downloads/)** 
* **[Flask](flask.pocoo.org/)** 
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** 
* **[PostgreSQL](https://www.postgresql.org/download/)** 
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Then Git clone this repo to your local machine


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd todoList
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 venv
        $ pip install autoenv
        ```

* #### Environment Variables
    Create a .env file and add the following:
    ```
    source venv/bin/activate
    export SECRET="secrect key"
    export APP_SETTINGS="development"
    export DATABASE_URL="postgresql://localhost/test_db"
    ```

    Save the file. CD out of the directory and back in. Please input the correct info of your local machine before saving this file

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

* #### Migrations
    On your psql console, create your database:
    ```
    > CREATE DATABASE test_db;
    ```
    Then, make and apply your Migrations
    ```
    (venv)$ python manage.py db init

    (venv)$ python manage.py db migrate
    ```

    And finally, migrate your migrations to persist on the DB
    ```
    (venv)$ python manage.py db upgrade
    ```

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ flask run
    ```
    You can test creating todolists using Postman
    ```
    http://localhost:5000/todolists/
    ```
