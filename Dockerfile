# syntax=docker/dockerfile:experimental
# vim: set ft=dockerfile expandtab ts=4 sw=4:

FROM python:3.12 AS base


RUN export DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update      && \
    apt-get upgrade -y  && \
    apt-get install -y python3 python3-pip \
    python3-paramiko \
    python3-yaml \
    vim-common \
    libpq-dev \
    dumb-init \
    git 


WORKDIR /app/
COPY src/ ./
COPY example-srv/ /srv
COPY powergrader_event_utils/ /custom_pip/powergrader_event_utils
COPY setup.py /custom_pip/setup.py
COPY README.md /custom_pip/README.md


RUN --mount=type=cache,target=/root/.cache/ \
    pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install /custom_pip

ARG CACHEBUST=1
ARG GITHUB_AUTH_TOKEN

# RUN python3 -m pip install git+https://oauth2:$GITHUB_AUTH_TOKEN@github.com/WhaleCoded/powergrader_event_utils.git


COPY entrypoint/ /
ENTRYPOINT [ "/bin/bash" ]
ENV PYTHONUNBUFFERED TRUE

