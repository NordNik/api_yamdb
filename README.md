# Description

This project is made by Nikolai Orlov (t.me/Nikolai_Orlov)(t.me/Nikolai_Orlov) as an additional project to add some API functionality to blog Yatube (https://github.com/NordNik/hw05_final).

# Getting started
The project was made using Django 2.2.16 and Python 3.7. Other necessary packajes are noticed in requirements.txt.

First, clone the repository from Github and switch to the new directory:

```PYTHON
git clone git@github.com/USERNAME/{{ project_name }}.git
cd {{ project_name }}
```

Secondly, create a new environment using

```PYTHON
python3 -m venv venv
```

Further activate the environment and instal all requirements using

```PYTHON
pip3 install -r requirements.txt
```

Then apply the migrations

```PYTHON
python manage.py migrate
```

and run a server

```PYTHON
python3 manage.py runserver
```

# Request examples

This API is documented and you can find request example at http://127.0.0.1:8000/redoc/ after running the server.
