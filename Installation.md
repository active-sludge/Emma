# Emma v0.9.0 Pre-release setup

The application is in pre-release state. 
It only works locally, in development setup.
Deployment or dockerization is not ready.
After installation please refer to the user manual.

Pre-requisites:
- Python > 3.2.9
- pip > 21.3.0
- virtualenv > 20.8.0

Follow below steps to run the app.

1. Download the latest release from the repo.

[Emma-0.9.0](https://github.com/active-sludge/Emma/releases/tag/v0.9.0)

2. Extract the .zip file to the desired location and go into the project directory

`cd /EmmaProject`

3. Create a virtual environment 

`virtualenv venv`

4. Activate virtual environment

`source venv/bin/activate`

5. Install external libraries. Wait for it to complete.

`pip install -r requirements.txt`

6. Make database migrations and migrate

`python manage.py makemigrations`

`python manage.py migrate`

7. Start the application

`python manage.py runserver`

You should see something like below.

```
(venv) ➜  EmmaProject git:(main) ✗ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 15, 2022 - 12:59:14
Django version 3.2.9, using settings 'EmmaProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

8. Access the app from the local host.

http://localhost:8000/


