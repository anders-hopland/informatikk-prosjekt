default: migrate

rebuild-db:
	@echo Rebuilding database
	@rm -rf db.sqlite3
	@python3 manage.py migrate --run-syncdb

	@echo "\nCreating superuser"
	@echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3 manage.py shell

	@echo "\nLoading user objects"
	@python3 manage.py loaddata users.json

runserver:
	@echo Starting server
	@python3 manage.py runserver

build:
	@echo Building project
	@rm -rf db.sqlite3
	@python3 manage.py migrate --run-syncdb

	@echo "\nCreating superuser"
	@echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3 manage.py shell

	@echo "\nLoading user objects"
	@python3 manage.py loaddata users.json

save-data-from-db:
	@python3 manage.py dumpdata --exclude contenttypes --exclude admin.logentry --exclude auth.permission --exclude sessions.session --indent 4 > users.json
	@echo "\nCloned data from databse to file"



