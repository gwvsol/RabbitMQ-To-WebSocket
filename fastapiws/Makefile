#=============================================
# Определение переменных для установки и запуска FASTAPIWS
SETUP=${SETUP_FASTAPIWS} 
fastapiws: ${DEPENDENCES_FASTAPIWS} install
	${PIP} install pip wheel -U
	${PIP} install --editable ${FASTAPIWS}

# Запуск приложения FASTAPIWS в Gunicorn с классом UvicornWorker
run-fastapiws: ${SETUP_FASTAPIWS} venv
	${GUNICORN} --chdir ${FASTAPIWS} \
		"${FASTAPIWS}.__main__:${FASTAPIWS_WEBAPP}()" \
		--bind ${FASTAPIWS_HOST}:${FASTAPIWS_PORT} \
		--worker-class ${FASTAPIWS_WORKER_CLASS} \
		--log-level ${FASTAPIWS_DEBUG} \
		--workers ${FASTAPIWS_WORKERS} \
		--name ${FASTAPIWS} \
		--reload

# Сборка FASTAPIWS в Docker, используется для отладки
build: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	make release
	${DOCKER} build \
	--file ./${DOCKERFILE_FASTAPIWS} \
	--build-arg TIMEZONE=${TIMEZONE} \
	--build-arg USER_ID=${USER_ID} \
	--build-arg GROUP_ID=${USER_ID} \
	--tag ${FASTAPIWS}:${RELEASE_IMAGE} ./

# Cтарт FASTAPIWS в Docker, используется для отладки
start: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	${DOCKER} run \
	--name ${FASTAPIWS} \
	--rm \
	--volume ${ENVFILE}:/usr/src/.env \
	--publish ${FASTAPIWS_PORT}:${FASTAPIWS_PORT} \
	--detach ${FASTAPIWS}:${RELEASE_IMAGE}
# 	--restart=always

# Стоп FASTAPIWS в Docker, используется для отладки
stop: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	! [ `${DOCKER} ps | grep ${FASTAPIWS} | wc -l` -eq 1 ] || \
	${DOCKER} stop ${FASTAPIWS}

# Удаление FASTAPIWS в Docker, используется для отладки
remove: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	make stop-fastapiws
	${DOCKER} rmi ${FASTAPIWS}:${RELEASE_IMAGE}

# Логирование FASTAPIWS в Docker, лог выводится в файл, который читается
log: ${DOCKER} ${DOCKERFILE_FASTAPIWS}  
	! [ `${DOCKER} ps | grep ${FASTAPIWS} | wc -l` -eq 1 ] || \
		${DOCKER} logs --follow --tail 500 ${FASTAPIWS}

# Рестарт FASTAPIWS
restart: ${DOCKER}
	make stop
	sleep 3
	make start

#=============================================