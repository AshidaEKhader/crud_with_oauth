# crud_with_oauth
Django sample application with github oauth and CRUD

### Setting up in local machine
- Clone from the repository.
- Install Postgres if Not installed already 
- Change the settings in the settings.py 
- Create database and user based on the settings
- Grant all permissions for that user on that database
- Run the application 

##### Setting up virtual environemnt 
- Make sure to install python3.5
- Run the command : virtualenv .venv --python=python3.5
- Command to activate virtual environment: source/<virtual environment name>/bin/activate
##### Installing dependencies
- Activate virtual environment
- Run pip install -r requirements.txt

##### Creating local database
-Log in to the psql terminal
- Create database using the command, CREATE DATABASE database_name;
- Create database user using the command ,CREATE USER database_user  WITH PASSWORD 'password';
- GRANT ALL PRIVILEGES ON DATABASE database_name TO database_user;
- GRANT CREATE ON DATABASE database_name TO database_user ;
- Change the settings file accordingly with the cedentials of your DB.
##### Setting up initial migrations 
- Before running the application, make sure we set up the migrations.
-Activate virtual environment
- Run python manage.py migrate

##### Running the application
- Activate virtual environment
- Run the command: python manage.py runserver 0.0.0.0:8000#: Make sure you run by specifying this command itself. The application should be accesible at 'http://localhost:8000/login?user=<Github user>', even if you run on your ip , you may not get the access token since the call back URL for the Github application is configuted with http://localhost:8000/callback
#####  For running unit tests for the application
- Activate virtual environment
- Run the command: python manage.py test #: TestCase - <no> will give the number of tests run.
