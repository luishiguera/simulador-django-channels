DCOMPOSE = docker-compose -f docker-compose.yaml

help:
	@echo "help               -- Opciones disponibles.							"
	@echo "build              -- Build contenedor, elimna archivos cache.		"
	@echo "up                 -- Run webserver.									"
	@echo "manage             -- Run django 'manage.py' permite migrate/shell.	"
	@echo "pytest             -- Run pytest, pruebas unitarias.					"

#https://stackoverflow.com/a/30659970
rmpyc:
	find . | grep -E "__pycache__|\.pyc|\.pyo" | xargs sudo rm -rf

build: rmpyc
	$(DCOMPOSE) build

up:
	$(DCOMPOSE) up

manage:
	$(DCOMPOSE) run --rm web python manage.py ${CMD}

pytest:
	$(DCOMPOSE) run --rm web /bin/bash -c "pytest ."