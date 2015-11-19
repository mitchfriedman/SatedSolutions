SatedSolutions code for the backend and API

Note:
This project is built with python 3.  Make sure python3 is installed and accessible via "python3" on command line.


Installation:
    - clone repo
    - make install
 
Run instructions:
    - python run.py


.gitignore <-- add files you IDE might generate, etc
Makefile <-- targets for installation, cleaning, etc
run.py <-- script to run the app
requirements.txt <-- holds dependencies that will install with make target (Flask, flask-restful, etc)
app/ <-- holds the actual application
    resouces/v1 <-- api endpoints
    models/ <-- sqlalchemy models
    application.py <-- create app builder method
    errors.py <-- add errors to be returned to frontend


Flask restful:
http://flask-restful-cn.readthedocs.org/en/0.3.4/

Flask:
http://flask.pocoo.org/

