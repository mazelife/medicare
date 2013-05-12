=============================================
Welcome to the medicare project
=============================================

This project uses Django 1.5.1.

Locations of important files:

* ``project_name/`` Django project and apps
* ``docs/`` - project documentation (Sphinx)
* ``requirements/`` - project dependencies
* ``static/`` - static media
* ``templates/`` - project HTML templates

Getting Started
-----------------

The following will help you get a development environment up and running::

    ?> virtualenv --distribute medicare_env
    ?> cd medicare_env
    ?> source ../bin/activate
    ?> git clone git@github.com:Threespot/medicare.git
    ?> cd medicare
    ?> pip install -r requirements/base.txt
    ?> pip install -r requirements/development.txt
    ?> ./manage.py syncdb --settings=medicare.settings.dev
    ?> ./manage.py runserver --settings=medicare.settings.dev


You can avoid having to pass the ``--settings=medicare.settings.dev`` argument to management commands by setting the ``DJANGO_SETTINGS_MODULE`` environmental variable. Just add the following line to your virtualenv's ``bin/activate`` script::

    export DJANGO_SETTINGS_MODULE="medicare.settings.dev"


Data Sources
-------------

* `One hospital charges $8,000 -- another, $38,000 <http://www.washingtonpost.com/blogs/wonkblog/wp/2013/05/08/one-hospital-charges-8000-another-38000/>`_
* `Medicare Provider Charge Data <http://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/index.html>`_