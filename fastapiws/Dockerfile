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