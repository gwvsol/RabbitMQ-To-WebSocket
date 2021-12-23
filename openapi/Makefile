#=============================================
# Определение переменных для установки и запуска OpenAPI
SETUP=${SETUP_OPENAPI} 
install-openapi: ${DEPENDENCES_OPENAPI} install
	${PIP} install pip wheel -U
	${PIP} install --editable ${OPENAPI}

# Запуск приложения OpenAPI в Gunicorn с классом UvicornWorker
run-openapi: ${SETUP_OPENAPI} venv
	${GUNICORN} --chdir ${OPENAPI} \
		"${OPENAPI}.__main__:${OPENAPI_WEBAPP}()" \
		--bind ${OPENAPI_HOST}:${OPENAPI_PORT} \
		--worker-class ${OPENAPI_WORKER_CLASS} \
		--log-level ${OPENAPI_DEBUG} \
		--workers ${OPENAPI_WORKERS} \
		--name ${OPENAPI} \
		--reload

# Сборка OpenAPI в Docker, используется для отладки
build-openapi: ${DOCKER} ${DOCKERFILE_OPENAPI}
	make release
	${DOCKER} build \
	--file ./${DOCKERFILE_OPENAPI} \
	--build-arg TIMEZONE=${TIMEZONE} \
	--build-arg USER_ID=${USER_ID} \
	--build-arg GROUP_ID=${USER_ID} \
	--tag ${OPENAPI}:${RELEASE_IMAGE} ./

# Cтарт OpenAPI в Docker, используется для отладки
start-openapi: ${DOCKER} ${DOCKERFILE_OPENAPI}
	${DOCKER} run \
	--name ${OPENAPI} \
	--rm \
	--volume ${ENVFILE}:/usr/src/.env \
	--publish ${API_PORT}:${OPENAPI_PORT} \
	--detach ${OPENAPI}:${RELEASE_IMAGE}
# 	--restart=always

# Стоп OpenAPI в Docker, используется для отладки
stop-openapi: ${DOCKER} ${DOCKERFILE_OPENAPI}
	! [ `${DOCKER} ps | grep ${OPENAPI} | wc -l` -eq 1 ] || \
	${DOCKER} stop ${OPENAPI}

# Удаление OpenAPI в Docker, используется для отладки
remove-openapi: ${DOCKER} ${DOCKERFILE_OPENAPI}
	make stop-openapi
	${DOCKER} rmi ${OPENAPI}:${RELEASE_IMAGE}

# Логирование OpenAPI в Docker, лог выводится в файл, который читается
log-openapi: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} ${DOCKERFILE_OPENAPI}  
	! [ `${DOCKER} ps | grep ${OPENAPI} | wc -l` -eq 1 ] || \
		${DOCKER} logs --follow --tail 500 ${OPENAPI}
#		${COMPOSE} -f ${COMPOSE_FILE} logs --follow --tail 500 ${OPENAPI}

#=============================================