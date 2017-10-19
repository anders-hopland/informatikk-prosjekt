default: migrate

migrate:
	@echo Migrating database
	@python3 manage.py migrate

rebuild-db:
	@echo Rebuilding database
	@rm -rf db.sqlite3
	@python3 manage.py migrate --run-syncdb
	@echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3 manage.py shell

runserver:
	@echo Starting server
	@python3 manage.py runserver

build:
	@echo Building project
	@rm -rf db.sqlite3
	@python3 manage.py migrate --run-syncdb
	@echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3 manage.py shell


