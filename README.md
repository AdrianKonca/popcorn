# Popcorn recipes app

### Goal

Main goal of this app, is to provide a website where any user can create recipe, watch recipes of others, vote and
comment.

### Reason

This app was created as a part of University group project. Our task was to create an app as a Team - we chose to do so
in Django.

### Authors

- TODO

### Setup

- Install dependencies using [Pipfile](https://pipenv-fork.readthedocs.io/en/latest/basics.html "Pipfile basics") lock.
- Copy `app_secrets.py` (stored on our Microsoft Teams "Files" tab) into `./main` folder
- Run command `python manage.py migrate`
- Run command `python manage.py runserver`
- Connect to the website
- If everything works, you are good to go to create your own branch.

### Migrating initial data

- `python manage.py loaddata popcorn/fixtures/InitialData.json`

### Dumping data

- `python manage.py dumpdata popcorn > popcorn/fixtures/InitialData.json`

### Translating third-party libraries

- Create symlink to the desired third-party library in links folder.
- In case of powershell in can be done like this (it needs to be launched in elevated mode)
- `New-Item -ItemType Junction -Path "links/LibraryName" -Target "TargetToEnvFolder"`
- Remember that you must create link all of the currently used applications, as the translations will get lost when
  regenerating the file!
- Create localization files using `python manage.py makemessages --locale=pl`
- To test transaction run `python manage.py compilemessages`
- After translating everything that needs translation you can commit the file.

### Todos

- Fix user page
- Fix category page
- Fix reset passwort page
- Fix js in main page

### Copyrights

This software includes the django-registration-defaults Copyright (c) 2010 Charlie DeTar

- https://github.com/yourcelf/django-registration-defaults
  with changes made by https://github.com/dfrankow/django-registration-defaults for django 3.x
