# Copyright (c) IBM Corporation 2021
# ---------------------------------------------------------------------------- #
#                   Docker Image for Testing Environment                       #
# ---------------------------------------------------------------------------- #
FROM python:3.8-buster
RUN apt-get update && apt-get install -y gnupg2 git python-pip python3-pip openssh-client && python2.7 -m pip install virtualenv
# -------------------- Map UID and GID to Jenkins host IDs ------------------- #
ARG UNAME=jenkins
ARG UID=114
ARG GID=121
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER ${UNAME}
ENV PATH="/home/jenkins/.local/bin:${PATH}"