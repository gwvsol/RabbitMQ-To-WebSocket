FROM debian:bullseye-slim
LABEL maintainer="Mikhail Fedorov" email="jwvsol@yandex.ru"
LABEL version="latest"

# Используется в некоторых случаях если не возможно собрать образ
#ENV HTTP_PROXY="http://192.168.93.1:3128"
#ENV HTTPS_PROXY="https://192.168.93.1:3128"

ARG TIMEZONE
ENV TIMEZONE=${TIMEZONE:-Europe/Moscow}
ARG USER_ID
ENV USER_ID ${USER_ID:-1000}
ARG GROUP_ID
ENV GROUP_ID ${GROUP_ID:-1000}

ENV SHELL=/bin/bash
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APPS=fastapiws
ENV APPS_DIR=/usr/src
ENV APPS_USER=fastapiws
COPY release/${APPS}-*.zip /tmp/

RUN groupadd --gid ${GROUP_ID} $APPS_USER \
    && useradd --uid ${USER_ID} --gid $APPS_USER \
       --shell $SHELL --create-home $APPS_USER

RUN set -eux \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install locales procps \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    && ln -snf /usr/share/zoneinfo/$TIMEZONE \
        /etc/localtime && echo $TIMEZONE > /etc/timezone

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN apt-get install -y build-essential git make unzip tzdata curl \
    && apt-get install -y python3 python3-dev python3-pip \
       python3-venv python3-setuptools python3-wheel procps atop \
    && pip3 install setuptools wheel \
    && apt-get clean \
    && rm -rf /root/.cache/pip

RUN set -eux \
    && mkdir -p ${APPS_DIR} \
    && mv /tmp/${APPS}-*.zip ${APPS_DIR} \
    && cd ${APPS_DIR} \
    && unzip ${APPS}-*.zip \
    && rm *.zip \
    && cd .. \
    && chown -R ${APPS_USER}:${APPS_USER} ${APPS_DIR}

USER ${APPS_USER}
WORKDIR ${APPS_DIR}

RUN make install-fastapiws \
    && rm -rf /home/${APPS_USER}/.cache/pip

HEALTHCHECK --interval=180s \
            --timeout=1s \
            --retries=3 \
            --start-period=10s \
            CMD curl --fail -X GET http://localhost:9015/ping || kill 1

EXPOSE 9015

ENTRYPOINT ["make", "run-fastapiws"]
