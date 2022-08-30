# Description

This project is made by Nikolai Orlov team (t.me/Nikolai_Orlov)(t.me/Nikolai_Orlov) as an additional project to add some API functionality to blog Yatube (https://github.com/NordNik/hw05_final).

# About
The YaMDb project collects user reviews on works (Titles). The works are divided into categories: "Books", "Films", "Music". The list of categories can be expanded by the administrator (for example, you can add the category "Fine Art" or "Jewelry").
The works themselves are not stored in YaMDb, you cannot watch a movie or listen to music here.
In each category there are works: books, movies or music. For example, in the category "Books" there may be works "Winnie the Pooh and everything-everything-everything" and "Martian Chronicles", and in the category "Music" - the song "Just Now" by the group "Insects" and the second suite by Bach.
A work can be assigned a genre from the preset list (for example, "Fairy Tale", "Rock" or "Arthouse"). Only the administrator can create new genres.
Grateful or outraged users leave text reviews for the works and give the work a rating in the range from one to ten (an integer); an average rating of the work is formed from user ratings — a rating (an integer). The user can leave only one review for one work.


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
