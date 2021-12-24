.PHONY: help build start stop restart log remove

#=============================================
# Общие настройки и переменные
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate
PYTHON=${VENV_BIN}/python3
PIP=${VENV_BIN}/pip3
GUNICORN=${VENV_BIN}/gunicorn
DOCKER=$(shell which docker)
COMPOSE=$(shell which docker-compose)

ifneq ("$(wildcard $(shell which timedatectl))","")
	export TIMEZONE=$(shell timedatectl status | awk '$$1 == "Time" && $$2 == "zone:" { print $$3 }')
endif

export USER_ID=$(shell id -u `whoami`)
export PWD=$(shell pwd)

ENVIRONMENT=.env
ENVFILE=$(PWD)/${ENVIRONMENT}
ifneq ("$(wildcard $(ENVFILE))","")
    include ${ENVFILE}
    export ENVFILE=$(PWD)/${ENVIRONMENT}
endif

#=============================================
.DEFAULT: help

help:
	@echo "make install	- Installing the project" 
	@echo "make uninstall	- Deleting a project"
	@echo "make build	- Building services in Docker using Docker Compose"
	@echo "make start	- Running services in Docker using Docker Compose"
	@echo "make stop	- Stopping services in Docker using Docker Compose"
	@echo "make restart	- Restart services in Docker using Docker Compose"
	@echo "make log	- Displaying service logs in Docker using Docker Compose"
	@echo "make remove	- Deleting services in Docker"
	@exit 0

#=============================================
# Установка зависимостей для работы приложений
install:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U

# Активация виртуального окружения для работы приложений
venv: ${VENV_NAME}/bin/activate
$(VENV_NAME)/bin/activate: ${SETUP}
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -e .
	${VENV_ACTIVATE}

# Удаление виртуального окружения для приложений
uninstall:
	make clean
	make clean-pyc
	rm -fr ${VENV_NAME}

#=============================================
# Создание релиза приложения
release: clean clean-pyc ${FASTAPIWS} ${COMPOSE_FILE} ${MAKEFILE} \
				   		 ${ENVIRONMENT} ${README}
	[ -d $(RELEASE) ] || mkdir ${RELEASE}
	[ -d $(ARCHIVE) ] || mkdir ${ARCHIVE}
	find "$(RELEASE)" -name '*.zip' -type f -exec mv -v -t "$(ARCHIVE)" {} +
	zip -r ${RELEASE}/${FASTAPIWS}-$(shell date '+%Y-%m-%d-%H-%M-%S').zip \
	${FASTAPIWS} ${COMPOSE_FILE} ${MAKEFILE} ${ENVIRONMENT} ${README}

#=============================================
# Очистка мусора
clean:
	rm -fr .eggs
	rm -fr *.egg-info
	find . -name '.eggs' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +

# Очистка мусора, удаление файлов создающихся Python
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

#=============================================
# Работа с приложением OpenAPI
ifneq ("$(wildcard $(PWD)/$(FASTAPIWS_MAKEFILE))","")
    include ${FASTAPIWS_MAKEFILE}
endif

#=============================================