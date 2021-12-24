#=============================================
# Определение переменных для установки и запуска FASTAPIWS
SETUP=${SETUP_FASTAPIWS} 
install-fastapiws: ${DEPENDENCES_FASTAPIWS} install
	${PIP} install pip wheel -U
	${PIP} install --editable ${FASTAPIWS}

# Запуск приложения OpenAPI в Gunicorn с классом UvicornWorker
run-fastapiws: ${SETUP_FASTAPIWS} venv
	${GUNICORN} --chdir ${FASTAPIWS} \
		"${FASTAPIWS}.__main__:${FASTAPIWS_WEBAPP}()" \
		--bind ${FASTAPIWS_HOST}:${FASTAPIWS_PORT} \
		--worker-class ${FASTAPIWS_WORKER_CLASS} \
		--log-level ${FASTAPIWS_DEBUG} \
		--workers ${FASTAPIWS_WORKERS} \
		--name ${FASTAPIWS} \
		--reload

# Сборка OpenAPI в Docker, используется для отладки
build-fastapiws: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	make release
	${DOCKER} build \
	--file ./${DOCKERFILE_FASTAPIWS} \
	--build-arg TIMEZONE=${TIMEZONE} \
	--build-arg USER_ID=${USER_ID} \
	--build-arg GROUP_ID=${USER_ID} \
	--tag ${FASTAPIWS}:${RELEASE_IMAGE} ./

# Cтарт OpenAPI в Docker, используется для отладки
start-fastapiws: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	${DOCKER} run \
	--name ${FASTAPIWS} \
	--rm \
	--volume ${ENVFILE}:/usr/src/.env \
	--publish ${API_PORT}:${FASTAPIWS_PORT} \
	--detach ${FASTAPIWS}:${RELEASE_IMAGE}
# 	--restart=always

# Стоп OpenAPI в Docker, используется для отладки
stop-fastapiws: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	! [ `${DOCKER} ps | grep ${FASTAPIWS} | wc -l` -eq 1 ] || \
	${DOCKER} stop ${FASTAPIWS}

# Удаление OpenAPI в Docker, используется для отладки
remove-fastapiws: ${DOCKER} ${DOCKERFILE_FASTAPIWS}
	make stop-fastapiws
	${DOCKER} rmi ${FASTAPIWS}:${RELEASE_IMAGE}

# Логирование OpenAPI в Docker, лог выводится в файл, который читается
log-fastapiws: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} ${DOCKERFILE_FASTAPIWS}  
	! [ `${DOCKER} ps | grep ${FASTAPIWS} | wc -l` -eq 1 ] || \
		${DOCKER} logs --follow --tail 500 ${FASTAPIWS}
#		${COMPOSE} -f ${COMPOSE_FILE} logs --follow --tail 500 ${FASTAPIWS}

#=============================================