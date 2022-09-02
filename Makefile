setup:
	python3 -m venv venv 
	source venv/Scripts/activate
	pip3 install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate