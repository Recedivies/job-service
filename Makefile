server:
	python3 manage.py runserver

makemigrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

test:
	coverage run manage.py test

start-db:
	docker run -d --name law-2-cassandra -p 9042:9042 --hostname cassandra --network cassandra cassandra

.PHONY: server makemigrations migrate test, start-db