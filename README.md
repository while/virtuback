virtuback
=========

A simple backend serving an API for a user resource 


## Installation
This is a simple project not really intended for production. Here is how you
set it up for development.

Get the code from github

    $ git clone git@github.com:while/virtuback.git

Set up a virtual python environment

    $ cd virtuback
    $ virtualenv env
    $ source env/bin/activate

Install required packages

    $ pip install -r requirements.txt

Now we are done! This app uses MongoDB for persistance. All you need to set up
for this is the connection string in `config.py`. This is set to use a local
mongodb install per default. 

Once configured we can test 

    $ nosetests --with-coverage --cover-package=virtuback

and run the app

    $ python run.py

Don't hesitate to send me an email if you have any questions. 


