# syntax=docker/dockerfile:experimental
# vim: set ft=dockerfile expandtab ts=4 sw=4:

FROM ubuntu:jammy AS base

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



RUN --mount=type=cache,target=/root/.cache/ \
    pip3 install --no-cache-dir -r requirements.txt


ARG CACHEBUST=1
ARG GITHUB_AUTH_TOKEN

RUN python3 -m pip install git+https://oauth2:$GITHUB_AUTH_TOKEN@github.com/WhaleCoded/powergrader_event_utils.git


COPY entrypoint/ /

ENV PYTHONUNBUFFERED TRUE

