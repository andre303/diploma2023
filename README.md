UbeTrip
-------

https://ubetrip.herokuapp.com/

Admin panel:

https://ubetrip.herokuapp.com/admin/

User: admin / admin

Translation panel:

https://ubetrip.herokuapp.com/rosetta/files/project/

Development
-----------

Setup virtual environment:

    python -m venv venv

Activate it:

    source ./venv/bin/activate

Install packages:

    pip install -r requirements.txt

Django uses local assets, so first, you’ll need to run collectstatic:

    python manage.py collectstatic

Run locally:

    heroku local web


Changed models?
---------------

    python manage.py makemigrations
    python manage.py migrate

Need admin user?
----------------

    python manage.py createsuperuser


Translations
------------

When added new lines of text:

    django-admin makemessages -l en
    django-admin makemessages -l uk-ua
    django-admin makemessages -l ru


Deploy
------

    git status
    git commit -a -m "What was changed?"
    git push origin main

Wait for CI to build and deploy code from GitHub.

If models was changed:

    heroku run python manage.py migrate -a ubetrip

Create a superuser (default is admin/admin)

    heroku run python manage.py createsuperuser -a ubetrip

Heroku help
-----------

https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true
